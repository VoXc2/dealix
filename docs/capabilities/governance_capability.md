# Capability Blueprint — Governance Capability

> One of the 7 capabilities Dealix builds inside customers (per
> `docs/company/CAPABILITY_OPERATING_MODEL.md`). Mirrors the structure of
> `docs/capabilities/revenue_capability.md`. Concerns the customer's
> ability to use AI safely: PDPL alignment, an approval matrix, an audit
> trail, a forbidden-action perimeter, and a board-readable governance
> posture.

## Business purpose
Make AI safe for the customer to scale — without the brakes being a
single nervous lawyer. Stand up an organization-wide governance program
that inventories every AI tool, every data flow, and every action the AI
is allowed to take. Make the controls real (enforced at runtime, not in
a policy PDF) so the customer can answer "yes, we govern AI" to SAMA,
NCA, ZATCA, or SDAIA without rehearsal.

> **Hard rule**: every governance control is **enforced at runtime**, not
> on paper. The 8 runtime checks in `docs/governance/RUNTIME_GOVERNANCE.md`
> are the bar — anything weaker is decorative. The
> **ComplianceGuardAgent** is the mandatory gate for every other agent;
> it cannot be bypassed by a customer request, a sales pressure, or a
> "just this once" approval.

## Typical problems
- Shadow-AI: ChatGPT, Copilot, Gemini, and three vertical SaaS tools
  used by employees with no inventory, no policy, no logs.
- PDPL exposure: customer data pasted into public LLM windows without
  consent, lawful basis, or notice.
- Board / regulator panic: "We need an AI strategy. Are we compliant?"
  Nobody can answer.
- No approval matrix: nobody knows who is allowed to sign off on AI-
  generated emails to customers, contracts, or external posts.
- No audit log: when an inspector asks "show me who approved this AI-
  drafted message", silence.
- "Forbidden actions" exist only in the founder's head — agents,
  contractors, and integrators improvise.
- Sector regulators (SAMA for BFSI, NCA for cyber, ZATCA for fiscal)
  approaching, and the customer hasn't mapped which controls apply.

## Required inputs from customer
- AI tool inventory draft (what employees use today — even informally).
- Data inventory: which datasets touch personal data, special category,
  financial, health, HR.
- Org chart with named approvers per role (CSM / Head of CS / Head of
  Legal / CTO / CEO equivalents on the customer side).
- Sector and regulator exposure (BFSI / health / public / fintech /
  retail / education).
- Existing policies (if any) to baseline against.
- PDPL Art. 13 acknowledgement before any customer dataset is processed
  (per `docs/governance/PDPL_DATA_RULES.md` §3.2).
- A named governance owner (often Head of Legal or DPO).

## AI functions that build this capability
- AI tool inventory + risk classification (per
  `docs/services/ai_governance_program/ai_tool_inventory.md`).
- Data inventory + ROPA-aligned mapping (per
  `docs/services/ai_governance_program/data_inventory.md`).
- Saudi-specific risk assessment — PDPL + SAMA / NCA / ZATCA / SDAIA
  overlays (per `docs/services/ai_governance_program/risk_assessment.md`).
- Approval-matrix authoring on top of `dealix/trust/approval_matrix.py` —
  every high-stakes action mapped to a named approver and an evidence
  floor (per `docs/governance/APPROVAL_MATRIX.md`).
- Forbidden-action catalog (AR + EN) generated and customized (per
  `docs/governance/FORBIDDEN_ACTIONS.md`).
- Runtime policy wiring: 8 checks (source, PII, permission, claims,
  external-action, approval, audit, proof) executed before any AI
  side-effect.
- Bilingual AI usage policy + acceptable-use addendum.
- Board briefing pack (60/30/15-min agenda) + monthly evidence pack.

## Governance controls (binding)
- **Enforced at runtime** per `docs/governance/RUNTIME_GOVERNANCE.md` —
  every AI workflow passes all 8 checks; any BLOCK halts the operation.
- **Permission Mirroring** — AI inherits the requesting user's RBAC
  scope; no "super-user AI", no bypass.
- **Separation of duties** — the approver and the action initiator
  cannot be the same person (per
  `docs/governance/APPROVAL_MATRIX.md` §4).
- **Forbidden-claim filter** on every customer-facing output
  ("نضمن / guarantee / 100% / risk-free") via
  `dealix/trust/forbidden_claims.py`.
- **No PII in training pipelines**; **no card / IBAN passthrough** —
  hard block, no override (per
  `docs/governance/FORBIDDEN_ACTIONS.md` §3.3).
- **Policy override** requires CEO sign-off + audit entry, no exceptions.
- **Audit log append** for every action, approval, rejection, and
  redaction (per `docs/governance/AUDIT_LOG_POLICY.md`).
- **No autonomous external actions** — Level 6 in the AI Action Taxonomy
  is forbidden, no exceptions (per
  `docs/governance/RUNTIME_GOVERNANCE.md` §AI Action Taxonomy).

