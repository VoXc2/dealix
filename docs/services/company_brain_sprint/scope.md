# Scope — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Lead — Knowledge
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [scope_AR.md](./scope_AR.md)

## Context
The contractually binding scope of the Company Brain Sprint. The Sprint is medium-length and bounded to a specific document set — it must finish without sprawl. References `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` for strategic positioning and `docs/governance/AI_INFORMATION_GOVERNANCE.md` for the governance rules the Sprint must respect.

## Duration
- **15–20 business days** (3–4 calendar weeks) end-to-end.
- Kickoff within 5 business days of signed SOW + deposit.

## In Scope
1. **Document inventory** — up to 200 documents in this Sprint.
2. **Source registry** entries for each ingested source.
3. **Ingestion + indexing** using approved tools (`docs/AI_STACK_DECISIONS.md`).
4. **Retrieval tuning** — chunking, embeddings, similarity thresholds.
5. **RAG-style assistant** with citation-bearing answers.
6. **Insufficient-evidence mode** — explicit "I don't have enough source coverage to answer" path.
7. **Access control** — mirroring existing user-group permissions.
8. **Up to 3 user groups** with distinct access scopes (e.g., Sales / Ops / Policy).
9. **Knowledge quality report** with coverage map and gap list.
10. **Proof report** + **proof pack**.

## Not In Scope
- **More than 200 documents** in one Sprint. Larger corpora = scoped engagement or multiple Sprints.
- **Migration** of documents to a new platform.
- **Real-time sync** with source systems (we ingest a snapshot; sync is the Monthly Brain Management retainer).
- **Custom UI** beyond a basic chat interface or a Slack/Notion integration. Custom dashboards are out of scope.
- **Public-facing or customer-facing** assistant.
- **Translation** of documents to a new language.
- **Auto-update** of documents (the assistant reads; it does not write back).
- **Custom embedding-model training.**
- **Long-term operation.** Operation is **Monthly Brain Management**.

## Assumptions
1. The client provides **document exports** within 3 business days of kickoff.
2. Each document has (or can be tagged with) an **owner** and a **sensitivity** level.
3. The client defines **user groups** with current allowed-document mappings.
4. The client provides an **allowed-use statement** per source ("for internal use", "do not share with vendors", etc.).
5. The client agrees to the DPA (`docs/DPA_DEALIX_FULL.md`) and the cross-border posture (`docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`).
6. The client tolerates the "insufficient evidence" mode as a feature, not a bug.

## Dependencies
- Document inventory list delivered by end of Day 3.
- Sensitivity tags applied by end of Day 5 (collaborative effort).
- User-group definitions by end of Day 7.
- Reviewer feedback completed by Day 18.

## Change Control
- Document additions up to 25 above the agreed count → no fee.
- Beyond 25 additions → re-scope.
- Out-of-scope additions become a new SOW.

## Geography & Language
- Delivery in Arabic + English.
- Documents indexed in their native language.
- PDPL-aware. Cross-border per `CROSS_BORDER_TRANSFER_ADDENDUM`.

## Acceptance
The Sprint is accepted when:
1. The assistant is live with the documented corpus.
2. The knowledge quality report is delivered.
3. The sponsor signs the handoff note.

Auto-acceptance after 5 business days of silence.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed SOW + deposit | Kickoff schedule | Dealix Ops + Sponsor | T-5 days |
| Document inventory | Source registry | Knowledge Owner + Analyst | Week 1 |
| Sensitivity tags | Access rules | Sec/IT + Analyst | Week 2 |
| Tuning feedback | Citation-bearing assistant | Knowledge Owner + DL | Week 3–4 |
| Final QA pass | Handoff + proof | QA + Sponsor | Week 4 |

## Metrics
- **Scope-change request rate** — Target ≤ 20%.
- **On-time delivery** — Target ≥ 90%.
- **Hallucinated citations** — Target = 0.

## Related
- `docs/capabilities/knowledge_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/governance/AI_INFORMATION_GOVERNANCE.md` — governance regime
- `docs/ledgers/SOURCE_REGISTRY.md` — source registry standard
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — model routing
- `docs/AI_STACK_DECISIONS.md` — approved stack
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
