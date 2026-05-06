{
    'name': 'AllEnergy Worksheets',
    'version': '19.0.1.0.0',
    'summary': 'Field Service worksheet templates for biomass and solar service visits.',
    'description': """
AllEnergy Worksheets
====================
Service worksheet templates used by the AllEnergy field engineers.

Provides:
- Biomass service sheet (82 line items, four conditional sections)
- Solar service sheet (skeleton pending final spec)
""",
    'author': 'UP-STRIDE Limited',
    'website': 'https://up-stride.co.uk',
    'license': 'LGPL-3',
    'category': 'Services/Field Service',
    'depends': [
        'allenergy_core',
        'industry_fsm',
        'industry_fsm_report',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/biomass_worksheet_items.xml',
        'data/solar_worksheet_items.xml',
        'views/allenergy_worksheet_biomass_views.xml',
        'views/allenergy_worksheet_solar_views.xml',
        'views/project_task_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
