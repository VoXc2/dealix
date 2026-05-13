---
title: Dealix Quality Standard — 5-Gate QA + 100-Point Score
doc_id: W6.T36.quality-standard
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
ar_companion: none
related: [W6.T36, W6.T34, W4.T25]
kpi:
  metric: avg_quality_score
  target: 85
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 0.5
  score: quality-foundation
---

# Dealix Quality Standard — Summary

## 1. Context

Every Dealix project passes the same five QA gates and is scored on the same
hundred-point rubric. **Floor for shipping: 80.** Below 80, the project
cannot transition Validate → Deliver. This is the operator-friendly summary
of the canonical Standard.

The authoritative version lives in
[`../strategy/dealix_delivery_standard_and_quality_system.md`](../strategy/dealix_delivery_standard_and_quality_system.md)
(§4 and §5). The execution code is `auto_client_acquisition/delivery_factory/qa_review.py`.

## 2. Audience

CS, Delivery, Engineering. New hires read this; canonical doc for detail.

## 3. The 5 Gates

| Gate | Catches | Sample question |
|------|---------|-----------------|
| **Business** | Vague problem, no KPI, no next action | "Is there a numeric KPI?" |
| **Data** | Unattributed sources, missing PII redaction | "Is lawful basis (PDPL Art. 5) documented?" |
| **AI** | Hallucinations, untraced citations, wrong AR tone | "Are sources cited?" |
| **Compliance** | Forbidden claims, missing approval, audit gaps | "Is human approval logged where required?" |
| **Delivery** | Missing handoff items, unclear exec report | "Is the executive report clear to a non-technical reader?" |

Any single FAIL across any gate blocks shipping. Detailed question lists are
encoded in `qa_review.py`.

## 4. The 100-Point Score

Seven criteria, weighted. Floor for handoff = 80.

| Criterion | Weight |
|-----------|-------:|
| Business impact clarity | 20 |
| Data quality | 15 |
| AR/EN output quality | 15 |
| Customer usability | 10 |
| Safety & compliance | 15 |
| Productization potential | 15 |
| Retainer upgradeability | 10 |
| **Total** | **100** |

Detailed scoring rubric per criterion is in
[`SERVICE_READINESS_SCORE.md`](SERVICE_READINESS_SCORE.md) (for offerings)
and in the canonical Standard (for projects).

## 5. Operating Rule

```python
ships = all(gate.passed for gate in gates) and score.total >= 80
```

`ships=True` is required for the Stage Machine to allow Validate → Deliver.

## 6. Why This Matters

The same offering delivered to two customers must produce the same QA
scoreboard. Variability is the enemy of productization. The Quality Standard
is what turns Dealix from a freelance shop into a productized AI Operating
Partner.

## 7. Cross-links

- Canonical Standard: [`../strategy/dealix_delivery_standard_and_quality_system.md`](../strategy/dealix_delivery_standard_and_quality_system.md)
- Review process: [`QA_REVIEW_PROCESS.md`](QA_REVIEW_PROCESS.md)
- AI evals: [`AI_OUTPUT_EVALS.md`](AI_OUTPUT_EVALS.md)
- Arabic quality: [`ARABIC_QUALITY_GUIDE.md`](ARABIC_QUALITY_GUIDE.md)
- Report quality: [`REPORT_QUALITY_GUIDE.md`](REPORT_QUALITY_GUIDE.md)
- Service readiness: [`SERVICE_READINESS_SCORE.md`](SERVICE_READINESS_SCORE.md)
- Code: `auto_client_acquisition/delivery_factory/qa_review.py`

## 8. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: weekly scoreboard meeting; quarterly rubric refresh.

## 9. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial summary of 5 gates + 100-point score + 80 floor |
