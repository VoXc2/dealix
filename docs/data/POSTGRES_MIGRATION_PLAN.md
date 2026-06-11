# Postgres Migration Plan (Dealix)

## Steps
1. Create `revenue_events` table in Postgres
2. Create `accounts`, `drafts`, `proposals`, `deals`, `proof_items` tables
3. Use Alembic for schema versioning
4. Migrate from JSON to Postgres row-by-row
5. Keep JSON files as read-only archive for 30 days

## Mapping (JSON → SQL)

| JSON file | Table | Notes |
|-----------|-------|-------|
| leads.json (accounts) | accounts | id PK |
| outreach_review_queue.json (drafts) | drafts | draftId PK |
| proposals.index.json (proposals) | proposals | id PK |
| deals.ledger.json (deals) | deals | id PK |
| proof_vault.json (items) | proof_items | id PK |
| account_notes.json (notes) | account_notes | id PK |
| revenue_events.json (events) | revenue_events | id PK |

## Safety
- Migration is non-destructive
- After migration, both JSON and Postgres are valid
- Operator can roll back by switching `DATABASE_URL` to demo_json

## CI
- Demo mode must pass without DATABASE_URL
- Postgres migration tested in a separate workflow
