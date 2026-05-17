# Dealix Full Ops Blueprint — مخطط التشغيل الكامل

> **Status / الحالة:** Reference document. Records strategic intent and a build
> ordering. It does **not** change runtime behavior, pricing, or architecture by
> itself. Each build wave is executed separately and gated by
> `docs/V12_1_TRIGGER_RULES.md` and the `DEALIX_OPERATING_CONSTITUTION.md`.

> **Doctrine anchor / المرجع:** This blueprint is subordinate to the
> `DEALIX_OPERATING_CONSTITUTION.md`. Where this document and the Constitution
> disagree, the Constitution wins. Where this document and
> `OFFER_LADDER_AND_PRICING.md` disagree on price, the offer ladder wins until a
> founder decision says otherwise (see §A.3).

---

## A. Reconciliation notes — ملاحظات المواءمة

The original Full Ops blueprint proposed a new package layout and config format.
After review against the existing codebase, the following adjustments apply.

### A.1 Package layout — لا يوجد تفرّع معماري

The blueprint proposed new top-level packages: `dealix/growth/`, `dealix/sales/`,
`dealix/support/`, `dealix/partners/`, etc.

**Not adopted.** Dealix already ships 80+ `auto_client_acquisition/*_os` modules,
117 API routers, 290+ tests, and an Operating Constitution. Creating a parallel
`dealix/*` package would fork the architecture. The blueprint's "machines" are
mapped onto the modules that already implement them — see §B.

### A.2 Config format — YAML config directory deferred

The blueprint proposed `dealix/config/*.yaml` (offers, pricing, lead_scoring,
stage_transitions, approval_policy, claim_policy, affiliate_rules, etc.).

**Deferred.** Config today lives as Python + Markdown:
- offers / pricing → `docs/OFFER_LADDER_AND_PRICING.md`, `core/config/settings.py`
- lead scoring → `auto_client_acquisition/growth_beast/icp_score.py`
- stage transitions → `auto_client_acquisition/revenue_pipeline/stage_policy.py`
- approval policy → `auto_client_acquisition/approval_center/approval_policy.py`
- governance rules → `auto_client_acquisition/governance_os/rules/*.yaml` (already YAML)

A consolidated YAML config layer is a possible future refactor, not part of any
current wave. It must not be done as a fork — it would replace, not duplicate, the
Python definitions.

### A.3 Pricing conflict — تعارض التسعير (founder decision required)

The blueprint proposes a paid diagnostic priced **4,999 – 25,000 SAR** with a
Revenue Intelligence Sprint at **25,000 SAR+**.

The canonical `docs/OFFER_LADDER_AND_PRICING.md` defines:
- Rung 0 — Free AI Ops Diagnostic — **free**
- Rung 1 — 7-Day Revenue Proof Sprint — **499 SAR**
- Rung 2 — Data-to-Revenue Pack — 1,500 SAR
- Rung 3 — Managed Revenue Ops — 2,999–4,999 SAR/mo
- Rung 4 — Executive Command Center — 7,500–15,000 SAR/mo
- Rung 5 — Agency Partner OS — custom + rev-share

These are materially different go-to-market models (free-entry land-and-expand vs.
paid-diagnostic). **This blueprint does not change pricing.** The divergence is
flagged here as an explicit founder decision. Until that decision,
`OFFER_LADDER_AND_PRICING.md` remains canonical.

### A.4 Governance — already enforced

The blueprint's "8 forbidden actions" are already the **Operating Constitution
Article 4 immutable hard gates**: `NO_LIVE_SEND`, `NO_LIVE_CHARGE`,
`NO_COLD_WHATSAPP`, `NO_LINKEDIN_AUTOMATION`, `NO_SCRAPING`, `NO_FAKE_PROOF`,
`NO_FAKE_REVENUE`, `NO_UNAPPROVED_TESTIMONIAL`. The 5 action modes
(`suggest_only`, `draft_only`, `approval_required`, `approved_manual`, `blocked`)
are in `auto_client_acquisition/decision_passport/schema.py`. No new governance
layer is needed; future machines plug into the existing one.

---

