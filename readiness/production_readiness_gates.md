# Production Readiness Gates

The ordered gates a control-plane change must clear before it ships.
The verify script enforces gates 1–5; gates 6–8 are organisational.

| # | Gate | Enforced by | Blocking? |
|---|---|---|---|
| 1 | Code compiles | `python -m compileall api auto_client_acquisition` | yes |
| 2 | API imports clean | `python -c "from api.main import app"` | yes |
| 3 | Control modules lint clean | `ruff check` (control-plane scope) | yes |
| 4 | 10 proof tests pass | `pytest tests/test_*control_plane*` + 8 more | yes |
| 5 | End-to-end flow passes | `tests/test_enterprise_control_plane_e2e.py` | yes |
| 6 | CI green on the PR | `.github/workflows/enterprise-control-plane.yml` | yes |
| 7 | No new doctrine violation | founder review (11 non-negotiables) | yes |
| 8 | Scorecard updated | `readiness/enterprise_control_plane_scorecard.md` | yes |

## Single command

```
bash scripts/verify_enterprise_control_plane.sh
```

Gates 1–5 fail fast inside that script. A change that cannot make the
script print `ENTERPRISE CONTROL PLANE: PASS` does not ship.

## Doctrine guards (always on, never weakened)

- No external send / charge / scrape without human approval.
- Approval-required and forbidden tools cannot be auto-executed.
- Rollback and self-evolving "apply" are approval-gated.
- Every operational object carries a `tenant_id`.
- Measured value requires a `source_ref`.
