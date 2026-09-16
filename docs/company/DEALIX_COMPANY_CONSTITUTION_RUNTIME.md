# Dealix Company Constitution Runtime — Index & Coverage Contract

> **Status:** Index / coverage contract over **ONE Company Machine** — not a second authority.

This document does not create a new company system, second scheduler, second brain, or independent approval/proof/economic store. It is a **read-only index** that maps the 33 governed domains in `config/company/company_constitution_registry.yaml` onto existing ONE Company Machine authorities (Omega V3, Agentic Holding, Control Plane, Sector Companies, Arm Pods) and verifies coverage.

- **Canonical source:** `config/company/company_constitution_registry.yaml`
- **Loader:** `dealix/company_constitution.py` (`load_registry()`, `validate_registry()`, `summary()`, `gap_report()`)
- **Verifier (fail-closed):** `scripts/ops/verify_company_constitution_coverage.py`
- **Tests:** `tests/test_company_constitution_coverage.py`

All domain authority reuses existing repo paths; no new domain systems are introduced.

## ONE Company Machine principle

```
Holding -> Control Plane -> Sector Companies -> Arm Pods -> Specialist Logical Agents -> ResourceGovernor-bounded runtime workers
```

- Single approval path (`dealix/governance`, `dealix/trust`, `dealix/agentic_holding/governance.py`)
- Single proof path (`dealix/commercial/proof_builder.py`, `api/routers/proof_ledger.py`)
- Single model routing policy (provider-neutral, local/free-first, no silent paid spill)
- Single scheduler inventory (`dealix/commercial/scheduler_inventory.py`)

The constitution registry is a **coverage index** that points to these authorities; it does not duplicate them.

## How to run

### Verifier

```bash
python3 scripts/ops/verify_company_constitution_coverage.py
# explicit registry
python3 scripts/ops/verify_company_constitution_coverage.py --registry config/company/company_constitution_registry.yaml
```

Exit code `0` = PASS, non-zero = FAIL. Prints concise `DEALIX_COMPANY_CONSTITUTION_COVERAGE: PASS|FAIL` summary.

Fail-closed rules (any failure → FAIL):
- missing required domains (33 required, see `dealix/company_constitution.py:REQUIRED_DOMAINS`)
- duplicate `primary_authority` (never allowed; shared reuse belongs only in `authority_paths`)
- invalid `state` or `autonomy_ceiling`
- missing/empty `evidence_refs` or `receipt_requirements`
- any local path in `authority_paths`/`evidence_inputs`/`verifier_paths`/`evidence_refs` that does not exist
- L5-sensitive domains lacking `action_bound_l5_gate: true`
- active (`IMPLEMENTED`/`PARTIAL`) production authority refs reintroducing Railway/Vercel/GitHub Actions as production runtime authority

### Tests

```bash
APP_ENV=test pytest tests/test_company_constitution_coverage.py -v
# or focused
pytest tests/test_company_constitution_coverage.py -k happy_path -v
```

Tests use temporary mutated registry files (`tmp_path`) and never modify the canonical registry.

### Other checks

```bash
python3 -m py_compile dealix/company_constitution.py scripts/ops/verify_company_constitution_coverage.py
python3 -c "import yaml; yaml.safe_load(open('config/company/company_constitution_registry.yaml'))"
python3 -c "from dealix.company_constitution import validate_registry; print(validate_registry())"
git diff --check
```

## Current state vocabulary

Allowed `state` values (see `dealix/company_constitution.py:ALLOWED_STATES`):

- `IMPLEMENTED` — live authority + verifier + evidence exist (e.g., COMMAND, REVENUE, GOVERNANCE, SECURITY, PROOF)
- `PARTIAL` — authority exists but coverage incomplete or gated (e.g., MARKETING, DISTRIBUTION, CLIENT)
- `HOLD_EXTERNAL` — requires qualified external authority (e.g., LEGAL)
- `NOT_PROVEN` — no evidence-backed implementation yet (e.g., PEOPLE, ACADEMY)
- `NOT_APPLICABLE` — intentionally out of scope for current horizon (e.g., VENTURE)

Allowed `autonomy_ceiling`:

- `L0` observe · `L1` analyze · `L2` draft · `L3` internal execute · `L4` repo execute with acceptance · `L5` exact-action-bound only

`action_bound_l5_gate` is `true` for L5-sensitive domains: `COMMAND, REVENUE, MARKETING, DISTRIBUTION, CLIENT, SECURITY, PRIVACY, TAX, LEGAL, PROCUREMENT, PARTNER, B2G, GOVERNANCE, VENTURE`.

## Related authorities

- `config/company/dealix_operating_constitution.json`
- `config/company/dealix_control_kernel_v2.json`
- `config/company/dealix_omega_master_v3.json`
- `config/company/dealix_arm_registry.json`
- `docs/company/DEALIX_CONSTITUTION.md`
- `docs/company/DEALIX_SOVEREIGN_OPERATING_MODEL.md`

## Notes

- No hardcoded SHA, provider, agent count, price, duration, or compliance claim is present in registry/loader/verifier.
- No production/DB/DNS/secrets/provider/external effects are performed by verifier or loader.
- Every domain has a unique `primary_authority`. Shared underlying components may appear only as secondary `authority_paths`; there is no duplicate-primary escape hatch.
