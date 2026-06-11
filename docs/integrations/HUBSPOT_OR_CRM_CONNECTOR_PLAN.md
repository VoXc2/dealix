# HubSpot CRM Connector Plan

## Purpose
Sync accounts and deals from a HubSpot portal the client owns.

## Required env
- `HUBSPOT_PRIVATE_APP_TOKEN` (read-only scope)

## Endpoints
- `crm.objects.contacts.read` — fetch contacts
- `crm.objects.deals.read` — fetch deals
- `crm.objects.companies.read` — fetch companies

## Safety
- Read-only by default
- Token rotation every 90 days
- No PII stored beyond what the client already has
- Respect HubSpot rate limits (110 req / 10s)

## Implementation (V1 plan)
- `connectors/hubspot_connector.py`
- Returns normalized accounts
- Marks `sourceType: "hubspot"`
- Requires `sourceNote` (the portal id)