## B. Machine → module map — خريطة الماكينات

The blueprint names 12 "machines". Status: `exists` (implemented), `partial`
(some pieces exist), `gap` (not built).

| # | Machine / الماكينة | Existing module(s) | Status |
|---|---|---|---|
| 1 | Market Signal | `auto_client_acquisition/market_intelligence/`, `intelligence_os/` | partial |
| 2 | Founder Media | — (content workflow, no module) | gap |
| 3 | Lead Magnet (Risk Score) | `growth_beast/` (scoring), no public risk-score page | gap |
| 4 | Sales Autopilot | `growth_beast/icp_score.py`, `revenue_pipeline/stage_policy.py`, `agents/` (intake, icp_matcher, pain_extractor, qualification, proposal, outreach, followup, booking, crm) | exists |
| 5 | Demo & Proof | `proof_ledger/`, `proof_os/`, `evidence_control_plane_os/` | exists |
| 6 | Closing & Billing | `payment_ops/`, `revops/payment_confirmation.py` | exists |
| 7 | Delivery Factory | `delivery_os/`, `execution_os/` | exists |
| 8 | Support Autopilot | `support_os/classifier.py` | partial |
| 9 | Customer Success / Upsell | `customer_success/`, `growth_beast/offer_intelligence.py` | partial |
| 10 | Partner Distribution | `partnership_os/` | partial |
| 11 | Affiliate | — (no `affiliate_rules`, no affiliate module) | gap |
| 12 | Governance & Evidence | Constitution Art. 4, `governance_os/rules/*.yaml`, `approval_center/`, `decision_passport/schema.py`, `value_os/value_ledger.py`, `evidence_control_plane_os/`, `capital_os/`, `friction_log/` | exists |
| ★ | Founder Command Center | API: `api/routers/founder_dashboard.py`, `api/routers/founder_command_summary.py`, `auto_client_acquisition/founder_command_summary/` — **frontend page is a gap** | partial |

Conclusion: most machines already exist as modules. The blueprint's value is
**distribution, trust, proof, and an operator surface** over the existing product —
not new core engines.

---

## C. The blueprint — المخطط

### C.1 Top decision — القرار الأعلى

Dealix is already a strong product. Winning now = **Distribution + Trust + Proof +
Full Ops**. Do not ask "what is the next feature?" Ask: how does every day produce a
lead, a conversation, a meeting, a scope, an invoice, a proof, an upsell, a partner,
content, and a learning?

### C.2 The nine operating systems — أنظمة التشغيل التسعة

Growth · Sales · Marketing/Media · Support · Customer Success · Delivery ·
Partner/Affiliate · Compliance/Governance · Executive/Self-Improvement. Each OS must
produce a **daily decision, evidence, and a next action** — not just be a module.

### C.3 Command center — مركز القيادة

The most important screen is `/ar/ops/founder` (Founder Command Center), not the
marketing page. It must show daily: Top 3 Actions, Revenue Pipeline, Qualified
Leads, Meetings Today, Scopes Pending, Invoices Pending, Support Escalations,
Partner Leads, Affiliate Compliance Flags, Proof Packs in Progress, Blocked Risky
Actions, No-Build Warning. Rule: if the founder cannot tell within 30 seconds what
to do today, the system is incomplete.

> **Wave 1 builds this screen** — see §D.

### C.4 The offer — العرض

Sell one thing: a **governed revenue & AI ops diagnostic** that produces a Revenue
Workflow Map, Source/CRM Quality Review, Approval Boundary Map, Evidence Trail Gaps,
Top 3 Governed Decisions, a Proof Pack, and a Sprint/Retainer recommendation. Do not
sell "a platform", "AI", or "automation". (Pricing per §A.3 — canonical ladder.)

### C.5 Machine 1 — Market Signal

Find companies hiring RevOps/Sales Ops/AI, founders talking growth/AI, agencies
with weak follow-up, companies with a CRM but unclear pipeline, service centers with
many leads, consultants selling CRM/AI/automation, VCs/accelerators needing AI
governance. Flow: signal → account → ICP score → pain hypothesis → offer angle →
outreach draft → **approval** → manual send → evidence event. Weekly KPI target:
50 scanned, 15 high-fit, 10 drafts, 5 approved sends, 3 replies, 1 meeting.

