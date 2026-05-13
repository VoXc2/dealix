# Offer — AI Governance Program

**Layer:** Service Catalog · Operational Kit
**Owner:** Governance Capability Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [offer_AR.md](./offer_AR.md)

## Context
This file defines the public-facing promise of the **AI Governance Program**, the top-tier service on the Dealix ladder. It exists because enterprises in KSA/GCC are adopting AI faster than their governance can keep up — exposing them to PDPL violations, ZATCA risk, board-level discomfort, and reputational harm. The Program plugs into the governance capability blueprint in `docs/capabilities/governance_capability.md`, the runtime governance regime in `docs/governance/RUNTIME_GOVERNANCE.md`, and the strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`. It implements the action taxonomy in `docs/governance/AI_ACTION_TAXONOMY.md` and the action control regime in `docs/governance/AI_ACTION_CONTROL.md`.

## Promise
> Build a **complete governance operating model** for AI usage across your company in **1–3 months** — covering inventory, approval workflows, audit, risk register, and controls matrix.

The Program replaces the "we're being careful with AI" assertion with a documented, audit-ready, PDPL-aware operating model that a board, regulator, or auditor can read.

## The Problem We Solve
- AI tools are being adopted by every department, often without IT or legal awareness.
- There's no inventory of which AI processes touch which data.
- No approval matrix exists; risky use cases ship by accident.
- No audit trail; when something goes wrong, nobody can reconstruct it.
- PDPL obligations, ZATCA implications, and sector regulations are unclear.
- The board asks "are we safe?" and there's no document to point to.

The Program compresses this into a structured 4–12 week build of a governance OS the client owns.

## Deliverables
1. **Governance Operating Model** — roles, authorities, escalation paths, meeting cadences.
2. **Approval workflows** — matrix mapping AI use cases to approver roles and approval evidence.
3. **Audit process** — quarterly self-audit + annual third-party-style audit checklist.
4. **Risk register** — ranked AI risks with owners, controls, and review cadence.
5. **Controls matrix** — controls × risks, with control maturity scoring.
6. **AI inventory** — every AI tool / process in use, with owner, data flow, lawful basis.
7. **Training package** — role-based training: executives, owners, builders, users.
8. **Proof pack** — events log, governance log, anonymization rules.

All deliverables under `QUALITY_STANDARD_V1` and shipped with a `PROOF_PACK_TEMPLATE` instance.

## What's NOT Included
- **Legal counsel substitute.** We work with the client's lawyers, not in place of them.
- **Certification audit** (ISO 27001, SOC 2). We prepare for it; we do not issue the certification.
- **Technical penetration testing.** We assess governance posture; we do not pen-test systems.
- **Vendor due-diligence reports** for specific AI providers (separate scope if needed).
- **PDPL legal filing** with the Saudi Data & AI Authority. We prepare; counsel files.
- **Ongoing operation.** Operation is the **Monthly Governance retainer**.

## Buyer Profile
- Enterprise or mid-market organization in KSA/GCC with 50–5,000 employees.
- 5+ AI tools or AI-touching processes already in use.
- Board, regulator, or audit pressure for governance.
- Existing data protection officer or compliance lead.
- Willingness to undergo a structured assessment.

## Why It Sells
- **Audit-ready in 1–3 months.** Faster than building governance internally from scratch.
- **PDPL-aware.** Designed for Saudi/Gulf reality, not bolted-on Western frameworks.
- **Board-ready output.** Documents written for executives, not just legal.
- **Bridge to retainer.** Every Program upsells into Monthly Governance, AI Readiness Reviews, or Policy updates.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| AI tool list | AI inventory + data flows | Client DPO + Dealix DL | Phase 1 |
| Data flow descriptions | Risk register | Client + Dealix Analyst | Phase 1 |
| Existing policies | Approval matrix + policy updates | Client Legal + Dealix | Phase 2 |
| Incident history | Audit process + risk controls | Client Audit + Dealix | Phase 3 |
| Trained team | Controls matrix + training package | Client HR + Dealix | Phase 4 |

## Metrics
- **Program completion rate** — Target ≥ 90%.
- **Inventory completeness** — `% AI uses inventoried`. Target ≥ 95%.
- **Lawful basis coverage** — `% datasets with documented lawful basis`. Target = 100%.
- **Approval matrix completeness** — `% AI use cases mapped to an approver`. Target = 100%.
- **Upsell rate** — `% programs converted to Monthly Governance within 90 days`. Target ≥ 60%.

## Related
- `docs/capabilities/governance_capability.md` — capability blueprint behind this service
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime governance regime
- `docs/governance/AI_ACTION_TAXONOMY.md` — action taxonomy
- `docs/governance/AI_ACTION_CONTROL.md` — action control regime
- `docs/enterprise/CONTROLS_MATRIX.md` — enterprise controls matrix
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — compliance certifications
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
