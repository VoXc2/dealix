# Dealix Growth System — نظام النمو في ديالكس

> Purpose — الغرض: this is the canonical internal doctrine for how Dealix grows. It maps the founder's 22-section Growth System playbook onto the current codebase, names what already exists, names the gaps, and sets the build order. It is a **contract and a roadmap, not an implementation** — every machine described here is built *against* this document. Cross-link: [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md), [WHAT_DEALIX_REFUSES.md](../00_constitution/WHAT_DEALIX_REFUSES.md), [GOVERNANCE_OS.md](../05_governance_os/GOVERNANCE_OS.md), [AGENCY_PARTNER_PROGRAM.md](../AGENCY_PARTNER_PROGRAM.md), [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md), [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md), [90_day_execution.yaml](../../dealix/registers/90_day_execution.yaml).

وثيقة عقيدة داخلية: كيف ينمو ديالكس. تصف ٢٢ آلة نمو، وتربط كل آلة بحالتها الحقيقية في الكود، وتحدد ترتيب البناء. هذه خارطة طريق وعقد — وليست تنفيذاً.

---

## 1. The growth loop — حلقة النمو والقاعدة الذهبية

Dealix grows through **one continuous loop**, not a set of disconnected campaigns. Every machine in this document exists only to feed or accelerate this loop:

```
Signal → Lead → Proof → Meeting → Scope → Invoice → Delivery → Upsell → Referral → Content → more Leads
```

**The golden rule — القاعدة الذهبية:**

> Every channel produces a **lead**. Every lead is **scored**. Every score yields a **next action**. Every risky action requires **approval**. Every result is recorded as **evidence**. Every evidence becomes **content, an upsell, or a playbook entry**.

كل قناة تنتج عميلاً محتملاً، وكل عميل يُقيَّم، وكل تقييم يولّد إجراءً تالياً، وكل إجراء خطِر يحتاج موافقة، وكل نتيجة تُسجَّل كدليل، وكل دليل يصبح محتوى أو ترقية أو سطراً في كتاب التشغيل.

This means:

- **No orphan channels.** A channel that does not produce a scored lead is not a growth machine — it is a cost. SEO, webinars, ads, media: each must terminate in a lead record.
- **No unscored leads.** A lead with no score has no defined next action. Scoring is the join between acquisition and sales.
- **No unrecorded results.** Delivery without an evidence record (Proof Pack) breaks the loop — there is nothing to turn into content, upsell, or a case-safe summary.
- **The loop is auditable end to end.** Signal provenance, scoring rationale, approval decisions, and evidence are all logged. The audit trail *is* the product, on the growth side as much as the delivery side.

The 22 machines are organised into four bands: **Acquisition** (1–14), **Platform** (15–17), **Governance** (18–19), and **Planning & Measurement** (20–22).

---

## 2. The 22 machines — الآلات الاثنتان والعشرون

Each machine below states: **Purpose · Flow/States · What exists in code · Gap · Priority.** Priority values: `extend` (works, only improve), `in build` (being built now), `P1`/`P2`/`P3` (roadmap order).

---

### Machine 1 — Sales Autopilot — قائد المبيعات الآلي

- **Purpose:** convert a scored lead into a meeting, a scope, and a paid invoice without manual triage of every lead.
- **Flow / States:** `lead_in → scored → qualified | nurtured | rejected → meeting_booked → scoped → proposal_sent → invoiced → won | lost`.
- **What exists in code:** `api/routers/sales_os.py`, `api/routers/crm_v10.py`, `api/routers/decision_passport.py`, `dealix/intelligence/lead_scorer.py`, `LeadScoreRecord` in `db/models.py`. Scoring is transparent and rubric-based; the decision passport carries the rationale.
- **Gap:** none structural. Improvements only — tighten the scoring rubric per sector, widen evidence capture on lost deals.
- **Priority:** `extend`.

### Machine 2 — Support Autopilot — قائد الدعم الآلي

