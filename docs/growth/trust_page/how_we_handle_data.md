# How We Handle Data — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Compliance
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [how_we_handle_data_AR.md](./how_we_handle_data_AR.md)

## Context
This is a public-facing page on the Dealix Trust hub. It describes — in
plain language — how Dealix handles client data. It must always agree with
the operational reality enforced by
`docs/DEALIX_OPERATING_CONSTITUTION.md`, the contract in
`docs/DPA_DEALIX_FULL.md`, and the retention policy in
`docs/DATA_RETENTION_POLICY.md`.

## Plain-language commitments

- **Approved sources only.** We never use client data that has not been
  explicitly approved by the client.
- **PII redacted.** Personal identifiers (phone, email, person names) are
  redacted or masked in outputs unless a lawful basis is documented.
- **Access mirrors permissions.** The access an AI agent has on a client's
  knowledge mirrors the access the user holds on the source systems.
- **Retention defined.** Each dataset has a published retention window;
  data is removed when the window closes or the contract ends.
- **Deletion on request.** Per the contract, clients can request deletion;
  we acknowledge within one business day and complete within the agreed
  SLA.

## What this means in practice

- We will not enrich a client dataset from external sources without their
  written approval and lawful basis.
- We will not share one client's data with another, ever.
- We log every data access and surface anomalies in the AI Control Tower.
- We label sensitivity on every dataset; agents honor the label.

## Trust evidence

- Data Processing Agreement: `docs/DPA_DEALIX_FULL.md`.
- Retention policy: `docs/DATA_RETENTION_POLICY.md`.
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`.
- Arabic trust pack: `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md`.

## Anti-patterns we publicly refuse

- Silent enrichment from unknown sources.
- Cross-tenant data reuse.
- Indefinite retention "in case we need it later."
- Opaque audit logs.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client agreement | Approved sources list | Compliance | Per engagement |
| Data inventory | Sensitivity labels | Data steward | Continuous |
| Deletion request | Confirmation + evidence | Compliance | Per request |
| Audit trail | Anomaly alert | Control Tower | Continuous |

## Metrics
- Approval Coverage — % of datasets with documented approval.
- PII Redaction Rate — % of external outputs with PII redacted as required.
- Deletion SLA Adherence — % of requests completed on time.
- Cross-Tenant Incidents — must remain zero.

## Related
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — business trust pack
- `docs/DPA_DEALIX_FULL.md` — data processing agreement
- `docs/DATA_RETENTION_POLICY.md` — retention rules
- `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md` — Arabic trust pack
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
