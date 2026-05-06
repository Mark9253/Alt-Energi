# Alt-Energi Odoo 19 build

Odoo 19 implementation for Alt-Energi Services Ltd (trading as AllEnergy), delivered by UP-STRIDE Limited.

## Modules

- `custom_addons/allenergy_core` — partner, site, asset, postcode band data model and cron jobs
- `custom_addons/allenergy_worksheets` — Field Service worksheet templates (biomass, solar)
- `custom_addons/allenergy_integrations` — REST endpoints for n8n, Companies House lookup, postcode geocoding

## Deployment

Odoo.sh pulls from this repo. Push to a feature branch, validate on the dev environment, then promote dev to staging to production.

## Docs

- `docs/api/endpoints.md` — REST endpoint reference
- `docs/runbooks/` — manual UI configuration runbooks
- `docs/decisions/` — architecture and pricing decisions log
- `docs/source-materials/` — original PDFs, worksheets, and reference documents
