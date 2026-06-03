# Dealix — Full-Ops 10-Layer Evidence Table

**Date:** 2026-05-07
**Branch:** `claude/service-activation-console-IA2JK`
**Verifier:** `bash scripts/full_ops_10_layer_verify.sh` → `DEALIX_FULL_OPS_10_LAYER_VERDICT=PASS`

---

## Summary table

| # | Layer | Files | Endpoints | Tests | Hard rules | Customer-visible |
|---|---|---|---|---|---|---|
| 1 | LeadOps Spine | `auto_client_acquisition/leadops_spine/` | 5 under `/api/v1/leadops/*` | `test_leadops_spine_golden_path.py` | NO_LIVE_SEND, NO_COLD_WHATSAPP, NO_SCRAPING, approval-required | leads counted in portal `enriched_view.ops_summary` |
| 2 | Customer Brain | `auto_client_acquisition/customer_brain/` | 4 under `/api/v1/customers/*/brain*` | `test_customer_brain_full_ops.py` | NO_PII_IN_SNAPSHOT, source_modules visible | profile/sector/channels surfaced via portal |
| 3 | Service Sessions | `auto_client_acquisition/service_sessions/` | 5 under `/api/v1/service-sessions/*` | `test_service_sessions_full_ops.py` | approval_required to activate, state-machine-validated | session count in `enriched_view.sequences` |
| 4 | Approval Center | `auto_client_acquisition/approval_center/` (extended) | 9 under `/api/v1/approvals/*` (2 new) | `test_approval_center_extensions.py` | NO_LINKEDIN_AUTO, per-channel policy, expiry sweep | drafts_pending count in portal |
| 5 | Proof Ledger | `auto_client_acquisition/proof_ledger/` (extended) | 10 under `/api/v1/proof-ledger/*` (3 new) | `test_proof_ledger_extensions.py` | 10MB cap, mime allowlist, consent_signature hash-binding | proof_pack section in portal |
| 6 | Support Inbox | `auto_client_acquisition/support_inbox/` | 5 under `/api/v1/support-inbox/*` | `test_support_inbox_full_ops.py` | NO_LIVE_SEND, drafts_only, PII redaction on storage | support_tickets section in portal |
| 7 | Executive Pack | `auto_client_acquisition/executive_pack_v2/` | 2 under `/api/v1/customers/*/executive-pack/*` | `test_executive_pack_full_ops.py` | NO_FAKE_REVENUE, NO_FAKE_FORECAST, NO_PII_IN_REPORT | weekly_report + digest_weekly in portal |
| 8 | Payment Ops | `auto_client_acquisition/payment_ops/` | 5 under `/api/v1/payment-ops/*` | `test_payment_ops_full_ops.py` | NO_LIVE_CHARGE, evidence_required, delivery_requires_payment_confirmed | billing_state in portal (planned wiring) |
| 9 | Customer Portal | `api/routers/customer_company_portal.py` (extended) | 2 under `/api/v1/customer-portal/*` | `test_customer_portal_live_full_ops.py` | 8-section invariant, NO internal terms, no fake data | EVERYTHING — single console |
| 10 | Case Study Engine | `auto_client_acquisition/case_study_engine/` | 5 under `/api/v1/case-study/*` | `test_case_study_engine_full_ops.py` | NO_PUBLISH_WITHOUT_CONSENT, NO_FAKE_PROOF, FORBIDDEN_TOKENS_SCRUBBED | sales library + per-customer narratives |

---

## Layer 1 — LeadOps Spine

**Files:**
- `auto_client_acquisition/leadops_spine/orchestrator.py` (200 LOC) — `run_pipeline`, `list_records`, `debug_lead`
- `auto_client_acquisition/leadops_spine/compliance_gate.py` — block-list check + suspicious patterns
- `auto_client_acquisition/leadops_spine/offer_router.py` — channel + medium picker
- `auto_client_acquisition/leadops_spine/next_action.py` — owner + deadline suggestion
- `auto_client_acquisition/leadops_spine/draft_builder.py` — bilingual templates + forbidden-token scrub

