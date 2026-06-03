# Dealix — Wave 4 Integration Upgrade · Current Reality (Phase 0)

**Date:** 2026-05-07
**Branch:** `claude/service-activation-console-IA2JK`
**Local HEAD before Wave 4:** `9bf7575 feat(full-ops): 10-layer customer-serving operating spine`
**Last 3 commits:**
```
9bf7575 feat(full-ops): 10-layer customer-serving operating spine
ec36239 feat(console): customer Operations Console + 3-state radar dashboard
931874d feat(turnkey): closed-package productization
```

---

## Modules to REUSE (90% of new functionality maps here)

| Existing module | What it gives us |
|---|---|
| `auto_client_acquisition/revenue_graph/graph.py:36-72` | GraphNode/GraphEdge + 11 node types + 10 edge types → basis for Phase 3 unified_operating_graph |
| `auto_client_acquisition/revenue_graph/maturity_score.py:44-80` | 8-dimension scoring framework → basis for Phase 4 full_ops_radar score |
| `auto_client_acquisition/revenue_graph/leak_detector.py` | Leak detection patterns → basis for Phase 4 weakness radar |
| `api/routers/founder_beast_command_center.py:44-80` | 9 of 15 sections already built (today_top_3, growth_beast_snapshot, revenue_truth, finance_brief, delivery_status, support_alerts, proof_summary, compliance_alerts, role_command_status, next_best_action) → Phase 5 reuse |
| `landing/command-center.html` | v12.5.1 layout template → Phase 6 frontend pattern |
| `auto_client_acquisition/whatsapp_safe_send.py:57-90` | 6-gate orchestration → Phase 7 decision-only wrapper |
| `auto_client_acquisition/orchestrator/policies.py` | KSA quiet-hours + default_policy → Phase 7+8 |
| `auto_client_acquisition/designops/safety_gate.py:16-108` | Forbidden-token + ROI-claim + fake-customer regexes → Phase 8 channel_policy_gateway |
| `auto_client_acquisition/customer_data_plane/pii_redactor.py` | Email/phone/Saudi-ID redactors → Phases 8, 9, 11 |
| `auto_client_acquisition/observability_v10/buffer.py:17-37` | Thread-safe append + PII re-redaction → Phase 9 radar_events store |
| `auto_client_acquisition/observability_v10/schemas.py:16-43` | TraceRecordV10 → Phase 11 agent_observability is 100% re-export |
| `auto_client_acquisition/customer_brain/builder.py` (Wave 3) | Per-customer snapshot composer → graph node aggregation |
| `auto_client_acquisition/full_ops_contracts/schemas.py` (Wave 3) | 11 canonical envelopes |
| `auto_client_acquisition/leadops_spine/`, `service_sessions/`, `support_inbox/`, `payment_ops/`, `case_study_engine/`, `executive_pack_v2/` (Wave 3) | Source data for graph + radar + executive sections |

## Modules to AVOID touching (would break Wave 3 tests)

- `api/routers/customer_company_portal.py` — only **additive** changes to `enriched_view`; never remove keys; `sections` MUST stay at 8
- `auto_client_acquisition/full_ops_contracts/schemas.py` — schemas frozen
- `auto_client_acquisition/approval_center/` (already extended in Wave 3 Phase 5)
- `auto_client_acquisition/proof_ledger/{schemas,consent_signature,file_storage,pack_assembly}.py` — frozen
- `auto_client_acquisition/observability_v10/` — **Phase 11 only re-exports**, never modifies internals

## Existing tests that MUST stay green (Wave 3 + earlier)

