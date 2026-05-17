# Dealix — Revenue Expansion System (12-Machine Operating Lens)

**Status:** strategy input — captured for execution, NOT yet founder-locked
**Date:** 2026-05-17
**Frame:** نظام توزيع وتشغيل كامل حول منتج قوي — a distribution + operations
system around an already-strong product, not a new product.

> This document captures the "Revenue Expansion System" plan as a **canonical
> organizing lens** over Dealix's existing operating modules. It does NOT
> introduce new pricing, new claims, or new doctrine. Where the source plan
> conflicted with locked doctrine, this file defers to doctrine and says so
> explicitly (see *Reconciliations*).

---

## 1. Operating thesis

Dealix does not need more product features right now. It needs a complete
distribution + operations system around the product:

```
Product → Proof → Funnel → Sales → Billing → Delivery → Support
        → Upsell → Referral → Partners → Affiliates → Media
        → Evidence → Governance → Learning
```

Governing rule of the loop:

- Every channel produces a lead.
- Every lead enters scoring.
- Every scoring produces a next action.
- Every high-risk action requires approval.
- Every outcome is recorded as evidence.
- Every evidence item becomes content, an upsell, or a playbook.
- Every repeated playbook becomes an automation.
- Every repeated automation becomes a module.

---

## 2. Reconciliations (where this plan defers to doctrine)

The source plan proposed values that conflict with locked repo doctrine. The
repo wins. These are the corrections applied in this document:

| Source plan said | Repo doctrine (canonical) | Resolution |
|---|---|---|
| Diagnostic priced 4,999–25,000 SAR | `docs/COMPANY_SERVICE_LADDER.md`: Rung 0 = free/token | Pricing is **NOT settled by this doc**. Rung 0 stays free/token. Rung 1 = 499 SAR. Rungs 2–4 = `recommended_draft` until ≥3 paid pilots inform a real number. Repo pricing is currently fragmented across `COMPANY_SERVICE_LADDER.md` (499), `V14_COMPREHENSIVE_STRATEGIC_PLAN.md` (5,000) — reconciling them is a **founder decision**, out of scope here. |
| Sprint 25,000 SAR+ | Rung 1 = 499 SAR / Rung 2 = `recommended_draft` | Use `recommended_draft`; never publish an unvalidated number. |
| Retainer 4,999–35,000 SAR/mo | Rung 3 = `recommended_draft` | Use `recommended_draft`. |
| "12 new machines" | 175+ OS modules already exist | The 12 machines are a **lens over existing modules**, not greenfield builds. See §4 mapping. |

The plan's prohibitions section ("ممنوعات") already aligns with doctrine and
is adopted as-is.

---

## 3. The 11 non-negotiables (unchanged — enforced by tests)

1. No scraping systems.
2. No cold WhatsApp automation.
3. No LinkedIn automation.
4. No fake / un-sourced claims.
5. No guaranteed sales outcomes.
6. No PII in logs.
7. No source-less knowledge answers.
8. No external action without approval.
9. No agent without identity.
10. No project without Proof Pack.
11. No project without Capital Asset.

Every machine below MUST honor all 11. A machine with no KPI and no evidence
event is not Full Ops — it is just an activity.

---

## 4. The 12 machines → existing module map

Each machine carries a fixed schema: **Input · Agent · Automation · Approval
Gate · Evidence Event · KPI · Failure Mode**. None is greenfield except where
marked NET-NEW.

| # | Machine | Maps to existing module(s) | Status |
|---|---|---|---|
| 1 | Market Signal | `revenue-os/signals/normalize`, `MARKET_RADAR_SIGNALS.md` | wrap |
| 2 | Founder Media | `case_study_engine`, content docs | wrap |
| 3 | Lead Magnet | `diagnostic_engine`, public routers | wrap |
| 4 | Sales Autopilot | `sales_os`, `commercial_engagements` | wrap |
| 5 | Demo & Proof | `proof_os`, `diagnostic_engine` | wrap |
| 6 | Billing & Closing | `finance_os`, `api/routers` checkout | wrap |
| 7 | Delivery Factory | `delivery_factory`, `delivery_os` | wrap |
| 8 | Support Autopilot | `commercial_engagements` support desk | wrap |
| 9 | Customer Success & Upsell | `customer_success`, `expansion_engine` | wrap |
| 10 | Partner Distribution | `partnership_os`, `ecosystem_os` | wrap |
| 11 | Affiliate / Commission | — | **NET-NEW** (lowest priority, gated) |
| 12 | Governance & Evidence | `governance_os`, `approval_center`, `evidence_control_plane_os` | wrap |

