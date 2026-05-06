# 0001 — Geocoding source of truth lives in Odoo

Date: 2026-05-06
Status: Accepted

## Context

Initial brief proposed using RAM Tracking Location IDs (`qaifn_location_id`)
as the link between an Odoo customer/site and an external geographic location,
with the n8n journey classifier matching journey endpoints to RAM-side
Locations.

That meant two registers of customer locations (RAM and Odoo) and a manual
mapping step per new site. It also locked out project sites that aren't
recurring service customers.

## Decision

Odoo holds latitude, longitude, and a geofence radius for every site. The
RAM tracker becomes a pure GPS feed. The n8n classifier matches journey
coordinates against Odoo coordinates.

Geocoding source is postcodes.io (free, no key, postcode-centroid accuracy).
Coordinates can be overridden manually for sites where the centroid is
wrong (large farms, multi-building industrial sites, shared postcodes).

The same fields exist on `res.partner` (with `is_site=True`) and on
`project.project` so one-off project sites without a recurring customer
record are still matchable.

## Consequences

- New customer onboarding is one workflow not two.
- Task-level journey matching becomes possible (location + time + engineer).
- Existing customer base needs a one-off bulk geocode pass; covered by the
  `POST /geocode_site` endpoint added in `allenergy_integrations`.
- Sites whose geocoded point sits more than
  `allenergy.geocoding_review_threshold_meters` from a prior coordinate, or
  where postcodes.io returns no match, get a `mail.activity` for review.
