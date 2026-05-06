from odoo import _, api, fields, models


class AllenergyWorksheetSolar(models.Model):
    _name = 'allenergy.worksheet.solar'
    _description = 'AllEnergy Solar PV Service Worksheet (skeleton)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # TODO: Charlotte to provide the final solar inspection spec.
    # The structure here is a placeholder modelled on the existing
    # "Solar PV System Inspection Report" PDF in /docs/source-materials/.
    # Sections and items below are starter content; replace via the master
    # item view when the final list is ready, then bump the module version.

    name = fields.Char(compute='_compute_name', store=True)
    task_id = fields.Many2one(
        'project.task',
        required=True,
        ondelete='cascade',
        index=True,
    )
    equipment_id = fields.Many2one(
        'maintenance.equipment',
        domain="[('asset_type', 'in', ['solar_panel', 'inverter'])]",
        required=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        related='equipment_id.partner_id',
        store=True,
    )
    client_id = fields.Many2one(
        'res.partner',
        related='equipment_id.client_id',
        store=True,
    )

    visit_date = fields.Date(default=fields.Date.context_today)
    engineer_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    line_ids = fields.One2many(
        'allenergy.worksheet.solar.line',
        'worksheet_id',
        string='Inspection Items',
    )

    overall_condition = fields.Selection(
        selection=[
            ('poor', 'Poor'),
            ('fair', 'Fair'),
            ('good', 'Good'),
            ('very_good', 'Very Good'),
        ],
    )
    client_print_name = fields.Char()
    client_position = fields.Char()
    client_signature = fields.Binary()
    client_signature_date = fields.Date()

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('signed', 'Signed'),
        ],
        default='draft',
        tracking=True,
    )

    @api.depends('equipment_id.name', 'visit_date')
    def _compute_name(self):
        for ws in self:
            parts = []
            if ws.equipment_id:
                parts.append(ws.equipment_id.name)
            if ws.visit_date:
                parts.append(fields.Date.to_string(ws.visit_date))
            ws.name = ' / '.join(parts) or _('Solar Worksheet')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for ws in records:
            ws._populate_default_lines()
        return records

    def _populate_default_lines(self):
        self.ensure_one()
        if self.line_ids:
            return
        Item = self.env['allenergy.worksheet.solar.item']
        items = Item.search([('active', '=', True)], order='sequence, id')
        Line = self.env['allenergy.worksheet.solar.line']
        Line.create([{
            'worksheet_id': self.id,
            'item_id': item.id,
            'sequence': item.sequence,
        } for item in items])

    def action_sign(self):
        for ws in self:
            if not ws.client_signature:
                continue
            ws.state = 'signed'
            if not ws.client_signature_date:
                ws.client_signature_date = fields.Date.context_today(ws)


class AllenergyWorksheetSolarLine(models.Model):
    _name = 'allenergy.worksheet.solar.line'
    _description = 'AllEnergy Solar Worksheet Line'
    _order = 'sequence, id'

    worksheet_id = fields.Many2one(
        'allenergy.worksheet.solar',
        required=True,
        ondelete='cascade',
        index=True,
    )
    item_id = fields.Many2one(
        'allenergy.worksheet.solar.item',
        required=True,
        ondelete='restrict',
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(related='item_id.name', readonly=True, store=True)
    section = fields.Selection(related='item_id.section', store=True)
    status = fields.Selection(
        selection=[
            ('satisfactory', 'Satisfactory'),
            ('defective', 'Defective'),
            ('na', 'N/A'),
        ],
    )
    comments = fields.Text()
