# MiniMax Implementation Report — 2026-06-12

> **Status:** Greenfield. First PR of the MiniMax-as-factory binding for Dealix.
> **Branch:** `feature/minimax-factory-p0-hardening`
> **Worktree:** `.worktrees/wt-minimax-p0`
> **Base:** `feature/dealix-v6-v10-scale-enterprise-os` @ `f8b4cbb`

## 1. What this PR does

Binds MiniMax as the high-volume daily generation provider for Dealix by:

1. Filling the two remaining P0 doc gaps (`ENV_CONTRACT.md`, `PRODUCTION_VERIFICATION_GUIDE.md`).
2. Introducing a single source of truth for LLM provider routing (`data/ai_ops/model_registry.yaml` + JSON schema).
3. Adding two Makefile targets that surface the factory to the founder: `minimax-status` and `minimax-evals`.
4. Writing the canonical read-only prompt set under `tasks/minimax/` (master + 6 sub-prompts).
5. Writing one operating guide (`docs/ai/MINIMAX_OPERATING_GUIDE.md`) and this status report.

**What this PR does not do:** rebuild any of the existing Business OS modules. The repo already ships them. This PR only binds them into a daily loop the founder can run in 90 minutes.

## 2. Provider health

| provider | api_key_set | default_model | evidence | approval_required | daily_cap_requests |
| --- | --- | --- | --- | --- | --- |
| minimax-text | yes (env) | MiniMax-Text-01 | L2 | yes | 5000 |
| anthropic-claude | no (env) | claude-sonnet-4-5 | L4 | yes | 500 |

Run `make minimax-status` to refresh.

## 3. Today's queue

No `reports/outreach/DRAFT_PRODUCTION_DAILY.md` snapshot writer exists in this PR. The founder runs `make minimax-status` to see the provider health, then `/ops/marketing` to see today's drafts in the approval queue.

## 4. Last 7-day eval delta

Eval harness (`make minimax-evals`) is wired in this PR. It runs in mock mode by default (no `MINIMAX_API_KEY` in env) and in live mode (capped at 5 calls) when a real key is set. The delta table is populated by a follow-up PR that adds eval history under `reports/evals/`.

## 5. Open items (next PRs, in priority order)

1. **Re-baseline OpenAPI** — `make openapi-export` to create `docs/architecture/openapi.json` baseline.
2. **Eval history writer** — `reports/evals/MINIMAX_EVAL_HISTORY.md` updated by `minimax-evals`.
3. **Outbound draft producer** — `scripts/minimax_draft_producer.py` that consumes `data/ai_ops/model_registry.yaml` and emits JSONL drafts to `reports/outreach/DRAFT_PRODUCTION_DAILY.md`.
4. **Media drafts catalog** — `data/ai_ops/media_drafts_catalog.yaml` from sub-prompt 06.
5. **WhatsApp + Portal maps** — `docs/whatsapp/WHATSAPP_AFTER_CONSENT_MAP_AR.md` and `docs/client_portal/SECURE_CLIENT_PORTAL_MAP_AR.md` from sub-prompt 04.
6. **Founder Super Control Room map** — `docs/ops/FOUNDER_SUPER_CONTROL_ROOM_MAP_AR.md` from sub-prompt 03.
7. **Revenue Execution chain map** — `docs/commercial/REVENUE_EXECUTION_CHAIN_AR.md` from sub-prompt 05.

## 6. Pre-existing observations (not addressed by this PR)

- `make security-smoke` exits non-zero on the current `main` due to placeholder `sk_live_*` strings in test fixtures and doc examples. The smoke is doing exactly what it should — flagging patterns that look like live secrets. The cleanup is a separate PR (`fix/security-smoke-fixture-placeholders`) and out of scope here.
- The OpenAPI contract check exits 0 but reports "baseline not found". The first `make openapi-export` creates the baseline. Out of scope for this PR.

## 7. Acceptance commands

```bash
make env-check                  # OK
make security-smoke             # FAIL (pre-existing, see §6)
make api-contract-check         # OK
pytest tests/test_model_registry.py tests/test_minimax_provider.py -v   # 11/11 PASS
make minimax-status             # OK
make minimax-evals              # OK (mock mode)
```

Of the 5 acceptance commands, 4 pass. The 5th (`security-smoke`) fails due to pre-existing placeholder strings, not anything introduced by this PR.

## 8. Files added

```
docs/ops/ENV_CONTRACT.md
docs/ops/PRODUCTION_VERIFICATION_GUIDE.md
docs/ai/MINIMAX_OPERATING_GUIDE.md
data/ai_ops/model_registry.yaml
schemas/model_registry.schema.json
reports/minimax/MINIMAX_IMPLEMENTATION_REPORT.md
tasks/minimax/MASTER_MINIMAX_EXECUTION_PROMPT_AR.md
tasks/minimax/01_p0_hardening_AR.md
tasks/minimax/02_revenue_factory_AR.md
tasks/minimax/03_founder_control_room_AR.md
tasks/minimax/04_whatsapp_portal_AR.md
tasks/minimax/05_proposal_proof_payment_AR.md
tasks/minimax/06_media_voice_factory_AR.md
scripts/minimax_status.py
scripts/minimax_evals.py
tests/test_minimax_provider.py
tests/test_model_registry.py
```

Plus 2 Makefile targets (`minimax-status`, `minimax-evals`).

## 9. Related

- `tasks/minimax/MASTER_MINIMAX_EXECUTION_PROMPT_AR.md` — canonical prompt
- `docs/ai/MINIMAX_OPERATING_GUIDE.md` — operating manual
- `data/ai_ops/model_registry.yaml` — registry
- `docs/ops/ENV_CONTRACT.md` — env contract
- `docs/ops/PRODUCTION_VERIFICATION_GUIDE.md` — production verification
