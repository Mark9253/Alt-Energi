from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

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
    )
    coords_manual_override = fields.Boolean(
        string='Manual Coordinate Override',
    )
    geocoding_source = fields.Char(
        string='Geocoding Source',
    )
    geocoding_accuracy = fields.Char(
        string='Geocoding Accuracy',
    )

    def _default_geofence_radius_meters(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'allenergy.default_geofence_radius_meters', '150')
        try:
            return int(param)
        except (TypeError, ValueError):
            return 150
