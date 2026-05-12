# RAG architecture — Dealix knowledge layer

Per-tenant retrieval-augmented generation. Every paying customer can
upload their own playbooks, contracts, sector data, and have the
Dealix agents answer *from those* instead of the open web.

## Pipeline

```
  Document (URL / upload / crawl)
        │
        ▼
   chunk + clean   (dealix.rag.ingest.split — LlamaIndex when installed,
                    naive recursive splitter otherwise)
        │
        ▼
   embed           (dealix.rag.embeddings.embed —
                    Voyage v3 → Cohere multilingual v3 → OpenAI 3-small)
        │
        ▼
   write           (knowledge_documents + knowledge_chunks tables;
                    pgvector `embedding` column on Postgres)
        │
        ▼
   query           (cosine `<=>` ORDER BY top-25 candidate pool)
        │
        ▼
   rerank          (Cohere Rerank multilingual v3 → top-5)
        │
        ▼
   inject into prompt  (proposal agent, qualification agent, etc.)
```

## Tables

| Table | Owner | Purpose |
| --- | --- | --- |
| `knowledge_documents` | tenant | One row per ingested source. |
| `knowledge_chunks` | tenant | One row per chunk; 1024-dim pgvector embedding. |

Index: HNSW on `embedding vector_cosine_ops` — sub-millisecond at our scale.

## Evaluation

Use **Ragas** to evaluate the retrieval + generation:

```bash
python -m dealix.agents.optimise.run --metric ragas_faithfulness
```

`evals/datasets/ragas_*.jsonl` contains the labelled (question,
context, answer) tuples; each PR that touches `dealix.rag.*` must
keep the score within 5% of the baseline (gated by
`.github/workflows/llm_evals.yml`).

## PDPL alignment

Documents inherit the tenant's DPA. `DELETE /api/v1/knowledge/{id}`
hard-deletes chunks and soft-deletes the document row. The PDPL DSR
deletion path cascades: when a tenant requests deletion via
`/api/v1/pdpl/dsr/delete`, the DPO-approved follow-up runs the same
cascade against the tenant's entire knowledge base.

## Cost guardrails

Embedding cost lands in `llm_calls` via the standard cost tracker; the
per-tenant day cap from `core/llm/cost_guard.py` enforces a ceiling so
a runaway ingest doesn't blow the budget. Default $25/tenant/day still
applies.

## What's pending vendor signup

- Voyage AI account → `VOYAGE_API_KEY`.
- Cohere account → `COHERE_API_KEY` (covers both embed + rerank).
- LlamaIndex is a Python lib only — no vendor account.

Without any of those keys the embed chain still tries OpenAI, then
returns `provider="none"` and the ingest endpoint persists the doc
with `status="failed"`. Customers see the failure in the FE so they
know we couldn't index yet.
