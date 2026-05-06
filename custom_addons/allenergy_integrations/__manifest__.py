{
    'name': 'AllEnergy Integrations',
    'version': '19.0.1.0.0',
    'summary': 'REST endpoints and external integrations: n8n, RAM Tracking, SolisCloud, Companies House, Xero.',
    'description': """
AllEnergy Integrations
======================
External-facing integration layer for the Alt-Energi Services build.

Provides:
- REST controller at /api/allenergy/v1/ with API key authentication
- Endpoints for n8n: timesheet_line, alarm_event, tasks_for_today, partners_with_portal_id
- Companies House lookup wizard on the partner form
- Postcode geocoding helper for distance and drive time to HQ
""",
    'author': 'UP-STRIDE Limited',
    'website': 'https://up-stride.co.uk',
    'license': 'LGPL-3',
    'category': 'Services/Integrations',
    'depends': [
        'allenergy_core',
        'base',
        'contacts',
        'industry_fsm',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