### C.6 Machine 2 — Founder Media

Become the media face of the category. Publish on AI-without-governance, CRM
readiness, revenue leakage, approval boundaries, evidence trails, decision
passports, no-autonomous-external-sends, proof packs, Saudi/GCC AI ops, founder
operating lessons. Every post carries a CTA. Each idea is repurposed into LinkedIn
post, X thread, video script, newsletter paragraph, sales email, affiliate asset,
webinar slide, FAQ article.

### C.7 Machine 3 — Lead Magnet

First step is not "book a call" — it is a small value gate: AI & Revenue Ops Risk
Score, Sample Proof Pack, Decision Passport Template, AI Approval Policy Template,
CRM Readiness Checklist, Revenue Workflow Maturity Score. Funnel: content/DM/partner
→ Risk Score → Sample Proof Pack → lead score → booking → diagnostic scope.
Outcomes: Low/Medium/High/Partner fit routing.

### C.8 Machine 4 — Sales Autopilot

Every lead has a stage and a next action. Stages: `new_lead`, `qualified_A/B`,
`nurture`, `partner_candidate`, `meeting_booked`, `meeting_done`, `scope_requested`,
`scope_sent`, `invoice_sent`, `invoice_paid`, `delivery_started`, `proof_pack_sent`,
`sprint_candidate`, `retainer_candidate`, `closed_lost`. Lead score routes: 15+ →
Qualified A; 10–14 → Qualified B; 6–9 → educate/partner; <6 → archive. **Rule: AI
drafts, founder approves, manual send, evidence logged.**

### C.9 Machine 5 — Demo & Proof

12-minute demo: open `/ar/business-now#strategy` → "this is a founder decision
console, not a dashboard" → pick sector → simulate → show current focus → show GTM
first-10 → open sales script → show Proof Demo → close with diagnostic scope. The
Proof Pack proves source clarity, approval boundary, evidence trail, decision
passport, value report — and contains no fake KPI.

### C.10 Machine 6 — Closing & Billing

Do not build a heavy payment system; build guardrails around the invoice. Flow:
`scope_requested` → `scope_draft` → founder approval → `invoice_draft` → founder
approval → `invoice_sent` → `payment_confirmed` → `invoice_paid` →
`delivery_started`. Forbidden: invoice without scope, delivery before payment,
revenue before `invoice_paid`, discount/refund without founder review.

### C.11 Machine 7 — Delivery Factory

Every paid customer enters the delivery loop: onboarding → required inputs →
workflow map → source quality review → approval gap review → evidence gap review →
top 3 decisions → proof pack → delivery call → upsell recommendation. Proof Pack:
Executive Summary, Workflow Map, Source Quality, Approval Boundary, Evidence Gaps,
Revenue Leakage, Top 3 Governed Decisions, Recommended Sprint, Evidence Appendix,
30-Day Action Plan. Every finding has a source; every number has a source or
`is_estimate=true`; missing data shows as missing.

### C.12 Machine 8 — Support Autopilot

AI-first but knowledge-base-bound. Tiers: T0 self-serve FAQ, T1 AI answer from
approved KB, T2 AI draft + human approval, T3 founder/specialist, T4
policy/security/legal escalation. Auto-answer only for low-risk, KB-covered,
no-security-claim, no-refund/discount questions. Escalate anything touching
security, refunds, discounts, custom scope, client-specific diagnosis, complaints,
case-study permission, or data deletion/export.

### C.13 Machine 9 — Customer Success & Upsell

After delivery, ask: is value clear? actionable workflow? budget? Sprint needed?
Retainer? partner/referral fit? case-study fit? Upsell rules: clear workflow + high
pain → Sprint; recurring monthly workflow → Retainer; security questions → Trust
Pack; weak data → CRM/Data Readiness; executive need → Board Decision Memo.
Follow-up cadence: Day 0 deliver, Day 2 value confirmation, Day 5 propose
sprint/retainer, Day 10 referral ask, Day 21 reactivation.