- **Purpose:** resolve customer questions from sourced knowledge, escalate cleanly, and feed support signals back into upsell and content.
- **Flow / States:** `ticket_in → classified → answered_from_kb | escalated → resolved → satisfaction_logged`.
- **What exists in code:** `auto_client_acquisition/support_os/` (inbox, knowledge base, customer journey), `api/routers/support_os.py`, `api/routers/support_journey.py`, `api/routers/support_webhook.py`.
- **Gap:** none structural. Improvements only — wider KB coverage, sharper escalation thresholds.
- **Priority:** `extend`.

### Machine 3 — Marketing Factory — مصنع المحتوى التسويقي

- **Purpose:** turn delivered evidence and sector patterns into a steady stream of governed content assets (posts, briefs, landing copy) on a calendar.
- **Flow / States:** `topic_proposed → drafted (AR+EN) → governance_review → approved → scheduled → published → lead_attributed`.
- **What exists in code:** documentation and templates only — `docs/sales-kit/`, content calendar docs, 200+ `landing/*.html` pages. **No backend tables, no content pipeline, no attribution join.**
- **Gap:** large. Need content-asset tables, a draft→approve→publish pipeline, and lead attribution back into Machine 1.
- **Priority:** `P2` — first roadmap machine after the Affiliate/Partner build.

### Machine 4 — Media Authority Engine — محرك السلطة الإعلامية

- **Purpose:** build durable category authority (talks, articles, sector reports) so inbound leads arrive pre-warmed.
- **Flow / States:** `authority_topic → asset_produced → placed → mention_tracked → inbound_lead_attributed`.
- **What exists in code:** docs and landing pages only. No backend.
- **Gap:** large, but lowest urgency — authority compounds slowly and depends on Machine 3 existing first.
- **Priority:** `P3` — last in the roadmap order.

### Machine 5 — Affiliate Machine — آلة المسوّقين بالعمولة

