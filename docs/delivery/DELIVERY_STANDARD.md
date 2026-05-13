---
title: Dealix Delivery Standard — 8-Stage Summary
doc_id: W6.T36.delivery-standard-summary
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
ar_companion: none
related: [W6.T36, W6.T34, W6.T35]
kpi:
  metric: stage_completion_rate
  target: 100
  window: per_project
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 0.5
  score: delivery-summary
---

# Dealix Delivery Standard — Summary

## 1. Context

Every Dealix project — Sprint, Pilot, Retainer, Enterprise — follows the same
**eight-stage Delivery Standard**. This file is the operator-friendly summary.
The canonical, authoritative version lives in
[`docs/strategy/dealix_delivery_standard_and_quality_system.md`](../strategy/dealix_delivery_standard_and_quality_system.md).

## 2. Audience

CS, Delivery, Engineering, CRO. New hires read this first; reference the
canonical doc for detail.

## 3. The 8 Stages (at a glance)

```
Discover → Diagnose → Design → Build → Validate → Deliver → Prove → Expand
```

| # | Stage | Purpose | Stage Output |
|---|-------|---------|--------------|
| 1 | **Discover** | Understand the company, data, pains | Intake form + discovery summary |
| 2 | **Diagnose** | Score situation, identify quick wins | Diagnostic report + top-3 use cases |
| 3 | **Design** | Architect the solution | Signed design document |
| 4 | **Build** | Execute with minimum complexity, reusing OS modules | Working build in customer env |
| 5 | **Validate** | Stress-test for quality, safety, AR/EN tone, PII | Validation report (pass/fail) |
| 6 | **Deliver** | Hand over with discipline | Handoff packet (acknowledged) |
| 7 | **Prove** | Quantify impact within 14 days | Proof pack in Proof Ledger |
| 8 | **Expand** | Open the next conversation | Signed renewal or documented "no" |

## 4. Why the Standard Matters

A consistent eight-stage rhythm is what turns Dealix from a freelance-style
shop into a **productized AI Operating Partner**. The same offering delivered
to a second customer must score the same on QA, run the same timebox, and
produce the same kind of evidence. Variability is the enemy.

## 5. How to Use This

- Open every project in the Stage Machine (`stage_machine.py`) at Stage 1.
- Each transition requires the prior stage's stated output to exist.
- Stage 5 → Stage 6 is gated by `ships=True` from the QA evaluator.
- Stage 8 must produce a written next step (yes or documented no).

## 6. Cross-links

- Canonical Standard: [`docs/strategy/dealix_delivery_standard_and_quality_system.md`](../strategy/dealix_delivery_standard_and_quality_system.md)
- Lifecycle by day: [`DELIVERY_LIFECYCLE.md`](DELIVERY_LIFECYCLE.md)
- Handoff process: [`HANDOFF_PROCESS.md`](HANDOFF_PROCESS.md)
- Renewal process: [`RENEWAL_PROCESS.md`](RENEWAL_PROCESS.md)
- Quality system: [`../quality/QUALITY_STANDARD.md`](../quality/QUALITY_STANDARD.md)
- Stage machine code: `auto_client_acquisition/delivery_factory/stage_machine.py`
- Pilot framework (extended scope): [`pilot_framework.md`](pilot_framework.md)

## 7. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: refresh when the canonical doc changes; otherwise quarterly.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial summary file pointing to canonical Standard |
