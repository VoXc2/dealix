# Controls Matrix — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Founder / Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CONTROLS_MATRIX_AR.md](./CONTROLS_MATRIX_AR.md)

## Context
Enterprise buyers do not buy promises; they buy controls. This Controls
Matrix is the single page that maps every Dealix control to who needs
it and where it is implemented. It is the answer Dealix gives to
procurement, InfoSec, and Compliance teams. It is referenced by
`docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`,
`docs/DPA_DEALIX_FULL.md`, and the certifications register in
`docs/legal/COMPLIANCE_CERTIFICATIONS.md`.

## The Matrix

| Control | Description | Required For |
|---|---|---|
| RBAC | Role-based access control inside the platform | enterprise |
| SSO | Single sign-on integration | enterprise |
| Audit exports | Export of audit logs to client systems | enterprise |
| Data retention | Retention rules per dataset | sensitive clients |
| Approval workflows | Action approval routing | all |
| PII redaction | Detection and redaction of personal data | all |
| Model run logs | Traceability for every AI run | all |
| Eval reports | Quality evaluation results per service | production AI |
| Incident response | AI failures, PII exposure, mis-actions | enterprise |

## Notes on Each Control
- **RBAC.** Aligned with Permission Mirroring in
  `docs/governance/PERMISSION_MIRRORING.md`; every request is bound to
  a user's effective ACL.
- **SSO.** Required for enterprise; supports SAML/OIDC providers most
  common in Saudi enterprise.
- **Audit exports.** Append-only, signed exports; structure follows
  `docs/product/MANAGEMENT_API_SPEC.md`.
- **Data retention.** Schedule defined in
  `docs/DATA_RETENTION_POLICY.md` and PDPL schedule in
  `docs/ops/PDPL_RETENTION_POLICY.md`.
- **Approval workflows.** Defined as part of the Action Taxonomy in
  `docs/governance/AI_ACTION_TAXONOMY.md`.
- **PII redaction.** Applied at the LLM Gateway; logged with redaction
  policy version.
- **Model run logs.** Stored per `docs/ledgers/AI_RUN_LEDGER.md`.
- **Eval reports.** From `docs/product/EVALUATION_REGISTRY.md`.
- **Incident response.** See `docs/governance/INCIDENT_RESPONSE.md`.

## Enterprise Readiness Definition
A client is "enterprise-ready" inside Dealix when all of the
following hold:

- Audit logs are exported on schedule.
- RBAC and SSO are enabled for that workspace.
- A retention policy is signed and applied.
- A support and incident process is named and tested.
- This Controls Matrix is signed.
- An incident response runbook is in place and accepted.

Without these, the workspace is treated as "growth-tier" and
Level-5 external actions are not enabled.

## Use in Sales and Delivery
- **Sales:** the matrix is the appendix attached to every enterprise
  proposal.
- **Delivery:** every enterprise project's RACI references the matrix
  to assign control ownership.
- **Audit:** the matrix is the index against which third-party audits
  are scoped.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Enterprise procurement questions | Filled controls answers, evidence links | Governance Lead | Per deal |
| Control implementation status | Per-control evidence (logs, configs) | Platform Lead | Continuous |
| Audit findings | Matrix updates | Governance Lead | Per audit |

## Metrics
- **Control Coverage** — share of "Required For: all" controls
  enabled in production workspaces (target = 100%).
- **Evidence Currency** — share of controls with evidence updated in
  the last 90 days (target ≥ 95%).
- **Enterprise Coverage** — share of enterprise workspaces with all
  enterprise-tier controls enabled (target = 100%).
- **Audit Findings Closed** — share of audit findings closed within
  agreed SLA (target ≥ 90%).

## Related
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — the trust pack this
  matrix anchors.
- `docs/DPA_DEALIX_FULL.md` — data processing agreement bound to these
  controls.
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — certifications register.
- `docs/governance/INCIDENT_RESPONSE.md` — sibling file for incident
  control.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
