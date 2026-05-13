---
title: Revenue OS Policy Rules — enumerated rules enforced by dealix/trust/policy.py
doc_id: W4.T14.revenue-os-policy-rules
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T21.adr-0001, W4.T21.adr-0003, W4.T23.slo-framework, W4.T24.model-cost-governance, W4.T25.data-quality-gates, W4.T12.event-taxonomy]
kpi: { metric: policy_violations_in_prod, target: 0, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.9, effort: 7pw, score: engineering }
---

# Revenue OS Policy Rules

## 1. Purpose

This document is the single source of truth for the policy rules enforced by `dealix/trust/policy.py`. Every action taken by Revenue OS — sending a message, enriching data, dispatching a payment, escalating a lead — flows through this policy. The rules below are enforced **in code**, not by goodwill. Each rule has an identifier, an enforcement point, a failure mode, and an audit-trail contract.

## 2. Core Invariant

> **No action is dispatched without a corresponding Decision Passport.** Every passport carries every policy decision evaluated, the evidence consulted, and the actor (human or agent). No exceptions.

If a passport cannot be produced, the action fails closed.

## 3. Rule Catalogue

Rules are numbered `P-XXX`. Categories: passport, evidence, PDPL, sub-processor, rate, escalation, audit.

### P-001 No action without passport

- **Statement**: any outbound side-effect (HTTP POST to an integration, message dispatch, billing event) MUST reference a passport ID that exists in the event store.
- **Enforcement**: `policy.require_passport(action)`. If `passport_id is None` or not found → `PolicyBlock(reason="missing_passport")`.
- **Failure mode**: fail closed; emit `action_blocked` event with reason.
- **Audit**: `passport_id` is carried as the idempotency key for every outbound call.

### P-010 Evidence level thresholds per action type

Action types are bucketed by stakes. Each bucket has a minimum evidence level. Evidence level is computed by the enrichment waterfall (low / medium / high) based on number of corroborating sources and source-trust scores.

| Action type | Minimum evidence level | Rationale |
|---|---|---|
| Internal classification | low | no external side-effect |
| Enrichment of own dataset | low | no external side-effect |
| Inbound notification to tenant | low | tenant-internal |
| Outbound email (cold) | **medium** | brand and reputation risk |
| Outbound WhatsApp | **medium** | Meta policy + brand risk |
| Sales call dial-out | **medium** | human cost; brand risk |
| Pricing quote | **high** | revenue commitment |
| Contract draft / send | **high** | legal commitment |
| Payment dispatch | **high** | financial commitment |
| PDPL-relevant disclosure | **high** | regulatory commitment |
| Cross-tenant data merge | **high** | tenancy invariant |

Enforcement: `policy.check_evidence_level(action_type, evidence_level)`.

### P-020 PDPL Article 13 — Lawful basis on collection

- **Statement**: every record of personal data must carry a `lawful_basis` field with one of: `consent`, `contract`, `legal_obligation`, `vital_interests`, `legitimate_interests`. No record without lawful basis enters the event store.
- **Enforcement**: gate at stage 1 (source ingest). Failing records are quarantined (`MISSING_LAWFUL_BASIS`) and never enriched.
- **Audit**: lawful basis is part of every passport's `evidence_summary`.

### P-021 PDPL Article 14 — Data subject rights

- **Statement**: any data subject rights request (access, correction, deletion, restriction, portability, objection) MUST be acknowledged within 24 h and fulfilled within 30 days per PDPL.
- **Enforcement**: requests routed via `/api/v1/dsr/*` create a `dsr_*` event that gates downstream processing of the subject's records. Deletion request blocks all new actions on the subject's records and triggers async purge.
- **Audit**: every DSR request produces a passport documenting the action taken and its evidence.

### P-022 PDPL Article 19 — Cross-border transfer

- **Statement**: personal data of KSA residents may not be transferred outside KSA without satisfying one of: (i) adequacy decision, (ii) approved standard contractual clauses, (iii) explicit consent for that transfer, (iv) regulator authorization.
- **Enforcement**: `policy.check_data_residency(record, target_processor)`. Each registered processor in `auto_client_acquisition/revenue_os/source_registry.py` carries a `residency` flag (`ksa`, `gcc`, `eu`, `us`, `other`). Transfers to non-KSA processors are blocked for Sovereign tenants except where an SCC or consent is present and recorded.
- **Audit**: cross-border transfer events are an explicit event category (`pdpl_*`).