**Endpoints:**
- `GET  /api/v1/leadops/status`
- `POST /api/v1/leadops/run`
- `POST /api/v1/leadops/brief`
- `POST /api/v1/leadops/draft`
- `GET  /api/v1/leadops/debug?leadops_id=X`

**Reused:** `lead_inbox.py:43-144`, `pipeline.py:52-120`, `agents/intake.py`, `agents/qualification.py`

**Persistence:** in-memory + JSONL (`data/leadops_records.jsonl`)

**What stays manual:** the actual outreach send (founder approves draft via approval_center)

**What unlocks after first paid customer:** Postgres ORM swap (matches `proof_ledger/postgres_backend.py` pattern)

---

## Layer 2 — Customer Brain

**Files:**
- `auto_client_acquisition/customer_brain/builder.py` — composer over crm_v10 + customer_loop + proof_ledger + support + market
- `auto_client_acquisition/customer_brain/context_pack.py` — ≤3KB JSON for LLM context

**Endpoints:**
- `GET  /api/v1/customers/{handle}/brain`
- `POST /api/v1/customers/{handle}/brain/build`
- `GET  /api/v1/customers/{handle}/context-pack`
- `GET  /api/v1/customers/brain/status`

**Reused:** `company_brain/brain.py:95-108`, `crm_v10/schemas.py:28-46`, `market_intelligence.signal_detectors`

**What stays manual:** customer profile data entry (until first customer fills the diagnostic)

---

## Layer 3 — Service Sessions

**Files:**
- `auto_client_acquisition/service_sessions/store.py` — start, transition, attach, complete (in-memory + JSONL)
- `auto_client_acquisition/service_sessions/lifecycle.py` — state machine + transition validation

**Endpoints:**
- `POST /api/v1/service-sessions/start`
- `GET  /api/v1/service-sessions/{id}`
- `POST /api/v1/service-sessions/{id}/advance`
- `POST /api/v1/service-sessions/{id}/attach-deliverable`
- `POST /api/v1/service-sessions/{id}/complete`

**Reused:** `customer_loop.JourneyState` truth table, `crm_v10.ServiceSession` schema

**State machine:** `draft → waiting_for_approval → active → delivered → proof_pending → complete` (any → blocked)

**Hard rule:** transition to `active` REQUIRES approval_id (founder go-ahead)

---

## Layer 4 — Approval Center (extended in-place)

**Extensions added:**
- `approval_policy.py` — `CHANNEL_POLICY` table + `can_auto_approve()` + LinkedIn auto-execute strip
- `approval_store.py` — `expire_overdue()` + `bulk_approve()`
- `api/routers/approval_center.py` — 2 new endpoints: `/expire-sweep` + `/bulk-approve`

**Per-channel rules:**
| Channel | Required approver | Max auto-approve risk |
|---|---|---|
| whatsapp | founder | NEVER |
| linkedin | founder | NEVER |
| phone | founder | NEVER |
| email | csm_or_founder | low |
| dashboard | csm_or_founder | medium |

**No new schemas** — all extensions use existing `ApprovalRequest`.

---

## Layer 5 — Proof Ledger (extended in-place)

**Extensions added:**
- `proof_ledger/file_storage.py` — 10MB cap, mime allowlist, customer-scoped dirs
- `proof_ledger/consent_signature.py` — `ConsentSignature` model + `request_consent`/`record_signature` with hash-binding
- `proof_ledger/pack_assembly.py` — `assemble_proof_pack` with internal_only/external_publishable audiences
- `api/routers/proof_ledger.py` — 3 new endpoints: `/attachments`, `/consent/request`, `/pack/build`

**Hash-binding rule:** `record_signature` rejects when `confirmed_document_hash != original document_hash` — prevents narrative-swap attacks.

---

## Layer 6 — Support Inbox

