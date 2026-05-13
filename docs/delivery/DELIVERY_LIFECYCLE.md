# Delivery Lifecycle — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DELIVERY_LIFECYCLE_AR.md](./DELIVERY_LIFECYCLE_AR.md)

## Context
This file is the detailed lifecycle of a Dealix engagement, with
timing, owners, gates, and artifacts at each stage. It extends the
Delivery Standard in `docs/delivery/DELIVERY_STANDARD.md` and pairs
with `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` for the relationship motion
and `docs/V14_FOUNDER_DAILY_OPS.md` for founder oversight. The default
timing assumes a 10-business-day Sprint engagement; longer engagements
multiply the timings proportionally.

## Default Timing (10-Day Sprint)
| Day | Stage | Owner | Gate | Artifact |
|---|---|---|---|---|
| 0 | Kickoff | Delivery lead | Scope signed | `intake_form.md` started |
| 1 | Discover | Delivery lead | Intake complete | `intake_form.md` final |
| 2 | Diagnose | Data lead | DRS ≥ 50 | DRS record + diagnosis brief |
| 3 | Design | AI platform lead | Workflow design approved | Workflow plan |
| 4-6 | Build | AI platform lead | All AIRuns logged | Drafts |
| 7 | Validate | QA reviewer | QA ≥ 85 | QA record |
| 8 | Deliver | Delivery lead | Approval recorded | Delivery note |
| 9 | Prove | Delivery lead | Hero metric tied to audit event | Proof pack |
| 10 | Expand | Revenue | Renewal proposal sent | `renewal_proposal.md` |

## Gates In Detail
Each gate is a hard pass/fail. If a gate fails, the project either
re-enters the prior stage or escalates to the founder.

- **G1 — Intake gate**: all mandatory fields present, no consent
  issues; otherwise re-run Discover.
- **G2 — Data readiness gate**: DRS computed; if < 50, switch to a
  Data Cleanup engagement; if 50-69, schedule cleanup before Build.
- **G3 — Design gate**: workflow declares governance class, prompts
  are registered, schemas validated.
- **G4 — Build gate**: every AIRun has a ledger entry; no Gateway
  bypass; no forbidden-action block.
- **G5 — QA gate**: QA score ≥ 85 across bilingual review; otherwise
  rework.
- **G6 — Delivery gate**: Approval logged per matrix; recipient list
  and consent verified.
- **G7 — Proof gate**: hero metric tied to an `AuditEvent` and
  `ProofEvent`; otherwise no Expand.
- **G8 — Expand gate**: renewal or expansion proposal sent within 7
  days.

## Owners And Roles
The owner of each stage is the single responsible person for the
gate. RACI matrices live in the project workspace.

## Artifacts
- `intake_form.md` (Discover)
- `data_request.md` and DRS record (Diagnose)
- Workflow plan + governance class (Design)
- Drafts + AI run records (Build)
- `qa_checklist.md` filled (Validate)
- Delivery note + audit event (Deliver)
- Proof pack with `executive_report.md` (Prove)
- `renewal_proposal.md` (Expand)

## Escalations
- A failed G2 escalates to the founder within 24 hours.
- A failed G5 triggers up to two rework cycles; a third failure
  escalates to the founder.
- A failed G6 with a forbidden-action match triggers
  `docs/INCIDENT_RUNBOOK.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Scope | Stage timeline | Delivery lead | Per project |
| Gate review | Pass/fail decision | Owner of stage | Per gate |
| Escalation | Founder review | Founder | Per escalation |
| Closeout review | Lessons learned record | Delivery lead | Per project |

## Metrics
- **Lifecycle adherence** — share of projects following the default
  timing. Target: ≥ 80%.
- **Mean cycle time** — days from kickoff to Prove gate. Target: ≤
  10 for Sprint, ≤ 30 for Pilot.
- **Escalation frequency** — escalations per 10 projects. Target: ≤
  2.
- **Closeout completion** — share of projects with a lessons-learned
  record. Target: 100%.

## Related
- `docs/delivery/DELIVERY_STANDARD.md` — sibling delivery standard.
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — customer success motion.
- `docs/V14_FOUNDER_DAILY_OPS.md` — founder daily ops.
- `docs/ops/DAILY_OPERATING_LOOP.md` — daily operating loop.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
