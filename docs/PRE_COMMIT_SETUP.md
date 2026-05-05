# Pre-commit hooks — setup

Dealix uses [pre-commit](https://pre-commit.com) to enforce hygiene
+ policy on every local commit. The same checks run in CI, so a
clean `git commit` is also a clean PR.

## One-time install

```bash
pip install pre-commit
pre-commit install
```

## What each hook prevents

| Hook | Prevents |
|---|---|
| `trailing-whitespace` | sloppy diffs |
| `end-of-file-fixer` | files without trailing newline |
| `check-yaml` | invalid YAML in any committed file |
| `check-json` | invalid JSON in any committed file |
| `check-added-large-files` | accidentally committing >1MB blobs |
| `check-merge-conflict` | leaving `<<<<<<<` markers in a file |
| `ruff` + `ruff-format` | style drift |
| `mypy` | type drift (excluded for tests/ + dashboard/) |
| `bandit` | obvious Python security issues |
| `gitleaks` | accidentally committed API keys / Stripe keys |
| `verify-service-readiness-matrix` | fake-`live` services or forbidden marketing claims in YAML |
| `export-service-readiness-json` | YAML edits that don't regenerate the committed JSON snapshot |

## Manual run

```bash
pre-commit run --all-files
```

## When a hook fails

- If `verify-service-readiness-matrix` fails: read its message; fix
  the YAML (gates are missing, status is fake, or a forbidden phrase
  leaked in).
- If `export-service-readiness-json` fails: the JSON snapshot is out
  of date. Run `python scripts/export_service_readiness_json.py` and
  re-stage.
- If `gitleaks` fails: a real or test-shaped secret crept in. Move
  it to `os.getenv(...)` and rotate if it ever hit a real value.
- **NEVER use `--no-verify`**. If a hook is wrong, fix the hook in
  a separate PR. The hooks are policy.

## CI mirror

`.github/workflows/ci.yml` runs the same `verify_service_readiness_matrix.py`
+ `seo_audit.py` + the full pytest bundle, so green-locally =
green-in-CI for the most part.
