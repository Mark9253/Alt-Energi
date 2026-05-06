from odoo import _, api, fields, models


class AllenergyWorksheetBiomass(models.Model):
    _name = 'allenergy.worksheet.biomass'
    _description = 'AllEnergy Biomass Service Worksheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(compute='_compute_name', store=True)
    task_id = fields.Many2one(
        'project.task',
        required=True,
        ondelete='cascade',
        index=True,
    )
    equipment_id = fields.Many2one(
        'maintenance.equipment',
        domain="[('asset_type', '=', 'boiler')]",
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
    manufacturer = fields.Char(related='equipment_id.manufacturer', store=True)
    is_heizomat = fields.Boolean(compute='_compute_is_heizomat', store=True)

    visit_date = fields.Date(default=fields.Date.context_today)
    engineer_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    line_ids = fields.One2many(
        'allenergy.worksheet.biomass.line',
        'worksheet_id',
        string='Inspection Items',
    )
    remedial_ids = fields.One2many(
        'allenergy.worksheet.biomass.remedial',
        'worksheet_id',
        string='Recommended Remedial Works',
    )
    part_ids = fields.One2many(
        'allenergy.worksheet.biomass.part',
        'worksheet_id',
        string='Parts and Materials Used',
    )

    overall_condition = fields.Selection(
        selection=[
            ('poor', 'Poor'),
            ('fair', 'Fair'),
            ('good', 'Good'),
            ('very_good', 'Very Good'),
        ],
        string='Overall Condition',
    )
    client_print_name = fields.Char(string='Client Print Name')
    client_position = fields.Char(string='Client Position')
    client_signature = fields.Binary(string='Client Signature')
    client_signature_date = fields.Date(string='Signature Date')

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('signed', 'Signed'),
        ],
        default='draft',
        tracking=True,
    )

    @api.depends('task_id.name', 'equipment_id.name', 'visit_date')
    def _compute_name(self):
        for ws in self:
            parts = []
            if ws.equipment_id:
                parts.append(ws.equipment_id.name)
            if ws.visit_date:
                parts.append(fields.Date.to_string(ws.visit_date))
            ws.name = ' / '.join(parts) or _('Biomass Worksheet')

    @api.depends('manufacturer')
    def _compute_is_heizomat(self):
        for ws in self:
            ws.is_heizomat = (ws.manufacturer or '').strip().lower() == 'heizomat'

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
        Item = self.env['allenergy.worksheet.biomass.item']
        if self.is_heizomat:
            applies = ['always', 'heizomat']
        elif self.manufacturer:
            applies = ['always', 'non_heizomat']
        else:
            return
        items = Item.search(
            [('applies_when', 'in', applies), ('active', '=', True)],
            order='sequence, id',
        )
        Line = self.env['allenergy.worksheet.biomass.line']
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


class AllenergyWorksheetBiomassLine(models.Model):
    _name = 'allenergy.worksheet.biomass.line'
    _description = 'AllEnergy Biomass Worksheet Line'
    _order = 'sequence, id'

    worksheet_id = fields.Many2one(
        'allenergy.worksheet.biomass',
        required=True,
        ondelete='cascade',
        index=True,
    )
    item_id = fields.Many2one(
        'allenergy.worksheet.biomass.item',
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
        string='Status',
    )
    comments = fields.Text()


class AllenergyWorksheetBiomassRemedial(models.Model):
    _name = 'allenergy.worksheet.biomass.remedial'
    _description = 'AllEnergy Biomass Worksheet Remedial Work'
    _order = 'urgency, sequence, id'

    worksheet_id = fields.Many2one(
        'allenergy.worksheet.biomass',
        required=True,
        ondelete='cascade',
        index=True,
    )
    sequence = fields.Integer(default=10)
    description = fields.Text(required=True)
    urgency = fields.Selection(
        selection=[
            ('urgent', 'Urgent'),
            ('non_urgent', 'Non-Urgent'),
            ('advisory', 'Advisory'),
        ],
        default='non_urgent',
        required=True,
    )


class AllenergyWorksheetBiomassPart(models.Model):
    _name = 'allenergy.worksheet.biomass.part'
    _description = 'AllEnergy Biomass Worksheet Part Used'
    _order = 'sequence, id'

    worksheet_id = fields.Many2one(
        'allenergy.worksheet.biomass',
        required=True,
        ondelete='cascade',
        index=True,
    )
    sequence = fields.Integer(default=10)
    product_id = fields.Many2one('product.product')
    description = fields.Char()
    quantity = fields.Float(default=1.0, digits=(10, 2))
    chargeable = fields.Boolean(
        default=True,
        help='Chargeable to customer when set; '
             'unset for customer-supplied or no-charge parts.',
    )
