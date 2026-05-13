---
title: Forbidden Actions — The Hard "No" List
doc_id: W6.T37.forbidden-actions
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
ar_companion: none
related: [W4.T14, W3.T07b]
kpi:
  metric: forbidden_action_blocks_pre_send
  target: 100
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.95
  effort: 0.5
  score: governance-foundation
---

# Forbidden Actions

## 1. Context

This is the exhaustive list of actions Dealix will not take, regardless of
customer request, commercial pressure, or convenience. The list is enforced
in code via `dealix/trust/forbidden_claims.py` (content gate),
`dealix/trust/approval_matrix.py` (action gate), and the policy engine
(`dealix/trust/policy.py`).

## 2. Audience

Every employee, contractor, partner, integrator. This list is the operating
perimeter; breaches are incidents, not "Monday fixes".

## 3. The Hard "No" List

### 3.1 Content — Unverifiable or Banned Claims

Enforced by `forbidden_claims.scan_text` (`dealix/trust/forbidden_claims.py`).

**AR banned terms** include: أفضل, الأفضل, الأقوى, ضمان, نضمن, حصري, الوحيد,
100%, مجاني تمامًا, ربح مضمون, أرخص, بدون مخاطر.

**EN banned patterns** include: `guarantee*`, `best in saudi/kingdom/region`,
`100% (satisfaction|success|secure)`, `risk[- ]free`, `only
(provider|company|solution)`, `free forever`, `unbeatable`.

Any AR or EN content containing a banned term is blocked **before send**.
`assert_clean(text)` raises on detection.

### 3.2 Action — Without Required Approval

Enforced by `required_approver(action, evidence_level)` in `approval_matrix.py`.

- No `OUTBOUND_EMAIL` without CSM approval at L2+ evidence.
- No `OUTBOUND_WHATSAPP` without Head of CS approval at L3+.
- No `OUTBOUND_SMS` without Head of CS approval at L3+.
- No `PUBLIC_POST` without Head of Legal approval at L4+.
- No `EXTERNAL_API_WRITE` without CTO approval at L3+.
- No `DATA_EXPORT` without Head of Legal approval at L2+.
- No `CRM_BULK_UPDATE` without AE approval at L2+.
- No `INVOICE_GENERATION` without Head of CS approval at L3+.
- No `POLICY_OVERRIDE` without CEO approval at L5.

See [`APPROVAL_MATRIX.md`](APPROVAL_MATRIX.md) for the canonical table.

### 3.3 Data — PII, Cross-Border, Training

- No **PII in customer-facing outputs**, logs, or training pipelines.
  Enforced by `pii_detector.decide_for_record` and `decide_for_batch`.
- No **card / IBAN financial PII** in any downstream pass-through. Hard
  `BLOCKED` verdict — no override.
- No **training on customer data**; no sharing of customer data with
  third-party LLM providers for their training.
- No **cross-border transfer** outside the documented bases in
  [`PDPL_DATA_RULES.md`](PDPL_DATA_RULES.md) §3.4.

### 3.4 Engagement — Process Bypasses

- No **handoff without QA pass + Quality Score ≥ 80** (`ships=False` blocks
  Stage 6).
- No **action without an audit event**.
- No **bypass token** without HoLegal + CTO sign-off and an audit entry
  explaining the business reason.
- No **policy override** without CEO sign-off.
- No **scope creep absorbed silently** — see
  [`../delivery/SCOPE_CONTROL.md`](../delivery/SCOPE_CONTROL.md).

### 3.5 Commercial — Sales Bypass of Standard

- No **selling a sub-80 Service Readiness Score offering** without HoP sign-
  off and disclosure to the buyer ([`../quality/SERVICE_READINESS_SCORE.md`](../quality/SERVICE_READINESS_SCORE.md)).
- No **direct delivery outside Saudi** — GCC expansion goes through
  partners per the Expansion Playbook §3.6.
- No **free pilots** — see `docs/delivery/pilot_framework.md` §1.

## 4. Enforcement

- **Pre-send blocking**: violations are caught at the action gate or the
  content scanner before egress.
- **Audit entries**: every block is logged. Repeat patterns surface in the
  weekly QA scoreboard.
- **Personnel**: repeat individual violations are a performance issue
  reviewed by HoLegal + the individual's manager.

## 5. Cross-links

- Forbidden claims code: `dealix/trust/forbidden_claims.py`
- Approval matrix code: `dealix/trust/approval_matrix.py`
- Compliance perimeter: [`COMPLIANCE_PERIMETER.md`](COMPLIANCE_PERIMETER.md)
- Approval matrix doc: [`APPROVAL_MATRIX.md`](APPROVAL_MATRIX.md)
- PDPL rules: [`PDPL_DATA_RULES.md`](PDPL_DATA_RULES.md)
- PII policy: [`PII_REDACTION_POLICY.md`](PII_REDACTION_POLICY.md)
- Arabic quality (forbidden phrases): [`../quality/ARABIC_QUALITY_GUIDE.md`](../quality/ARABIC_QUALITY_GUIDE.md)

## 6. Owner & Review Cadence

- **Owner**: HoLegal.
- **Review**: quarterly + immediately on any new regulator guidance.

## 7. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoLegal | Initial hard "no" list — content, action, data, engagement, commercial |
