# Audit Logging Plan (Dealix)

## What we log
- Every outreach draft (with reviewer + status)
- Every proposal (with offer + lang)
- Every deal (won / lost, with value)
- Every proof item
- Every change request
- Every credential rotation
- Every external send (template id + contact + reviewer)

## Format
- Append-only JSONL
- Stored in `reports/audit/*.jsonl`
- One file per month

## Retention
- 12 months minimum
- Encrypted at rest
- Accessible only to founder

## Tools
- `scripts/backup_business_data.py` — includes audit
- `scripts/restore_business_data.py` — requires explicit confirm
