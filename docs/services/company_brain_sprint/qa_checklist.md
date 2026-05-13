# QA Checklist — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer (independent)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [qa_checklist_AR.md](./qa_checklist_AR.md)

## Context
Quality gates the Sprint must clear at the end of Week 3 (Round 1) and Week 4 (Round 2). The QA Reviewer must not have produced the deliverables. The protocol enforces `docs/quality/QUALITY_STANDARD_V1.md` and the governance regime in `docs/governance/AI_INFORMATION_GOVERNANCE.md`. It connects to the strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## How To Use
1. Open the sprint Notion record.
2. Walk every gate; mark Pass / Fail / N/A + evidence pointer.
3. Failures create same-day fix tickets.
4. Round is "passed" when all gates are Pass or N/A.

## Gate 1 — Every Answer Has a Source or Insufficient-Evidence
- [ ] 100% of test answers include at least one citation from the retrieved corpus, OR the assistant returns "insufficient evidence".
- [ ] No mid-answer fabricated citation.
- [ ] Citations point to specific, retrievable chunks (not generic links).

## Gate 2 — Access Mirrored to User Permissions
- [ ] Group A test user cannot retrieve a Group-B-only document.
- [ ] Group B test user cannot retrieve a Group-A-only document.
- [ ] Restricted documents never appear in non-restricted answers.
- [ ] Permission rules are versioned and logged.

## Gate 3 — Freshness Policy Applied
- [ ] Each source has a `freshness_window`.
- [ ] When an answer is older than the window, the assistant flags it ("Source dated <DATE>; please verify with the owner").
- [ ] Outdated sources are queued for re-ingestion in the upsell motion.

## Gate 4 — Sensitive Sources Gated
- [ ] Sensitive sources isolated to their own index partition.
- [ ] Sensitive answers carry a watermark in the response.
- [ ] Sensitive-source retrieval logged for audit.

## Gate 5 — No Hallucinated Citations
- [ ] Sample of 50 answers reviewed: no answer cites a source that wasn't retrieved.
- [ ] Citation linker resolves to a real chunk for every cite.
- [ ] Test queries with no good source return "insufficient evidence".

## Gate 6 — Governance Log Written
- [ ] Every query + response logged with timestamp, user group, retrieved sources, citation list.
- [ ] Log retained per `DATA_RETENTION_POLICY`.
- [ ] Sensitive data redacted from the log per `AI_INFORMATION_GOVERNANCE`.

## Gate 7 — Source Registry Complete
- [ ] Every ingested document has a source registry entry.
- [ ] Entries have owner, allowed-use, sensitivity, retention.
- [ ] Source registry diff against ingestion list = empty.

## Gate 8 — Knowledge Quality Report Delivered
- [ ] Coverage map produced (which topics are well-covered, which are thin).
- [ ] Gap list with suggested ingestions.
- [ ] At least 20 test questions logged with verdicts (good answer / insufficient / wrong source).

## Gate 9 — Proof Pack Complete
- [ ] All required events present.
- [ ] Each event has timestamp, actor, value.
- [ ] Pack signed by DL + QA + GR + KO.

## Gate 10 — DPA / PDPL / Cross-Border
- [ ] Signed acknowledgement on file.
- [ ] Cross-border posture matches `CROSS_BORDER_TRANSFER_ADDENDUM`.
- [ ] Retention matches `DATA_RETENTION_POLICY`.

## Escalation
- 3+ gate failures → escalate to capability owner.
- Gate 2 failure → engagement paused; redo access model.
- Gate 5 failure → hallucinated-citation root cause hunted before delivery.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Week 3 deliverables | Round 1 result | QA | End of Week 3 |
| Week 4 deliverables | Round 2 result | QA | End of Week 4 |
| Fix tickets | Resolutions | DL + KE | Same day |

## Metrics
- **First-time pass rate** — Target ≥ 65%.
- **Gate failures per Sprint** — Target ≤ 3.
- **Hallucinated citations** — Target = 0.
- **Access-control failures** — Target = 0.

## Related
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/capabilities/knowledge_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/governance/AI_INFORMATION_GOVERNANCE.md` — governance
- `docs/ledgers/SOURCE_REGISTRY.md` — source registry
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — routing
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
