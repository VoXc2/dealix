# Unimplemented-feature tests — اختبارات لميزات غير منفّذة

## Summary — ملخّص

These 9 test files fail at **collection** because they import symbols that
their target module never implemented. They are **not regressions** — the
modules never exported these names (verified against the Wave 1/2 baseline
commit `fe334e5`). Each test describes an *intended* feature surface that
the current module only partially (or differently) implements.

هذه الاختبارات التسعة تصف ميزات لم تُنفَّذ بعد. لم تُحذف ولم تُعلَّم skip —
تُترك كسجل للثغرات حتى يُقرَّر تنفيذ الميزة أو تحديث الاختبار.

Per the cleanup decision: **documented and left as-is** — neither deleted
nor `skip`-marked, and the feature is not guessed/implemented here.

## The 9 tests — الاختبارات

| Test file | Imports (missing) | Module | What the module has instead |
|---|---|---|---|
| `tests/test_agent_os.py` | `AgentStatus`, `clear_for_test`, `is_tool_allowed`, `kill_agent`, `new_card` | `auto_client_acquisition.agent_os` | `AgentLifecycleState`, `clear_agent_registry_for_tests`, `tool_allowed_mvp`, `agent_card` |
| `tests/test_audit_export.py` | `AuditEventKind`, `record_event`, `list_events`, `clear_for_test` | `auto_client_acquisition.auditability_os.audit_event` | `AuditEvent`, `audit_event_valid` only |
| `tests/test_benchmark_os.py` | `aggregate_with_k_anonymity`, `generate_readiness_report`, `is_k_anonymous` | `auto_client_acquisition.benchmark_os` | `anonymize_label`, `benchmark_engine`, `report_generator` |
| `tests/test_evidence_control_plane.py` | `build_control_graph` | `auto_client_acquisition.evidence_control_plane_os.evidence_graph` | `mini_evidence_chain_complete`, `MINI_CHAIN_KEYS` |
| `tests/test_market_power_os.py` | `MarketPowerDimensions`, `PartnerGateSignals`, `compute_market_power_score`, … | `auto_client_acquisition.market_power_os` | `category_metrics`, `inbound_quality`, `language_drift_score` |
| `tests/test_operating_empire_os.py` | `PartnerGateSignals` | `auto_client_acquisition.market_power_os` | (same as above) |
| `tests/test_qualification.py` | `Decision`, `qualify` | `auto_client_acquisition.sales_os.qualification` | `QualificationVerdict`, `qualify_opportunity` (different signature) |
| `tests/test_secure_agent_runtime.py` | `RuntimeState`, `can_transition`, `check_all_boundaries`, … | `auto_client_acquisition.secure_agent_runtime_os` | `AgentRuntimeState`, `evaluate_runtime_state`, `*_boundary_ok` |
| `tests/test_trust_pack.py` | `assemble_trust_pack` | `auto_client_acquisition.trust_os.trust_pack` | `ENTERPRISE_TRUST_SECTIONS`, `TRUST_PACK_MARKDOWN_PATH` (constants only) |

## Resolution options — خيارات المعالجة

For each, a future change should pick **one**:

1. **Implement the feature** — add the missing symbols so the module
   matches the test contract (the test then becomes the spec).
2. **Update the test** — rewrite the test against the module's actual API
   (only if the module's API is the intended one).

Until then these 9 files are excluded from a clean `pytest` collection.
`tests/test_qualification.py` is confirmed *not* a simple rename: the
module's `qualify_opportunity` takes `icp`/`risk` dataclasses, while the
test expects boolean keyword flags — a genuinely different design.
