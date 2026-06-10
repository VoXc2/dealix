# Dealix — Full-Ops 10-Layer Current Reality (Phase 0 audit)

**Date:** 2026-05-07
**Branch:** `claude/service-activation-console-IA2JK`
**Author:** acting CTO mode, Claude
**Purpose:** name what already exists, name every gap, prove the upcoming Wave 3 spine is wiring + extension, NOT new V13/V14 architecture (Article 11 / Article 3 compliance).

---

## Reuse map per layer (from Explore-agent reports)

| Layer | % already built | Verdict |
|---|---|---|
| 1 LeadOps Spine | 85% | NEEDS_THIN_SPINE — orchestrator wrapper |
| 2 Customer Brain | 70% | NEEDS_THIN_SPINE — per-customer aggregator |
| 3 Service Sessions | 65% | NEEDS_THIN_SPINE — persistence + executor |
| 4 Approval Center | 95% | REUSE_OK — minor gap features only |
| 5 Payment Ops | 60% | NEEDS_THIN_SPINE — HTTP surface + webhook |
| 6 Support Inbox | 90% | REUSE_OK — webhook handler + state store |
| 7 Proof Ledger | 90% | REUSE_OK — attachments + consent signature |
| 8 Executive Pack | 75% | NEEDS_THIN_SPINE — market context + KPIs |
| 9 Customer Portal | 85% | NEEDS_THIN_SPINE — live data wiring |
| 10 Case Study Engine | 50% | NEEDS_BUILD — narrative builder + sales library |

**Aggregate:** ~76% of the spine already exists in code. Wave 3 adds the missing 24% as **integration glue**, not new architecture.

---

## Layer 1 — LeadOps Spine

### Existing
- `auto_client_acquisition/lead_inbox.py:43-144` — append/list/stats (JSONL store)
- `auto_client_acquisition/pipeline.py:52-120` — AcquisitionPipeline (Intake → ICP Match → Pain → Qualification → CRM Sync → Booking → Proposal)
- `auto_client_acquisition/pipelines/{normalize,dedupe,scoring,enrichment}.py`
- `auto_client_acquisition/agents/{intake,qualification}.py`
- `POST /api/v1/leads`, `POST /api/v1/leads/discover/local`, `POST /api/v1/leads/discover/web`, `POST /api/v1/leads/enrich/full`

### Gaps to close in Wave 3
- No compliance pre-check (blocked-customer list)
- No offer routing (which channel for whom)
- No next-action framework
- No draft-to-approval-queue wiring

---

## Layer 2 — Customer Brain

### Existing
- `auto_client_acquisition/company_brain/brain.py:95-108` — CompanyBrain snapshot (self-referential)
- `auto_client_acquisition/crm_v10/schemas.py:28-46` — Account / Contact / Lead / Deal / ServiceSession / CustomerHealth
- `auto_client_acquisition/crm_v10/{customer_health,account_timeline}.py`
- `auto_client_acquisition/company_brain_v6/`
- `GET /api/v1/company-brain` (self-referential, NOT per-customer)

### Gaps to close
- No per-customer profile aggregator endpoint
- No fit/risk inference
- No channel/tone/service_history aggregation
- No next-action inference

---

## Layer 3 — Service Sessions

### Existing
- `auto_client_acquisition/workflow_os_v10/service_session_workflow.py:12-32` — GROWTH_STARTER_7_DAY workflow def
- `auto_client_acquisition/crm_v10/schemas.py:83-90` — ServiceSession (id, account_id, status, started_at, completed_at)
- `auto_client_acquisition/customer_loop/schemas.py:12-80` — JourneyState (12 states) + ALLOWED_TRANSITIONS truth table
- `GET /api/v1/customer-loop/states`, `POST /api/v1/customer-loop/journey/advance`

### Gaps to close
- No persistence layer (in-memory only)
- No workflow executor (definitions exist, no runner)
- No deliverable tracking
- No approval-gated advance
- No SLA / commitment / expected-end fields

---

## Layer 4 — Approval Center

### Existing (95% — production-ready)
- `auto_client_acquisition/approval_center/` — `__init__.py`, `schemas.py:18-53` (ApprovalRequest with action_mode + risk_level + edit_history), `approval_store.py`, `approval_policy.py`, `approval_renderer.py`
- 7 endpoints under `/api/v1/approvals/*`
- 14 tests in `tests/test_approval_center.py`

