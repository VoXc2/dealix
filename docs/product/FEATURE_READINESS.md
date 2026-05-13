---
title: Feature Readiness — Criteria for Promotion to Production
doc_id: W6.T37.feature-readiness
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T37, W4.T23, W4.T24]
kpi:
  metric: features_meeting_readiness_at_merge
  target: 100
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 0.5
  score: engineering-quality
---

# Feature Readiness

## 1. Context

A feature enters production only when it can be operated by anyone on the
team without the original author present. The five readiness criteria below
are the gate; without all five, a feature is in beta, behind a flag, or in
internal-only use.

This is the operator-friendly summary of the Production Readiness Gate in
[`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md)
§5.4.

## 2. Audience

Engineers (must meet the criteria before opening a release PR), CTO
(approves promotion), HoP (assesses readiness for customer-facing
exposure), SRE on-call (consumes operational artifacts).

## 3. The Five Criteria

| # | Criterion | What "ready" looks like |
|---|-----------|-------------------------|
| 1 | **Tests** | Unit + integration tests cover happy path + critical edge cases; CI green |
| 2 | **Logging** | Structured logs at decision points; error logs include actor + subject; no PII |
| 3 | **Audit** | Every policy-relevant action emits an audit event per [`../governance/AUDIT_LOG_POLICY.md`](../governance/AUDIT_LOG_POLICY.md) |
| 4 | **Docs** | Engineering README + customer-facing description (where applicable) + ADR if architecturally significant |
| 5 | **Cost guard** | Per-tenant rate limit; LLM cost capped; circuit breaker on third-party calls |

A feature failing any criterion is **not** promoted. It stays behind a
feature flag, in internal-only state, or is removed.

## 4. Additional Conditions (Per the Production Readiness Gate)

- No **PII leakage** path (verified against `pii_detector` boundaries).
- **Output schema** defined where the feature returns structured data.
- **Fallback path** defined for any LLM-backed feature (degraded mode
  when the model is unavailable).
- **SLO** declared and observable (latency p95, error rate, cost per
  request — see [`../sre/slo_framework.md`](../sre/slo_framework.md)).

## 5. The "Build Only After Repetition" Rule

Per [`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md)
§7, a feature is added to the platform only after the underlying need has
occurred ≥ 2 times in real delivery. This rule prevents premature
engineering and ensures every feature is paid for in delivery time before
its build cost is incurred.

## 6. Promotion Workflow

```
Feature flag (off) →
  internal-only beta (small tenant set) →
  external beta (named customer + monitoring) →
  general availability (flag default on)
```

Each step requires explicit approval: CTO for internal beta, HoP for
external beta, CTO + HoP for general availability.

## 7. Anti-Patterns

- **Tests-after-merge**: tests in a separate PR. The five criteria are
  all met *before* merge to main.
- **Logging-on-demand**: adding logs only after the first incident.
  Decision-point logging is required at merge.
- **Cost-guard-as-afterthought**: an LLM-backed feature without per-
  tenant caps. Cost incidents follow.
- **Docs as PRD**: the engineering README explains *how to operate*, not
  *what was once planned*.

## 8. Cross-links

- Production Readiness Gate (canonical): [`../strategy/dealix_maturity_and_verification.md`](../strategy/dealix_maturity_and_verification.md) §5.4
- Audit log policy: [`../governance/AUDIT_LOG_POLICY.md`](../governance/AUDIT_LOG_POLICY.md)
- SLO framework: [`../sre/slo_framework.md`](../sre/slo_framework.md)
- FinOps cost governance: [`../finops/model_cost_governance.md`](../finops/model_cost_governance.md)
- ADR template: [`../adr/0000-template.md`](../adr/0000-template.md)

## 9. Owner & Review Cadence

- **Owner**: CTO.
- **Review**: quarterly criteria refresh; immediate on a production
  incident traced to a missing criterion.

## 10. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CTO | Initial 5-criteria readiness gate summary |
