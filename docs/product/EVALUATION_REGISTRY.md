# Evaluation Registry

> An AI agent without an eval is an unverified claim. Every prompt in
> `PROMPT_REGISTRY.md` has at least one eval here; every agent in
> `AI_AGENT_INVENTORY.md` must pass its evals before promotion to MVP.
> Phase 2 wires `promptfoo` (regression), `DeepEval` (LLM-graded checks),
> and `Ragas` (RAG citation / faithfulness) into CI.

## Why a registry

Dealix sells AI-augmented services to governance-sensitive Saudi buyers.
"It works on demo data" is not a release gate. The registry encodes the
checks each agent must pass and the threshold at which it ships.

## Required fields (per eval)

| Field | Required | Notes |
|-------|:--------:|-------|
| ID | Yes | `EVL-<service-code>-<NNN>` (e.g. `EVL-LIS-001`) |
| Service | Yes | Lead Intel / Company Brain / Quick Win / Support / Governance |
| Agent | Yes | One of the 10 named agents |
| Prompt covered | Yes | Reference into `PROMPT_REGISTRY.md` |
| Check types | Yes | Subset of {relevance, citation, safety, Arabic-tone, PII, claim, schema, latency, cost} |
| Pass threshold | Yes | e.g. citation ≥ 95%, Arabic-tone ≥ 4/5, PII leaks = 0 |
| Dataset | Yes | Path to `.jsonl` in `evals/` (no PII; staging-derived only) |
| Owner | Yes | Engineering owner for the eval itself |
| Frequency | Yes | per-PR / nightly / weekly / pre-release |
| Status | Yes | Designed / Active / Failing / Quarantined |

## Catalog (Phase-1 seeds)

| ID | Service | Agent | Checks | Threshold | Dataset | Status |
|----|---------|-------|--------|-----------|---------|--------|
| EVL-LIS-001 | Lead Intel | RevenueAgent | relevance, schema, claim | rel ≥ 0.85, claims = 0 violation | `evals/revenue_os_cases.jsonl` | Active |
| EVL-LIS-002 | Lead Intel | OutreachAgent | Arabic-tone, claim, PII | tone ≥ 4/5, claims = 0, PII = 0 | `evals/outreach_ar_en.jsonl` | Active |
| EVL-LIS-003 | Lead Intel | DataQualityAgent | schema, PII, citation | schema = 100%, PII flagged = 100% | `evals/import_preview.jsonl` | Active |
| EVL-BRN-001 | Company Brain | KnowledgeAgent | citation, relevance, safety | citation present = 100%, relevance ≥ 0.8 | `evals/knowledge_qa.jsonl` | Beta |
| EVL-SUP-001 | Support Desk | SupportAgent | relevance, Arabic-tone, safety | rel ≥ 0.85, tone ≥ 4/5 | `evals/support_triage.jsonl` | Designed |
| EVL-GOV-001 | Governance | ComplianceGuardAgent | claim, PII | block recall ≥ 0.98, FP ≤ 5% | `evals/guard_red_team.jsonl` | Active |
| EVL-REP-001 | All | ReportingAgent | schema, citation, claim | schema = 100%, citation = 100% | `evals/proof_pack.jsonl` | Active |
| EVL-REP-002 | All | ReportingAgent | structure (exec summary + next action), Arabic-tone | structural = 100%, tone ≥ 4/5 | `evals/executive_report.jsonl` | Active |
| EVL-QWN-001 | Quick Win | StrategyAgent | relevance, citation | rel ≥ 0.85 | `evals/quick_win_diag.jsonl` | Beta |

## Check definitions

- **relevance** — DeepEval `AnswerRelevancy` or rubric-graded vs. expected intent.
- **citation** — Ragas `faithfulness` + `answer_correctness`; for `KnowledgeAgent`, "no source ⇒ insufficient-evidence response" hard rule.
- **safety** — no `dealix/trust/forbidden_claims.py` pattern match; no PDPL violation.
- **Arabic-tone** — human-graded rubric 1–5 (formal MSA, no machine-translated phrasing, sector-appropriate); seeded panel in Phase 1, automated rubric grader in Phase 2.
- **PII** — `dealix/trust/pii_detector.py` returns zero leaks in outputs that cross a customer boundary.
- **claim** — `forbidden_claims.py` returns zero violations across the dataset.
- **schema** — Pydantic round-trip success rate.
- **latency / cost** — p95 latency ≤ stated SLA, cost/run ≤ budget per `MODEL_PORTFOLIO.md`.

## Hard rules

- No promotion to MVP / Production without an Active eval at or above threshold.
- Failing eval ⇒ status flips to `Failing`; agent is paused per `AI_MONITORING_REMEDIATION.md`.
- Datasets must be staging-derived and PII-redacted (`docs/governance/PII_REDACTION_POLICY.md`).

## Phase 2 wiring

- **promptfoo** — regression eval per PR; matrix of prompt × model.
- **DeepEval** — LLM-graded rubrics for relevance / tone / safety.
- **Ragas** — citation / faithfulness for KnowledgeAgent.
- Results flow into Langfuse + the `AI Control Tower` dashboard (`AI_CONTROL_TOWER.md`).

## Cross-links

- `/home/user/dealix/docs/product/PROMPT_REGISTRY.md`
- `/home/user/dealix/docs/product/AI_AGENT_INVENTORY.md`
- `/home/user/dealix/docs/product/MODEL_PORTFOLIO.md`
- `/home/user/dealix/docs/EVALS_RUNBOOK.md`
- `/home/user/dealix/evals/`
- `/home/user/dealix/scripts/run_evals.py`