### P-023 PDPL Article 23 — Breach notification

- **Statement**: any confirmed breach of personal data must be reported to the SDAIA regulator within 72 h and to affected subjects "without undue delay".
- **Enforcement**: triggered by the incident response runbook, not by this policy module — but `policy.py` exposes `record_breach_event(scope, severity)` which is the trigger.
- **Audit**: see `docs/PDPL_BREACH_RESPONSE_PLAN.md`.

### P-030 Sub-processor allowlist

- **Statement**: outbound API calls may only target processors that appear in `auto_client_acquisition/revenue_os/source_registry.py` AND in the tenant's sub-processor agreement.
- **Enforcement**: every outbound call goes through a routing layer that checks `(tenant_id, processor_id)` against the allowlist. Unauthorized targets → `PolicyBlock(reason="unlisted_subprocessor")`.
- **Onboarding new processor**:
  - DPA review (legal).
  - Residency classification.
  - Listed in source registry with metadata.
  - Notify all tenants whose contracts include sub-processor opt-in; 30-day notice required.
- **Audit**: the registry is version-controlled; every change is reviewable.

### P-040 Rate limits per source

Per-source soft and hard caps. Source registry declares them; policy enforces them. Limits exist for three reasons: respect partner rate limits, avoid cost overruns, contain blast radius of a buggy worker.

| Source class | Default soft cap (per tenant per hour) | Default hard cap (per tenant per hour) | Default soft cap (global per hour) |
|---|---|---|---|
| Government / regulatory | 120 | 240 | 2,000 |
| Paid enrichment API | 200 | 400 | 5,000 |
| Public web scrape | 60 | 120 | 1,000 |
| LLM provider | per-workflow caps (see FinOps doc) | per-tenant caps | global daily budget |
| Outbound messaging | 100 | 200 | 1,500 |

- Per-tenant soft cap → log + ticket; continue.
- Per-tenant hard cap → block, return `429` upstream.
- Global hard cap → block, page on-call (this is rare and usually indicates a bug).

Enforcement: token-bucket per `(tenant_id, source_id)` in Redis. Source-specific overrides in registry config.

### P-050 Escalation matrix

Some decisions cannot be fully automated. The matrix below defines the escalation tier per scenario:

| Scenario | Tier 1 (auto) | Tier 2 (CSM review) | Tier 3 (legal/compliance) | Tier 4 (CEO) |
|---|---|---|---|---|
| Standard enrichment | ✓ | | | |
| Cold outbound email | ✓ | | | |
| Outbound to a regulated entity (bank, ministry) | | ✓ | | |
| Contract draft > 50,000 SAR ARR | | ✓ | | |
| Contract draft > 250,000 SAR ARR | | | ✓ | |
| Sovereign tenant action with `evidence_level=medium` | | ✓ | | |
| PDPL breach scope > 10 subjects | | | ✓ | ✓ |
| Cross-tenant data merge | | | ✓ | |
| Payment refund > 5,000 SAR | | ✓ | | |
| Refund > 25,000 SAR | | | | ✓ |

Enforcement: `policy.classify_escalation(action)` returns the tier. Tier ≥ 2 holds the action in a queue with explicit human approval; passport is emitted on approval with the approver recorded.

### P-060 Full audit trail

- **Statement**: every policy decision (allow, block, escalate) is an event in the event store with `(passport_id, tenant_id, actor, rule_id, decision, reason, evidence_refs)`.
- **Enforcement**: `policy.py` writes the audit event before returning from any decision function. Failure to write the event aborts the action.
- **Retention**: 84 months hot+cold per the data retention policy.
- **Access**: read-only via `/api/v1/audit/*` endpoints; access itself is audited (meta-audit).

### P-070 Idempotency

- **Statement**: every outbound action carries an idempotency key derived from `passport_id`. Repeated dispatch with the same key is a no-op.
- **Enforcement**: idempotency table keyed on `(tenant_id, idempotency_key)`. First write wins.
- **Audit**: a re-dispatch attempt that hits an existing row produces a `action_dispatch_deduplicated` event.

