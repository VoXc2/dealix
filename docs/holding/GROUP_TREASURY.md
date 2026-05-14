# Group Treasury — Dealix Group

> Canonical computation in
> `auto_client_acquisition/operating_finance_os/*` (17 modules).
> This doc states the **rules**; the modules implement them.

## Treasury Principles

1. **One source of truth.** Cash position, runway, and BU allocations
   live in the Holding ledger. BU-level finance modules feed up; the
   Holding writes down. No parallel ledgers.

2. **Stage-gated spend.** Every spend is classified by
   `auto_client_acquisition/operating_finance_os/budget_stage.py`:
   `prove → repeat → scale`. Spend not allowed in the current stage
   is blocked at the policy layer (see `spend_allowed_for_stage()`).

3. **Margin discipline.** Margin checks live in
   `operating_finance_os/margin_by_offer.py` and
   `margin_protection.py`. Offers below the published margin floor
   trigger a `margin_protection` action.

4. **AI cost as a line item.** `ai_cost_accounting.py` +
   `model_cost_tracker.py` track USD per Proof Pack and USD per run.
   These feed the annual-report COGS section.

5. **Hiring trigger discipline.** Hiring is gated by
   `hiring_triggers.py:recommended_hire_focus()` — no role added
   before the trigger condition is met. See
   `docs/funding/FIRST_3_HIRES.md`.

## Cash Position Record

The Dealix Group cash position is recorded in a **founder-maintained
spreadsheet** (not in this repo for privacy). The annual report renders
**only ratios** (margin %, retainer attach rate, allocation share per
BU), never absolute amounts in the public version.

## Inter-BU Capital Transfers

When a unit is at `SCALE` and another is at `BUILD`:
- `SCALE` unit's surplus is the source.
- `BUILD` unit receives transfer up to a cap based on
  `capital_allocation_score.py` band (high → up to 30% of surplus;
  medium → up to 15%; low → 0%).
- Every transfer is recorded as a Capital Asset event of type
  `governance_rule` with the source / target BU slugs in the
  description. The amount is internal-only.

## Runway

`runway_months` is computed monthly using:
- Confirmed revenue (`business_metrics_board/computer.py` Article 8:
  payment_confirmed gate).
- Stage-allowed spend (`operating_finance_os/budget_stage.py`).
- AI cost forecast (`ai_cost_accounting.py`).

The runway figure is **never publicly disclosed**. The annual report
discloses qualitative runway state ("at or above the published floor
of N months") only.

## Forbidden

- Off-ledger transfers between BUs.
- Spending out of the stage's allowed bucket.
- Booking unconfirmed revenue (Article 8 violation).
- Public disclosure of absolute cash amounts.

## Verification

- `tests/test_capital_allocation_policy_matches_board_engine.py` (PR12)
  locks the policy ↔ code parity.
- The annual-report renderer (PR12) reads from the live data sources
  and is byte-stable for identical inputs (drift-gated in CI).
