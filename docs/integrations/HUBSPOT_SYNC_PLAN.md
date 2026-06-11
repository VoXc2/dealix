# HubSpot Sync Plan (Dealix)

## Setup
1. Create private app in HubSpot
2. Scopes: `crm.objects.contacts.read`, `crm.objects.deals.read`, `crm.objects.companies.read`
3. Set `HUBSPOT_PRIVATE_APP_TOKEN`
4. Run `python3 scripts/audit_lead_sources.py` to verify

## Sync
- `python3 scripts/hubspot_sync.py` (planned, V8)
- Reads deals, contacts, companies
- Normalizes to Dealix schema
- Appends to `business/_data/leads.json` (demo)
- Or writes to Postgres (production)

## Safety
- Read-only
- Token rotation every 90 days
- Source marked `sourceType: "hubspot"`
- All records require human review
