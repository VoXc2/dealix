# Prompt Registry

> Every prompt that ships in a Dealix workflow is a versioned, owned, evaluated artifact.
> No prompt reaches a customer-facing output without a row in this registry.
> Phase 2 wires the registry into LiteLLM (model abstraction) and Langfuse (versioning + traces).

## Why a registry

Free-text prompts buried in code rot fast: nobody knows which version produced which output, which eval covers it, what it must never say. The Prompt Registry treats every prompt as a first-class governed asset — like a database migration or a policy rule.

## Required fields (per prompt)

| Field | Required | Notes |
|-------|:--------:|-------|
| Name | Yes | `service.agent.purpose` form, e.g. `lead_intel.revenue.score_account` |
| Version | Yes | Semver-style `vMAJOR.MINOR` (e.g. `v1.3`) — MAJOR breaks I/O schema |
| Service | Yes | Lead Intelligence / Company Brain / AI Quick Win / Support Desk / Governance Program |
| Agent | Yes | One of the 10 named agents in `AI_AGENT_INVENTORY.md` |
| Purpose | Yes | One-sentence intent |
| Owner | Yes | Named role (HoData / HoP / CRO / HoLegal / HoCS) |
| Eval test ref | Yes | ID in `EVALUATION_REGISTRY.md` (e.g. `EVL-LIS-001`) |
| Input schema | Yes | Pydantic model name in `auto_client_acquisition/*` |
| Output schema | Yes | Pydantic model name; unstructured text not allowed |
| Forbidden behavior | Yes | What this prompt must never produce — references `dealix/trust/forbidden_claims.py` patterns |
| Model class | Yes | classification / balanced / high-stakes / compliance / RAG (see `MODEL_PORTFOLIO.md`) |
| Last review date | Yes | Quarterly review minimum |
| Status | Yes | Draft / Beta / MVP / Production / Deprecated |

## Catalog (Phase-1 seeds)

| Name | Version | Service | Agent | Owner | Eval | Output schema | Status |
|------|:-------:|---------|-------|-------|------|---------------|--------|
| `lead_intel.revenue.score_account` | v1.0 | Lead Intelligence | RevenueAgent | CRO | EVL-LIS-001 | `LeadScore` | MVP |
| `lead_intel.outreach.draft_ar_en` | v1.0 | Lead Intelligence | OutreachAgent | HoCS | EVL-LIS-002 | `OutreachDraft` | MVP |
| `lead_intel.data.import_preview` | v1.0 | Lead Intelligence | DataQualityAgent | HoData | EVL-LIS-003 | `ImportPreview` | MVP |
| `brain.knowledge.cited_answer` | v0.9 | Company Brain | KnowledgeAgent | HoP | EVL-BRN-001 | `Answer` (with citation) | Beta |
| `support.triage.classify` | v0.5 | AI Support Desk | SupportAgent | HoCS | EVL-SUP-001 | `Triage` | Designed |
| `governance.guard.claim_filter` | v1.0 | All | ComplianceGuardAgent | HoLegal | EVL-GOV-001 | `GuardDecision` | MVP |
| `reporting.exec.proof_pack` | v1.0 | All | ReportingAgent | HoP | EVL-REP-001 | `ProofPack` | MVP |
| `reporting.exec.executive_report` | v1.0 | All | ReportingAgent | HoP | EVL-REP-002 | `ExecutiveReport` | MVP |
| `qw.diagnostic.findings` | v0.8 | AI Quick Win | StrategyAgent | CRO | EVL-QWN-001 | `Diagnostic` | Beta |

## Hard rules

- No prompt in production without (Owner + Eval test ref + Output schema + Status = MVP/Production).
- Any change to the prompt body bumps `MINOR`; any change to I/O schema bumps `MAJOR`.
- Every customer-facing AI run records the prompt name + version it used (per `docs/ledgers/AI_RUN_LEDGER.md`).
- Prompts that operate on PII must reference `dealix/trust/pii_detector.py` redaction in their `Forbidden behavior` field.

## Phase 2 wiring

- **LiteLLM** — model abstraction so prompt versions are not coupled to a specific provider; routing per `MODEL_PORTFOLIO.md`.
- **Langfuse** — prompt versioning store, traces per run, eval score correlation.
- **Storage**: `auto_client_acquisition/ai_workforce/prompts/` (YAML/JSON files) backed by Langfuse for runtime resolution.

## Cross-links

- `/home/user/dealix/docs/product/AI_AGENT_INVENTORY.md`
- `/home/user/dealix/docs/product/AI_WORKFORCE_OPERATING_MODEL.md`
- `/home/user/dealix/docs/product/EVALUATION_REGISTRY.md`
- `/home/user/dealix/docs/product/MODEL_PORTFOLIO.md`
- `/home/user/dealix/docs/ledgers/AI_RUN_LEDGER.md`
- `/home/user/dealix/dealix/trust/forbidden_claims.py`
- `/home/user/dealix/auto_client_acquisition/ai_workforce/` (Phase 2 home)
