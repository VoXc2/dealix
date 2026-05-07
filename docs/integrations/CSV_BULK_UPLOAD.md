# CSV Bulk Upload — Setup Guide

**Status:** NOT_BUILT — manual founder-led import for customers 1-3 (Article 11 — deferred)
**Audience:** Dealix paying customers + Sami (founder)
**Companion:** `auto_client_acquisition/lead_inbox.py` · `scripts/dealix_first_prospect_intake.py`
**Wave:** 7.5 §24.4

> **Honest disclosure:** Self-serve CSV upload is NOT built. Sami imports first batch manually for customers 1-3. Self-serve activates in Wave 8 when 3rd customer asks.

---

## Current workaround (Sami-led, customers 1-3)

### Step 1 — Customer prepares CSV

Required columns (case-insensitive, will be normalized):

| Column | Type | Required | Example |
|---|---|---|---|
| `email` | string | ✅ | `ali@acme.sa` |
| `first_name` | string | recommended | `Ali` |
| `last_name` | string | recommended | `Al-Saud` |
| `company_name` | string | recommended | `Acme Riyadh Real Estate` |
| `phone` | E.164 string | optional | `+966512345678` |
| `industry` | enum | optional | `real_estate` (or `consulting`, `agencies`, etc.) |
| `country` | ISO-2 | optional | `SA` |
| `city` | string | optional | `Riyadh` |
| `notes` | string | optional | "Met at Saudi Real Estate Conf 2026" |
| `consent_status` | enum | required for outbound use | `signed` / `verbal` / `pending` |
| `created_at` | ISO 8601 | optional | `2026-05-01T10:00:00+03:00` |

**Encoding:** UTF-8. Saudi-Arabic names + addresses fully supported.

### Step 2 — Customer secure-share

Customer uploads CSV to **shared 1Password vault** with Sami:
1. Sami creates "Dealix - {customer-handle} - imports" vault
2. Customer adds CSV as file attachment with note: "first batch, N rows, exported from <source>, exported on <date>"
3. Sami acknowledges receipt within 24h

**NEVER share CSV via:**
- Plain WhatsApp / Telegram (PII exposure)
- Plain email (PDPL violation risk)
- Public Google Drive link
- Scrapeable URL

### Step 3 — Sami pre-flight check

```bash
# Sami runs locally (data NEVER touches dealix.me until validated):
python3 -c "
import csv
with open('input.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f'Rows: {len(rows)}')
    print(f'Columns: {list(rows[0].keys())}')
    # Validate required cols
    for col in ['email', 'consent_status']:
        assert col in rows[0], f'Missing required column: {col}'
    # Sample
    print(f'Sample row: {rows[0]}')
"
```

### Step 4 — Sami imports row-by-row (until Wave 8 self-serve)

For first 3 customers, manual loop:

```bash
# For each row in CSV (Sami's local script — gitignored)
python3 scripts/dealix_first_prospect_intake.py \
  --prospect-handle <derived-from-email> \
  --sector <customer-sector-mapped> \
  --relationship warm \
  --note "Imported from <customer> CSV $(date +%Y-%m-%d)"
```

For 50+ rows, Sami runs a wrapper bash loop (kept locally, NOT committed):

```bash
# scripts/local_import_loop.sh (gitignored)
while IFS=, read -r email first_name company; do
  handle=$(echo "$email" | sed 's/@.*//' | tr '.' '-')
  python3 scripts/dealix_first_prospect_intake.py \
    --prospect-handle "$handle" --sector real_estate --relationship warm \
    --note "$company - imported $(date +%Y-%m-%d)"
done < input.csv
```

**Limits per Wave 7 hard caps:**
- Max 100 rows imported per customer per week (founder-time budget)
- Pre-import: customer signals quality (which rows are HOT vs cold leads)
- Pre-import: sector mapping confirmed

### Step 5 — Customer verifies in Customer Portal

```
https://dealix.me/customer-portal.html?org=<handle>&access=<token>
```

Lead Inbox should show new rows under "Imported" filter.

---

## What activates in Wave 8 (`csv_bulk_upload` TARGET)

When triggered (3rd customer asks for self-serve):

### Self-serve UI

- `landing/customer-portal.html` adds "Import CSV" button
- Drag-drop file → preview first 5 rows → field-mapping wizard
- Confirm → background job processes (with progress bar)
- Error CSV downloadable for failed rows

### API endpoint

```bash
POST https://api.dealix.me/api/v1/leads/bulk-import
Content-Type: multipart/form-data
Authorization: Bearer <customer-token>
file=@input.csv
&customer_handle=acme-real-estate
&sector_mapping={"Real Estate Office": "real_estate"}
```

Returns:
```json
{
  "import_id": "imp_<timestamp>",
  "rows_processed": 142,
  "rows_imported": 138,
  "rows_failed": 4,
  "error_csv_download_url": "/api/v1/leads/bulk-import/imp_xxx/errors.csv",
  "estimated_complete_at": "..."
}
```

---

## Verification (current state)

```bash
# Confirm Lead Inbox surfaces imported rows
curl -s "https://api.dealix.me/api/v1/customer-portal/<handle>?access=<token>" | jq '.sections.lead_inbox.recent_leads'

# Should show entries with "imported" tag
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Saudi-Arabic names show as `???` | CSV not UTF-8 | Re-export CSV with UTF-8 encoding (Excel: Save As → CSV UTF-8) |
| Phone numbers fail validation | Mixed formats | Normalize to E.164 before import: `+966XXXXXXXXX` |
| Duplicate emails create duplicate handles | Pre-existing customer leads | Dedup runs automatically (`pipelines/dedupe.py`); duplicates merge |
| `consent_status=signed` but customer can't show DPA | DPA gap | STOP import — go back to `LEGAL_ENGAGEMENT.md` and engage lawyer |

---

## Hard rules (immutable in code)

- ❌ NO_SCRAPING: customer cannot import scraped data; consent must come from customer's own collection
- ❌ NO_BLAST: CSV import does NOT trigger outbound; Sami still approves each first contact 1-by-1
- ❌ NO_LIVE_CHARGE: bulk import never costs customer extra
- ✅ Every imported lead has `consent_status` field — outbound BLOCKED until `signed`
- ✅ DPA chain enforced (customer = Controller, Dealix = Processor)

---

## What's deferred to Wave 8

- Self-serve UI in Customer Portal
- API endpoint with multipart upload
- Field-mapping wizard for non-standard CSVs
- Async import with progress + error CSV download
- Sample CSV template downloadable from `/customer-portal.html`
- Bulk import test mode (validate without writing)
