from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    equipment_ids = fields.Many2many(
        'maintenance.equipment',
        'project_task_maintenance_equipment_rel',
        'task_id',
        'equipment_id',
        string='Assets',
        help='Assets serviced or affected by this task. Used by worksheets to '
             'log work against the asset register and to populate '
             'maintenance.equipment.last_service_date.',
    )