### C.14 Machine 10 — Partner Distribution

Partners open trust and context (not affiliates). Best partners: CRM implementers,
HubSpot/Zoho/Salesforce consultants, ERP/accounting consultants, AI consultants,
GRC/security advisors, VC portfolio operators, B2B agencies, fractional COOs/CROs,
accelerators. Model: Dealix diagnoses, partner implements, client gets proof, Dealix
keeps the governance/proof layer. No white-label before 3 paid pilots; no partner
portal before 5 active partners.

### C.15 Machine 11 — Affiliate

Powerful but the highest reputational risk — must be tightly governed. Tiers 0–4
(Applicant → Approved → Qualified Referral → Strategic → Implementation).
Commission only **after `invoice_paid`**. No payout for traffic-only, unqualified,
duplicate, no-consent, out-of-ICP, or refunded-in-clawback leads. Required:
disclosure on every endorsement (FTC-aligned — visible, with the endorsement, not
hidden), approved messaging only, no spam, no cold WhatsApp under the Dealix name,
no ROI or compliance guarantees.

### C.16 Machine 12 — Governance & Evidence (the moat)

Doctrine chain: Signal → Source → Approval → Action → Evidence → Decision → Value →
Asset. Approval gates on every external message, scope/invoice send, diagnostic and
proof-pack finalization, case-study publish, security claim, discount/refund,
affiliate payout, and agent tool action. Health KPIs: approval compliance = 100%,
high-risk auto-send = 0%, evidence completeness ≥ 90%.

### C.17 Full Ops Health Score — مؤشر الجاهزية

Score out of 100: Sales 20, Marketing 15, Support 15, Partner/Affiliate 15,
Governance 20, Delivery 10, Reporting 5. **Do not expand** before: Full Ops Health
≥ 75, approval compliance = 100%, high-risk auto-send = 0%, lead-scoring coverage
= 100%, evidence completeness ≥ 90%.

### C.18 What not to do now — ما لا يُفعل الآن

No new major version before revenue, no live WhatsApp/Gmail send, no LinkedIn
automation, no scraping, no fake proof, no guaranteed ROI, no ads before message
clarity, no customer portal before a paid customer, no open affiliate program
before approved assets, no hiring before repeatability.

---

## D. Build-wave ordering — ترتيب موجات البناء

Per `docs/V12_1_TRIGGER_RULES.md`: a new workflow becomes a checklist; repeated
twice → template; 3 times → automation; with 2 customers → internal module; with 3
customers + retainers → product feature. Build waves below follow that rule.

| Wave | Deliverable | Notes |
|---|---|---|
| **1** | **Founder Command Center page** (`/ar/ops/founder`) | API exists; wire the UI. **In progress with this document.** |
| 2 | Risk Score lead magnet (public page + scoring) | Machine 3 — gap |
| 3 | Support KB v1 + tiered classifier UI | Machine 8 — partial → exists |
| 4 | Partner application + approved-asset library | Machine 10 — partial |
| 5 | Affiliate rules + tracking (governed) | Machine 11 — gap; highest reputational risk, build last |
| — | Founder Media workflow, consolidated YAML config | Deferred; not a fork |

Each wave is a separate change set, separately reviewed, and must pass the existing
test suite and governance gates before the next wave starts.

---

## E. Wave 1 scope (this change) — نطاق الموجة الأولى

Wave 1 ships the **Founder Command Center frontend page** that surfaces the existing
`GET /api/v1/founder/dashboard` API:

- New route `frontend/src/app/[locale]/ops/founder/page.tsx` → `/ar/ops/founder`,
  `/en/ops/founder`.
- New component `frontend/src/components/ops/FounderCommandCenter.tsx` rendering the
  six API sections (leads waiting 24h+, friction 7d, renewals due, pending
  approvals, recent proof events, capital assets this week), the `is_estimate`
  badge, and the `governance_decision` value.
- Sidebar nav entry + bilingual translation keys.

No backend, pricing, governance, or architecture change. Future waves are tracked in
§D and remain out of scope until separately approved.
