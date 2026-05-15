# Enterprise Control Plane Hardening Report

**Phase:** 1 — Stability
**Branch:** `claude/enterprise-control-plane-hardening-z8Qst`
**Date:** 2026-05-15

---

## What was broken

`from api.main import app` failed. The blocking import errors, in order of
discovery, were genuine code-compatibility gaps (not just missing pip
dependencies):

1. **`auto_client_acquisition.value_os.value_ledger`** exposed only
   `ValueLedgerEvent` / `value_ledger_event_valid`, but
   `value_os.monthly_report`, `api/routers/value_os.py`, and
   `tests/test_value_os.py` import `ValueEvent`, `ValueDisciplineError`,
   `add_event`, `list_events`, `summarize`, and `clear_for_test`. The
   value ledger had no event model, no tier discipline, and no store.

2. **`auto_client_acquisition.governance_os.runtime_decision`** had no
   `decide` function. `api/routers/data_os.py` and
   `delivery_factory/delivery_sprint.py` both call
   `decide(action=..., context=...)` and read `.decision`, `.reasons`,
   `.safe_alternative` off the result.

3. **`auto_client_acquisition.data_os`** was missing the compatibility
   surface that `api/routers/data_os.py` consumes:
   `import_preview.preview`, `data_quality_score.compute_dq`, and
   `source_passport.validate`.

## What was fixed

| Area | Change |
|---|---|
| Value ledger | Rewrote `value_os/value_ledger.py` with a `ValueEvent` dataclass (carries `tenant_id`), `ValueDisciplineError`, JSONL-backed `add_event` / `list_events` / `summarize` / `clear_for_test`, and tier sourcing discipline (`observed`/`verified` require `source_ref`; `client_confirmed` requires both refs). Kept `ValueLedgerEvent` re-export for backwards compatibility. |
| Runtime decision | Added `RuntimeDecision` and `decide(action, context)` to `governance_os/runtime_decision.py`. High-risk actions escalate; drafts with forbidden terms are blocked; cold outreach requires approval; scoring without a Source Passport degrades to review. Kept the existing `governance_decision_from_*` mapping helpers. |
| Data OS | Added `ImportPreview` + `preview()` to `data_os/import_preview.py`, `DataQualityScore` + `compute_dq()` to `data_os/data_quality_score.py`, and `PassportValidation` + `validate()` to `data_os/source_passport.py`. |
| Data OS router | `governance_decision` is now lowercased to match the router contract / tests. |
| Lint | Cleared pre-existing `RUF100` directives in `api/routers/value_os.py`. |
| Verification | Added `scripts/verify_enterprise_control_plane.sh`. |

## Verification status

`bash scripts/verify_enterprise_control_plane.sh` prints
`ENTERPRISE CONTROL PLANE: PASS`.

| Check | Status | Evidence |
|---|---|---|
| Compile health | PASS | `python -m compileall api auto_client_acquisition` |
| API import health | PASS | `python -c "from api.main import app"` |
| Lint (stabilized modules) | PASS | `ruff check` — all checks passed |
| Targeted tests | PASS | 25 passed (`value_os`, `data_os_*`, `governance_runtime_decision`) |

## Premise gap — Systems 26-35

The broader hardening plan (tenant sweep, control-plane rollback flow,
agent mesh, assurance contracts, runtime safety, sandbox, org graph,
human-AI oversight, value engine, self-evolving) assumes modules named
`control_plane_os`, `agent_mesh_os`, `assurance_contract_os`,
`sandbox_os`, `org_graph_os`, `human_ai_os`, `value_engine_os`, and
`self_evolving_os`.

**None of these modules exist in the repository**, and `api/main.py`
does not wire any "Systems 26-35". Related modules that *do* exist:
`evidence_control_plane_os`, `institutional_control_os`,
`secure_agent_runtime_os`. Building the named systems would mean
authoring entirely new subsystems — which the plan's own master prompt
explicitly forbids ("Do not add new futuristic systems").

## What remains MVP / not done

- In-memory and JSONL stores remain the dev backend; no Postgres ledger.
- No `tenant_id` sweep across other operational schemas (only the value
  ledger carries it so far).
- No end-to-end governed-workflow proof, because the control-plane /
  agent-mesh / assurance-contract modules it would exercise do not exist.
- No frontend control surfaces.
- No dedicated CI workflow for this gate.

## Next milestones

1. Decide whether Systems 26-35 are to be **designed and built** (a new
   product workstream) or whether the hardening plan should be re-scoped
   to the modules that actually exist.
2. If building: start with `control_plane_os` (workflow run registry +
   control events) and `assurance_contract_os`, since the rest depend on
   them.
3. Tenant-awareness sweep once the target schemas exist.
4. Postgres persistence + repositories.
5. Frontend control surfaces and a dedicated CI gate.
