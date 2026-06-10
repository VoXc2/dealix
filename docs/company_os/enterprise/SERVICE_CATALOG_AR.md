# Dealix Service Catalog

## Public Services

| Service | URL | Purpose | Owner |
|---|---|---|---|
| API | https://api.dealix.me | backend, contracts, health | Founder/Ops |
| Web | https://web-production-380c3.up.railway.app | landing, demo, revenue pages | Founder/Ops |
| Demo | /ar/demo | sales demo | Sales |
| ZATCA Readiness | /ar/zatca-readiness | compliance-led GTM | Sales/Ops |
| Revenue OS | /revenue-os | core product narrative | Sales |

## Private Services

| Service | Purpose | Public Networking |
|---|---|---|
| company-brain | daily CEO brain + drafts + scorecards | OFF |
| production-watchdog | periodic health checks | OFF |
| Postgres | production data | private only |

## Rule

Every service must have:
- owner
- health signal
- rollback path
- no-secret logs
- clear deployment config
