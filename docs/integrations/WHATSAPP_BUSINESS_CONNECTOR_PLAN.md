# WhatsApp Business Connector Plan

## Purpose
Send approved outreach drafts via WhatsApp Business API using approved templates.

## Required env
- `WHATSAPP_BUSINESS_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`

## Rules
- No template = no send
- Pre-approved templates only
- Opt-out keyword STOP honored within 24 hours
- 1 message per contact per week (unless explicitly replied)
- No group messages to non-consenting contacts

## Implementation (V1 plan)
- `connectors/whatsapp_business_connector.py`
- Function: `send_template(template_id, contact, params, review_status)`
- Hard guard: refuses if `review_status != "approved"`

## Testing
- `tests/test_whatsapp_no_auto_send.py` — fails if any path sends without review
