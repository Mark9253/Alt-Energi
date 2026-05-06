from odoo import fields, models


class AllenergyWorksheetSolarItem(models.Model):
    _name = 'allenergy.worksheet.solar.item'
    _description = 'AllEnergy Solar Worksheet Item (Master)'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    section = fields.Selection(
        selection=[
            ('dc_array', '1. DC Array Design'),
            ('overvoltage', '2. Overvoltage Protection'),
            ('ac_circuit', '3. AC Circuit'),
            ('labelling', '4. Labelling'),
            ('mechanical', '5. Mechanical Installation'),
            ('performance', '6. Performance Comparison'),
        ],
        required=True,
    )
    active = fields.Boolean(default=True)
