{
    'name': 'AllEnergy Core',
    'version': '19.0.1.0.0',
    'summary': 'Core data model for Alt-Energi Services: partners, sites, assets, postcode bands.',
    'description': """
AllEnergy Core
==============
Foundation module for the Alt-Energi Services Ltd Odoo 19 build.

Provides:
- res.partner extensions for sites, monitoring portal IDs, postcode bands
- maintenance.equipment extensions for the asset register
- Postcode-to-distance lookup data
- System parameters for depot, business hours, commute deduction
- Cron job for anniversary-based subscription task scheduling
""",
    'author': 'UP-STRIDE Limited',
    'website': 'https://up-stride.co.uk',
    'license': 'LGPL-3',
    'category': 'Services/Field Service',
    'depends': [
        'base',
        'contacts',
        'maintenance',
        'project',
        'sale_subscription',
        'industry_fsm',
    ],
    'data': [
        'security/allenergy_security.xml',
        'security/ir.model.access.csv',
        'data/allenergy.postcode.distance.csv',
        'views/postcode_distance_views.xml',
        'views/res_partner_views.xml',
        'views/project_project_views.xml',
        'views/maintenance_equipment_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