## KPIs (measured before/after)
- Actions executed without required approval (target: 0).
- PDPL audit findings on quarterly internal review (target: 0).
- Forbidden-action pre-send blocks (target: 100% of attempts caught).
- AI tool inventory coverage (% of in-use tools registered).
- Audit log completeness (% of actions with full event record).
- Approval median latency (operational health).
- Staff completing bilingual AI usage training (% of in-scope headcount).

## Maturity ladder (per `docs/company/CAPABILITY_OPERATING_MODEL.md`)
- **Level 0** — no policy, no inventory, no approver named.
- **Level 1** — verbal "be careful" policy; founder approves ad-hoc.
- **Level 2** — written AI policy exists; some approvers named; no audit log.
- **Level 3** — policy + approval matrix + inventory + audit log live
  (AI Readiness Review + AI Usage Policy).
- **Level 4** — runtime enforcement of the 8 checks + monthly evidence
  pack + bilingual training + risk register
  (PDPL-Aware Data Review + AI Governance Program).
- **Level 5** — Governance OS: continuous monitoring dashboard,
  cross-BU reporting, SAMA/NCA/SDAIA-ready evidence on demand.

## Dealix services that build / advance this capability
| Service | Lifts capability from → to | Indicative price |
|---------|----------------------------|------------------|
| AI Readiness Review | L0–L1 → L2 | scoped (sub-component of Diagnostic) |
| AI Usage Policy | L1 → L3 | scoped |
| PDPL-Aware Data Review | L1–L2 → L3 | scoped |
| AI Governance Program | L0–L2 → L4 | SAR 35,000–150,000 · 1–3 months |
| Governance Retainer (Phase 3+) | L4 → L5 | scoped |

Status note: AI Governance Program is **Not Ready / Beta candidate**
pending the Phase-3 governance dashboard
(per `docs/company/SERVICE_REGISTRY.md`). Until promotion to Sellable,
pilot only with explicit framing — and quote AI Readiness Review or
PDPL-Aware Data Review as the entry door.

## Agents involved (per `docs/product/AI_AGENT_INVENTORY.md`)
- **ComplianceGuardAgent** — autonomy level 3, MVP. **Mandatory gate
  for every other agent.** Runs source / PII / permission / claims /
  approval / audit checks before any side-effect. Cannot be bypassed.
- (Cross-cutting) every other agent (Revenue / Customer / Operations /
  Knowledge / Workflow / Reporting) **must call ComplianceGuardAgent**
  before producing an output. An agent that ships without the gate is
  retired (per `docs/product/AI_AGENT_INVENTORY.md` Agent Lifecycle).

## Proof types produced
- **Risk Proof** — actions blocked, approvals captured, PII redactions,
  PDPL acknowledgements, audit completeness. This is the headline.
- **Knowledge Proof** — bilingual AI usage policy + training completion
  records.
- **Quality Proof** — evidence pack quality (sampling 20 approvals per
  quarter, every one has the right approver at the right evidence floor).
- **Time Proof (indirect)** — speed of regulator response: "show me the
  audit" answered in minutes, not weeks.

## Saudi-specific notes
- **PDPL Art. 5 / 13 / 14 / 18 / 21** map to runtime controls in
  `docs/governance/PDPL_DATA_RULES.md`. Every customer-facing flow
  carries Art. 13 notice; cross-border transfers only via the
  documented Art. 18 bases.
- **SAMA, NCA, ZATCA, SDAIA** overlays in the risk assessment per
  `docs/services/ai_governance_program/risk_assessment.md`.
- **Kingdom Residency** (Enterprise plan) pins all data and processing
  to Kingdom-eligible regions.
- **Bilingual** policy, training, and board pack (AR/EN) are the default —
  Saudi boards and regulators expect Arabic-first documentation.
- **Sector mode**: BFSI customers inherit SAMA-aligned audit trails;
  fintech / payments customers get the ZATCA / SAMA overlay; public-
  sector adjacent customers get the SDAIA AI Ethics Framework overlay.

## Cross-links
- `docs/services/ai_governance_program/`
- `docs/services/ai_governance_program/offer.md`
- `docs/services/ai_governance_program/risk_assessment.md`
- `docs/services/ai_governance_program/policy_template.md`
- `docs/services/ai_governance_program/approval_matrix.md`
- `docs/services/ai_governance_program/audit_requirements.md`
- `docs/services/ai_governance_program/handoff.md`
- `docs/company/CAPABILITY_OPERATING_MODEL.md`
- `docs/company/AI_CAPABILITY_FACTORY.md`
- `docs/company/CAPABILITY_PACKAGES.md`
- `docs/company/VALUE_REALIZATION_SYSTEM.md`
- `docs/product/AI_AGENT_INVENTORY.md`
- `docs/governance/RUNTIME_GOVERNANCE.md`
- `docs/governance/APPROVAL_MATRIX.md`
- `docs/governance/FORBIDDEN_ACTIONS.md`
- `docs/governance/PDPL_DATA_RULES.md`
- `docs/governance/AUDIT_LOG_POLICY.md`
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
