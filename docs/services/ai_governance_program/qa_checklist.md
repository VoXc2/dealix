# QA Checklist — AI Governance Program

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer (independent)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [qa_checklist_AR.md](./qa_checklist_AR.md)

## Context
Quality gates the Program must clear at the end of each phase. Reviewer must not have produced the deliverables. Enforces `docs/quality/QUALITY_STANDARD_V1.md` and the runtime governance regime in `docs/governance/RUNTIME_GOVERNANCE.md`. Connects to the strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## How To Use
1. Open the program Notion record.
2. Walk every gate: Pass / Fail / N/A + evidence pointer.
3. Failures create same-day fix tickets.
4. Phase passes when all gates are Pass or N/A.

## Gate 1 — Every AI Use is Mapped
- [ ] AI inventory contains every AI tool / process surfaced in intake plus any discovered during Phase 1.
- [ ] Each entry has owner, purpose, data categories, users, vendor.
- [ ] No "TBD" entries.
- [ ] Inventory validated by each named owner.

## Gate 2 — Every Dataset Has Lawful Basis
- [ ] Each dataset has a documented lawful basis statement.
- [ ] Each statement references PDPL provisions where applicable.
- [ ] Counsel-of-record reviewed and approved.

## Gate 3 — Approval Matrix Complete
- [ ] Every AI use case pattern has an approver role.
- [ ] Every approver role has a named backup.
- [ ] Matrix tested on 5 random recent AI use requests.
- [ ] No "ask the CEO" catch-all clause.

## Gate 4 — Audit Log Defined
- [ ] Quarterly self-audit template exists.
- [ ] Annual third-party-style audit checklist exists.
- [ ] Audit owners named.
- [ ] Audit evidence retention policy aligned with `DATA_RETENTION_POLICY`.

## Gate 5 — Controls Matrix Matches Enterprise Needs
- [ ] Controls matrix aligned with `docs/enterprise/CONTROLS_MATRIX.md`.
- [ ] Each high-residual-risk has at least one assigned control.
- [ ] Control maturity scored honestly (not all "5").
- [ ] Gaps identified with remediation owners.

## Gate 6 — Incident Response Runbook Delivered
- [ ] Runbook covers detection, triage, containment, notification, postmortem.
- [ ] PDPL breach notification timing addressed (`docs/ops/PDPL_BREACH_RUNBOOK.md` referenced).
- [ ] Roles named, not just titles.
- [ ] Sample tabletop scenario completed.

## Gate 7 — PDPL-Aware Throughout
- [ ] PDPL provisions explicitly referenced in policies and risk register.
- [ ] Cross-border posture documented per `CROSS_BORDER_TRANSFER_ADDENDUM`.
- [ ] PDPL retention applied to all relevant datasets.
- [ ] Sector overlays applied where required.

## Gate 8 — Training Package Complete
- [ ] Exec, owner, builder, user materials exist.
- [ ] Train-the-trainer session completed with client.
- [ ] Materials in AR + EN.
- [ ] Knowledge check questions included.

## Gate 9 — Proof Pack Complete
- [ ] All required events present.
- [ ] Each event has timestamp, actor, value.
- [ ] Pack signed by DL + QA + GR + CL-cap + Sponsor + DPO.

## Gate 10 — Counsel Engagement Documented
- [ ] Counsel-of-record was engaged at the required moments (policy review, regulatory questions).
- [ ] Counsel did NOT sign off on Dealix deliverables (that's the client's choice).
- [ ] No Dealix deliverable claims to substitute for legal advice.

## Escalation
- 3+ gate failures → escalate to Governance Capability Lead.
- Gate 2 (lawful basis) failure → engagement paused; counsel review.
- Gate 7 (PDPL-aware) failure → re-audit by Compliance Specialist.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| End-of-phase deliverables | Phase result | QA | End of each phase |
| Final deliverables | Program signoff | QA + GR + CL-cap | Final week |
| Fix tickets | Resolutions | DL + Owner | Same day |

## Metrics
- **First-time pass rate** — Target ≥ 60%.
- **Gate failures per Program** — Target ≤ 4.
- **PDPL-aware audit** — Target = 100% on Gate 7.
- **Counsel engagement compliance** — Target = 100% on Gate 10.

## Related
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/capabilities/governance_capability.md` — capability blueprint
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime governance
- `docs/governance/AI_ACTION_TAXONOMY.md` — action taxonomy
- `docs/governance/AI_ACTION_CONTROL.md` — action control
- `docs/enterprise/CONTROLS_MATRIX.md` — enterprise controls
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/ops/PDPL_BREACH_RUNBOOK.md` — PDPL breach runbook
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — compliance
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
