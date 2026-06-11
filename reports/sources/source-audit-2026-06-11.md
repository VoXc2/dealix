# Source Audit — 2026-06-11

Total sources registered: 8

## By risk
- low: 5
- medium: 2
- high: 1

## By review status
- no-review: 4
- review: 4

## Per-source summary
### Saudi Open Data
- type: open_data
- risk: low
- review: not required
- allowed: Public aggregate sector data
- notes: data.gov.sa public datasets

### Founder CSV
- type: csv_import
- risk: low
- review: not required
- allowed: Bulk upload from approved public lists
- notes: Founder must provide source URL/note per row

### Manual research
- type: manual_research
- risk: low
- review: not required
- allowed: Public web + social reading by founder
- notes: URL/quote required per lead

### Website signal (local)
- type: website_signal
- risk: low
- review: not required
- allowed: Read saved HTML/text snapshot
- notes: Founder must save the file

### HubSpot CRM
- type: hubspot
- risk: medium
- review: required
- allowed: Read from client-owned portal
- notes: OAuth scope review required

### Google Places
- type: google_places
- risk: low
- review: required
- allowed: Public business profile
- notes: Rate-limit aware

### WhatsApp Business
- type: whatsapp_business
- risk: high
- review: required
- allowed: Approved templates only
- notes: Send only after human approval

### Email provider
- type: email_provider
- risk: medium
- review: required
- allowed: Approved outreach drafts
- notes: SMTP or transactional API

