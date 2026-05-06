from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    partner_id = fields.Many2one(
        'res.partner',
        string='Site',
        domain="[('is_site', '=', True)]",
        index=True,
        help='Site where this asset is installed.',
    )
    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        related='partner_id.parent_id',
        store=True,
        index=True,
        help='Parent client of the site.',
    )

    manufacturer = fields.Char(string='Manufacturer')
    model_number = fields.Char(string='Model Number')
    serial_number = fields.Char(string='Serial Number', index=True)
    vg_number = fields.Char(
        string='VG Number',
        help='Verification Group number, used by biomass boiler manufacturers.',
    )

    install_date = fields.Date(string='Install Date')
    warranty_end_date = fields.Date(string='Warranty End Date')
    system_capacity_kw = fields.Float(
        string='System Capacity (kW)',
        digits=(10, 2),
    )

    asset_type = fields.Selection(
        selection=[
            ('solar_panel', 'Solar Panel'),
            ('inverter', 'Inverter'),
            ('boiler', 'Boiler'),
            ('pump', 'Pump'),
            ('other', 'Other'),
        ],
        string='Asset Type',
        index=True,
    )
    monitoring_portal = fields.Selection(
        selection=[
            ('solis', 'SolisCloud'),
            ('solaredge', 'SolarEdge'),
            ('fox', 'FoxESS'),
            ('sma_ema', 'SMA Ennexos / EMA'),
            ('sungrow', 'Sungrow iSolarCloud'),
            ('argand', 'Argand'),
            ('juggle', 'Juggle'),
            ('metris', 'Metris'),
            ('none', 'None'),
        ],
        string='Monitoring Portal',
        default='none',
    )
    monitoring_plant_id = fields.Char(
        string='Monitoring Plant ID',
        help='Plant or device identifier on the monitoring portal.',
    )

    task_ids = fields.Many2many(
        'project.task',
        'project_task_maintenance_equipment_rel',
        'equipment_id',
        'task_id',
        string='Service Tasks',
    )
    last_service_date = fields.Date(
        string='Last Service Date',
        compute='_compute_last_service_date',
        store=True,
    )
    next_service_due_date = fields.Date(
        string='Next Service Due',
        compute='_compute_next_service_due_date',
        store=True,
    )

    @api.depends('task_ids.date_end', 'task_ids.stage_id.fold')
    def _compute_last_service_date(self):
        for equipment in self:
            done = equipment.task_ids.filtered(
                lambda t: t.date_end and t.stage_id and t.stage_id.fold
            )
            if done:
                equipment.last_service_date = max(t.date_end.date() for t in done)
            else:
                equipment.last_service_date = False

    def _compute_next_service_due_date(self):
        for equipment in self:
            equipment.next_service_due_date = False