### Gaps (refinements only — not blockers)
- No per-channel approval policy
- No expiry enforcement (field exists, sweep doesn't run)
- No bulk approval ("approve all from this customer")
- In-memory only (Redis swap point unimplemented)

---

## Layer 5 — Payment Ops

### Existing
- `dealix/payments/moyasar.py:27-100` — MoyasarClient (create_invoice, fetch_payment, verify_webhook constant-time)
- `auto_client_acquisition/revops/invoice_state.py:28-77` — InvoiceState model + transitions
- `auto_client_acquisition/revops/payment_confirmation.py:23-84` — evidence_reference REQUIRED, no verbal confirmation
- `auto_client_acquisition/revops/{finance_brief,margin}.py`

### Gaps to close
- **No FastAPI router exists for payment_ops** (only internal modules)
- No webhook → confirmation handler wired
- No "payment_confirmed → kickoff delivery" orchestration
- No refund SOP, no retry logic, no thank-you

---

## Layer 6 — Support Inbox

### Existing (90%)
- `auto_client_acquisition/support_os/{classifier,ticket,escalation,sla,responder,knowledge_answer}.py` — 12 categories AR/EN, SLA p0-p3, mandatory-escalation 5 categories
- `auto_client_acquisition/customer_inbox_v10/{conversation_model,sla_policy,escalation,reply_suggestion}.py`
- 7 endpoints under `/api/v1/support-os/*` and `/api/v1/customer-inbox-v10/*`
- 25+ tests in `test_support_os_v12.py`

### Gaps to close
- No webhook handler (classifier is pure; needs HTTP entry)
- No conversation state machine (open → in_progress → waiting_customer → resolved → closed)
- No SLA timer enforcement
- No draft persistence

---

## Layer 7 — Proof Ledger

### Existing (90%)
- `auto_client_acquisition/proof_ledger/schemas.py:1-82` — ProofEvent (25 fields, 12 event types) + RevenueWorkUnit (13 unit types)
- `auto_client_acquisition/proof_ledger/postgres_backend.py:1-150` — SQLAlchemy ORM with PII redaction on insert
- `auto_client_acquisition/proof_ledger/{file_backend,evidence_export,hmac_signing}.py`
- 7 endpoints under `/api/v1/proof-ledger/*`
- 4+ tests

### Gaps to close
- No EvidenceAttachment file storage
- No ConsentSignature model
- No proof-pack assembly orchestration

---

## Layer 8 — Executive Pack

### Existing (75%)
- `api/routers/executive_os.py:1-99` — daily-brief, weekly-pack
- `auto_client_acquisition/executive_reporting/{weekly_report_builder,decision_summary,next_week_plan,proof_summary,risk_summary}.py`
- `api/routers/role_command_os.py:1-73` — CEO / sales / growth / cs / finance / compliance briefs
- `auto_client_acquisition/designops/generators/executive_weekly_pack.py` — HTML+MD render
- 12+ tests

### Gaps to close
- No revenue line chart / sparkline
- No leads-this-week breakdown
- No support SLA breaches aggregation
- No formal blockers list
- No "next 3 actions" prioritization
- No market context (sector_pulse) wired

---

## Layer 9 — Customer Portal

### Existing (85% — Wave 2.6 just landed)
- `api/routers/customer_company_portal.py:1-267` — 8 sections + `enriched_view` (ops_summary, sequences, radar_today, digest_weekly, digest_monthly, service_status_for_customer)
- `landing/customer-portal.html` — 9-section console
- `landing/assets/js/customer-dashboard.js` — 3-state orchestrator (DEMO / SIGNED-UP / LIVE)

### Gaps to close
- All `enriched_view` keys return zero-state stubs (no real data)
- Need to wire to layers 1-8 for live data when customer activated

---

## Layer 10 — Case Study Engine

### Existing (50%)
- `auto_client_acquisition/proof_to_market/engine.py:1-99` — approval_gate_check, proof_to_snippet, case_study_candidate
- `api/routers/proof_to_market.py:1-88` — 5 endpoints

### Gaps to close (the only NEEDS_BUILD layer)
- No consent-signature acquisition workflow
- No narrative builder (LLM-backed, with redaction + forbidden-token scrub)
- No quote request form
- No sales library storage
- No publish-pack assembly

---

## Hard gates currently enforced (DO NOT relax)

| Gate | Routers enforcing |
|---|---|
| `no_live_send` | support_os, customer_inbox_v10, customer_success_os, delivery_os, delivery_factory, full_ops, growth_beast, company_growth_beast, founder_beast_command_center, role_command_os |
| `no_live_charge` | support_os, full_ops, founder_beast_command_center |
| `no_cold_whatsapp` | support_os, founder_beast_command_center (via escalation patterns) |
| `no_scraping` | support_os, growth_beast, company_growth_beast, delivery_factory, full_ops, founder_beast_command_center, role_command_os |
| `no_fake_proof` | support_os, proof_to_market, delivery_os, customer_success_os, full_ops, founder_beast_command_center, company_growth_beast |
| `no_fake_revenue` / `no_fake_forecast` | executive_os |
| `approval_required_for_external_actions` | All layer routers |

Every new endpoint added in Phases 1-15 MUST include the relevant `_HARD_GATES` dict.

---

## Forbidden tokens currently scanned

`tests/test_landing_forbidden_claims.py` enforces (case-insensitive):
- `\bguaranteed?\b`
- `\bblast\b`
- `\bscraping\b`
- `\bcold\s+(whatsapp|outreach|email|messaging)\b`
- `نضمن`

Every new narrative / draft generated by Wave 3 MUST pass this scan.

---

## Pre-flight check (executed before Phase 1)

```
$ git status -s
(clean)
$ git branch --show-current
claude/service-activation-console-IA2JK
$ python3 -m pytest tests/test_constitution_closure.py tests/test_landing_forbidden_claims.py -x -q --no-cov
19 passed
$ python3 scripts/seo_audit.py
OK: pages=44, required_gap=0, advisory_gap=1
$ python3 scripts/verify_service_readiness_matrix.py
OK: SERVICES_TOTAL=32 LIVE=8 PILOT=0 PARTIAL=0 TARGET=24
$ python3 -c "from auto_client_acquisition.self_growth_os.internal_linking_planner import is_clean; assert is_clean()"
PLANNER_CLEAN
```

All baselines green. Ready to start Phase 1.
