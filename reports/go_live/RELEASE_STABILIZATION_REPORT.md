# Dealix Release Stabilization Report — 2026-09-09

Status: **DRAFT / HOLD / NOT PRODUCTION GREEN**

## Scope

Canonical P0 release-trust repair after the 2026-09-09 acceptance run produced false-green labels despite real Python and Web failures.

Branch: `fix/release-trust-fail-closed-20260909-chatgpt`  
Base main: `53d193d505315eea3153719d914112e50865384e`

## Fresh live evidence at start

- GitHub `main` was still exactly `53d193d505315eea3153719d914112e50865384e`.
- No open pull requests were observed before this repair branch was created.
- No remote `release-trust` repair branch existed; the earlier VPS repair branch was local-only.
- Repository rulesets visible to the connected integration were disabled; classic branch-protection state could not be read because the integration lacks that administration endpoint.
- Railway production had a staged patch with **62 changes**. It was not applied.
- Railway Web current-main deployment records for `53d193d...`, `a203545...`, and `d5b70d...` were `SKIPPED`; the latest actual successful Web release was an older commit.
- Railway API current-main deployment records were also `SKIPPED`; the latest actual API deployment shown in production status was `FAILED` and older than current main.
- GitHub commit status showed Railway Web/API contexts as success for current main while Railway deployment records were `SKIPPED`. Treat commit-status success as insufficient release-parity evidence.

## False-green incident

The supplied VPS acceptance evidence contained:

```text
196 failed, 9091 passed, 29 skipped, 16 xfailed, 10 errors
PYTHON_TESTS=PASS
```

and Web verification contained a TypeScript error in `apps/web/app/manifest.ts` followed by:

```text
WEB_ACCEPTANCE=PASS
```

The exact ad-hoc VPS wrapper that emitted those labels was not found in repository code by literal search. Therefore this branch hardens the reusable repository release path and adds a generic fail-closed gate rather than pretending the external pasted orchestration was already fixed in place.

## Repairs prepared on this branch

### Acceptance truth

- Added `scripts/ops/fail_closed_gate.sh`.
- The wrapper emits `LABEL=PASS` only for real exit code 0 and propagates non-zero exit codes.
- Added `tests/test_fail_closed_gate.py` to prove Python/Web failures cannot be relabelled PASS.
- Hardened `.agents/skills/dealix/release-engineer/SKILL.md` so required validation no longer uses `|| true` and explicitly preserves pipeline producer status.

### Web / PWA

- Replaced invalid single manifest icon purpose `"any maskable"` with separate `"any"` and `"maskable"` entries.
- Exact Node 20/22 `npm ci -> typecheck -> build` is still required before merge recommendation can change from HOLD.

### Living Fleet

- Replaced owner-command accidental word splitting with structured argv execution.
- Kept the owner command constrained to the registry-controlled `.venv/bin/python scripts/*.py ...` shape; no `eval` was introduced.
- Removed the unused council timer.
- Replaced the quoted one-path pseudo-loop with one exact pending-job move.
- Added `tests/test_living_fleet_shell_safety.py`, including ShellCheck execution when available.
- Existing Living Fleet lifecycle/concurrency/crash-recovery tests remain required.

### Brand truth

- Preserved the ban on unsupported first-in-market / market-leading claims while removing literal prohibited phrases from negation-only prose in `docs/BRAND_PRESS_KIT.md` that a context-insensitive scanner classified as a positive claim.
- Both brand verifiers still need exact-branch execution before this is considered resolved.

### Commercial contract drift

The historical Wave6 tests still enforced `499 SAR / 7 days / refund` semantics even though `scripts/dealix_pilot_brief.py` explicitly declares that contract retired and now requires a customer-specific quote evidence reference for a non-binding 30-day Pilot scope.

- Updated `tests/test_wave6_pilot_brief.py` to the current quote-only 30-day authority.
- The updated tests explicitly ensure legacy amounts are rejected and no send/payment/execution authority is granted.

### Delivery fixture drift

Current delivery workspace code correctly blocks real workspaces without commercial handoff evidence. Several old tests attempted to create real-looking workspaces with no handoff, causing fixture errors before assertions.

- Updated delivery workspace, acceptance-criteria, and proof-pack fixtures to use the explicit `synthetic_test=True` lane with `dry-run-*` slugs.
- Added a negative check that a real workspace without commercial handoff is rejected.

### AI Workforce ownership drift

`AgentTask.canonical_owner` is now required so historical specialist roles remain bounded under the five canonical agents. The policy test factory had not been updated.

- Updated the AI Workforce policy fixture to provide a canonical owner.
- Compliance guard is explicitly owned by `dealix-pm` in its test case.

### Operator/agent authority drift

Aligned active operator text with already-current tests and commercial doctrine:

- sales: quote authority is not payment execution authority;
- PM: verified revenue requires payment evidence; primary company WIP = 1;
- delivery: invoice != payment made explicit;
- TODAY page: 30-Day Revenue Command Pilot, payment-request gate, and action-specific production approval made explicit.

## Validation state

The connected GitHub/Railway tools used for this repair do not provide a shell runner for this private repository. Therefore no local test command is claimed as executed by this report.

Required exact-head validation remains:

1. `shellcheck scripts/ops/living_fleet_dispatch.sh scripts/ops/fail_closed_gate.sh`
2. targeted pytest:
   - `tests/test_fail_closed_gate.py`
   - `tests/test_living_fleet_shell_safety.py`
   - Living Fleet acceptance/concurrency/crash-recovery suites
   - `tests/test_wave6_pilot_brief.py`
   - delivery workspace/acceptance/proof-pack suites
   - `tests/test_ai_workforce_policy.py`
   - `tests/test_active_operator_commercial_authority.py`
3. brand/truth verifiers
4. Node supported runtime (20 or >=22): `npm ci`, `npm run typecheck`, `npm run build`
5. broader canonical Python suite with truthful exit-code propagation

Any skipped gate must be reported as `SKIPPED_ENVIRONMENT` or `BLOCKED_ENVIRONMENT`, never PASS.

## Production safety

No merge, Railway deploy, staged-patch apply, DNS mutation, DB mutation, secret mutation, payment, publish, or customer send was performed.

`PRODUCTION_GREEN=false`

## Merge recommendation

**HOLD** until exact-head validation demonstrates the branch is clean. After that, merge still requires action-bound founder authority. Railway parity must be established only after merge/current-main acceptance and after the 62 staged production changes are inspected/reconciled rather than applied blindly.

## Next evidence sequence

`branch exact-head tests -> PR checks -> exact-head acceptance receipt -> action-bound merge -> fresh main -> inspect Railway staged diff -> governed current-main deploy -> release SHA parity -> front-door/API acceptance -> only then reconsider PRODUCTION_GREEN`
