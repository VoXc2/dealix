# CRM Connector Integration — Setup Guide

**Status:** SCHEMA_ONLY — no real HubSpot/Zoho/Salesforce client built (Article 11 — deferred)
**Audience:** Dealix paying customers + Sami (founder)
**Companion:** `api/routers/crm_v10.py` · `auto_client_acquisition/crm_v10/`
**Wave:** 7.5 §24.4

> **Honest disclosure:** Dealix has the CRM data **schema** (Lead/Contact/Account/Deal) but does NOT have working connectors to HubSpot, Zoho, or Salesforce. This guide explains the manual CSV-export workaround that works for customers 1-3 + what activates when the connector TARGET services trigger.

---

## What works today (manual CSV workaround)

### Weekly CSV export (covers HubSpot / Zoho / Salesforce)

1. Customer's CRM admin exports a CSV weekly:
   - HubSpot: Contacts → Filter (recent leads) → Export → CSV
   - Zoho CRM: Leads → All → Bulk Export → CSV
   - Salesforce: Reports → Recent Leads → Export Details → CSV

2. Required columns (renamed if necessary):
   - `email` (required)
   - `first_name`, `last_name`
   - `company_name`
   - `phone` (Saudi format with +966)
   - `industry`, `country`, `city`
   - `created_at` (ISO 8601)
   - `notes` (optional)

3. Customer shares CSV with Sami via secure channel:
   - Recommended: 1Password vault item with file attachment
   - Alternative: encrypted email (PGP)
   - **NEVER:** plain WhatsApp/email attachment with PII

4. Sami runs (after DPA chain confirmed):

```bash
# Manual ingestion (Wave 6 + Wave 7.5 — interim until self-serve built)
python3 scripts/dealix_first_prospect_intake.py \
  --prospect-handle <derived> --sector <customer-sector> \
  --relationship warm --note "From CRM export $(date +%Y-%m-%d)"

# For each row in CSV (loop or hand-entry for first 3 customers)
```

**Cadence:** weekly. Sami's Friday review (per `SALES_OPS_SOP.md` §10) includes "ingest customer CSVs."

---

## CRM-specific notes

### HubSpot

- Free CMS Hub provides 1,000-5,000 contact tier
- Export limit: 10K rows/CSV
- Webhooks available on Marketing Hub Pro+ (deferred to Wave 8 connector)

### Zoho CRM

- Standard Edition supports CSV export
- Up to 5K records per export batch
- API limits: 1K calls/day (free tier — too restrictive for live sync)

### Salesforce

- Sales Cloud Essentials (entry tier) supports CSV export via Reports
- Bulk API requires Lightning Edition+
- Per-account API limit: 15K calls/day (free tier — adequate when connector built)

---

## What activates with `crm_connector` TARGET (Wave 8)

When triggered (per Article 11 — first customer asks for live sync):

### HubSpot connector (priority — highest market share in KSA)

```bash
# Future state
curl -X POST https://api.dealix.me/api/v1/integrations/crm/hubspot/connect \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"customer_handle": "acme-real-estate", "hubspot_api_key": "<paste>"}'
```

- Webhook on contact-create event
- Deal-stage updates synced from Dealix back to HubSpot
- 2-way sync with conflict resolution (last-write-wins on configurable fields)

### Generic CRM webhook

```bash
POST https://api.dealix.me/api/v1/webhooks/crm/inbound
{
  "source": "salesforce",
  "event": "lead.created",
  "lead": {...}
}
```

---

## Verification (current state)

```bash
# Verify schema accepts CSV-derived leads
curl -s -X POST https://api.dealix.me/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ali@example.sa",
    "first_name": "Ali",
    "company_name": "Acme",
    "industry": "real_estate",
    "phone": "+966512345678"
  }'
# Should return 200 with qualification result inline
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| CSV import takes hours | Customer has 10K+ rows | Split into batches of 1K; first import = "warm fan only" filter |
| Phone format errors | International formatting variance | Normalize to E.164 (`+966...`) before ingestion |
| Duplicate detection misses some | Different email cases | Run dedup with `email.lower()` normalization (already done in `pipelines/dedupe.py`) |
| Industry field unmapped | Customer's CRM uses non-standard taxonomy | Map to Dealix's 8 sectors manually first time; save mapping in `data/customers/<handle>/sector_mapping.json` |

---

## Hard rules (immutable in code)

- ❌ NO_SCRAPING: never pull data from competitor CRMs / public registries / scraped sources
- ❌ NO_LIVE_CHARGE: CSV import never triggers payments
- ✅ Every imported lead gets a consent_record_id of "pending" until verified
- ✅ DPA chain enforced before any customer PII is stored

---

## PDPL compliance for CRM imports

When importing customer's CRM data, Dealix is **Processor**, customer is **Controller**:
- Customer holds the legal basis (legitimate interest / consent)
- Dealix processes only per DPA terms
- Each imported PII record carries the customer's `data_subject_owner_id` for downstream DSAR routing

---

## What's deferred to Wave 8

- HubSpot live API connector
- Zoho live API connector
- Salesforce live API connector
- 2-way sync with conflict resolution
- Self-serve CSV upload UI for customer (currently founder-led)
- Field-mapping wizard for non-standard CRM taxonomies
