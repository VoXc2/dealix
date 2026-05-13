# Dealix Data — Business Unit

**Layer:** Holding · Compound Holding Model
**Owner:** Dealix Data GM
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [dealix_data_AR.md](./dealix_data_AR.md)

## Context
Dealix Data is the Business Unit that prepares a client's data for **decisions and AI** — not for theoretical "data strategy" decks, but for the concrete inputs that other Dealix BUs (Revenue, Operations, Brain, Support, Governance) actually need. It sits in the BU layer of [`docs/holding/DEALIX_HOLDING_OS.md`](../holding/DEALIX_HOLDING_OS.md), is paired with `docs/capabilities/data_capability.md`, and connects to the data-lake posture in `docs/ops/DATA_LAKE_PLAYBOOK.md`.

## Function
Data assesses readiness, runs cleanup (dedup, missing-field repair, PII tagging), publishes a Data Quality Score, and stands up a Data Intelligence Sprint that delivers an analytics-ready dataset wired into Core OS.

## Services offered

| Service | Duration | Outcome |
|---|---|---|
| Data Readiness Assessment | 1–2 weeks | Readiness score + remediation plan |
| Data Cleanup | 2–4 weeks | Dedup, missing-field fixes, PII tagging, lineage |
| Data Quality Dashboard | 1–2 weeks | Live quality score by source |
| Data Intelligence Sprint | 3–6 weeks | Analytics-ready dataset + first dashboards |

## Product modules (in Core OS)

| Module | Function |
|---|---|
| Data Quality Score | Per-source 0–100 score with breakdown |
| Deduplication | Configurable dedup with audit trail |
| PII Detection | Auto-tagging + retention policy binding |
| Source Registry | Inventory, owners, freshness, lineage |

## KPIs

- **Data readiness score** — composite 0–100.
- **Duplicates removed.**
- **Missing fields reduced** — % drop from baseline.
- **PII risk handled** — # fields tagged + retention applied.
- **Pipeline freshness** — % datasets within freshness SLA.
- **Downstream consumption** — # BU modules consuming the cleaned dataset.

## Core OS dependencies

| OS module | How Data consumes it |
|---|---|
| Data OS | Native consumer — registers sources, scores, lineage |
| Governance Runtime | Retention + DSR enforcement |
| LLM Gateway | When AI is used in cleansing (e.g., entity resolution) |
| Proof Ledger | Data Proof Pack: quality lift, dedup count, time saved |
| Capital Ledger | Reusable cleansing rules, dedup rule sets, sector schemas |
| AI Control Tower | Cost and quality of AI-assisted cleansing |

## Owner

| Role | Responsibility |
|---|---|
| Data BU GM | P&L, service ladder, retainer pull-through |
| Data Delivery Lead | Sprint execution + QA |
| Data CSM | Adoption + retainer health |
| Data Product Owner | Module backlog into Core OS |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Raw client sources | Cleansed datasets in Data OS | Data Delivery | Per sprint |
| Source updates | Quality + freshness telemetry | Data Quality Score | Realtime |
| Cleansing rules | Capital Ledger entries | Head of Core | Per sprint |
| Retainer renewal | Monthly data ops | Data CSM | Monthly |

## Metrics
- **MRR (Data BU).**
- **Gross margin.**
- **Quality lift** — average score uplift after cleanup.
- **Time-to-ready** — days from raw source to "Brain-ready" / "Revenue-ready".
- **PII tagging coverage.**

## Related
- `docs/capabilities/data_capability.md` — capability spec for this BU.
- `docs/ops/DATA_LAKE_PLAYBOOK.md` — data lake posture.
- `docs/EMBEDDINGS_PIPELINE.md` — downstream Brain pipeline.
- `docs/PRIVACY_PDPL_READINESS.md` — PDPL readiness.
- `docs/holding/DEALIX_HOLDING_OS.md` — umbrella holding model.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
