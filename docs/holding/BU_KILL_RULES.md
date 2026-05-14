# BU Kill Rules — Dealix Group

> Canonical code:
> `auto_client_acquisition/holding_os/unit_governance.py:evaluate_unit_decision()`.
>
> The rules listed here MIRROR the code branches. Doctrine-as-code
> test `tests/test_bu_kill_rules_match_unit_governance.py` enforces
> parity — any commit that adds a rule here without updating the code
> (or vice-versa) fails CI.

## Rule 1 — Governance Risk

If `governance_risk_acceptable == False` → recommend `HOLD`.

A BU whose governance posture is not acceptable cannot scale. HOLD
buys time to fix the governance gap. It is **not** a kill, but it
removes the BU from `landing/group.html` until the gate is cleared.

## Rule 2 — Client Health

If `client_health_ok == False` → recommend `PILOT`.

A BU losing client confidence drops to PILOT — it can continue running
small engagements but cannot expand.

## Rule 3 — Kill Threshold

If `qa_score < 55` AND `revenue_growing == False` → recommend `KILL`.

This is the kill rule. Both conditions must be true. Either alone is
not sufficient.

## Rule 4 — Spinout Eligibility

If `venture_signal_strong` AND `module_usage_growing` AND
`qa_score >= 85` → recommend `SPINOUT`.

Strong-signal BUs leave the holding to become independent ventures.
Spinout requires a board memo + new BU charter at the spinout target.

## Rule 5 — Scale Eligibility

If `revenue_growing` AND `margin_ok` AND `qa_score >= 80` AND
`retainers_growing` → recommend `SCALE`.

All four required. Missing any → next rule.

## Rule 6 — Build Eligibility

If `playbook_maturity_ok` AND `proof_delivery_on_track` →
recommend `BUILD`.

The BU is operating but not yet ready to scale.

## Rule 7 — Default

Otherwise → recommend `PILOT`.

## Reversal Policy

A KILL decision is **not** reversed without:

1. A board memo that explicitly references which kill rule triggered.
2. Evidence that the triggering condition has changed (e.g.,
   qa_score now >= 80 over three consecutive months).
3. A new Capital Asset entry registering the reversal rationale.

## What "Kill" Means Operationally

When a BU's status is set to `KILL` via `register_business_unit.py`:

1. The BU is removed from `landing/group.html` (PR13 portfolio filter).
2. The BU is removed from `/api/v1/holding/portfolio` aggregations
   except in the by_status count.
3. The BU's public-facing endpoint
   (`/api/v1/business-units/<slug>/public`) still returns 200 with
   status `KILL` — partners with stale links see the honest state.
4. The BU's charter file remains in the repository (no deletion) as a
   permanent record. An "Archived:" header line should be added
   manually by the founder.

## Verification

- `tests/test_bu_kill_rules_match_unit_governance.py` — every branch
  in `evaluate_unit_decision()` is documented here, and every rule
  here has a code branch.
- `tests/test_business_unit_registry.py` (PR10) — KILL entries
  require a non-empty reason.
