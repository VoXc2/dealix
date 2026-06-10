# Dealix Knowledge Graph (concept)

Over time, Dealix encodes **relationships** between sectors, problems, services, and controls—today as docs; later as data for recommendations.

## Core relationships

```text
Sector has Problems.
Problems map to Services.
Services require Inputs.
Services produce Outputs.
Outputs map to KPIs.
KPIs create Proof.
Risks require Governance Controls.
Repeated patterns become Playbooks.
```

## Example

```text
B2B Services
→ messy leads / no source attribution
→ Lead Intelligence Sprint
→ CSV / CRM export (client-provided)
→ top 50 accounts + drafts + hygiene report
→ pipeline clarity; qualified-account focus
→ consent / source / outreach risk
→ docs/playbooks/b2b_services.md + GOVERNANCE_LEDGER
```

**Maps:** [`SERVICE_KPI_MAP.md`](../company/SERVICE_KPI_MAP.md), [`PROOF_TO_UPSELL_MAP.md`](../growth/PROOF_TO_UPSELL_MAP.md), [`../playbooks/README.md`](../playbooks/README.md).

**Future:** graph-backed “next best sprint” inside the product—same edges as [`OFFER_ARCHITECTURE.md`](../company/OFFER_ARCHITECTURE.md).