Cross-cutting spine all machines write to: `governance_os` (approval gates),
`evidence_control_plane_os` (evidence events), `friction_log` (failure modes),
`value_os` + `capital_os` (proof → asset).

---

## 5. Machine specifications (compact)

Only the fields that differ from the standard schema are listed; all machines
share: Approval Gate = `approval_center`, Evidence Event = logged to
`evidence_control_plane_os`, Failure Mode → `friction_log`.

**M1 Market Signal** — Input: founder-supplied signals (no scraping). Agent:
MarketSignalAgent. KPI: 50 target accounts/wk, 15 high-fit/wk, 10 approved
outreach drafts/wk, 3 real conversations/wk.

**M2 Founder Media** — Input: sales objections + proof snippets. KPI: 5
posts/wk, 1 newsletter/wk, 1 webinar/mo, 10 proof-pack requests/mo.

**M3 Lead Magnet** — Input: risk-score / template downloads. Gate: consent
required before any proof pack is sent. KPI: lead → scored → next action.

**M4 Sales Autopilot** — Input: any lead. Agents: LeadCapture, ICPScoring,
Positioning, OutreachDraft, ReplyClassifier, MeetingBrief, SalesCoach,
ScopeBuilder, BillingDraft, Upsell, Governance. KPI: no lead un-scored. Hard
rule: no autonomous external send — drafts only.

**M5 Demo & Proof** — Input: qualified lead. Proof Pack must show source
clarity, approval boundary, evidence trail, decision passport, value report.
Any estimated score carries `is_estimate=true`.

**M6 Billing & Closing** — Gates: no invoice without approved scope; no
delivery without `invoice_paid`; no revenue mark without payment proof.

**M7 Delivery Factory** — Input: `invoice_paid`. Output: 10-section Proof
Pack. Rule: every finding has a source or `is_estimate=true`.

**M8 Support Autopilot** — Tiers 0–4. Auto-answer only low-risk from approved
KB; escalate security/refund/discount/custom/complaint.

**M9 Customer Success & Upsell** — No upsell without a customer-approved
Proof Pack from the prior rung.

**M10 Partner Distribution** — Referral / Implementation / Co-selling /
White-label (white-label only after 3 paid pilots). Referral fee paid only
after `invoice_paid`.

**M11 Affiliate / Commission** — NET-NEW. Commission only after
`invoice_paid`; FTC-style disclosure mandatory; no cold WhatsApp / spam / ROI
guarantees. Build last, behind a gate.

**M12 Governance & Evidence** — The moat. Doctrine chain:
`Signal → Source → Approval → Action → Evidence → Decision → Value → Asset`.
KPI: approval compliance 100%, high-risk auto-send 0%, evidence completeness
≥90%.

---

## 6. Roadmap (phased — capability gates, not dates)

**Phase V1 (~14 days)** — public diagnostic page, risk score, lead capture +
scoring, founder command center (basic), approval center, evidence ledger,
sales pipeline, support KB v1, partner/affiliate application intake.

**Phase V2 (~30 days)** — marketing dashboard, newsletter sequence, webinar
engine, affiliate tracking, commission calc, support classifier, meeting
brief + scope draft generators, invoice guard, proof-pack shell.

**Phase V3 (~90 days)** — partner portal, affiliate portal, customer
workspace (basic), agent orchestrator, governance dashboard, proof-pack
generator, delivery automation, retargeting events.

**After paid proof** — client workspace, benchmark engine, decision passport
builder, multi-client modules. Gated by `docs/V12_1_TRIGGER_RULES.md`: each
rung unlocks only when the prior rung ships real evidence.

---

## 7. Single constraint that matters

The repo's standing constraint is unchanged: **3 paid pilots**. No machine in
this document overrides that. If revenue is below target by the relevant
gate, stop building machines and double down on sales — per the `dealix-pm`
decision rules.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
