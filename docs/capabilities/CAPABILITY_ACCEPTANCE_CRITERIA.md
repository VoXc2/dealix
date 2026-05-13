---
doc_id: capabilities.acceptance_criteria
title: Capability Acceptance Criteria — What Counts as Built at L2 / L3 / L4 / L5
owner: HoCS
status: approved
last_reviewed: 2026-05-13
audience: [internal, customer]
---

# Capability Acceptance Criteria

> A capability is not "built" because we shipped a deliverable. A
> capability is built when the level-specific acceptance criteria are
> satisfied **with evidence in the ledgers**. This file is the
> referenced checklist for every level transition declared in
> `CAPABILITY_MATURITY_MODEL.md`.

## Hard rule

No level transition is recognized internally (or claimed to a customer)
without all of the rows below marked DONE in the relevant ledger
entry. Half-met criteria → the capability stays at the previous level
in the Capability Roadmap.

## L2 — Structured

The work is documented enough that another team member could run it.

- [ ] **Owner named** in writing on the customer side.
- [ ] **Process documented** in a runbook or SOP (in the customer's
      space or in `clients/<codename>/`).
- [ ] **Inputs and outputs explicit** — schema-level, not narrative.
- [ ] **KPI defined** with baseline, target, and measurement method
      (per `SERVICE_KPI_MAP.md`).
- [ ] **First artifact shipped** (report, list, workflow, draft pack).
- [ ] Evidence filed in Delivery Ledger.

## L3 — AI-Assisted

AI produces drafts; humans review and approve every external action.

- [ ] All L2 criteria still satisfied.
- [ ] **AI output produced** with schema-bound responses (no free-form
      JSON drift).
- [ ] **Human review step** in the workflow before any external action.
- [ ] **QA score ≥ 80** on the 5-gate review
      (`auto_client_acquisition/delivery_factory/qa_review.py`).
- [ ] **Proof Pack v6 delivered** within 14 days of Sprint close
      (`docs/PROOF_PACK_V6_STANDARD.md`).
- [ ] **At least 1 cited measurement** in the Proof Ledger (before / after).
- [ ] **Next-step opportunity named** (per `DEALIX_STANDARD.md` #8).
- [ ] Evidence filed in Delivery + Proof Ledger.

## L4 — Governed AI Workflow

The capability operates inside the customer's business with governance
embedded, not bolted on.

- [ ] All L3 criteria still satisfied.
- [ ] **Approval matrix wired** for every external-action class
      (`dealix/trust/approval_matrix.py` or equivalent in customer
      stack).
- [ ] **Audit log live** — every AI run produces an event in an
      immutable store (append-only).
- [ ] **Approval coverage ≥ 95%** of external actions in the trailing
      30 days.
- [ ] **Recurring report shipped** (weekly executive pack at minimum).
- [ ] **At least 1 governance review** held with the customer
      (decisions logged in `docs/ledgers/GOVERNANCE_LEDGER.md`).
- [ ] **Zero major governance incidents** during the pilot window.
- [ ] **PDPL register snippet** updated for any personal-data flow.
- [ ] Evidence filed in Governance + Delivery Ledger.

## L5 — Optimized Operating System

The capability recurs, measures itself, and improves on a documented
cadence.

- [ ] All L4 criteria still satisfied.
- [ ] **Recurring cadence in place** — weekly or monthly, on a
      calendar, with named attendees.
- [ ] **KPI dashboard live** — visible to the customer, refreshed
      automatically.
- [ ] **Improvement backlog maintained** — ≥ 1 improvement item
      shipped per month over the last 3 months.
- [ ] **Monthly Proof Pack** filed (`MONTHLY_OPERATING_REVIEW` per
      retainer line).
- [ ] **Retainer model in force** — contracted, billed, renewing.
- [ ] **NRR ≥ 100%** over the last 90 days for this capability.
- [ ] **At least 1 anonymized case study** ready for publication.
- [ ] Evidence filed across Delivery + Proof + Client + Learning
      Ledgers.

## Anti-patterns (any one of these blocks the transition)

- "We ran the workflow once" → not L3 without QA + Proof Pack.
- "Audit log is on the roadmap" → not L4. Live or not, no half-credit.
- "We meet sometimes" → not L5. Calendar entry + named attendees
  required.
- "Customer is happy" → not evidence. Numbers in the Proof / Value
  Ledger are evidence.

## Saudi / PDPL note

L4 acceptance includes a PDPL register snippet for any personal-data
flow. This is the line Saudi enterprise procurement looks for; without
it, the capability is treated as L3 regardless of internal claims.

## Cross-links

- `docs/company/CAPABILITY_MATURITY_MODEL.md` — full level model
- `docs/company/CAPABILITY_OPERATING_MODEL.md` — 7 capabilities
- `docs/company/DEALIX_STANDARD.md` — the 8 standards (the gate)
- `docs/company/SERVICE_KPI_MAP.md` — KPI definitions
- `docs/PROOF_PACK_V6_STANDARD.md` — proof pack standard
- `docs/company/VALUE_REALIZATION_SYSTEM.md` — value categories
- `docs/ledgers/README.md` — ledger templates
- `docs/quality/QUALITY_STANDARD.md` — QA scoring
