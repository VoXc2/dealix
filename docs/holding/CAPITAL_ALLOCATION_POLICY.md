# Capital Allocation Policy — Dealix Group

> Canonical code: `auto_client_acquisition/board_decision_os/capital_allocation_board.py`.
> The rules in this document mirror the buckets in code. Doctrine-as-code
> test (PR12) asserts parity.

## Six Allocation Decisions

Every investment proposal — feature build, hire, acquisition, BU spin-up
— is routed to exactly one bucket. The decision is recorded in the
group's monthly board memo (PR14).

### 1. `must_fund`

Things that **must** be funded because they are the operating spine.
Examples on disk:
- `proof_pack_generator`
- `source_passport`
- `governance_runtime`
- `revenue_intelligence_sprint`
- `board_memo_generator`

Rule: must_fund items override hiring caps. Cuts to must_fund require
a board memo with explicit risk acknowledgment.

### 2. `should_test`

Things that look promising but need a small allocation + a learning
target. Examples on disk:
- `client_workspace_mvp`
- `approval_center`
- `monthly_value_report`
- `partner_referral_program`

Rule: each `should_test` item must publish a learning report within
30 days of funding. Items without a learning report are demoted to
`hold` at the next board cycle.

### 3. `hold`

Things deferred until a clearer trigger fires. Examples on disk:
- `academy_portal`
- `marketplace`
- `white_label`
- `complex_rbac`

Rule: `hold` items consume zero capital. A `hold` item becomes
`should_test` only when a buyer / partner request makes the case.

### 4. `kill`

Things explicitly forbidden by doctrine. Examples on disk:
- `scraping_engine`
- `cold_whatsapp_automation`
- `guaranteed_sales_claims`
- `sourceless_chatbot`

Rule: any commit that names a `kill` item as a feature blocks CI
(see `tests/test_no_forbidden_features_in_diff.py` from PR4).

### 5. `spinout` (BU-level)

A unit at the `SCALE` status with strong venture signal + module-usage
growth + QA >= 85 is eligible for spinout per
`auto_client_acquisition/holding_os/unit_governance.py`.

Rule: spinout requires a board memo + a new BU charter at the
spinout-target group. Doctrine adoption is mandatory.

### 6. `acquire` (BU-level)

External targets that meet the Acquisition Thesis (PR14).

Rule: acquisitions require ALL of: doctrine compatibility, evidence
inheritability, capital fit. See `docs/holding/ACQUISITION_THESIS.md`.

## Allocation Cycle

Monthly:
1. Each BU produces a `UnitMonthlySnapshot` (per `unit_governance.py`).
2. `evaluate_unit_decision()` recommends SCALE / BUILD / PILOT / HOLD /
   KILL / SPINOUT.
3. The board reviews recommendations.
4. Final decisions update `data/business_units.json` via
   `scripts/register_business_unit.py --update-status`.
5. The annual-report renderer (`scripts/render_annual_report.py`) folds
   the year's decisions into the group narrative.

## Verification

- `tests/test_capital_allocation_policy_matches_board_engine.py` asserts
  this document enumerates the same buckets as `CAPITAL_BOARD_BUCKETS`
  in code.
- Any commit that adds a bucket here without updating the code (or
  vice versa) fails CI.
