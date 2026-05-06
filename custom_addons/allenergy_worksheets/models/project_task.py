from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    biomass_worksheet_ids = fields.One2many(
        'allenergy.worksheet.biomass', 'task_id', string='Biomass Worksheets')
    biomass_worksheet_count = fields.Integer(
        compute='_compute_worksheet_counts')

    @api.depends('biomass_worksheet_ids')
    def _compute_worksheet_counts(self):
        for task in self:
            task.biomass_worksheet_count = len(task.biomass_worksheet_ids)

    def action_open_biomass_worksheets(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Biomass Worksheets'),
            'res_model': 'allenergy.worksheet.biomass',
            'view_mode': 'list,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
        }
