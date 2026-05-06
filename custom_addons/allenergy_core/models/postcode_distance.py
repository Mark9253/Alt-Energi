from odoo import fields, models


class AllenergyPostcodeDistance(models.Model):
    _name = 'allenergy.postcode.distance'
    _description = 'AllEnergy Postcode Area Distance Lookup'
    _order = 'distance_miles, outward_code'
    _rec_name = 'outward_code'

    outward_code = fields.Char(
        string='Postcode Area',
        required=True,
        index=True,
        help='UK postcode area code (the leading letters of an outward code, '
             'e.g. WR for Worcester, B for Birmingham).',
    )
    area_name = fields.Char(string='Area Name', required=True)
    distance_miles = fields.Float(
        string='Distance (mi)',
        digits=(8, 2),
        help='Approximate one-way road distance from the Worcester HQ depot.',
    )
    drive_hours = fields.Float(
        string='Drive Time (hrs)',
        digits=(6, 2),
        help='Approximate one-way drive time from the Worcester HQ depot.',
    )
    active_customer_count = fields.Integer(
        string='Active Customers',
        help='Reference data: customers in this area at the time of seeding. '
             'Not maintained automatically.',
    )

    _sql_constraints = [
        ('outward_code_unique', 'UNIQUE(outward_code)',
         'Each postcode area must have only one distance record.'),
    ]
