# Analytics Plan (Dealix)

## Goals
- Track the **5 KPIs** per Command Center
- Track conversion (proposal → close)
- Track time-in-review
- No PII in events

## Event taxonomy
| Event | When | Properties |
|-------|------|-----------|
| page_view | page load | path, locale |
| cta_click | CTA press | cta_id, source_page |
| sales_pack_download | API call | format |
| ceo_brief_download | API call | format |
| proposal_generated | script | account_id, offer |
| lead_imported | import script | count |
| draft_reviewed | approve/reject | reviewer |
| proof_report_generated | script | account_id |

## Provider (V1)
- No provider by default
- Console log in dev only
- If `NEXT_PUBLIC_ANALYTICS_ENABLED=true`, prepare event payload
- Never send PII

## API
- `GET /api/analytics/event-taxonomy` — returns the event list
