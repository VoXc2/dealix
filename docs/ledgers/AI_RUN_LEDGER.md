# AI Run Ledger

> Every customer-facing AI output at Dealix is a logged **run**. A run that
> isn't logged didn't ship. Phase-1 is a markdown / spreadsheet ledger
> with the table template below; Phase-2 backs it with the event store
> (`auto_client_acquisition/revenue_memory/event_store.py`) and surfaces
> it in the AI Control Tower (`AI_CONTROL_TOWER.md`).

## The hard rule

```
Every customer-facing AI output is an AI Run with:
  1. Prompt version (from PROMPT_REGISTRY.md)
  2. Output schema (Pydantic model name)
  3. Redaction status (clean / redacted / blocked)
  4. QA score (1–5 or eval pass)
  5. Risk class (Low / Medium / High / Critical)
```

If any of the five is missing, the run is rejected by the runtime gate in
`dealix/trust/policy.py` and the output does not ship.

## Table template

| ID | Project | Task | Model | Prompt Version | Inputs Redacted | Output Schema | Cost (SAR) | QA Score | Risk |
|----|---------|------|-------|----------------|-----------------|---------------|-----------:|---------:|------|
| RUN-2026-XXXX | <customer code> | <workflow step> | <class:provider> | <name>@<vN.N> | yes / partial / no | <Pydantic model> | <SAR> | <1–5 or eval pass> | Low / Med / High |

## Worked example rows

| ID | Project | Task | Model | Prompt Version | Inputs Redacted | Output Schema | Cost (SAR) | QA Score | Risk |
|----|---------|------|-------|----------------|-----------------|---------------|-----------:|---------:|------|
| RUN-2026-0001 | LIS-AC01 | Account scoring batch | Sonnet:litellm | `lead_intel.revenue.score_account@v1.0` | yes | `LeadScore` | 12.40 | pass | Medium |
| RUN-2026-0002 | LIS-AC01 | Outreach draft (top-10) | Sonnet:litellm | `lead_intel.outreach.draft_ar_en@v1.0` | yes | `OutreachDraft` | 6.10 | 4.5/5 | High |
| RUN-2026-0003 | BRN-AC04 | Knowledge answer | Sonnet:litellm + retrieval | `brain.knowledge.cited_answer@v0.9` | yes | `Answer` | 0.85 | pass | High |
| RUN-2026-0004 | REP-AC01 | Executive report | Opus:litellm | `reporting.exec.executive_report@v1.0` | yes | `ExecutiveReport` | 4.20 | 4.7/5 | Medium |

## Required fields (per row)

| Field | Notes |
|-------|-------|
| ID | `RUN-YYYY-NNNN`; one per customer-facing artifact |
| Project | Engagement code (e.g. `LIS-AC01`) |
| Task | Workflow step from `WORKFLOW_REGISTRY.md` |
| Model | Class + concrete provider (per `MODEL_PORTFOLIO.md`) |
| Prompt Version | `<name>@<version>` from `PROMPT_REGISTRY.md` |
| Inputs Redacted | `yes` / `partial` / `no` (Public-class only) |
| Output Schema | Pydantic model name; no free text outputs |
| Cost (SAR) | From gateway; budgeted per `MODEL_PORTFOLIO.md` |
| QA Score | Eval pass/fail or rubric ≥ 4 for customer-facing |
| Risk | Workflow risk from `WORKFLOW_REGISTRY.md` |

## Optional fields

Governance decision (ALLOW / REDACT / BLOCK), named approver, eval IDs,
and source IDs that fed the run.

## How runs are generated

Workflow steps invoke the LLM gateway, which returns ID, model, cost, and
latency. The runtime appends prompt version, schema, redaction, QA, and
risk. Phase-1 stores rows in `docs/ledgers/runs/YYYY-MM/`. Phase-2 makes
each row an event in the event store; this markdown table becomes a
rendered view.

## Audit & retention

Rows are retained per `DATA_RETENTION_POLICY.md` (default 24 months).
Inputs (redacted) are linked, not embedded, to keep the ledger PII-free.
Friday Control Tower review samples runs across services for QA drift.

## Cross-links

- `/home/user/dealix/docs/product/PROMPT_REGISTRY.md`
- `/home/user/dealix/docs/product/MODEL_PORTFOLIO.md`
- `/home/user/dealix/docs/product/EVALUATION_REGISTRY.md`
- `/home/user/dealix/docs/product/WORKFLOW_REGISTRY.md`
- `/home/user/dealix/docs/product/AI_CONTROL_TOWER.md`
- `/home/user/dealix/docs/ledgers/SOURCE_REGISTRY.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/dealix/trust/policy.py`
- `/home/user/dealix/dealix/trust/audit.py`
- `/home/user/dealix/auto_client_acquisition/revenue_memory/event_store.py`
