# Dealix AI Intelligence Architecture

> Layered, deterministic-first design. LLMs are used only for tone polish
> and never on the safety hot path. Every layer below has a non-LLM
> fallback so the system stays useful when keys are missing.

## Layers

### 1. Language Layer
- Implementation: `auto_client_acquisition.safety.intent_classifier._detect_language`
- Output: `Language.AR | Language.EN | Language.MIXED`
- Mode: deterministic (regex over Unicode ranges).
- Status: PROVEN_LOCAL (95+ test asserts).

### 2. Intent Layer
- Implementation: `classify_intent(text) -> IntentDecision`
- Outputs: `intent`, `recommended_bundle`, `action_mode`, `requires_intake`.
- Intents covered today:
  - `cold_or_blast_outreach_request` (BLOCKED)
  - `has_list` (data_to_revenue, approval_required)
  - `want_partnerships` (partnership_growth, approval_required)
  - `want_proof_report` (executive_growth_os, suggest_only)
  - `want_more_customers` (growth_starter, approval_required)
- Mode: deterministic. No LLM.
- Status: PROVEN_LOCAL.

### 3. Service Recommendation Layer
- Implementation: `recommended_bundle` field of `IntentDecision`, plus
  `GET /api/v1/services/{bundle_id}` for full contract.
- Mode: deterministic mapping; LLM optional for tone of `reason_ar`.
- Status: PROVEN_LIVE (catalog + intake-questions are live on prod).

### 4. Safety Layer (input + output + tool)
- Input guardrails: `classify_intent` blocks unsafe intents before any tool.
- Output guardrails: `tests/test_no_guaranteed_claims.py` static sweep.
- Tool guardrails: `WHATSAPP_ALLOW_LIVE_SEND=false` + Moyasar webhook
  HMAC + Gmail config check + no LinkedIn automation route.
- Status: PROVEN_LIVE.

### 5. Company Brain Layer
- Implementation: `auto_client_acquisition.customer_ops.build_company_brain`
- Output keys: company_name, website, sector, city, offer, icp,
  language_preference, tone_preference, approved_channels,
  blocked_channels, consent_records, current_service, open_decisions,
  proof_summary, past_objections, next_best_actions.
- Falls back to `build_demo_company_brain` when no DB session available.
- Status: PROVEN_LOCAL.

### 6. Tool Layer
- Read-side tools (PROVEN_LIVE): services catalog, role-briefs, proof
  ledger units, support classify/sla, business recommend-plan, command
  center snapshot, objections bank.
- Write-side tools (PROVEN_LOCAL only): leads, deals, payments
  (manual-request + mark-paid), customers/{id}/proof-pack,
  compliance/check-outreach.
- Blocked tools: live WhatsApp customer outbound, Gmail live send,
  Moyasar live charge, LinkedIn automation (no automation route exists).

### 7. Evaluation Layer
- `tests/test_operator_saudi_safety.py` — 28 cases, Arabic + English + mixed.
- `tests/test_operator_bilingual_intent.py` — positive-path regression.
- `tests/test_safe_action_gateway.py` — ActionMode invariants.
- `tests/test_no_guaranteed_claims.py` — static text sweep for forbidden tokens.
- `tests/test_live_gates_default_false.py` — Settings defaults.
- `tests/test_whatsapp_policy.py` — canonical unsafe phrasings.
- `tests/test_company_brain.py` — brain shape invariants.
- `tests/test_support_bot_bilingual.py` — live remote checks (with xfail
  for the 3 documented deploy-branch escalation gaps).

## Failure handling

- LLM key missing → rule-based classifier still works (deterministic).
- DB unreachable → `build_company_brain` returns demo payload labelled `source=demo`.
- Live external action requested → blocked at gate; safe alternatives returned.
- Unknown intent → defaults to `growth_starter` + `requires_intake=True` (never `approved_execute`).

## Observability hooks (BACKLOG)

Lightweight surface to add later without changing this branch:

- request_id (already enforced via `RequestIDMiddleware`)
- intent + action_mode → emit as a structured log event
- proof_event_id when an outcome is realized
- safety_result counter per blocked_reasons key

These exist in skeleton form via the deploy branch's
`/api/v1/observability/*` routes — full wiring is BACKLOG.
