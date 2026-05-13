---
title: Generic Project Delivery Lifecycle — Day 0 to +30
doc_id: W6.T36.delivery-lifecycle
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T36, W6.T35, W5.T10]
kpi:
  metric: on_time_delivery_rate
  target: 90
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.85
  effort: 1
  score: delivery-operating
---

# Project Delivery Lifecycle (Day 0 → +30)

## 1. Context

Every Dealix Sprint or Pilot follows the same calendar shape. The duration
slot (7 / 10 / 14 / 21 / 30 days) varies by offering, but the daily rhythm,
artifacts, and gates are identical. This document is the day-by-day operating
guide for a generic project.

## 2. Audience

CS lead (project owner), assigned engineer, AE shadow, customer day-to-day
owner. Used to prep a kickoff and to keep mid-flight projects on tempo.

## 3. The Calendar

### 3.1 Day 0 — Pre-Kickoff

- Signed scope + payment terms in writing.
- Project row created via `client_intake.process_intake`.
- Stage Machine initialized in Discover.
- Kickoff invite sent (≤ 48h slot).
- PDPL Art. 13 acknowledgement captured.

### 3.2 Day 1 — Kickoff

- 60-minute video call. Three roles required on customer side: economic
  buyer, exec sponsor, day-to-day owner.
- Walk the Delivery Standard's 8 stages.
- Confirm success metrics (numeric + dated).
- Capture data sources + access list.
- Transition: Discover → Diagnose.

### 3.3 Day 2–3 — Diagnose & Design

- Diagnostic scoring (data, process, AI fit, risk, ROI).
- Top-3 use cases shortlisted; #1 chosen.
- Design doc drafted (workflow, data schema, prompts, dashboard wireframe,
  approval rules, success metrics).
- Customer signs design doc before any build work.
- Transition: Diagnose → Design → Build.

### 3.4 Day 4 → Day N-3 — Build

- Reuse existing OS modules first; bespoke code requires CTO sign-off
  (per `internal_os_modules.md` §6).
- Human-in-the-loop default; audit logs from minute zero.
- Daily Slack/email standup with day-to-day owner (≤ 5 lines).
- Mid-project checkpoint at 50% of duration: spot-check outputs vs success
  metrics; if drift, escalate to HoCS.

### 3.5 Day N-2 → Day N-1 — Validate

- Run the 5-Gate QA review (`qa_review.py`).
- Customer UAT session: 30-minute walkthrough.
- Quality Score computed; must be ≥ 80 to ship.
- Edge-case + AR/EN tone + PII red-team checks.
- Transition: Validate → Deliver (gated on `ships=True`).

### 3.6 Day N — Deliver (Handoff)

- Handoff packet generated via `client_handoff.build_handoff`.
- Includes: deliverables, executive report, SOP/runbook, training video,
  audit log link, proof pack stub, next-step proposal.
- Live handoff session recorded.
- Customer signs the handoff (see [`HANDOFF_PROCESS.md`](HANDOFF_PROCESS.md)).
- Stage: Deliver complete.

### 3.7 Day N+14 — Prove

- Quantify the impact: hours saved, leads generated, tickets classified,
  pipeline value, data quality delta, feedback rating.
- Append entry to the Proof Ledger.
- Send the customer a one-page Impact Brief.
- Transition: Prove complete.

### 3.8 Day N+30 — Expand

- AE + CSM joint call: present the renewal/next-sprint proposal.
- Use `renewal_recommendation.recommend(...)` output as the conversation
  anchor.
- Outcome must be written: signed renewal, signed additional sprint,
  enterprise path, or documented "no".
- See [`RENEWAL_PROCESS.md`](RENEWAL_PROCESS.md) for the conversion playbook.

## 4. Per-Offering Duration Slots

| Offering | Day N | Notes |
|----------|------|-------|
| AI Quick Win Sprint | 7 | Single use case, 1 workflow |
| Revenue Intelligence Sprint | 10 | Data → scoring → outreach |
| AI Support Desk Sprint | 14 | KB + replies + dashboard |
| Workflow Automation Sprint | 14–21 | 1 internal process |
| Company Brain Sprint | 21 | Files → RAG with citations |
| Enterprise AI OS | 60+ | Multi-workflow, multi-pillar |

## 5. Cross-links

- Delivery Standard: [`DELIVERY_STANDARD.md`](DELIVERY_STANDARD.md)
- Canonical 8 stages: [`../strategy/dealix_delivery_standard_and_quality_system.md`](../strategy/dealix_delivery_standard_and_quality_system.md)
- Onboarding: [`CLIENT_ONBOARDING.md`](CLIENT_ONBOARDING.md)
- Pilot (extended): [`pilot_framework.md`](pilot_framework.md)
- Scope discipline: [`SCOPE_CONTROL.md`](SCOPE_CONTROL.md)
- Code: `auto_client_acquisition/delivery_factory/stage_machine.py`,
  `auto_client_acquisition/delivery_factory/delivery_checklist.py`

## 6. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: monthly until first 10 projects shipped; quarterly thereafter.

## 7. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial generic lifecycle Day 0 → +30 |
