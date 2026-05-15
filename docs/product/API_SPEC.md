# API Spec — ideal vs implemented

## Ideal (north star)

| Area | Ideal endpoint |
|------|----------------|
| Data | `POST /api/v1/data/import-preview` |
| Data | `POST /api/v1/data/quality-score` |
| Revenue | `POST /api/v1/revenue/score-accounts` |
| Knowledge | `POST /api/v1/knowledge/search` |
| Governance | `POST /api/v1/governance/check` |
| Reports | `POST /api/v1/reports/proof-pack` |

## Implemented today (representative)

| Purpose | Actual path |
|---------|-------------|
| CSV preview | `POST /api/v1/revenue-data/csv-preview` |
| Commercial engagements | `POST /api/v1/commercial/engagements/lead-intelligence-sprint` |
| Company brain | `POST /api/v1/company-brain/query` |
| Governance dashboard | `GET /api/v1/governance/risk-dashboard` |
| Service readiness | `GET /api/v1/commercial/service-readiness/{service_id}` |
| Readiness gates | `POST /api/v1/commercial/readiness-gates/check` |

Gap list shrinks as routers align naming; do not break clients without versioning.
