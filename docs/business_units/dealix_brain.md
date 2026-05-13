# Dealix Brain — Business Unit

**Layer:** Holding · Compound Holding Model
**Owner:** Dealix Brain GM
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [dealix_brain_AR.md](./dealix_brain_AR.md)

## Context
Dealix Brain is the Business Unit that turns a company's knowledge — its policies, manuals, contracts, decks, FAQs, sector docs — into **source-cited answers** for employees, customers, and partners. Brain is the BU that makes "ask the company" a real, governed, auditable capability. It sits in the BU layer of [`docs/holding/DEALIX_HOLDING_OS.md`](../holding/DEALIX_HOLDING_OS.md), is paired with `docs/capabilities/knowledge_capability.md`, and grounds its retrieval stack in `docs/EMBEDDINGS_PIPELINE.md`.

## Function
Brain ingests, classifies, and indexes the customer's knowledge base; routes questions through the LLM Gateway with the right policy and prompt; returns answers with citations; surfaces gaps where evidence is missing; and runs a freshness monitor that flags stale or contradictory sources.

## Services offered

| Service | Duration | Outcome |
|---|---|---|
| Company Brain Sprint | 3–6 weeks | First 200–2,000 docs indexed; cited Q&A live |
| Sales Knowledge Assistant | 2–4 weeks | Salesperson Q&A with playbook citations |
| Policy Assistant | 2–4 weeks | Policy / HR / compliance Q&A with audit log |
| Monthly Brain Management (retainer) | Ongoing | Ingestion, freshness, evals, gap reporting |

## Product modules (in Core OS)

| Module | Function |
|---|---|
| Source Registry | Doc-by-doc inventory with owner, version, expiry |
| Answer with Citations | RAG response with inline source references |
| Knowledge Gaps | Auto-detected questions with insufficient evidence |
| Freshness Monitor | Alerts on stale, contradictory, or expiring sources |

## KPIs

- **Documents indexed.**
- **Answers with sources** — % responses returning ≥ 1 valid citation.
- **Insufficient-evidence rate** — % responses flagged as "not enough sources".
- **Search-time reduction** — minutes saved per question.
- **Freshness compliance** — % of sources within freshness window.
- **Source coverage** — % of customer-defined critical doc set indexed.

## Core OS dependencies

| OS module | How Brain consumes it |
|---|---|
| Data OS | Source Registry, PII tagging, retention controls |
| LLM Gateway | RAG inference, prompt registry, evals |
| Governance Runtime | Per-doc access policies + audit log of every query |
| Proof Ledger | Brain Proof Pack: search-time saved, audit count |
| Capital Ledger | Sector knowledge graphs, reusable embedding configs |
| AI Control Tower | Cost per answer, eval pass rate, citation accuracy |

## Owner

| Role | Responsibility |
|---|---|
| Brain BU GM | P&L, service ladder, retainer pull-through |
| Brain Delivery Lead | Ingestion + sprint QA |
| Brain CSM | Adoption + freshness retention |
| Knowledge Product Owner | Module backlog into Core OS |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Customer doc set | Indexed Source Registry | Brain Delivery | Per sprint |
| User queries | Cited answers + telemetry | LLM Gateway | Realtime |
| Detected gaps | Gap report to customer | Brain CSM | Weekly |
| Stale alerts | Refresh tasks | Brain CSM | Daily |

## Metrics
- **MRR (Brain BU).**
- **Gross margin.**
- **Citation accuracy** — % cited answers where citations support the claim (sampled).
- **Eval pass rate** — % prompts in Brain prompt registry passing thresholds.
- **Daily active queries.**

## Related
- `docs/capabilities/knowledge_capability.md` — capability spec for this BU.
- `docs/EMBEDDINGS_PIPELINE.md` — retrieval stack.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval framework.
- `docs/COMPANY_SERVICE_LADDER.md` — group service ladder.
- `docs/holding/DEALIX_HOLDING_OS.md` — umbrella holding model.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
