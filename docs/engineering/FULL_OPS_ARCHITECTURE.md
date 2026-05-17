# Dealix Full Ops Architecture

The single map of the Dealix Full Ops platform: every customer-facing surface,
every operating domain, the governance spine they all share, and an honest
status of what is built versus what is still target.

This doc supersedes nothing — it consolidates. `docs/V12_FULL_OPS_ARCHITECTURE.md`
describes the 9-OS model; this doc places that model, the newer domains, and
the genuine gaps on one page.

## The governing rule

> Anything that goes to the outside world needs trust. Anything internal can be
> automated. Every claim needs a source. Every revenue figure needs a payment
> proof. Every commission needs a paid deal. Every final diagnosis needs review.

Concretely, no action is "Full Ops" unless it has all five of:
**source · risk level · approval rule · evidence event · KPI.**

## The five surfaces

| Surface | Audience | Where it lives today |
|---|---|---|
| Public Growth Site | prospects, applicants | `landing/*.html` (static mockups) + Next.js `frontend/src/app/[locale]/` |
| Founder Ops Console | the founder | `frontend/src/app/[locale]/{dashboard,approvals,pipeline}` + `GET /api/v1/founder/dashboard` |
| Customer Workspace | paying customers | `frontend/src/app/[locale]/customer-portal` (partial) |
| Partner Portal | strategic partners | backed by `partnership_os/` — no dedicated portal page yet (target) |
| Affiliate Portal | commission marketers | backed by `affiliate_os/` (new) — no dedicated portal page yet (target) |

The `landing/` HTML files are legacy branding/demo mockups. The real console is
the Next.js app under `frontend/`.

## Domain map — status honesty

Status vocabulary matches `dealix/registers/no_overclaim.yaml`:
**Production · Partial · Missing.**

| Domain | Status | Backing module(s) |
|---|---|---|
| Governance / Trust | Production | `dealix/contracts/`, `dealix/trust/`, `governance_os/`, `approval_center/`, `auditability_os/`, `evidence_control_plane_os/`, `compliance_trust_os/` |
| Sales | Production | `dealix/intelligence/lead_scorer.py`, `revenue_pipeline/`, `sales_os/`, `crm_v10/` |
| Support | Production | `support_os/` (classifier, KB, escalation, SLA) |
| Customer Success | Production | `customer_success/` (health, churn, QBR) |
| Delivery | Production | `diagnostic_engine/`, `proof_to_market/`, `case_study_engine/`, `delivery_os/` |
| Billing | Partial | `revops/invoice_state.py`, `revops/payment_confirmation.py`, `dealix/payments/moyasar.py` |
| Partners | Partial | `partnership_os/` (profile, fit, referral log) — commissions/payouts Missing |
| **Affiliates** | **Partial (new)** | **`affiliate_os/`** — intake, scoring, links, asset gate, commission, payout |
| Marketing automation | Missing | campaigns/content/webinars/retargeting — documented, not built |

## The governance spine

Every domain action funnels through the same spine:

```
contracts  → A/R/S classification (Approval / Reversibility / Sensitivity)
trust      → PolicyEvaluator + ApprovalCenter
governance_os → claim guards (draft_gate, claim_safety, runtime_decision)
approval_center → ApprovalStore (human-in-the-loop, founder rules)
auditability_os → record_event() append-only JSONL ledger
evidence_control_plane_os → chain completeness + gap detection
```

Decision vocabulary (`compliance_trust_os/approval_engine.GovernanceDecision`):
`ALLOW · ALLOW_WITH_REVIEW · DRAFT_ONLY · REQUIRE_APPROVAL · REDACT · BLOCK ·
ESCALATE`.

The Affiliate OS is the worked example: affiliate copy clears `audit_claim_safety`
+ `runtime_decision.decide` before becoming an asset; commissions are gated on a
payment-confirmation evidence event; payouts are gated on an `ApprovalStore`
approval. New domains compose the spine — they never reimplement it.

## Agent orchestrator contract

Agents never act freely. Every agent run follows:

```
Event → Policy Check → Agent Selection → Tool Permission Check
      → Agent Run → Output Validation → Approval (if required)
      → Evidence Event → State Update
```

Detail in `docs/engineering/AGENT_ORCHESTRATOR.md`.

## The ops loops

| Loop | Shape |
|---|---|
| Sales | Lead → Score → Route → Draft → Approve → Meeting → Scope → Invoice → Paid |
| Support | Ticket → Intent → KB → Risk → Answer/Escalate → KB Gap → Improve |
| Marketing | Signal → Content → Lead Magnet → Form → Score → Sales Route |
| Affiliate | Apply → Score → Approve → Asset gate → Link → Referral → Paid invoice → Commission → Approved payout |
| Partner | Identify → Pitch → Call → Referral → Diagnostic → Handoff |
| Delivery | Paid → Onboard → Analyze → Draft → Review → Proof Pack → Upsell |
| Governance | Action → Risk → Approval → Evidence → Audit → Policy Update |
| Learning | Reply→Objection, Ticket→KB, Repeat→Playbook→Automation |

## Full Ops Health Score

A 100-point readiness rubric:

| Dimension | Points |
|---|---|
| Sales readiness | 20 |
| Support readiness | 15 |
| Marketing readiness | 15 |
| Partner/Affiliate readiness | 15 |
| Governance readiness | 20 |
| Delivery readiness | 10 |
| Reporting readiness | 5 |

**Pre-scale gates** (do not scale until all hold):
Full Ops Health ≥ 75 · approval compliance = 100% · high-risk auto-send = 0% ·
evidence completeness ≥ 90% · lead-scoring coverage = 100%.

## Version roadmap

- **V1 — done.** Governance spine, Sales, Support, Delivery, founder dashboard,
  approval center, evidence ledger.
- **V2 — done / partial.** Billing (partial), Affiliate OS (new this round).
- **V3 — target.** Partner portal, Affiliate portal, Customer workspace,
  agent orchestrator runtime, governance dashboard, partner commissions.
- **V4 — after paid proof.** Marketing automation, benchmark engine,
  multi-client modules.

## Doctrine (non-negotiable)

No live send · no live charge · no scraping · no cold WhatsApp · no fake proof ·
no LinkedIn automation · no guaranteed-outcome claims · approval-first ·
Arabic primary · real data only · placeholder identifiers in the repo.

## Bilingual one-liner

**العربية**: منصة تشغيل كاملة — نمو وبيع ودعم وتسويق وشراكات وتسليم — كل إجراء
خارجي يمر بموافقة المؤسس، كل ادعاء له مصدر، كل عمولة مربوطة بدفعة مؤكدة، كل
خطوة مسجلة في سجل الأدلة. لا إرسال حيّ، لا خصم حيّ، لا نتائج مضمونة.

**English**: One Full Ops platform — growth, sales, support, marketing,
partners, delivery — where every external action passes founder approval, every
claim has a source, every commission is tied to a confirmed payment, and every
step is written to the evidence ledger. No live send, no live charge, no
guaranteed outcomes.
