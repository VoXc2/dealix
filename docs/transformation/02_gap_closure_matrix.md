# 02 — Gap Closure Matrix

## Objective

Close MVP and readiness gaps with explicit owner, acceptance criteria, verification command, and review evidence.

## Closure matrix

| Gap | Owner OS | Closure criteria | Verification |
|---|---|---|---|
| In-memory fallback on critical operational paths | Platform + Control Plane | Postgres-first mode with explicit fallback policy, runbook, and rollback plan | `python3 scripts/verify_global_ai_transformation.py` |
| Legacy JSONL outside critical control paths | Platform + Value + Delivery | JSONL usage cataloged with migration tier and target date | `python3 scripts/verify_global_ai_transformation.py --check-jsonl` |
| Minimal enterprise UI surfaces | Product + Frontend | Operator workflows are documented with required controls | `bash scripts/verify_enterprise_control_plane.sh` |
| Full trace coverage and telemetry contracts | Observability + Trust | Contract files and validation checks published | `python3 scripts/verify_global_ai_transformation.py --check-observability` |
| Enterprise package standardization | GTM + Trust + Delivery | Pilot package, trust pack, procurement kit, ROI narrative templated and linked | `python3 scripts/verify_global_ai_transformation.py --check-enterprise-package` |
| Mission-critical drills automation | Reliability + Runtime Safety | Drill schedules and scorecards defined with closure evidence | `python3 scripts/verify_global_ai_transformation.py --check-reliability` |

## Evidence index (repo)

| Matrix row (short) | Evidence file |
| --- | --- |
| Postgres-first / in-memory fallback | [evidence/gap_closure_in_memory_fallback.md](evidence/gap_closure_in_memory_fallback.md) |
| Legacy JSONL catalog | [evidence/gap_closure_legacy_jsonl.md](evidence/gap_closure_legacy_jsonl.md) |
| Enterprise UI surfaces | [evidence/gap_closure_enterprise_ui.md](evidence/gap_closure_enterprise_ui.md) |
| Trace / telemetry contracts | [evidence/gap_closure_trace_telemetry.md](evidence/gap_closure_trace_telemetry.md) |
| Enterprise package | [evidence/gap_closure_enterprise_package.md](evidence/gap_closure_enterprise_package.md) |
| Drills automation | [evidence/gap_closure_drills_automation.md](evidence/gap_closure_drills_automation.md) |

## Acceptance policy

- Every closure must produce:
  - Artifact path
  - Owner
  - KPI impact
  - Risk impact
  - Verification output
- Any closure without measurable KPI linkage is considered incomplete.
