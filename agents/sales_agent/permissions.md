# Sales Agent Permissions

## Allowed

- Normalize lead intake payloads.
- Enrich company profile from approved sources.
- Score lead qualification readiness.
- Draft CRM commit payloads.
- Publish internal workflow metrics.

## Approval-required

- Any external CRM write (`crm.create_lead`).
- Any pricing commitment or commercial promise.
- Any external communication action.

## Forbidden

- Cold WhatsApp auto-send.
- LinkedIn DM automation.
- External email send without explicit approval.
- Unauthorized scraping or data harvesting.
