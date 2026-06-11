# Integration Architecture (Dealix)

## الطبقات
1. **Data sources** — CSV, manual research, open data, official APIs
2. **Adapters** — normalize to internal schema
3. **CRM** — accounts, drafts, proposals, deals
4. **Outreach** — drafts + review queue (no auto-send)
5. **Delivery** — workflow + proof + retention
6. **Reporting** — daily CEO brief, weekly review, monthly review

## Connectors (V1)
| Connector | Status | Notes |
|-----------|--------|-------|
| CSV | Implemented | Local file |
| Manual research | Implemented | Founder-supplied |
| Website signal | Implemented | Local file |
| Open Data SA | Implemented | Public aggregate |
| Google Places | Plan | Needs API key |
| HubSpot | Plan | Needs OAuth |
| WhatsApp Business | Plan | Needs template approval |
| Email | Plan | SMTP provider |

## Contracts
- Every connector has `inputs`, `outputs`, `safety_flags`, `requires_env`
- Every connector returns a normalized list of records
- Connectors are deterministic + idempotent
