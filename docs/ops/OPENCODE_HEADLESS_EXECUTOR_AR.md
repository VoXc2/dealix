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
