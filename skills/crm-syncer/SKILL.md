# CRM Syncer

Bidirectionally syncs leads/deals/contacts between Dealix and the
customer's CRM. HubSpot is live today; Salesforce is a stub.

## Inputs

`crm: hubspot | salesforce`, `entity: lead | deal | contact`,
`direction: pull | push | both`, `since: ISO`.

## Linked code

- `integrations/hubspot.py` (existing live client).
- `auto_client_acquisition/agents/crm.py` (existing CRM agent).
