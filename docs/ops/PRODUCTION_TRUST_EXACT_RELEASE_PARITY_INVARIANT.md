# Production Trust — Exact Release Parity Invariant

## Invariant

`production_state=GREEN` is forbidden when Dealix has proved only endpoint reachability.

GREEN requires evidence that the public Web and API are serving the expected release identity for the current trusted repository head. A `2xx`/`3xx` response is availability evidence only and MUST NOT be promoted to release identity.

## Fail-closed states

If release identity cannot be read, cannot be compared, differs across Web/API, or differs from the expected trusted head, Production Trust must remain `UNKNOWN`, `HOLD`, `DEGRADED`, or `RED` according to the caller contract. It must not write GREEN.

## Current incident motivating this guard

On 2026-09-11 the VPS Company Autopilot reported Production GREEN from HTTP probes while independent live deployment evidence did not establish current-main Web/API release parity. This is classified as a false-green semantic defect, not as customer proof or Production Green evidence.

## Acceptance

- `pytest -q tests/test_company_autopilot_release_truth_guard.py` passes.
- `python scripts/ops/verify_canonical_company_autopilot.py` passes.
- Bash syntax and ShellCheck error-level verification pass for the canonical and delegated legacy entrypoints.
- Production probe compares immutable Web/API release SHAs with the current trusted `origin/main` SHA.
- Missing identity fails closed.
- Web/API identity disagreement fails closed.
- HTTP success without identity never writes GREEN.
- No merge, deploy, DNS, DB, secret, payment, publish, or external-send authority is implied by this change.