- `tests/test_constitution_closure.py` — 16 tests · 8-section portal invariant + no internal leakage
- `tests/test_landing_forbidden_claims.py` — 3 tests · forbidden-token scrub
- `tests/test_full_ops_contracts.py` — 13 tests · canonical schemas
- `tests/test_leadops_spine_golden_path.py` — 8 tests
- `tests/test_customer_brain_full_ops.py` — 6 tests
- `tests/test_service_sessions_full_ops.py` — 8 tests
- `tests/test_approval_center.py` + `test_approval_center_extensions.py` — 26 tests
- `tests/test_proof_ledger_extensions.py` — 15 tests
- `tests/test_support_inbox_full_ops.py` — 8 tests
- `tests/test_executive_pack_full_ops.py` — 6 tests
- `tests/test_payment_ops_full_ops.py` — 8 tests
- `tests/test_customer_portal_live_full_ops.py` — 7 tests
- `tests/test_case_study_engine_full_ops.py` — 8 tests

**Total Wave 3 + constitution baseline: 132 tests must remain green.**

## Existing verifiers (do not duplicate — call into)

- `scripts/full_ops_10_layer_verify.sh` (Wave 3) — 18-check master verifier
- `scripts/seo_audit.py`
- `scripts/verify_service_readiness_matrix.py`
- `auto_client_acquisition/self_growth_os/internal_linking_planner.is_clean()`

## Hard gates pattern (reuse exactly)

From `api/routers/founder_beast_command_center.py:24-33` and `api/routers/leadops_spine.py:26-32`:

```python
_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_cold_whatsapp": True,
    "no_scraping": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}
```

Every new router in Phases 3-11, 16 must include this dict in every response.

## Customer portal contract — DO NOT BREAK

- `GET /api/v1/customer-portal/{handle}` returns:
  - `customer_handle: str`
  - `company_name: str | None`
  - `language_default: "ar"`
  - `sections: dict[str, dict]` — exactly 8 keys (1_start_diagnostic … 8_next_decision), each with `title_ar` + `title_en`
  - `enriched_view: dict[str, dict]` — currently 6 keys, Wave 4 will ADD more (additive)
  - `promise_ar`, `promise_en`
- 3-state UX:
  - `/customer-portal.html` (no params) → DEMO
  - `/customer-portal.html?org=<handle>` → PRE-LAUNCH
  - `/customer-portal.html?org=<handle>&access=<token>` → LIVE

## Known weak points (will be addressed in Wave 4)

1. No unified node-graph view — each module's data is queryable separately but no single graph
2. No Full-Ops Score — score lives in `revenue_graph.maturity_score` but isn't exposed customer-side
3. No formal Weakness Radar — leak_detector exists but no prioritized customer-facing list
4. No unified Executive Command Center — founder_beast_command_center has 9 of 15 sections
5. No internal WhatsApp decision layer — `whatsapp_safe_send` does live-gate checks but never returns decision-only
6. No channel-agnostic policy gateway — each channel has its own gate spread across modules
7. No event taxonomy — observability_v10 has TraceRecordV10 but no high-level "radar event" semantics
8. `agent_observability` namespace doesn't exist (observability_v10 already does the work — just need re-export)

## Non-breaking upgrade plan (sequenced 20 phases)

See plan file Section 21 for the full 20-phase sequence. Summary:

1. **Phases 0-1:** docs only (no code)
2. **Phase 2:** thin adapter shim (`integration_upgrade/`) — safe_call, degrade, customer_safe_label
3. **Phases 3-11:** seven new modules + seven new routers, each ~70-150 LOC, ~90% reuse
4. **Phase 10:** customer_company_portal additive `enriched_view` keys (never remove)
5. **Phases 12-14:** docs (playbook, packaging, audit script)
6. **Phase 15-16:** master verifier + router registration
7. **Phase 17:** full verification chain
8. **Phases 18-19:** evidence table + single commit

## Acceptance for Phase 0

- [x] Branch `claude/service-activation-console-IA2JK` confirmed
- [x] Local HEAD `9bf7575` recorded
- [x] Working tree clean
- [x] Reuse map captured (above)
- [x] Modules-to-avoid list captured
- [x] No code changes in this phase
