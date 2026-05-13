---
doc_id: strategy.ai_ops_category_metrics
title: AI Operations Category Metrics — The Numbers Dealix Publishes Annually
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal, board, market]
---

# AI Operations Category Metrics

> Categories are created by **publishing the metrics the category is
> judged on**. Dealix publishes 9 metrics annually. These metrics
> become the Saudi reference for "AI Operations" and shift buyer
> conversations from features to outcomes. The aggregated report is
> the long-term moat described in `FROM_SERVICE_TO_STANDARD.md`
> Stage 4.

## The 9 metrics Dealix publishes

| # | Metric | Definition | Source ledger | Why it matters |
|---|--------|------------|---------------|----------------|
| 1 | AI Workflow Adoption | % of customer workflows running through the Dealix capability (vs untouched) | Delivery | Cuts through "we use AI" rhetoric — measures embedding |
| 2 | Data Readiness Score | 0–100 score per customer pre-AI | Delivery + Proof | Defines the precondition the category requires |
| 3 | Human Approval Rate | % of AI-proposed external actions approved by a human | Governance | Anti-pattern detector for runaway automation |
| 4 | Proof Pack Coverage | % of paid projects closed with a v6 Proof Pack within 14 days | Delivery + Proof | Defines "done" in the category |
| 5 | QA Score Average | Mean 100-point Project Quality Score across all deliveries | Delivery (QA) | Floor: 80 / Target: 85+ — the Dealix Standard |
| 6 | Governance Incidents | Count of major incidents per 100 deliveries (PII, forbidden claim, approval bypass) | Governance | Trust + procurement signal |
| 7 | Time to Value | Median calendar days from contract signature to first measured KPI delta | Delivery + Proof | Defines the speed promise of the category |
| 8 | Sprint-to-Retainer Conversion | % of Sprints (Tier 2) that progress to a Tier 3 Pilot or Tier 4 Retainer within 60 days | Client + Delivery | Health of capability framing vs deliverable framing |
| 9 | Capability Level Improvement | Average level delta across the 7 capabilities per customer per 90 days | Proof + Client | The core promise: capabilities mature, not stagnate |

## How the metrics are produced

The 8 ledgers (`OPERATING_LEDGER.md`) capture raw rows. The Control
Plane aggregates per quarter. CEO + CRO + CTO sign off the annual
snapshot. Anonymized per `EVIDENCE_SYSTEM.md`, then published as the
**Saudi AI Operations Benchmark** report. Each metric ships with
definition, method, and sample distribution — never a single number
without context.

## Audit + reproducibility

Each published metric must be reproducible from named ledger rows
(anonymized), auditable by HoLegal before publication (PDPL safe),
cited with sample size + standard deviation when ≥ 10 customers, and
comparable year over year — definitions versioned in git.

## Why these 9, not 15

Cost per token is engineering, not outcome. Model accuracy is a model
metric, not a capability metric. NPS is a survey, too easily gamed.
Logo count is in `12_MONTH_ROADMAP.md`, not a category metric. The 9
above are the smallest set that fully describes the AI Operations
category and uniquely positions Dealix.

## Long-term — the Saudi AI Operations Benchmark

By the end of 2027 (target), the Saudi AI Operations Benchmark is the
report Saudi enterprises cite in their own AI procurement RFPs.
Method:

- Annual publication (Q1, looking at prior year).
- Bilingual (AR + EN).
- Distributed to Vision 2030 program offices, SDAIA, large enterprise
  procurement teams.
- Backed by ≥ 25 paying customers' anonymized data (gate to publish:
  Stage 4, `FROM_SERVICE_TO_STANDARD.md`).

## Saudi / PDPL context

Metric 3 (Human Approval Rate) and Metric 6 (Governance Incidents)
are the two metrics PDPL enforcement actions track most closely.
Dealix publishing them transparently moves the category from "can we
trust AI?" to "here is the trust standard."

## Cross-links

- `docs/strategy/CATEGORY_DESIGN.md` — category claim
- `docs/strategy/FROM_SERVICE_TO_STANDARD.md` — Stage 4 (Standard)
- `docs/strategy/MENA_EXPANSION_LOGIC.md` — when the benchmark goes regional
- `docs/company/NORTH_STAR_METRICS.md` — internal North Stars
- `docs/company/OPERATING_LEDGER.md` — the 8 ledgers
- `docs/company/CONTROL_PLANE.md` — aggregation
- `docs/company/EVIDENCE_SYSTEM.md` — what counts as published evidence
- `docs/company/DEALIX_STANDARD.md` — the 8 standards behind these metrics
