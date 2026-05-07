# Dealix — Integration Contract Map (Phase 1)

**Date:** 2026-05-07
**Companion:** `docs/integration_contract_map.yaml` (machine-readable)

This map records every integration surface in Dealix today, who it serves, what's safe to call, and what new adapter (if any) is needed for Wave 4. **No invented modules** — anything missing is marked `missing`.

---

| # | Layer | Existing module/file | Existing endpoint/page | Current contract | Customer-visible? | Internal-only? | Safe to call? | Degraded behavior | Adapter needed? | Do-not-break | Tests protecting it |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Customer Portal frontend | `landing/customer-portal.html` + `landing/assets/js/customer-dashboard.js` | `/customer-portal.html` (DEMO/PRE-LAUNCH/LIVE 3-state) | DOM contract: 9 sections, state pill, lucide icons | yes | no | yes (read-only) | DEMO data fallback if API unavailable | yes — additive enriched_view renderer (Phase 10) | DEMO-state copy, 3-state UX, no internal terms | manual smoke + `test_landing_forbidden_claims` |
| 2 | Customer Portal API | `api/routers/customer_company_portal.py` | `GET /api/v1/customer-portal/{handle}` + `/` | 8-section `sections` (constitutional) + 6-key `enriched_view` + bilingual promise | yes | no | yes (read-only) | zero-state stubs already in code | yes — Phase 10 additive enriched_view keys | `len(sections)==8`, no internal terms, bilingual title_ar/en | `test_constitution_closure.py` (16) + `test_customer_portal_live_full_ops.py` (7) |
| 3 | LeadOps Spine | `auto_client_acquisition/leadops_spine/` (Wave 3) | `/api/v1/leadops/{status,run,brief,draft,debug}` | `LeadOpsRecord` envelope; in-memory + JSONL | indirect (count via portal) | yes (founder/CSM) | yes | empty list if no records | no — already complete | `_HARD_GATES`, draft never auto_execute | `test_leadops_spine_golden_path.py` (8) |
| 4 | Customer Brain | `auto_client_acquisition/customer_brain/` (Wave 3) | `/api/v1/customers/{handle}/brain*` | `CustomerBrainSnapshot` aggregator; in-memory + JSONL | indirect | yes | yes | empty snapshot for unknown handle | no — Phase 3 graph reuses snapshot | no PII in snapshot | `test_customer_brain_full_ops.py` (6) |
| 5 | Service Sessions | `auto_client_acquisition/service_sessions/` (Wave 3) | `/api/v1/service-sessions/*` | 7-state machine; transition into `active` requires approval_id | indirect (count via portal) | yes | yes | 404 on unknown session | no — Phase 3+5 read | state-machine validity | `test_service_sessions_full_ops.py` (8) |
| 6 | Approval Center | `auto_client_acquisition/approval_center/` (extended Wave 3) | `/api/v1/approvals/*` (9 endpoints incl. expire-sweep + bulk-approve) | `ApprovalRequest` schema; in-memory; per-channel policy | indirect | yes | yes | empty pending list | no — Phase 5+7 read | LinkedIn never auto-execute, expiry sweep | `test_approval_center.py` (14) + `test_approval_center_extensions.py` (12) |
| 7 | Payment Ops | `auto_client_acquisition/payment_ops/` (Wave 3) | `/api/v1/payment-ops/*` | 8-state machine; NO_LIVE_CHARGE env-gate | indirect (billing in portal) | yes | yes (test methods only) | 409 on invalid transition | no — Phase 3 reads state | invoice_intent != revenue, no live unless env | `test_payment_ops_full_ops.py` (8) |
| 8 | Proof Ledger | `auto_client_acquisition/proof_ledger/` (extended Wave 3) | `/api/v1/proof-ledger/{events,units,export,attachments,consent,pack}` | ProofEvent schema + 25 fields + redaction; consent-signature hash binding | indirect (proof_pack in portal) | yes | yes | unconditional PII redact on export | no — Phase 3 reads events | no publish without signed consent | `test_proof_ledger_extensions.py` (15) + `test_proof_ledger_redacts_on_export.py` (4) |
| 9 | Support Inbox / Support OS | `auto_client_acquisition/support_inbox/` + `support_os/` (Wave 3 + earlier) | `/api/v1/support-inbox/*` + `/api/v1/support-os/*` | classify→ticket→escalate→draft pipeline; SLA p0-p3 | indirect | yes | yes (drafts only) | empty list when no tickets | no — Phase 5 reads | NO_LIVE_SEND, mandatory-escalate categories | `test_support_inbox_full_ops.py` (8) + `test_support_os_v12.py` (25) |
| 10 | Case Study Engine | `auto_client_acquisition/case_study_engine/` (Wave 3) | `/api/v1/case-study/*` | Selection + redaction + narrative + library; consent-signature hash binding | indirect | yes | yes | zero in library if not built | no | NO_PUBLISH_WITHOUT_CONSENT, FORBIDDEN_TOKENS_SCRUB | `test_case_study_engine_full_ops.py` (8) |
| 11 | Growth/Sales/Partnership radar | `api/routers/{growth_os,sales_os,partnership_os,growth_beast,company_growth_beast}.py` | various `/api/v1/*-os/*` | per-OS status + briefs | no | yes | yes | role briefs return insufficient_data when empty | yes — Phase 5 reads role-command briefs | `_HARD_GATES` per router | various existing tests |
| 12 | Executive Pack | `api/routers/executive_os.py` + `auto_client_acquisition/executive_reporting/` + `executive_pack_v2/` (Wave 3) | `/api/v1/executive-os/*` + `/api/v1/customers/{h}/executive-pack/*` | weekly/daily reports; NO_FAKE_REVENUE | indirect (digest in portal) | yes | yes | data_status: insufficient_data \| live | no — Phase 5 reads | NO_FAKE_REVENUE, NO_FAKE_FORECAST | `test_executive_os_v12.py` (4) + `test_executive_pack_full_ops.py` (6) + `test_executive_reporting.py` (8+) |
| 13 | AI Workforce | `api/routers/{ai_workforce,ai_workforce_v10}.py` + `auto_client_acquisition/{ai,ai_workforce,ai_workforce_v10}/` | `/api/v1/ai-workforce*` | agent registry + run logs | no | yes | yes (read-only) | empty registry if not configured | no — Phase 5 may surface count | NO_LIVE_SEND on any agent | various |
| 14 | Full-Ops verifiers | `scripts/full_ops_10_layer_verify.sh` (Wave 3) + `scripts/v*_verify.sh` | shell scripts | exit 0 PASS, non-zero FAIL | no | yes | yes | reports per-layer PASS/FAIL | yes — Phase 15 chains them in `integration_upgrade_verify.sh` | must keep PASS after Wave 4 | `test_dealix_smoke_test_cli.py` |
| 15 | Channel policies / hard gates | `auto_client_acquisition/whatsapp_safe_send.py` + `orchestrator/policies.py` + `designops/safety_gate.py` + `consent_table.py` + per-router `_HARD_GATES` | (cross-cutting; no dedicated endpoint) | gate evaluation + KSA quiet-hours + 6-gate WhatsApp orchestration + consent table | no | yes | yes | gate refuses unsafe action | yes — Phase 8 unified `/api/v1/channel-policy/check` | NO_COLD_WHATSAPP, NO_LINKEDIN_AUTO, NO_SCRAPING, NO_FAKE_PROOF | `test_whatsapp_safe_send_v14.py` + various |

