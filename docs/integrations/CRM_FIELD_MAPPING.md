# CRM Field Mapping (Dealix)

See `docs/integrations/V7_CRM_SYNC_ARCHITECTURE.md` for full table.

## Local JSON
- `business/_data/leads.json` — `accounts[]`
- `business/_data/outreach_review_queue.json` — `drafts[]`
- `business/_data/proposals.index.json` — `proposals[]`
- `business/_data/deals.ledger.json` — `deals[]`
- `business/_data/proof_vault.json` — `items[]`

## CSV export
- `business/crm/exports/dealix-crm-export-YYYY-MM-DD.csv`
- Fields: see `scripts/export_crm_csv.py`