**Files:**
- `auto_client_acquisition/support_inbox/state_store.py` — `classify_and_store` (composes existing classifier+escalation+responder+ticket)
- `auto_client_acquisition/support_inbox/sla_monitor.py` — `find_breached_tickets`

**Endpoints:**
- `POST /api/v1/support-inbox/inbound`
- `GET  /api/v1/support-inbox/tickets[?customer_id=...&status=...]`
- `GET  /api/v1/support-inbox/tickets/{id}`
- `POST /api/v1/support-inbox/tickets/{id}/status`
- `GET  /api/v1/support-inbox/sla-breaches[?customer_id=...]`

**Reused:** `support_os/{classifier,ticket,escalation,sla,responder}.py`

**Mandatory escalation categories** (from existing support_os): refund, payment, privacy_pdpl, angry_customer + matched harassment/legal/security patterns

---

## Layer 7 — Executive Pack v2

**Files:**
- `auto_client_acquisition/executive_pack_v2/composer.py` — per-customer `build_daily_pack` + `build_weekly_pack`

**Endpoints:**
- `GET /api/v1/customers/{handle}/executive-pack/today`
- `GET /api/v1/customers/{handle}/executive-pack/week`

**Reused:** `executive_reporting/*`, `role_command_os.py`, `designops/generators/executive_weekly_pack.py`

**Sections composed:** lead_kpis (from leadops_spine), support_kpis (from support_inbox), next_3_actions (from approval_center), active_sessions + blockers (from service_sessions), sector_context (from customer_brain)

---

## Layer 8 — Payment Ops

**Files:**
- `auto_client_acquisition/payment_ops/orchestrator.py` — full state machine

**State machine:**
`invoice_intent → invoice_sent_manual → payment_pending → payment_evidence_uploaded → payment_confirmed → delivery_kickoff` (any → voided/refunded)

**Endpoints:**
- `POST /api/v1/payment-ops/invoice-intent`
- `POST /api/v1/payment-ops/manual-evidence`
- `POST /api/v1/payment-ops/confirm`
- `GET  /api/v1/payment-ops/{id}/state`
- `POST /api/v1/payment-ops/{id}/kickoff-delivery`

**Reused:** `dealix/payments/moyasar.py`, `revops/invoice_state.py`, `revops/payment_confirmation.py`

**NO_LIVE_CHARGE enforcement:** `moyasar_live` method refused unless `DEALIX_MOYASAR_MODE=live` env var is explicitly set. Test `test_moyasar_live_blocked_without_env` confirms.

**Revenue rule:** only `status >= payment_confirmed` counts as revenue. `is_revenue_now=true` flag exposed in `/confirm` response.

---

## Layer 9 — Customer Portal (live wiring)

**Extension:** `api/routers/customer_company_portal.py` — replaced zero-state stubs in `_ops_summary`, `_sequences_state`, `_digest_weekly`, `_digest_monthly` with live calls to layers 1-8 (best-effort, graceful degradation).

**Constitutional invariant preserved:** `len(sections) == 8` still holds; live data flows into `enriched_view`, NOT `sections`.

**Test coverage:** all 16 `test_constitution_closure.py` tests + 7 new `test_customer_portal_live_full_ops.py` tests = 23/23 green.

---

## Layer 10 — Case Study Engine

**Files:**
- `auto_client_acquisition/case_study_engine/builder.py` — `select_publishable`, `build_candidate`, `request_quote`, `approve_candidate`, `list_library`

**Endpoints:**
- `POST /api/v1/case-study/candidate`
- `POST /api/v1/case-study/build`
- `POST /api/v1/case-study/request-quote`
- `POST /api/v1/case-study/approve`
- `GET  /api/v1/case-study/library[?sector=...]`

