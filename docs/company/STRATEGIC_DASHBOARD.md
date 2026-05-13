# Dealix Strategic Dashboard

Capital-based view of company health. Refreshed monthly. Complements
`docs/company/FOUNDER_COMMAND_CENTER.md` (which is daily/weekly).

## Service Capital

| Metric | Current | Target (M+3) |
|--------|--------:|-------------:|
| Sellable services | 3 | 5 |
| Beta services | 0 | 1 |
| Designed services in catalog | 5 | 8 |
| Average Service Readiness Score | 88 | 92 |
| SOW templates ready | 3 | 5 |

## Product Capital

| Metric | Current | Target (M+3) |
|--------|--------:|-------------:|
| OS modules at MVP+ | 5 | 7 |
| Production-grade modules | 0 | 2 |
| Reusable templates / scripts | ~12 | 25 |
| Demos runnable | 3 | 4 |
| Active automated workflows in customer-facing use | 0 | 5 |

## Knowledge Capital

| Metric | Current | Target (M+3) |
|--------|--------:|-------------:|
| Vertical playbooks (drafted) | 3 (BFSI/Retail/Healthcare) | 6 |
| Objection counters | 12 | 25 |
| Reusable templates in `docs/assets/templates/` | 0 (pre-revenue) | 10 |
| Sector insights logged in Learning Ledger | 0 (pre-revenue) | 15 |

## Trust Capital

| Metric | Current | Target (M+3) |
|--------|--------:|-------------:|
| Anonymized Proof Packs in `docs/assets/proof_packs/` | 0 (pre-revenue) | 3 |
| Anonymized case studies | 0 | 1 published |
| Governance Ledger incidents | 0 | 0 (target stays 0) |
| Quality Score average | n/a | ≥ 85 |
| Customer NPS / satisfaction (when measured) | n/a | ≥ 8/10 |

## Market Capital

| Metric | Current | Target (M+3) |
|--------|--------:|-------------:|
| Outbound contacts | 0 | 200 |
| Discovery calls held | 0 | 30 |
| Paying customers | 0 | 5 |
| Active retainers | 0 | 1 |
| Partner channels signed | 0 | 2 |
| Authority content pieces published | 0 | 12 |

## Compounding indicator

The single number to watch: **time-to-deliver-same-service second customer
vs first**. Target ≤ 80% by 3rd customer; ≤ 60% by 5th. If this number
doesn't drop, the flywheel isn't turning — diagnose which station broke
via `docs/company/OPERATING_FLYWHEEL.md`.

## Decision tree from this dashboard

- Service Capital < target → ship the Designed → Beta → Sellable promotion this month.
- Product Capital < target → check Feature Prioritization backlog; promote next Build-Now.
- Knowledge Capital < target → playbook update missing from recent project; HoCS chase.
- Trust Capital < target → Proof Pack discipline broken; review COMPOUNDING_SYSTEM compliance.
- Market Capital < target → outbound velocity issue; CRO + SDR review.

## Owner & cadence

- **Owner**: CEO.
- **Refresh**: monthly during operating cadence (W5.T30).
- **Sources**: `verify_dealix_ready.py` + 8 Operating Ledgers.

## Cross-links

- `docs/company/DEALIX_CAPITAL_MODEL.md`
- `docs/company/FOUNDER_COMMAND_CENTER.md`
- `docs/company/MATURITY_BOARD.md`
- `docs/company/OPERATING_FLYWHEEL.md`
- `docs/ledgers/README.md`