- **Purpose:** let trusted individuals send leads via a tracked link/code and earn a one-time commission on the first paid Diagnostic.
- **Flow / States:** `applied → scored → approved → link_issued → referral_logged → qualified → deal_paid → commission_eligible → payout`.
- **What exists in code:** scaffolding only — `api/routers/referral_program.py` (customer referral), `api/routers/partnership_os.py` (in-memory), partial `PartnerRecord` in `db/models.py`, `docs/AGENCY_PARTNER_PROGRAM.md`.
- **Gap:** the largest genuine net-new code gap in the system.
- **Priority:** **`in build`** — being built end-to-end now (see §3 and the plan's Part B). Extends `partnership_os`; commission only after `invoice_paid`; clawback within 30 days; no self-referrals.

### Machine 6 — Partner Recruitment — استقطاب الشركاء

- **Purpose:** identify and onboard CRM / AI / GRC consultants and operators who serve Dealix's ICP, and score their fit before activation.
- **Flow / States:** `application → partner_scoring → auto_review | approve_candidate | reject → approval_queued → activated`.
- **What exists in code:** scaffolding — `/api/v1/public/partner-application` and a fit-score stub in `partnership_os.py`.
- **Gap:** scoring rubric, persistence, and approval gating.
- **Priority:** **`in build`** — bundled into the Affiliate/Partner machine. Partner activation queues an `ApprovalRequest` (non-negotiable #8).

### Machine 7 — Partner Distribution — توزيع الشركاء

- **Purpose:** give activated partners tracked links, an approved messaging library, and a portal showing referrals, commissions, and payout status.
- **Flow / States:** `activated → links_issued → assets_available → referrals_visible → commissions_visible → payout_visible`.
- **What exists in code:** scaffolding plus `docs/AGENCY_PARTNER_PROGRAM.md` (a 3-tier ladder being reconciled with the playbook's 4-tier ladder).
- **Gap:** the partner portal, approved-asset library, and link tracking.
- **Priority:** **`in build`** — bundled into the Affiliate/Partner machine. Partners only ever distribute **approved assets**; the messaging library ships AR+EN.

### Machine 8 — Paid Ads — الإعلانات المدفوعة

- **Purpose:** buy attention from in-market ICP segments and route every click to a lead record with full UTM provenance.
- **Flow / States:** `campaign → click → landing → lead_captured → scored → attributed_to_spend`.
- **What exists in code:** landing pages only. No campaign tables, no spend↔lead attribution.
- **Gap:** campaign/spend tables, UTM capture, cost-per-qualified-lead reporting.
- **Priority:** `P3` — second-last; ads amplify a loop that must already convert organically first.

### Machine 9 — Email / Newsletter — البريد والنشرة

- **Purpose:** nurture leads and customers with a governed, consented newsletter; convert nurture into meetings and upsells.
- **Flow / States:** `subscriber_consented → segmented → issue_drafted (AR+EN) → governance_review → sent → engagement_tracked → lead_or_upsell`.
- **What exists in code:** templates and docs only. No subscriber table, no consent ledger join for newsletter, no send pipeline.
- **Gap:** subscriber + consent tables, issue pipeline, engagement attribution.
- **Priority:** `P2` — third roadmap machine. Sends only to **consented** subscribers; consent recorded in the consent ledger.

### Machine 10 — Webinars / Workshops — الندوات وورش العمل

- **Purpose:** run governed live sessions that demonstrate the Diagnostic and produce a batch of warm, self-selected leads.
- **Flow / States:** `session_planned → registration → attended | no_show → follow_up → lead_scored`.
- **What exists in code:** docs and landing pages only.
- **Gap:** registration table, attendance tracking, follow-up→lead join.
- **Priority:** `P2` — fourth roadmap machine.

### Machine 11 — SEO — تحسين محركات البحث

- **Purpose:** earn durable inbound search traffic on category and sector terms, each page terminating in a lead capture.
- **Flow / States:** `keyword_targeted → page_published → indexed → organic_visit → lead_captured`.
- **What exists in code:** 200+ `landing/*.html` pages exist but are not organised as an SEO machine — no keyword register, no ranking/traffic→lead attribution.
- **Gap:** keyword register, page-to-keyword mapping, organic-lead attribution.
- **Priority:** `P2` — fifth roadmap machine; depends on Machine 3 for content supply.

### Machine 12 — Retargeting — إعادة الاستهداف

- **Purpose:** re-engage prior visitors and stalled leads with consented, governed touches — never cold.
- **Flow / States:** `prior_visitor | stalled_lead → audience_built → governed_touch → re_engaged → scored`.
- **What exists in code:** none beyond landing pages.
- **Gap:** audience tables built from **first-party, consented** data only.
- **Priority:** `P3` — sixth roadmap machine. Audiences are first-party only; no purchased or scraped lists (non-negotiable #1).

### Machine 13 — Customer-Referral Loop — حلقة إحالة العملaء

- **Purpose:** turn satisfied customers into a referral source — distinct from Machine 5 (external affiliates); this is *existing customers* referring peers.
- **Flow / States:** `customer_satisfied → referral_invited → referral_submitted → qualified → deal_paid → reward_logged`.
- **What exists in code:** `api/routers/referral_program.py` exists as a starting point.
- **Gap:** the referral invitation trigger off Support/Delivery satisfaction signals, and reward tracking.
- **Priority:** `P1` — first roadmap machine after the Affiliate/Partner build; it reuses Machine 5's referral and reward plumbing.

### Machine 14 — Upsell Machine — آلة الترقية

- **Purpose:** move a delivered Diagnostic customer to the Sprint, and a Sprint customer to the Managed Revenue Ops retainer, when evidence supports it.
- **Flow / States:** `delivered → retainer_readiness_evaluated → upsell_offered | not_ready → accepted | declined`.
- **What exists in code:** retainer-readiness logic is referenced in `SPRINT_DELIVERY_PLAYBOOK.md` (Day 6, `adoption_os.retainer_readiness`); upsell triggering is partial.
- **Gap:** a systematic upsell trigger and offer record tied to proof score and adoption score.
- **Priority:** `P1` — extend alongside the customer-referral loop; both fire off the same delivery-satisfaction signal.

### Machine 15 — Backend tables — جداول الخلفية

- **Purpose:** the durable record layer every machine reads and writes — leads, scores, partners, referrals, commissions, content assets, subscribers.
- **Flow / States:** n/a (data layer).
- **What exists in code:** `db/models.py` holds `LeadScoreRecord`, `PartnerRecord` (partial), and the delivery-side records. SQLAlchemy with `SoftDeleteMixin`, `String(64)` ids, UTC defaults; Alembic migrations under `db/migrations/`.
- **Gap:** affiliate/partner tables (added now in the Part B build); content, subscriber, and campaign tables (added per roadmap machine).
- **Priority:** `in build` (affiliate tables) then incremental per machine — never a big-bang schema.

### Machine 16 — APIs — واجهات البرمجة

- **Purpose:** the thin HTTP layer between machines and surfaces; every response carries governance state.
- **Flow / States:** n/a (interface layer).
- **What exists in code:** `api/routers/*.py` — routers are thin; domain logic lives in `auto_client_acquisition/`. Standard pattern: `prefix="/api/v1"`, `ConfigDict(extra="forbid")` request models, responses carry `hard_gates` + `governance_decision`.
- **Gap:** `api/routers/affiliate_machine.py` (added now); one router per roadmap machine.
- **Priority:** `in build` then incremental.

### Machine 17 — Frontend — الواجهة الأمامية

- **Purpose:** the customer-, partner-, and founder-facing surfaces.
- **Flow / States:** n/a (presentation layer).
- **What exists in code:** static `landing/*.html` pages; founder dashboard exists.
- **Gap:** partner recruitment page and partner portal (added now); marketing/content surfaces per roadmap machine.
- **Priority:** `in build` (`landing/affiliate.html`, `landing/partner-portal.html`) then incremental.

### Machine 18 — Governance Layer — طبقة الحوكمة

- **Purpose:** enforce the 11 non-negotiables at runtime and at build time, so no machine can ship an unsafe action.
- **Flow / States:** `request → policy_evaluation → ALLOW | DRAFT_ONLY | REQUIRE_APPROVAL | REDACT | BLOCK | RATE_LIMIT | REROUTE → logged`.
- **What exists in code:** **strong and complete** — `auto_client_acquisition/governance_os/`, `auto_client_acquisition/approval_center/`, value ledger, friction log, consent ledger; the 11 non-negotiables are enforced as CI guard tests (`tests/test_no_scraping_engine.py`, `tests/test_no_cold_whatsapp.py`, `tests/test_no_linkedin_automation.py`, `tests/test_no_guaranteed_claims.py`, `tests/test_no_pii_in_logs.py`, `tests/test_no_source_no_answer.py`, and others).
- **Gap:** none. Every new machine must register with this layer, not replace it.
- **Priority:** `extend` — coverage grows as machines are added; the layer itself is sound.

### Machine 19 — Sales / Marketing governance — حوكمة المبيعات والتسويق

- **Purpose:** apply Machine 18's policy specifically to acquisition: claims, channels, and consent.
- **Flow / States:** `acquisition_action → claim_check + channel_check + consent_check → decision`.
- **What exists in code:** the guaranteed-claim regex guards in `governance_os/runtime_decision.py`; channel policy in `docs/05_governance_os/CHANNEL_POLICY.md`; the WhatsApp boundary in `docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md`.
- **Gap:** a partner-content compliance scanner (added now as `compliance_guard.py` in the Affiliate build), reused by Machines 3, 4, 8, 9.
- **Priority:** `in build` (compliance scanner) then `extend`.

### Machine 20 — 30-day plan — خطة الثلاثين يوماً

- **Purpose:** the near-term execution slice — what ships in the next month.
- **Flow / States:** n/a (planning artefact).
- **What exists in code:** `dealix/registers/90_day_execution.yaml` (Phase 0, Days 0–30: "Control plane first").
- **Gap:** the current 30-day slice should name the Affiliate/Partner machine as the headline deliverable.
- **Priority:** `extend` — update the register, not a new file.

### Machine 21 — 90-day plan — خطة التسعين يوماً

- **Purpose:** the rolling quarter roadmap that sequences all machines.
- **Flow / States:** n/a (planning artefact).
- **What exists in code:** `dealix/registers/90_day_execution.yaml` (Phases 0–2).
- **Gap:** align Phase 1 ("Revenue + Partnership controlled MVP") with the build order in §3 of this document.
- **Priority:** `extend`.

### Machine 22 — Dashboards — اللوحات

- **Purpose:** surface the loop's health to the four audiences who steer it.
- **Flow / States:** n/a (measurement layer).
- **What exists in code:** the founder dashboard exists; partner ops dashboard endpoint is added in the Affiliate build (`GET /api/v1/ops/partners/dashboard`).
- **Gap:** marketing and a consolidated partner dashboard; see §5.
- **Priority:** `P1` for the partner dashboard (ships with the Affiliate machine); `P2` for the marketing dashboard.

---

## 3. Recommended build order — ترتيب البناء الموصى به

The order is deliberate: build what multiplies lead flow without violating doctrine, before building what merely amplifies an existing flow. Sales (1) and Support (2) already exist — they are **extended, never rebuilt**.

| # | Machine | Why this position |
|---|---|---|
| 1 | **Affiliate / Partner** (5, 6, 7, 15–17 slice) | Largest net-new code gap; multiplies leads through trusted humans, not automation. **Being built now.** |
| 2 | **Marketing Factory backend** (3) | Content is the loop's fuel; every later machine (SEO, email, media) consumes it. |
| 3 | **Customer-Referral loop** (13) | Reuses Affiliate plumbing; turns delivered proof into new leads at near-zero cost. |
| 4 | **Newsletter / Email** (9) | Nurtures the leads the above machines produce; consented, governed. |
| 5 | **Webinars / Workshops** (10) | Converts content + nurture into batches of warm leads. |
| 6 | **SEO** (11) | Durable inbound; depends on Marketing Factory output. |
| 7 | **Retargeting** (12) | Re-engages first-party audiences; needs traffic from the above to retarget. |
| 8 | **Paid Ads** (8) | Amplifies a loop that must already convert organically — buy scale, not survival. |
| 9 | **Media Authority** (4) | Compounds slowest; sequenced last so it builds on a working content engine. |

**Upsell (14)** is extended in parallel with the Customer-Referral loop — both fire off the same delivery-satisfaction signal. **Governance (18, 19)** and the **planning registers (20, 21)** are extended continuously, not scheduled as a slot.

The principle: **never run 22 builds at once.** One machine fully built and governed beats nine half-built channels.

---

## 4. Governance — الحوكمة: mapping machines to the 11 non-negotiables

Every machine inherits Machine 18. The 11 non-negotiables, quoted verbatim:

1. **No scraping.**
2. **No cold WhatsApp.**
3. **No LinkedIn automation.**
4. **No fake or un-sourced claims.**
5. **No guaranteed sales outcomes.**
6. **No PII in logs.**
7. **No source-less knowledge answers.**
8. **No external action without approval.**
9. **No agent without identity.**
10. **No project without a Proof Pack.**
11. **No project without a Capital Asset.**

These are enforced as CI guard tests (`tests/test_no_*.py`) — a machine that violates one cannot merge.

**Per-machine binding (the high-risk constraints):**

| Machine | Binding non-negotiables — what it must NOT do |
|---|---|
| 5 Affiliate, 6 Recruitment, 7 Distribution | #1, #2, #3 — `compliance_guard` **refuses** any recruitment or partner-content request mentioning scraping, cold WhatsApp, or LinkedIn automation. #5 — partners may not promise ROI or guaranteed sales; only approved claims. #8 — partner approval and payout mark-paid **queue an `ApprovalRequest`**. #6 — contact emails stored as `contact_email_hash`, never raw. |
| 3 Marketing Factory, 4 Media | #4 — every published claim traces to evidence or the no-overclaim register. #5 — no guaranteed-outcome language. |
| 8 Paid Ads, 12 Retargeting | #1 — audiences are first-party and consented only; no purchased or scraped lists. #4 — ad copy is governed like all content. |
| 9 Email / Newsletter | #2 — newsletter is not cold outreach; sends only to **consented** subscribers, recorded in the consent ledger. #6 — no PII beyond consented contact data. |
| 10 Webinars, 13 Customer-Referral | #8 — follow-up touches that leave Dealix infra require approval. #4 — case material is case-safe and anonymized. |
| 1 Sales, 14 Upsell | #5 — proposals state "estimated", never guaranteed. #8 — no proposal or message sent externally without logged approval. #9 — every acting agent has an identity. |
| 2 Support | #7 — answers come only from sourced knowledge; no source, no answer. #6 — no PII in support logs. |
| All delivered work (via 1, 14) | #10 — no project closes without a Proof Pack. #11 — no project closes without at least one Capital Asset deposited. |

**The recurring rule for every acquisition machine:** a channel may *attract* and *capture*, but it may not *act outbound* on a person without consent and approval. Dealix never sends external messages on a customer's or partner's behalf without explicit, logged approval (#8).

---

## 5. Measurement — القياس: the four dashboards

The loop is steered by four dashboards, one per audience. Metrics are drawn from the playbook's section 22. Every metric is an **observed count or an estimated rate** — never a guaranteed projection (#5).

### 5.1 Founder dashboard — لوحة المؤسس

The whole-loop health view.

- Leads in, by source machine.
- Qualified-lead rate (estimated).
- Pipeline value (SAR) and weighted forecast vs actual.
- Diagnostics / Sprints / retainers — count and revenue.
- Proof score distribution across delivered work.
- Capital assets deposited (period count).
- Open approvals and approval lag.
- Friction-log events (disputes, clawbacks, refunds).

### 5.2 Marketing dashboard — لوحة التسويق

How well the acquisition machines feed the loop.

- Content assets published (AR / EN), by machine.
- Organic visits and lead capture by page (SEO).
- Newsletter subscribers (consented), issue open and engagement rates.
- Webinar registrations, attendance rate, follow-up→lead conversion.
- Cost per qualified lead, by paid campaign.
- Lead attribution by source machine into Machine 1.

### 5.3 Partner dashboard — لوحة الشركاء

The Affiliate/Partner machine's operating view. Surfaced by `GET /api/v1/ops/partners/dashboard`.

- Active partners by tier.
- Referrals submitted vs qualified.
- Partner-sourced revenue (SAR).
- Commission due, by status (`pending → eligible → approved → paid → clawed_back`).
- Payouts built and marked paid (approval-gated).
- Compliance flags by kind (`forbidden_claim`, `spam`, `no_disclosure`, `self_referral`, `brand_bidding`).

The partner's own portal (`GET /api/v1/partner/{id}/portal`) shows their referral link, approved assets, submitted and qualified referrals, commission earned, payout status, and the compliance rules.

### 5.4 Support dashboard — لوحة الدعم

How support feeds satisfaction, upsell, and referral.

- Tickets in, resolution rate, KB-answered share.
- Escalation rate and time to resolution.
- Satisfaction signal (drives Machines 13 and 14).
- Knowledge-gap log — questions the KB could not source (#7).
- Upsell triggers raised from support signals.

---

## 6. How this document is used — كيف تُستخدم هذه الوثيقة

- **Before building a machine:** confirm its subsection here is current. If the gap or priority is stale, update this document *first* — it is the contract.
- **When extending Sales or Support:** they are marked `extend`; do not rebuild.
- **When a new machine ships:** update its "What exists in code" line with real file paths, move its priority forward, and update the relevant dashboard section.
- **Governance is not optional per machine.** Every machine registers with Machine 18; the `tests/test_no_*.py` guards are the merge gate.

This document does not implement anything. The Affiliate & Partner machine (Machines 5–7, the §3 build-order #1) is the first machine built against it; its full specification is in the approved plan's Part B.

---

## 7. Cross-references — مراجع متقاطعة

- Non-negotiables: [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md), [WHAT_DEALIX_REFUSES.md](../00_constitution/WHAT_DEALIX_REFUSES.md).
- Governance: [GOVERNANCE_OS.md](../05_governance_os/GOVERNANCE_OS.md), [RUNTIME_GOVERNANCE.md](../05_governance_os/RUNTIME_GOVERNANCE.md), [CHANNEL_POLICY.md](../05_governance_os/CHANNEL_POLICY.md), [APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md).
- Partner program (being unified to the 4-tier ladder): [AGENCY_PARTNER_PROGRAM.md](../AGENCY_PARTNER_PROGRAM.md).
- Delivery & proof: [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md), [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).
- Saudi channel boundary: [WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md).
- Planning register: [90_day_execution.yaml](../../dealix/registers/90_day_execution.yaml).

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
