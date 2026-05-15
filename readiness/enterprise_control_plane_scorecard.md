# Dealix Enterprise Control Plane Scorecard

| Layer | Required Score | Current | Evidence | Status |
|---|---:|---:|---|---|
| API import health | 100 | 100 | `python3 -c "from api.main import app"` | PASS |
| Tenant isolation | 95 | 92 | `tests/test_tenant_isolation_systems_26_35.py` | PASS |
| Control plane | 90 | 90 | run/pause/resume/trace/rollback tests | PASS |
| Approval gate | 95 | 95 | policy + rollback approval flow tests | PASS |
| Agent mesh | 90 | 90 | routing/isolation/autonomy tests | PASS |
| Assurance contracts | 95 | 95 | no contract = deny + external escalate tests | PASS |
| Runtime safety | 95 | 92 | kill switch + circuit breaker tests | PASS |
| Sandbox/replay | 85 | 40 | pending dedicated simulation/replay tests | PARTIAL |
| Org graph | 80 | 45 | pending incident impact drill coverage | PARTIAL |
| Human-AI oversight | 90 | 85 | approval queue + grant/reject tests | PARTIAL |
| Value engine | 90 | 90 | measured requires `source_ref` tests | PASS |
| Self-evolving | 90 | 90 | cannot apply without approval tests | PASS |
| Frontend control surfaces | 80 | 35 | pending admin control pages rollout | TODO |
| CI release gates | 95 | 90 | `.github/workflows/enterprise-control-plane.yml` | PASS |
