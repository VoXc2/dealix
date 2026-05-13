# Data Request — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Analyst
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [data_request_AR.md](./data_request_AR.md)

## Context
Client-facing checklist of what Dealix needs before Week 1 of the Company Brain Sprint. This enforces the DPA in `docs/DPA_DEALIX_FULL.md`, the retention regime in `docs/ops/PDPL_RETENTION_POLICY.md`, and the information governance regime in `docs/governance/AI_INFORMATION_GOVERNANCE.md`.

## Summary
Client provides:
1. **Document export** (the corpus) — 50–200 documents.
2. **Owner contacts** — owner per source.
3. **Sensitivity classifications** — per source or per document.
4. **User group definitions** — names + permission mappings.
5. **Allowed-use statement** — per source.
6. **Signed data handling acknowledgement.**

Time budget: **≤ 3 business days**.

## Item 1 — Document Export

### Acceptable Formats
- PDF, DOCX, MD, TXT, HTML.
- Notion page exports (MD or HTML).
- Drive shared folder with read-only access.
- SharePoint export.

### Naming
- Filenames should hint at content (`pricing_policy_v3.pdf`).
- Each document keeps its origin tag (source system + original path).

### What We'll Do
- Profile, chunk, embed, index.
- Build retrieval over approved documents only.
- Apply access rules.

### What We Will NOT Do
- Train a public AI model on it.
- Share with any third party.
- Retain past the retention policy.
- Process outside the agreed jurisdiction.

## Item 2 — Owner Contacts

Per source (or per document if more granular):
- Owner name, role, corporate email.
- Backup contact.

## Item 3 — Sensitivity Classifications

### Three Levels
- **Public** — fine to share broadly.
- **Internal** — internal employees only.
- **Restricted** — limited group only (defined in user_groups).

### Optional Sub-Tags
- `PDPL` — personal data present.
- `Finance` — financial figures.
- `Health` — health-related.
- `Government` — government engagement.
- `Customer-PII` — customer personal data.

## Item 4 — User Group Definitions

For each group (up to 3 in this Sprint):
- Group name.
- Members (named or "all of department X").
- Documents they may see (by tag or by list).
- Documents they may NOT see.

## Item 5 — Allowed-Use Statement

Per source, a 1-line statement: "for internal Q&A", "not to be quoted to external vendors", etc.

## Item 6 — Signed Data Handling Acknowledgement

Auto-generated from intake. Sponsor signs electronically. Confirms:
- Lawful basis for the corpus.
- Agreement to `docs/DPA_DEALIX_FULL.md`.
- Cross-border posture per `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.
- Retention per `docs/ops/PDPL_RETENTION_POLICY.md`.

## Sensitive Data Handling
If intake flagged sensitivity:
- All transfers encrypted in transit; all storage encrypted at rest.
- Two-person delivery team only.
- Sensitive sub-tags drive index-level isolation.
- Proof pack anonymizes sensitive fields automatically.
- Retention reduced to project + 30 days.

## Delivery Method
- Preferred: encrypted shared folder (Drive/OneDrive) with named access for the Dealix delivery team only.
- SFTP available on request.
- Not acceptable: WhatsApp file send, public link, personal email attachment unencrypted.

## SLA
- Client uploads expected within **3 business days** of kickoff.
- Per business day of delay, Sprint slips by 1 day.
- After 5 business days of delay, restart fee SAR 2,500.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Welcome email | Drop folder ready | Dealix Ops | T-1 |
| Client upload | Receipt + integrity check | Dealix Analyst | Week 1 |
| Sensitivity tags | Index isolation | Dealix QA + Analyst | Week 1 |
| Group definitions | Access rules | Sec/IT + Analyst | Week 2 |

## Metrics
- **On-time data provision** — Target ≥ 80%.
- **Sensitivity tag coverage** — `% documents with a sensitivity tag at indexing`. Target = 100%.
- **Lawful-basis acknowledgement** — Target = 100%.

## Related
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention
- `docs/governance/AI_INFORMATION_GOVERNANCE.md` — governance
- `docs/ledgers/SOURCE_REGISTRY.md` — source registry
- `docs/capabilities/knowledge_capability.md` — capability blueprint
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
