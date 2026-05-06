from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_site = fields.Boolean(
        string='Is Site',
        help='Indicates this partner is a site (child) record where assets are installed and work is delivered.',
    )

    site_latitude = fields.Float(
        string='Site Latitude',
        digits=(10, 6),
        index=True,
    )
    site_longitude = fields.Float(
        string='Site Longitude',
        digits=(10, 6),
        index=True,
    )
    geofence_radius_meters = fields.Integer(
        string='Geofence Radius (m)',
        default=lambda self: self._default_geofence_radius_meters(),
        help='Radius around the site coordinates used by the n8n journey classifier '
             'to match RAM Tracking GPS points to this site.',
    )
    coords_manual_override = fields.Boolean(
        string='Manual Coordinate Override',
        help='When set, automatic geocoding from the postcode will not overwrite '
             'the latitude and longitude on this record.',
    )
    geocoding_source = fields.Char(
        string='Geocoding Source',
        help='Source of the current coordinates (e.g. postcodes.io, manual).',
    )
    geocoding_accuracy = fields.Char(
        string='Geocoding Accuracy',
        help='Accuracy descriptor returned by the geocoding source '
             '(e.g. postcode_centroid).',
    )

    soliscloud_plant_id = fields.Char(
        string='SolisCloud Plant ID',
        index=True,
    )
    soliscloud_station_id = fields.Char(
        string='SolisCloud Station ID',
    )

    postcode_band = fields.Selection(
        selection=[
            ('local', 'Local (0-30 mi)'),
            ('near', 'Near (31-75 mi)'),
            ('mid', 'Mid (76-150 mi)'),
            ('far', 'Far (151+ mi)'),
        ],
        string='Postcode Band',
        compute='_compute_postcode_band',
        store=True,
    )

    @api.model
    def _default_geofence_radius_meters(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'allenergy.default_geofence_radius_meters', '150')
        try:
            return int(param)
        except (TypeError, ValueError):
            return 150

    @api.depends('zip')
    def _compute_postcode_band(self):
        for partner in self:
            partner.postcode_band = False
