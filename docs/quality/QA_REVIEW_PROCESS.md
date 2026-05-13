---
title: QA Review Process — Reviewers, Timing, Escalation, Scoreboard
doc_id: W6.T36.qa-process
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T36, W5.T30]
kpi:
  metric: first_time_qa_pass_rate
  target: 70
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.85
  effort: 0.5
  score: quality-operating
---

# QA Review Process

## 1. Context

The Quality Standard defines *what* gets checked. This document defines
*who* runs the checks, *when*, what happens when a gate fails, and how the
weekly QA scoreboard meeting works.

## 2. Audience

CSM (project owner), assigned engineer, HoCS, peer engineer (for cross-
review), HoP (called only on systemic findings).

## 3. Who Reviews What

| Gate | Primary reviewer | Secondary / sign-off |
|------|------------------|----------------------|
| Business | CSM | HoCS on every project |
| Data | Engineer | HoData on first project per customer |
| AI | Engineer + AR/EN reviewer | HoP on AI-heavy offerings |
| Compliance | CSM | HoLegal on PII / new sector / new geography |
| Delivery | CSM | HoCS on every project |

**The customer never sees a gate verdict directly** — they see the executive
report and the handoff packet, which are downstream artifacts of a passed QA.

## 4. When QA Runs

Inside the Stage Machine, QA fires at two points:

1. **Pre-build sanity** — end of Stage 3 (Design). Quick triage: do the
   five gates have plausible answers? If not, scope is wrong; rework Design.
2. **Full review** — end of Stage 5 (Validate). All 5 gates answered;
   QualityScore computed; `evaluate(...)` called in `qa_review.py`. Result
   gates Validate → Deliver.

## 5. Escalation When a Gate Fails

A failing gate is not a project failure — it is an instruction. The CSM:

1. Logs the failure reason from the QAReport (`reasons_blocked_en` /
   `_ar`).
2. Assigns the fix to engineer or content reviewer with a target date
   (≤ 3 working days for first miss).
3. Re-runs `evaluate(...)` after the fix. Loop continues until
   `ships=True` OR HoCS escalates.

HoCS escalates to HoP / HoData / HoLegal when:

- The same gate fails twice in a row on the same project.
- The same gate is failing across multiple projects (systemic).
- A Compliance gate fails on a PII or PDPL question — Legal is in the loop
  before any rework.

## 6. The Weekly QA Scoreboard Meeting

Every Monday, 30 minutes. Attendees: HoCS (chair), CTO, HoData, HoLegal,
HoP. Inputs (auto-generated from `QAReport` rows):

- Projects shipped this week + their QualityScore distribution.
- Projects blocked + the gate(s) blocking them.
- Trailing 30-day rolling pass rate per gate (target ≥ 90% per gate).
- Top 3 recurring failure reasons (what is the systemic fix?).

Outputs:

- One systemic fix committed per meeting (e.g., add a new check to
  `qa_review.py`, update a template, retrain a reviewer).
- Any project below 80 → named owner + due date for re-review.
- Escalation list for the founder/CEO if blocked > 7 days.

## 7. Anti-Patterns

- **Self-review only**: an engineer cannot be the sole reviewer of their
  own build. Peer cross-review is mandatory.
- **Gate fudging**: marking a gate `passed=True` without evidence. Audit-
  logged; repeat offence is a performance issue.
- **Scoreboard skipping**: cancelling the Monday meeting because "things
  are going well". The meeting is the discipline; skip it and quality
  drifts within 4 weeks.

## 8. Cross-links

- Quality Standard: [`QUALITY_STANDARD.md`](QUALITY_STANDARD.md)
- Canonical Standard: [`../strategy/dealix_delivery_standard_and_quality_system.md`](../strategy/dealix_delivery_standard_and_quality_system.md)
- Ops cadence: [`../operations/executive_operating_cadence.md`](../operations/executive_operating_cadence.md)
- Code: `auto_client_acquisition/delivery_factory/qa_review.py`

## 9. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: refresh quarterly with retro on which gates caught what.

## 10. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial QA review process + weekly scoreboard ritual |
