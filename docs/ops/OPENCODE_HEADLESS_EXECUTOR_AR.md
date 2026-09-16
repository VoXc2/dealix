# Headless OpenCode Executor — real-runtime repair

## Symptom

Autonomous jobs `JOB-20260912T055405-9900001` and `JOB-20260912T055932-7720001`
timed out `RC=124` after the full `TIME_BUDGET` with empty stdout/stderr. The
runtime log reached `message=init` and then stopped: no `created` session, no
`loop`, no `stream`, no error.

## Root cause (lock / control path)

`execute_opencode` launched `opencode run` against the **shared interactive
control path** (`/root/.local/share/opencode/opencode.db`, snapshot repo). Under
concurrent OpenCode instances (interactive TUIs + other jobs) the first write —
session creation, immediately after `init` — blocks on that single SQLite write
lock. With no output watchdog and an inherited stdin, the run looked identical
to a very slow one until the whole budget elapsed: `RC=124`, zero bytes.

A second, fail-open bug: `--auto` was appended only when the hardened permission
policy file existed. If the policy was missing on a host, the run launched
**without** `--auto` and would wait forever on a permission `ask`.

## Fix (smallest, fail-closed)

`scripts/ops/session_factory.py:execute_opencode` now:

1. **Isolates the control path** — sets `OPENCODE_DB` to a per-job database
   (`<session-factory state>/opencode/<JOB_ID>.db`), so session creation never
   contends on the interactive `opencode.db` lock. Auth/config still resolve
   from the normal data dir; no secret is read or copied.
2. **Refuses to launch without the hardened policy** — a missing
   `OPENCODE_PERMISSION` policy returns `rc=78` *before* spawn instead of running
   without `--auto`. An unwritable control-DB dir returns `rc=73`.
3. **Is strictly non-interactive** — `stdin=subprocess.DEVNULL`, plus
   `OPENCODE_DISABLE_AUTOUPDATE=1` and `OPENCODE_DISABLE_MODELS_FETCH=1` so no
   background fetch can stall a job.

Model selection, `OPENCODE_PERMISSION` deny set, L5 `WAITING_L5`, `DEEP_WIP_MAX=3`,
isolated worktrees, and disabled paid spill are all unchanged; there is no
external effect.

## Evidence

```bash
python3 scripts/ops/opencode_headless_canary.py --timeout 150   # -> PASS, external_effect NONE
pytest tests/test_session_factory.py tests/test_session_factory_watchdog.py -q
```

The canary runs one tiny prompt through the real `execute_opencode` path in a
throwaway dir with its own control DB; it must return `OPENCODE_HEADLESS_CANARY=PASS`.

---

## Master Prompt Binding Contract (2026-09-16)

**Canonical source-controlled prompt:**
`prompts/company/DEALIX_AUTONOMOUS_COMPANY_MASTER_EXECUTION_PROMPT_2026_09_16.md`

**SHA256:** `ba0b9d099eed236c3f6354bcdd5a7ff54146e7883237393173b8067b19431ad1`

**Binding config:**
`config/company/dealix_master_prompt_binding_v1.json`

**Runtime binding mode:** `INSTALLED_ARTIFACTS_SHA256_FAIL_CLOSED`

### Required Prompt Markers (enforced by verifier)

All of the following markers must be present in the master prompt (exact text as it appears in the Arabic/English prompt):

- `BOOTSTRAP`
- `LIVE TRUTH WINS`
- `ONE COMPANY LAW`
- `OPENCODE — DEFAULT DEVELOPMENT ENGINE`
- `ResourceGovernor`
- `PRODUCTION TRUST — P0`
- `COMMERCIAL TRUTH`
- `MEASUREMENT_NOT_PROVEN`
- `NEVER STOP RULE`
- `FIRST ACTION ON EVERY NEW CHAT`
- `لا تعتبر Merge = Deploy` (Arabic: "Don't consider Merge = Deploy")
- `لا تعتبر HTTP 200 = Production Green` (Arabic: "Don't consider HTTP 200 = Production Green")

### Agent Fleet Authority

The five permanent agents (`dealix-pm`, `dealix-sales`, `dealix-delivery`, `dealix-engineer`, `dealix-content`)
are **logical business roles / compatibility aliases only**.
The **Agentic Holding registry** (`dealix.agentic_holding.runtime.build_current_registry()`)
and **ResourceGovernor** remain the runtime fleet-size authority.

### Session Factory Integration

OpenCode jobs launched through Session Factory automatically inherit a verified
reference to the bound master prompt via:

1. **Environment variables** set by the installer launcher:
   - `DEALIX_COMPANY_MASTER_PROMPT` — path to runtime prompt
   - `DEALIX_COMPANY_MASTER_PROMPT_SHA256` — SHA256 of runtime prompt
   - `DEALIX_MASTER_BINDING_PATH` — path to runtime binding
   - `DEALIX_MASTER_BINDING_SHA256` — SHA256 of runtime binding

2. **Generated prefix context** passed to OpenCode jobs:
   - Jobs receive `master-prompt path+sha` context
   - OpenCode is instructed to read+verify the bound prompt before task instructions
   - No inlining of 843 lines — verified immutable path+hash is safer

3. **Read-only jobs** may use the same binding without increasing permissions

### Fail-Closed Verification Chain

The verifier (`scripts/commercial/verify_dealix_master_prompt_binding_v1.py`)
enforces:

- Prompt path matches `prompt_ref` in binding
- Installed runtime prompt hash equals source-controlled prompt hash
- All required markers present in prompt (exact text match)
- Source/runtime hash equality (no drift)
- No stale prompt behavior (fail closed on mismatch)
- Permanent agents are logical roles, not fleet-size authority
- Section 20 of founder prompt is conditional provider guidance, not current production authority
- Current self-host production authority preserved (not replaced by Railway/Vercel/GitHub Actions)

### Tests

```bash
pytest tests/test_dealix_master_prompt_binding_v1.py -v
python3 scripts/commercial/verify_dealix_master_prompt_binding_v1.py
```

Expected output:
```
DEALIX_MASTER_PROMPT_BINDING_V1=PASS
MASTER_PROMPT_SHA256=ba0b9d099eed236c3f6354bcdd5a7ff54146e7883237393173b8067b19431ad1
PERMANENT_AGENTS=5 (logical business roles / compatibility aliases)
```