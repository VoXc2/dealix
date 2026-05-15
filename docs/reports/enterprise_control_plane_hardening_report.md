# Enterprise Control Plane Hardening Report

**Branch:** `claude/enterprise-control-plane-hardening-z8Qst`
**Date:** 2026-05-15

---

## Summary

The repository was hardened in five passes: the API import chain was
repaired, the test suite was unblocked (it had been aborting at collection
for every run), cross-module contract mismatches were reconciled, the
lint debt was cleared, and a dedicated CI gate was added.

The planning brief referred to an "Enterprise Control Plane / Systems
26-35" built from modules (`control_plane_os`, `agent_mesh_os`,
`assurance_contract_os`, …) that **do not exist** in the repository, and
claimed missing infrastructure (frontend, migrations, CI) that in fact
**already exists** (`frontend/` is a Next.js 15 app, `db/migrations/` has
11 Alembic migrations, `.github/workflows/` has 18 workflows). Per the
project owner's decision, this work **completed the existing repository**
rather than building new systems.

## Pass 1 — API import chain (commit `7934d6e`)

`from api.main import app` failed on genuine code-compatibility gaps:

- `value_os/value_ledger.py` had no event model — added `ValueEvent`
  (carries `tenant_id`), `ValueDisciplineError`, tier discipline, and a
  JSONL-backed `add_event`/`list_events`/`summarize`/`clear_for_test`.
- `governance_os/runtime_decision.py` had no `decide` — added
  `RuntimeDecision` + `decide(action, context)`.
- `data_os` lacked the surface the router consumes — added
  `import_preview.preview`, `data_quality_score.compute_dq`,
  `source_passport.validate`.

## Pass 2 — Test-collection unblock (commits `f4d90dd`, `689e0d3`)

`python -m pytest` aborted the **entire** session: 11 test files failed
at import time, and pytest aborts collection on any such error. Zero
tests ran. Each missing symbol was implemented against its test contract:

| Module | Added |
|---|---|
| `agent_os` | `AgentStatus`, `new_card`, `kill_agent`, `is_tool_allowed`, `clear_for_test` (re-exports of existing logic) |
| `secure_agent_runtime_os` | `RuntimeState` + boundary checkers re-exported; `activate_kill_switch` signature extended |
| `auditability_os` | `AuditEventKind`, JSONL `record_event`/`list_events`, `evidence_chain.build_chain` |
| `evidence_control_plane_os` | `ControlGraph` + `build_control_graph`, `EvidenceRecord` store |
| `market_power_os` | re-exported `MarketPowerDimensions`, `PartnerGateSignals` + 5 functions |
| `capital_os` | `CapitalAsset`, `add_asset`, `list_assets` |
| `benchmark_os` | `is_k_anonymous`, `aggregate_with_k_anonymity`, `generate_readiness_report` |
| `trust_os` | `assemble_trust_pack` (11-section Trust Pack) |
| `sales_os` | `qualify` + `Decision`, `QualificationResult` |

Result: **4,011 tests collect with zero collection errors.**

## Pass 3 — Contract reconciliation (commit `c69bd29`)

Running the unblocked suite surfaced 4 cross-module mismatches, all
fixed: `PassportValidation.missing`; `audit_draft_text` now flags bare
"we guarantee" / "نضمن"; `delivery_sprint` step5 lowercases the
governance decision; `qualify()` accepts the router's `sector`/`city`
fields and gained `to_dict()`; `capital_ledger.add_asset` accepts the
`delivery_sprint` caller's full argument set.

## Pass 4 — Lint cleanup (commit `a934287` + follow-up)

`ruff` reported 1,104 issues. 966 were auto-fixed (unused-noqa, import
order, `datetime.UTC`, `__all__` sorting). The remaining ~138 were
resolved manually, including genuine bugs (`F821` undefined names,
`F811`/`F823`).

## Pass 5 — CI gate (commit `f4d90dd`)

Added `.github/workflows/enterprise-control-plane.yml` (compile, API
import, ruff, collection check, verification script). Fixed
`scripts/revenue_os_master_verify.sh` to invoke `python -m pytest`.

## Verification

`bash scripts/verify_enterprise_control_plane.sh` →
`ENTERPRISE CONTROL PLANE: PASS`.

| Check | Status |
|---|---|
| Compile (`api`, `auto_client_acquisition`, `core`, `integrations`) | PASS |
| API import (`from api.main import app`) | PASS |
| Test collection — 0 collection errors | PASS (4,011 collected) |
| Ruff (`api auto_client_acquisition core integrations`) | PASS |
| In-scope module suites (~120 tests) | PASS |

## Pre-existing failures — out of scope

Once the suite ran, ~52 failures + 8 errors appeared in subsystems
unrelated to this work: PDPL consent suppression, the LLM-router
fallback, API-key auth middleware, DB-backed features (referral program,
tenant theming, sector intel, the PG event store), and landing-page
content scanners. These were **confirmed pre-existing** — they fail
identically on `main` — and were masked only because collection had
never succeeded on this branch. They are a separate QA workstream:
several require a live database; the content scanners require landing
copy edits.

## Premise gap — Systems 26-35

Modules `control_plane_os`, `agent_mesh_os`, `assurance_contract_os`,
`sandbox_os`, `org_graph_os`, `human_ai_os`, `value_engine_os`,
`self_evolving_os` do not exist and `api/main.py` wires no "Systems
26-35". Governance/control capability is instead spread across existing
modules (`evidence_control_plane_os`, `institutional_control_os`,
`secure_agent_runtime_os`, `governance_os`, `auditability_os`,
`agent_os`). Building the named systems would be a separate product
workstream.

## Recommended next steps

1. Triage the ~52 pre-existing failures — provision a test database for
   the DB-backed suites; fix or update the PDPL / LLM-router / auth logic.
2. Refresh landing-page copy so the forbidden-claim scanners pass.
3. Decide whether "Systems 26-35" become a real workstream or the
   capability stays distributed across the existing modules.
