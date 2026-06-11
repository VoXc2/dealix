# Email Outreach Connector Plan

## Purpose
Send approved drafts via email (SMTP or transactional API).

## Required env
- `EMAIL_PROVIDER_API_KEY` (SendGrid, Postmark, SES, etc.)
- `EMAIL_FROM` (verified sender)
- `EMAIL_REPLY_TO` (founder inbox)

## Safety
- No send without `review_status == "approved"`
- Each email includes physical address + unsubscribe link
- Honor unsubscribe within 24 hours
- 1 email per contact per week (unless explicitly replied)

## Implementation (V1 plan)
- `connectors/email_connector.py`
- Function: `send_email(to, subject, body, review_status)`
- Hard guard: refuses if `review_status != "approved"`
