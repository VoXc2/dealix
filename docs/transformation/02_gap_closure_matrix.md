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

## Acceptance policy

- Every closure must produce:
  - Artifact path
  - Owner
  - KPI impact
  - Risk impact
  - Verification output
- Any closure without measurable KPI linkage is considered incomplete.
