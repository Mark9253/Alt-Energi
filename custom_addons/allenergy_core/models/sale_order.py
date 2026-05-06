import logging
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

ANNIVERSARY_LOOKAHEAD_DAYS = 30
UPLIFT_NOTICE_LOOKAHEAD_DAYS = 60
UPLIFT_NOTICE_DEADLINE_DAYS_BEFORE_ANNIVERSARY = 45
ACTIVE_SUBSCRIPTION_STATES = ('3_progress',)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _allenergy_cron_schedule_anniversaries(self):
        """Daily pass over active AllEnergy subscriptions.

        For each active subscription, computes the next start_date anniversary
        and acts on two checkpoints relative to it:

        - 30 days before: create an FSM task on the Planned Maintenance
          project, dated for the anniversary itself.
        - 60 days before: create a mail.activity on the subscription
          prompting an admin to send the RPI+1% uplift notice required by
          T&Cs clause 3.4. Activity deadline is anniversary - 45 days, the
          contractual notice deadline.

        Both create steps are idempotent: an existing task or activity that
        matches on subscription, partner, and date is left alone.
        """
        today = fields.Date.context_today(self)
        project = self._allenergy_planned_maintenance_project()

        domain = [
            ('is_subscription', '=', True),
            ('subscription_state', 'in', list(ACTIVE_SUBSCRIPTION_STATES)),
            ('start_date', '!=', False),
        ]
        subs = self.search(domain)
        for sub in subs:
            anniversary = sub._allenergy_next_anniversary(today)
            if not anniversary:
                continue

            if today == anniversary - timedelta(days=ANNIVERSARY_LOOKAHEAD_DAYS):
                if project:
                    sub._allenergy_create_anniversary_task(project, anniversary)
                else:
                    _logger.info(
                        "Skipped anniversary task for subscription %s: "
                        "Planned Maintenance project not configured.", sub.id)

            if today == anniversary - timedelta(days=UPLIFT_NOTICE_LOOKAHEAD_DAYS):
                sub._allenergy_create_uplift_notice_activity(anniversary)

    @api.model
    def _allenergy_planned_maintenance_project(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'allenergy.planned_maintenance_project_id')
        if not param:
            _logger.warning(
                "allenergy.planned_maintenance_project_id is not set. "
                "Configure it in System Parameters once the Planned "
                "Maintenance project is created (task 12) so the "
                "anniversary cron can land FSM tasks.")
            return False
        try:
            project_id = int(param)
        except (TypeError, ValueError):
            _logger.error(
                "Invalid allenergy.planned_maintenance_project_id: %r", param)
            return False
        project = self.env['project.project'].browse(project_id).exists()
        if not project:
            _logger.error(
                "allenergy.planned_maintenance_project_id %s not found.",
                project_id)
            return False
        return project

    def _allenergy_next_anniversary(self, today):
        """Next start_date anniversary on or after today, capped at end_date."""
        self.ensure_one()
        if not self.start_date:
            return False
        candidate = self.start_date + relativedelta(
            years=today.year - self.start_date.year)
        if candidate < today or candidate == self.start_date:
            candidate = candidate + relativedelta(years=1)
        if self.end_date and candidate > self.end_date:
            return False
        return candidate

    def _allenergy_create_anniversary_task(self, project, anniversary_date):
        self.ensure_one()
        Task = self.env['project.task']
        existing = Task.search([
            ('project_id', '=', project.id),
            ('partner_id', '=', self.partner_id.id),
            ('date_deadline', '=', anniversary_date),
        ], limit=1)
        if existing:
            return existing
        vals = {
            'name': _('Annual Service Visit - %(partner)s (%(year)s)') % {
                'partner': self.partner_id.name,
                'year': anniversary_date.strftime('%Y'),
            },
            'project_id': project.id,
            'partner_id': self.partner_id.id,
            'date_deadline': anniversary_date,
        }
        if 'sale_order_id' in Task._fields:
            vals['sale_order_id'] = self.id
        return Task.create(vals)

    def _allenergy_create_uplift_notice_activity(self, anniversary_date):
        self.ensure_one()
        activity_type = self.env.ref(
            'mail.mail_activity_data_todo', raise_if_not_found=False)
        if not activity_type:
            _logger.warning(
                "mail.mail_activity_data_todo not found; skipping uplift "
                "notice activity for subscription %s.", self.id)
            return False
        deadline = anniversary_date - timedelta(
            days=UPLIFT_NOTICE_DEADLINE_DAYS_BEFORE_ANNIVERSARY)
        summary = _('Send RPI+1%% uplift notice to %s') % self.partner_id.name
        Activity = self.env['mail.activity']
        existing = Activity.search([
            ('res_model', '=', 'sale.order'),
            ('res_id', '=', self.id),
            ('summary', '=', summary),
            ('date_deadline', '=', deadline),
        ], limit=1)
        if existing:
            return existing
        admin_user = self.env.ref(
            'base.user_admin', raise_if_not_found=False) or self.env.user
        return Activity.create({
            'res_model_id': self.env['ir.model']._get('sale.order').id,
            'res_id': self.id,
            'activity_type_id': activity_type.id,
            'summary': summary,
            'note': _(
                'Anniversary: %(anniversary)s. RPI+1%% uplift notice must '
                'be sent at least 45 days before the anniversary per T&Cs '
                'clause 3.4. Customer: %(partner)s.'
            ) % {
                'anniversary': anniversary_date,
                'partner': self.partner_id.name,
            },
            'date_deadline': deadline,
            'user_id': admin_user.id,
        })
