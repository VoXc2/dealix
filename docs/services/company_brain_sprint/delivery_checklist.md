# Delivery Checklist — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Lead — Knowledge
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [delivery_checklist_AR.md](./delivery_checklist_AR.md)

## Context
Week-by-week operational script for the 3–4 week Company Brain Sprint. Every Sprint must be reproducible and auditable per `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, the governance regime in `docs/governance/AI_INFORMATION_GOVERNANCE.md`, and the quality standard in `docs/quality/QUALITY_STANDARD_V1.md`. Each checkbox maps to a proof pack event.

## Roles
- **Delivery Lead (DL)** — single accountable.
- **Knowledge Engineer (KE)** — ingestion, indexing, retrieval tuning.
- **Governance Reviewer (GR)** — sensitivity, access, lawful basis.
- **Knowledge Owner (KO)** — client-side single point of contact.
- **QA Reviewer (QA)** — independent reviewer.
- **Sponsor (SP)** — final acceptance.

## Week-by-Week Plan

### T-5 to T-1 — Pre-kickoff
- [ ] Welcome email sent with shared folder, intake summary, Week 1 agenda. (DL)
- [ ] Internal Sprint board created in Notion. (DL)
- [ ] Premium re-validated against intake. (DL + Margin Controller)
- [ ] Proof pack initialized with `sprint_initialized`. (DL)

### Week 1 — Source Registry + Ingestion
- [ ] Kickoff call (60 min) with SP and KO. (DL)
- [ ] Document inventory list received. (KO + KE)
- [ ] Source registry built per `docs/ledgers/SOURCE_REGISTRY.md`. (KE + GR)
- [ ] Each source has: owner, allowed-use, sensitivity, retention. (GR)
- [ ] Ingestion started; raw text extracted from each document. (KE)
- [ ] Encrypted vault placement for sensitive sources. (GR + KE)
- [ ] Proof events: `documents_indexed = N`, `source_registry_complete`. (KE)

### Week 2 — Index + Retrieval Tuning
- [ ] Chunking strategy chosen per document type. (KE)
- [ ] Embeddings generated per `AI_MODEL_ROUTING_STRATEGY.md`. (KE)
- [ ] Initial retrieval tests run with KO's sample questions. (KE + KO)
- [ ] Retrieval tuned: chunk size, top-k, similarity threshold. (KE)
- [ ] Permission model implemented per group definitions. (GR + KE)
- [ ] Proof event: `index_tuned`. (KE)

### Week 3 — RAG + Citation + Insufficient-Evidence
- [ ] Prompt template enforcing source citation written. (KE)
- [ ] Insufficient-evidence path implemented: when retrieval scores below threshold, the assistant says "insufficient evidence". (KE)
- [ ] No-hallucinated-citation check: assistant only cites sources actually retrieved. (KE + QA)
- [ ] KO walks through 30 test questions. (KO)
- [ ] Errors logged and addressed. (KE)
- [ ] Proof events: `answers_with_sources = N`, `insufficient_evidence_responses = N`. (KE)

### Week 4 — Access Control + QA + Handoff
- [ ] User groups onboarded. (GR + KO)
- [ ] Permission test: each group can see only allowed documents. (GR + QA)
- [ ] Audit log captures who-asked-what-and-got-what. (KE)
- [ ] Knowledge quality report drafted: coverage, gaps, suggested next ingestions. (DL)
- [ ] Proof report drafted. (DL)
- [ ] Sensitive-field anonymization verified. (QA)
- [ ] Final QA pass. (QA)
- [ ] Handoff call (90 min) with SP, KO, and group leads. (DL)
- [ ] SP signs handoff note. (SP)
- [ ] Proof events: `blocked_unauthorized_accesses = N`, `sprint_delivered`. (DL)
- [ ] Upsell motion triggered. (DL + CSM)

## Cross-Cutting Controls
- Proof pack continuously updated.
- Sensitive content never moved off the encrypted vault.
- Audit log retained per `DATA_RETENTION_POLICY`.
- No deliverable ships without QA + GR sign-off.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed SOW + intake | Sprint board | DL | T-5 |
| Weekly review | Sprint board updates | DL | Weekly |
| QA + GR results | Fix tickets or signoff | QA + GR + DL | End of each week |
| Final assistant + report | Handoff | DL + SP | Week 4 |

## Metrics
- **On-time delivery** — Target ≥ 90%.
- **Hallucinated citations** — Target = 0.
- **Access-control failures** — Target = 0.
- **Permission test pass** — Target = 100%.

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
- `docs/V14_FOUNDER_DAILY_OPS.md` — operating loop
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
