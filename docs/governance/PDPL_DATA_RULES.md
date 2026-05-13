# PDPL Data Rules — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PDPL_DATA_RULES_AR.md](./PDPL_DATA_RULES_AR.md)

## Context
This file operationalizes the Saudi Personal Data Protection Law
(PDPL) for Dealix workflows. It complements the binding agreement in
`docs/DPA_DEALIX_FULL.md`, the retention rules in
`docs/DATA_RETENTION_POLICY.md`, the cross-border rules in
`docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`, the operational retention
runbook in `docs/ops/PDPL_RETENTION_POLICY.md`, and the breach response
in `docs/ops/PDPL_BREACH_RUNBOOK.md`. Together they define how Dealix
processes personal data, honors subject rights, and responds to
incidents.

## Scope
Applies to all personal data Dealix or its AI workforce processes on
behalf of a Saudi controller, including data ingested into the LLM
Gateway, the Company Brain, and any client tenant.

## Lawful Basis Registry
Each dataset must declare a lawful basis at intake. Approved bases:

| Code | Lawful basis | When used |
|---|---|---|
| LB-01 | Performance of a contract | Service delivery to a contracted client |
| LB-02 | Legal obligation | Tax, ZATCA, regulatory reporting |
| LB-03 | Consent | Marketing, public outreach |
| LB-04 | Legitimate interest | Internal analytics on existing relationships |
| LB-05 | Vital interest | Safety-critical incident handling |

The lawful basis is recorded against the dataset metadata and audited.
Datasets without a lawful basis are downgraded to `not_ready` per
`docs/data/DATA_READINESS_STANDARD.md`.

## Subject Rights Handling
Subjects may exercise the following rights. Dealix routes them via the
governance lead and logs the request in the audit ledger.

- **Access** — provide a copy of personal data within 30 days.
- **Correction** — correct inaccurate records within 14 days.
- **Deletion** — delete records within 30 days unless retention is
  required by law.
- **Restriction** — restrict processing pending dispute resolution.
- **Objection** — accept objection to legitimate-interest processing.

Each request produces a request record:

```json
{
  "subject_request_id": "SR-001",
  "subject_id_hash": "sha256:...",
  "right": "deletion",
  "received_at": "2026-05-13T09:00:00Z",
  "due_by": "2026-06-12T23:59:59Z",
  "status": "in_progress",
  "owner": "governance_lead"
}
```

## Consent Recording
Consent must be explicit, informed, and revocable. Each consent record
captures:

- subject identifier (hashed)
- purpose
- channel of consent (web form, signed document, recorded call)
- timestamp
- expiry (if applicable)
- revocation handle

Consent records are stored separately from operational datasets and
referenced by ID.

## Retention Defaults
| Data class | Default retention | Reference |
|---|---|---|
| Marketing consent | 24 months | `docs/DATA_RETENTION_POLICY.md` |
| Client business data | Contract term + 12 months | `docs/DPA_DEALIX_FULL.md` |
| Support messages | 24 months | `docs/ops/PDPL_RETENTION_POLICY.md` |
| Audit and governance logs | 36 months | `docs/ops/PDPL_RETENTION_POLICY.md` |
| AI Run Ledger | 36 months | `docs/AI_OBSERVABILITY_AND_EVALS.md` |
| Subject request records | 7 years | regulatory minimum |

Retention timers are enforced by the operational retention runbook.

## Cross-Border Transfer
Personal data is processed inside the Kingdom by default. Any transfer
outside KSA follows
`docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` and requires:

- a documented adequacy or contractual safeguard
- subject notice if required
- a logged transfer event

## Breach Response
On detection of a personal data breach, the governance lead activates
`docs/ops/PDPL_BREACH_RUNBOOK.md`. Required actions:

1. Contain — isolate affected systems within 1 hour.
2. Assess — classify severity and impacted subjects within 24 hours.
3. Notify — regulator and affected subjects per the runbook timeline.
4. Remediate — document root cause and remediation in the audit
   ledger.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Dataset intake | Lawful basis record | Governance lead | Per dataset |
| Subject request | Request record + response | Governance lead | Per request |
| Retention timer | Deletion or archive event | Backend lead | Daily |
| Breach detection | Activated breach runbook | Governance lead | Per incident |

## Metrics
- **Lawful basis coverage** — share of datasets with a lawful basis
  recorded. Target: 100%.
- **Subject request SLA** — share of requests fulfilled within their
  statutory due date. Target: 100%.
- **Retention compliance** — share of records older than retention
  default that are deleted. Target: 100% within 7 days of expiry.
- **Breach notification timeliness** — share of breaches notified
  within regulator-mandated windows. Target: 100%.

## Related
- `docs/DPA_DEALIX_FULL.md` — binding data processing agreement.
- `docs/DATA_RETENTION_POLICY.md` — retention policy.
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border addendum.
- `docs/ops/PDPL_RETENTION_POLICY.md` — operational retention runbook.
- `docs/ops/PDPL_BREACH_RUNBOOK.md` — breach response runbook.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
