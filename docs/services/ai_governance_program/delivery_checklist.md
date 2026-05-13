# Delivery Checklist — AI Governance Program

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Lead — Governance
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [delivery_checklist_AR.md](./delivery_checklist_AR.md)

## Context
Phase-by-phase operational script for the 4–12 week AI Governance Program. Reproducible and auditable per `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, `docs/governance/RUNTIME_GOVERNANCE.md`, and `docs/quality/QUALITY_STANDARD_V1.md`. Each checkbox maps to a proof pack event.

## Roles
- **Delivery Lead (DL)** — single accountable.
- **Governance Reviewer (GR)** — primary content owner.
- **Compliance Specialist (CS-comp)** — PDPL, ZATCA, sector overlays.
- **Capability Lead (CL-cap)** — sign-off + sector overlays (e.g., clinics).
- **Client Sponsor (SP)** — final acceptance.
- **Client DPO** — primary client counterpart.
- **Client Counsel** — engaged for any regulatory aspect.
- **QA Reviewer (QA)** — independent.

## Phase-by-Phase Plan

### T-10 to T-1 — Pre-kickoff
- [ ] Welcome packet sent. (DL)
- [ ] Internal program board created. (DL)
- [ ] Premium re-validated; sector premium applied. (DL + Margin Controller)
- [ ] Proof pack initialized with `program_initialized`. (DL)
- [ ] Counsel-of-record contact verified. (DL)

### Phase 1 — Inventory + Risk Map (Week 1–3)
- [ ] Kickoff workshop (90 min) with SP, DPO, counsel observer. (DL + GR)
- [ ] AI tool list received. (Client + GR)
- [ ] Each tool walked through with its named owner. (GR)
- [ ] Data flow workshop run if needed (2h). (GR)
- [ ] Lawful-basis assessment per dataset. (CS-comp + Client DPO)
- [ ] Initial risk register drafted: top 30 risks ranked. (GR)
- [ ] Inventory and risk register reviewed with SP. (DL)
- [ ] Proof events: `ai_uses_inventoried = N`, `risks_logged = N`. (GR)

### Phase 2 — Policy + Approval Matrix (Week 3–5)
- [ ] Existing policies analyzed; gaps identified. (CS-comp)
- [ ] Approval matrix drafted: AI use case patterns × approver roles. (GR + CS-comp)
- [ ] Up to 5 policies updated (AI Usage, Data Handling, Vendor, Incident, Approval). (CS-comp)
- [ ] Client counsel reviews policy updates. (Counsel + DL)
- [ ] Approval matrix tested against the inventory: every AI use has a clear approver. (GR)
- [ ] Proof events: `approvals_documented = N`, `policy_updates = M`. (GR)

### Phase 3 — Audit + Risk Register + Controls Matrix (Week 5–8)
- [ ] Audit process designed: quarterly self-audit + annual third-party-style checklist. (CS-comp + GR)
- [ ] Risk register finalized: owner, treatment, review cadence, residual risk. (GR + Client DPO)
- [ ] Controls matrix built, aligned with `docs/enterprise/CONTROLS_MATRIX.md`. (GR + CS-comp)
- [ ] Control maturity scored per row. (GR)
- [ ] Incident response runbook updated/created. (CS-comp + Client DPO)
- [ ] Dry-run audit on 3 randomly selected AI uses. (GR + QA)
- [ ] Proof events: `controls_implemented = N`, `incidents_addressed = N`. (GR + CS-comp)

### Phase 4 — Training + Handoff (Week 8–12)
- [ ] Training package built: exec (45 min), owner (90 min), builder (3h), user (30 min). (DL + GR)
- [ ] Train-the-trainer session with client (2h). (GR)
- [ ] Sector overlays delivered if applicable (clinics, finance, government). (CL-cap)
- [ ] Final proof report + executive summary drafted. (DL)
- [ ] Final QA pass. (QA)
- [ ] Handoff workshop (3h) with SP, DPO, counsel observer. (DL + GR)
- [ ] SP signs handoff note; DPO countersigns. (SP + DPO)
- [ ] Proof events: `program_delivered`, `proof_pack_signed_off`. (DL)
- [ ] Upsell motion triggered. (DL + CSM)

## Cross-Cutting Controls
- Sensitive data only handled in vault; never copied.
- Weekly steering call with SP, DPO, DL, GR.
- Counsel observer invited to all major workshops.
- For healthcare / government clients: CL-cap signs off in addition to QA.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed SOW + intake | Program board | DL | T-10 |
| Weekly steering | Program updates | DL | Weekly |
| QA + GR + CL-cap results | Fix tickets or signoff | QA + GR + CL-cap + DL | End of each phase |
| Final delivery + report | Handoff | DL + SP + DPO | Final week |

## Metrics
- **On-time delivery** — Target ≥ 85%.
- **Inventory completeness** — Target ≥ 95%.
- **Lawful-basis coverage** — Target = 100%.
- **Approval matrix coverage** — Target = 100%.

## Related
- `docs/capabilities/governance_capability.md` — capability blueprint
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime governance
- `docs/governance/AI_ACTION_TAXONOMY.md` — action taxonomy
- `docs/governance/AI_ACTION_CONTROL.md` — action control
- `docs/enterprise/CONTROLS_MATRIX.md` — enterprise controls
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — compliance
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