**Hard rules enforced:**
- `evidence_level in {customer_confirmed, payment_confirmed}` (rejects `observed`)
- `consent_for_publication=True` AND `consent_signature.status=signed` AND `document_hash` matches narrative
- `approval_status=approved`
- `pii_redacted=True`
- forbidden-token scrub on every narrative (same regex as `test_landing_forbidden_claims.py`)

**No publish without:** `is_publishable() == True` (gates: signed consent + hash match + redaction complete + approval)

---

## Cross-cutting evidence

| Concern | Evidence |
|---|---|
| 8 hard gates immutable | `_HARD_GATES` dict in every new router; existing gate-enforcement code untouched |
| Forbidden tokens | `tests/test_landing_forbidden_claims.py` 3/3 + `_scrub` enforced at draft + narrative time |
| 8-section portal invariant | `tests/test_constitution_closure.py::test_portal_has_exactly_8_sections` 1/1 |
| No internal terms in customer-facing | `test_portal_no_internal_leakage` 1/1 + `test_portal_no_internal_term_leak` 1/1 |
| NO_LIVE_CHARGE invariant | `tests/test_finance_os_no_live_charge_invariant.py` + `test_moyasar_live_blocked_without_env` |
| Proof redaction on export | `tests/test_proof_ledger_redacts_on_export.py` 4/4 |
| Internal linking planner | `is_clean()` returns True |
| Service registry | `LIVE=8` unchanged (no new TARGET → LIVE flips this PR) |
| SEO audit | 44 pages, `required_gap=0` |

---

## Founder daily flow (after this PR lands)

```
Morning:
  GET /api/v1/customers/{customer_handle}/executive-pack/today
  → Read summary_ar, scan blockers, look at next_3_actions

  GET /api/v1/leadops/status
  → Confirm new leads queued for review

  GET /api/v1/approvals/pending
  → Approve / reject / edit drafts (≤30 min)

Midday:
  POST /api/v1/service-sessions/{id}/advance  (with approval_id)
  → Move sessions through their state machine

  POST /api/v1/payment-ops/manual-evidence + /confirm
  → Confirm any received bank transfers (NO_LIVE_CHARGE)

Evening:
  POST /api/v1/approvals/expire-sweep
  → Clear stale pending approvals

  GET /api/v1/customer-portal/{handle}
  → Verify what the customer sees on /customer-portal.html
```

## Master verifier output

```
DEALIX_FULL_OPS_10_LAYER_VERDICT=PASS
COMPILEALL=PASS
FULL_OPS_CONTRACTS=PASS
LEADOPS_SPINE=PASS
CUSTOMER_BRAIN=PASS
SERVICE_SESSIONS=PASS
APPROVAL_CENTER=PASS
PROOF_LEDGER=PASS
SUPPORT_INBOX=PASS
EXECUTIVE_PACK=PASS
PAYMENT_OPS=PASS
CUSTOMER_PORTAL=PASS
CASE_STUDY_ENGINE=PASS
FORBIDDEN_CLAIMS=PASS
NO_LIVE_CHARGE_INVARIANT=PASS
PROOF_REDACTS_ON_EXPORT=PASS
PLANNER_CLEAN=PASS
SEO_AUDIT=PASS
REGISTRY_VALIDATOR=PASS

NEXT_FOUNDER_ACTION=All gates green. Open the Operations Console
(/customer-portal.html) and walk through the 5-warm-intro outreach
for first paid pilot.
```

## What stays MANUAL after this PR

- Outreach sends — every external action requires founder approval
- Payment confirmation — founder uploads evidence + flips state to confirmed
- Case study consent — customer signs the narrative explicitly
- LinkedIn — never automated, NO_LINKEDIN_AUTO

## What's deferred to next wave (when triggered by named customer)

- Postgres ORM for new layers (currently in-memory + JSONL — fine until customer #2)
- Multi-tenant RLS — when customer #2 signs
- Live news API for radar (Tavily / Google CSE) — when env keys provided
- Email digest delivery — when first Partner asks
- LLM-backed narrative builder — currently deterministic templates; LLM swap when customer asks for richer prose
