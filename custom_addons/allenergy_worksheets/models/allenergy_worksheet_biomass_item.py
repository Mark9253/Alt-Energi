from odoo import api, fields, models


class AllenergyWorksheetBiomassItem(models.Model):
    _name = 'allenergy.worksheet.biomass.item'
    _description = 'AllEnergy Biomass Worksheet Item (Master)'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    section = fields.Selection(
        selection=[
            ('heizomat_feed', '1. Heizomat Feed System'),
            ('heizomat_boiler', '2. Heizomat Boiler'),
            ('heizomat_fireplace', '3. Heizomat Fireplace'),
            ('controls', '4. Controls'),
            ('fuel_general', '5. Fuel General'),
            ('non_heizomat', '6. Non-Heizomat Boiler'),
        ],
        required=True,
    )
    applies_when = fields.Selection(
        selection=[
            ('heizomat', 'Heizomat installations only'),
            ('non_heizomat', 'Non-Heizomat installations only'),
            ('always', 'All installations'),
        ],
        compute='_compute_applies_when',
        store=True,
    )
    active = fields.Boolean(default=True)

    @api.depends('section')
    def _compute_applies_when(self):
        for item in self:
            if item.section in ('heizomat_feed', 'heizomat_boiler', 'heizomat_fireplace'):
                item.applies_when = 'heizomat'
            elif item.section == 'non_heizomat':
                item.applies_when = 'non_heizomat'
            else:
                item.applies_when = 'always'
