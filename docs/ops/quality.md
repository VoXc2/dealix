# Quality engineering — runbook

This document codifies the quality regime: what runs where, who owns it,
and how to react when a check fails.

## Static analysis pipeline

| Check | Tool | Trigger | Owner |
| --- | --- | --- | --- |
| Lint | `ruff` | Pre-commit + CI | Platform |
| Format | `ruff format` | Pre-commit | Platform |
| Type-check (lenient) | `mypy` | CI | Platform |
| Type-check (strict on subset) | `mypy --strict` per `pyproject.toml` overrides | `make mypy-strict` + CI on touched files | Platform |
| Custom security rules | `semgrep --config .semgrep/dealix.yaml` | `.github/workflows/security_lint.yml` | Platform |
| Bandit security | `bandit -ll -ii` | `.github/workflows/security_lint.yml` | Platform |
| Secret scan | `gitleaks` | Pre-commit + push protection | Platform |
| OpenAPI lint | `spectral lint` | `.github/workflows/api_lint.yml` on PR touching api/ | Platform |

## Coverage gate

`pytest --cov-fail-under=70` for the `api/`, `core/`, `db/`,
`integrations/` packages. Coverage uploads to Codecov; CI hard-fails on
upload error (after the P0.2 fix).

## Mutation testing — quarterly drill

Mutation testing complements line coverage: it changes a single operator
in production code and re-runs the test suite to see whether tests still
fail. A passing mutated suite means the test missed a case.

Cadence: every quarter (Q1 = Feb, Q2 = May, Q3 = Aug, Q4 = Nov).

```bash
make mutmut                       # runs against core/ + api/security/
mutmut results                    # surviving mutants list
mutmut show <id>                  # inspect a survivor
```

The output is captured in `docs/ops/mutmut/<YYYY-MM-DD>.txt` as part of
the quarterly drill. Any survivor that maps to a security-critical path
opens a P1 issue; survivors elsewhere go to a "test improvements"
backlog.

We do **not** gate CI on mutation testing — it's too slow. The drill is
the discipline.

## Performance budgets

| Check | Tool | Where | Budget |
| --- | --- | --- | --- |
| k6 smoke | `k6 run tests/perf/k6_smoke.js` | `.github/workflows/perf.yml` on PR + Mondays | p95 < 500 ms, error < 1 % |
| Locust scenarios | `locust -f locustfile.py` | `make perf` (manual) | 50 VUs / 1 min, p95 < 500 ms |

A failed performance budget blocks merge. The fix is usually a query
index or an n+1; the workflow attaches the API log on failure for triage.

## Code-style ceiling

- Line length: 100 (Ruff default override).
- Bilingual docstrings: English primary, Arabic where it adds clarity.
- No `print`, no `eval`, no `requests` — enforced via Semgrep.
- No `except Exception:` without `# noqa: BLE001` + a logger.exception
  comment explaining why the boundary handler is justified.

## Reacting to a CI failure

1. **Read the failing job, not the summary.** GitHub status checks are
   summaries — the cause is in the log.
2. **Reproduce locally** via the matching `make` target before pushing
   a "fix" commit. CI loops are expensive.
3. **If the failure is a budget regression**: open the artifact, look at
   the slowest endpoint, fix the query or add the right index.
4. **If it's a Semgrep error**: don't suppress globally — either justify
   the exception with a `# noqa` comment that documents the why, or fix
   the underlying issue.
5. **If it's a CodeQL alert** (separate workflow): assign to Platform
   and prioritise per severity.
