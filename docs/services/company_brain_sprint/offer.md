# Offer — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Knowledge Capability Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [offer_AR.md](./offer_AR.md)

## Context
This file defines the public-facing promise of the **Company Brain Sprint**, the knowledge-tier service on the Dealix ladder. It exists because every growing company drowns in scattered documents — Notion pages, PDFs in drives, Slack threads, policy memos in inboxes — and there is no source-cited way to ask "what is our policy on X?". The Sprint plugs into the strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and the information governance regime in `docs/governance/AI_INFORMATION_GOVERNANCE.md`. It is the productized expression of the knowledge capability in `docs/capabilities/knowledge_capability.md`.

## Promise
> Turn scattered company knowledge into a **source-cited internal assistant** in **3–4 weeks** — with built-in "insufficient evidence" mode so it never makes up an answer.

The Sprint replaces the "I'll get back to you on that" sales motion and the "where's the policy?" Slack thread with a single, governed, citation-bearing answer surface.

## The Problem We Solve
- Documents are scattered across Notion, Drive, SharePoint, and inboxes.
- New hires take weeks to learn what's where.
- Sales answers vary by who you ask.
- Policies get re-explained instead of consulted.
- Existing search returns 100 results when you need one.

The Sprint compresses this into a 3–4 week build of a curated, governed assistant that answers from approved documents with citations.

## Deliverables
1. **Document inventory** — every document Dealix touches is logged with owner, sensitivity, freshness, and use scope.
2. **Source registry** — formal registry per `docs/ledgers/SOURCE_REGISTRY.md`: source name, owner, allowed use, retention.
3. **RAG-style Q&A** — assistant that retrieves and cites from approved documents only.
4. **Insufficient-evidence mode** — when retrieval doesn't yield a confident source, the assistant says "insufficient evidence" instead of hallucinating.
5. **Access rules** — each user/group sees only the documents they are allowed to see; the assistant mirrors those rules.
6. **Knowledge quality report** — coverage, gaps, suggested next ingestions.
7. **Proof report** — executive-ready narrative with citation samples.
8. **Proof pack** — events log, governance log, anonymization rules.

All deliverables under `QUALITY_STANDARD_V1` and shipped with a `PROOF_PACK_TEMPLATE` instance.

## What's NOT Included
- **Public-facing chatbot.** Internal users only.
- **Customer support inbox automation.** That's the AI Support Desk Sprint.
- **Replacement** of existing systems (Notion, Drive, SharePoint).
- **Migration** of documents to a new platform.
- **Translation** of documents (we index in their existing language).
- **Pen-test or security certification.**
- **Long-term operation** beyond the Sprint. Continuation is **Monthly Brain Management**.
- **Custom model training.**

## Buyer Profile
- B2B company in KSA/GCC with 20–500 employees.
- 50–200 documents in scope for the Sprint.
- Defined user groups (sales, ops, finance, policy, etc.).
- A named knowledge owner (often Chief of Staff, Head of Operations, or Knowledge Manager).
- Willingness to tag documents for sensitivity.

## Why It Sells
- **3–4 weeks visible.** Short enough to fit a quarterly initiative.
- **Citation-bearing.** Every answer points to a real source — no hallucinated references.
- **Governance-first.** Access rules mirrored from existing systems; nothing leaks.
- **Bridge to retainer.** Every Sprint upsells into Monthly Brain Management or dedicated assistants (Sales Knowledge Assistant, Policy Assistant).

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Document inventory list | Approved corpus | Knowledge Owner + Analyst | Week 1 |
| Owner contacts | Source registry | Knowledge Owner + Analyst | Week 1 |
| Sensitivity tags | Access rules | Security/IT + Analyst | Week 2 |
| User-group definitions | Permission model | Sponsor + Analyst | Week 2 |
| Tuning feedback | Citation-bearing assistant | Knowledge Owner + DL | Week 3–4 |

## Metrics
- **Sprint completion rate** — `% sprints delivered within 4 weeks`. Target ≥ 95%.
- **Citation rate** — `% answers with at least one valid source`. Target ≥ 95%.
- **Insufficient-evidence usage** — `% queries where the assistant declines vs. hallucinates`. Target = 100% when no valid source exists.
- **Hallucinated citations** — `count`. Target = 0.
- **Upsell rate** — `% sprints converted within 60 days`. Target ≥ 40%.

## Related
- `docs/capabilities/knowledge_capability.md` — capability blueprint behind this service
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map placement
- `docs/governance/AI_INFORMATION_GOVERNANCE.md` — information governance regime
- `docs/ledgers/SOURCE_REGISTRY.md` — source registry standard
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — model routing decisions
- `docs/AI_STACK_DECISIONS.md` — approved AI stack
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