---

## Coverage by Wave

- **Wave 1 (V11/V12 base):** Layers 1-2, 6-9, 12-15 already had endpoints + tests
- **Wave 2.5 (Turnkey package):** added launchpad CTAs (no new layer)
- **Wave 2.6 (Customer Operations Console):** Layer 1+2 console rebuild + JS orchestrator
- **Wave 3 (Full-Ops 10-Layer Spine):** Layers 3-5, 7, 8, 10, 12 added or extended; Phase-based test coverage
- **Wave 4 (Integration Upgrade — this plan):** Layers 11+15 unified, +7 net-new modules (unified graph, full_ops_radar, exec command center, whatsapp_decision_bot, channel_policy_gateway, radar_events, agent_observability)

## Adapters needed (summary for Wave 4)

| Phase | Adapter | What it wraps |
|---|---|---|
| 2 | `integration_upgrade.safe_call` | every cross-module call, with degrade fallback |
| 3 | `unified_operating_graph.builder` | revenue_graph + customer_brain + Wave 3 modules |
| 4 | `full_ops_radar.score` | revenue_graph.maturity_score + 2 new dimensions |
| 5 | `executive_command_center.builder` | founder_beast_command_center 9 sections + 6 new |
| 7 | `whatsapp_decision_bot.policy` | whatsapp_safe_send 6 gates (decision-only) |
| 8 | `channel_policy_gateway.policy` | designops/safety_gate + per-channel rule sets |
| 9 | `radar_events.event_store` | observability_v10/buffer (event_type taxonomy) |
| 11 | `agent_observability` | observability_v10 (re-export shim) |

All adapters are READ-MOSTLY. Only `radar_events.event_store` writes (append-only, PII-redacted).

## What we will NOT touch

- The 8-section portal contract — locked by `test_constitution_closure.py::test_portal_has_exactly_8_sections`
- Any existing router's response schema — additive fields only on `customer_company_portal.enriched_view`
- `auto_client_acquisition/full_ops_contracts/schemas.py` — frozen at Wave 3
- `tests/*` for any existing test — only ADDITIONS
