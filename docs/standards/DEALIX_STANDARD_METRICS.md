# Dealix Standard Metrics — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** Group CFO + Head of Dealix Core
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DEALIX_STANDARD_METRICS_AR.md](./DEALIX_STANDARD_METRICS_AR.md)

## Context
The Dealix Standard Metrics are the **category-defining metrics** that Dealix publishes so that clients, partners, and the market use one vocabulary to talk about AI Operations. They are the public face of the [`DEALIX_METHOD`](./DEALIX_METHOD.md) — each metric measures one phase of the Method, with a clear definition and a clear formula. They feed `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` and the [`HOLDING_SCORECARD`](../holding/HOLDING_SCORECARD.md), and inherit observability from `docs/AI_OBSERVABILITY_AND_EVALS.md`.

## The eight standard metrics

### 1. Capability Level (CL)
- **Definition:** Maturity level of an AI capability at the customer, on a 1–5 scale.
- **Levels:** 1 Ad-hoc · 2 Repeatable · 3 Governed · 4 Productized · 5 Compounding.
- **Formula:** Composite of QA score, Governance Coverage, Productization, and adoption rate.

### 2. Data Readiness Score (DRS)
- **Definition:** How ready a data source is for AI consumption.
- **Range:** 0–100.
- **Formula:** Weighted blend of completeness, freshness, deduplication ratio, PII handling, lineage completeness, and schema conformance.
- **Threshold:** ≥ 70 = "Brain-ready"; ≥ 80 = "Revenue-ready".

### 3. Governance Coverage (GC)
- **Definition:** Share of model calls bound to at least one explicit policy.
- **Formula:** `(model_calls_with_policy_id ÷ total_model_calls) × 100`.
- **Target:** 100% for production workflows; ≥ 95% for sandbox.

### 4. QA Score (QAS)
- **Definition:** Quality score of a delivered workflow at the QA gate.
- **Range:** 0–100.
- **Formula:** Weighted blend of eval pass rate, citation accuracy, latency SLA, error rate, and review checklist.
- **Threshold:** ≥ 85 for delivery sign-off.

### 5. Proof Coverage (PC)
- **Definition:** Share of closed engagements with a Proof Pack in the Proof Ledger.
- **Formula:** `(closed_engagements_with_proof_pack ÷ closed_engagements) × 100`.
- **Target:** 100%.

### 6. Value Realization (VR)
- **Definition:** Measured economic value generated relative to fees paid.
- **Formula:** `(measured_value ÷ fees_paid)` over a rolling 90-day window.
- **Threshold:** ≥ 3× for "proven value"; ≥ 5× for "category-class".

### 7. Capital Creation (CC)
- **Definition:** Number of reusable Capital Ledger assets created per engagement.
- **Formula:** `capital_assets_created` per closed engagement.
- **Target:** ≥ 2 per engagement.

### 8. Retainer Readiness (RR)
- **Definition:** Likelihood, at sprint close, that the engagement will convert to a retainer within 60 days.
- **Range:** 0–100.
- **Formula:** Composite of QAS, PC, VR, and customer adoption indicators.
- **Threshold:** ≥ 60 = "retainer-ready".

## Summary table

| Metric | Definition | Formula | Target |
|---|---|---|---|
| Capability Level | Maturity 1–5 of an AI capability | Composite | ≥ 3 to scale |
| Data Readiness Score | 0–100 readiness | Weighted blend | ≥ 70 / ≥ 80 |
| Governance Coverage | Policy-bound model calls | calls_with_policy ÷ total | 100% prod |
| QA Score | Quality at QA gate | Weighted blend | ≥ 85 |
| Proof Coverage | Engagements with Proof Pack | proof_packs ÷ closed | 100% |
| Value Realization | Value ÷ fees | measured_value ÷ fees | ≥ 3× |
| Capital Creation | Reusable assets per engagement | count of `capital_asset_created` | ≥ 2 |
| Retainer Readiness | Likelihood to renew | Composite | ≥ 60 |

## Sources of truth

| Metric | Source system |
|---|---|
| CL | Capability registry (`docs/capabilities/*`) |
| DRS | Data OS / Source Registry |
| GC | Governance Runtime audit log |
| QAS | QA gate logs |
| PC | Proof Ledger |
| VR | Customer-verified value tracker + invoicing system |
| CC | Capital Ledger |
| RR | CSM workspace; computed |

## Publishing the standard
- The Standard Metrics are versioned (current `v1.0 — 2026-05-13`).
- Public methodology page references each metric by its definition.
- Partner certifications require demonstrating measurement of all eight in delivery.
- Academy curriculum teaches all eight.

## Anti-patterns
- Inventing per-BU variants of the standard metrics — disallowed; submit a change request to this file instead.
- Reporting a metric without its formula — disallowed in client materials.
- Marking a project "Closed" when PC = 0 — blocked at the QA gate.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Engagement telemetry | Per-engagement metric set | Core OS | Per project |
| Aggregated metrics | Holding Scorecard rows | CFO | Weekly |
| Metric definition changes | Versioned spec update | Head of Core | Quarterly |
| Public methodology page | Marketing collateral | Brand | Per release |

## Metrics (about the metrics)
- **Standard metric coverage** — % engagements reporting all 8 metrics.
- **Metric freshness** — max age in hours of any metric in the dashboard.
- **Definition drift** — number of unauthorized per-BU variants detected.
- **External adoption** — # partners and clients using the standard publicly.

## Related
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — dashboard spec.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability framework.
- `docs/EXECUTIVE_DECISION_PACK.md` — weekly decision packet.
- `docs/standards/DEALIX_METHOD.md` — methodology this measures.
- `docs/holding/HOLDING_SCORECARD.md` — board scorecard.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft (v1.0) |
