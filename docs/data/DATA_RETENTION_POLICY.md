# Data Retention Policy (Dealix)

| Record | Retention | Reason |
|--------|-----------|--------|
| Non-qualified lead | 90 days | Marketing interest |
| Rejected outreach draft | 12 months | Learning |
| Signed client | Lifetime + 24 months | Legal + reference |
| Proof item | Lifetime of client + 24 months | Case study |
| Audit log | 12 months | Compliance |
| Backup archives | 90 days rolling | Recovery |

## How we delete
- Client request: delete within 14 days
- Auto-cleanup: after retention period
- No backup after deletion

## Storage
- `business/_data/*.json` (demo)
- `business/_data/audit/*.jsonl` (audit)
- `reports/backups/*.zip` (manual backups)
- Postgres (when enabled)