### P-080 Cost governance integration

- **Statement**: any action whose projected cost exceeds the per-workflow caps in the FinOps doc is blocked.
- **Enforcement**: cost-budget hook in `policy.py` mirrors the FinOps caps. Hard cap breach → `PolicyBlock(reason="cost_cap_exceeded")` and passport marked accordingly.
- **Audit**: cost attribution carried in the passport.

### P-090 Tenant data boundary

- **Statement**: a passport for tenant A may never carry evidence rows owned by tenant B.
- **Enforcement**: the evidence assembler queries the event store with `tenant_id` already bound (ADR-0003 row-level isolation). A cross-tenant evidence reference fails closed.
- **Audit**: cross-tenant attempts are logged at P1 severity and trigger a security review.

## 4. Policy Decision Flow

```
action request
  → policy.classify_escalation()
  → policy.check_evidence_level()
  → policy.check_data_residency()
  → policy.check_subprocessor_allowlist()
  → policy.check_rate_limits()
  → policy.check_cost_budget()
  → policy.require_passport()
  → policy.record_audit_event()
  → dispatch (or block)
```

Order matters: cheap checks first, audit last (so audit is the last side-effect before dispatch and cannot be skipped on a fast-path).

## 5. Failure Modes

Every rule fails closed. A failure produces a typed `PolicyBlock` with:

- `rule_id` (e.g. `P-022`).
- `reason` (enum).
- `details` (structured, no free text).
- `remediation_hint` (which the API surface may translate to a customer-facing message).

The passport always carries the block; the customer-facing API returns `403` with a structured error body.

## 6. Change Management

- Adding or modifying a rule requires:
  - PR review with CTO + compliance owner (legal for PDPL rules).
  - Shadow-mode for 7 days where the new rule logs but does not block.
  - Backwards-compatibility analysis: which tenants would have been affected in the prior 28 days?
  - Update of this document; status flipped to `accepted` on merge.
- Rules are versioned; the policy module exposes `policy.version` which appears in every passport.

## 7. Observability

Per ADR-0004:

- Metric `policy_decisions_total{rule_id, decision}` — primary counter.
- Metric `policy_decision_latency_ms_bucket{rule_id}` — p95 target ≤ 5 ms per rule.
- Trace span `policy.evaluate` with rule-by-rule child spans.
- Alert: any rule with > 0 unexpected blocks during shadow → ticket.
- Alert: `P-090` (tenant boundary) block count > 0 → page (security event).

## 8. Compliance Mapping

| PDPL Article | Rule(s) |
|---|---|
| Art. 13 (Lawful basis) | P-020 |
| Art. 14 (Data subject rights) | P-021 |
| Art. 19 (Cross-border transfer) | P-022 |
| Art. 23 (Breach notification) | P-023 |
| Art. 26 (Records of processing) | P-060 (audit trail) |

| Other framework | Rule(s) |
|---|---|
| ZATCA e-invoicing | covered by `docs/INVOICING_ZATCA_READINESS.md`; surface boundary at P-070 idempotency |
| SAMA cybersecurity (Sovereign tenants) | P-090, P-060, schema isolation per ADR-0003 |

## 9. References

- Code: `dealix/trust/policy.py`, `api/routers/decision_passport.py`, `auto_client_acquisition/revenue_os/source_registry.py`, `auto_client_acquisition/revenue_os/enrichment_waterfall.py`.
- ADRs: ADR-0001 (event store), ADR-0003 (multi-tenant), ADR-0004 (observability), ADR-0005 (API versioning).
- Related docs: `docs/finops/model_cost_governance.md`, `docs/data/data_quality_gates.md`, `docs/sre/slo_framework.md`, `docs/analytics/event_taxonomy.md`.
- Compliance: `docs/PRIVACY_PDPL_READINESS.md`, `docs/PDPL_BREACH_RESPONSE_PLAN.md`, `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`, `docs/DPA_DEALIX_FULL.md`.

## 10. Review Cadence

Quarterly. Any new regulator guidance or any tenant incident reopens the relevant rule immediately.
