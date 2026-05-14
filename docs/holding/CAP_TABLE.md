# Cap Table — Dealix Group

> Machine-readable mirror: `data/cap_table.json`.
> Public API: `GET /api/v1/holding/cap-table/public` returns **ratios
> only**; absolute amounts are NEVER on the public surface.

## Initial State

| Holder | Class | Ratio | Vesting | Notes |
|---|---|---:|---|---|
| Founder | Common | 90.0% | Full vested | Sole founder at inception. |
| Reserved Option Pool | Pool | 10.0% | Unallocated | Reserved for the first three hires (see `docs/funding/FIRST_3_HIRES.md`). |

Ratios sum to 100.0%.

## Rules

1. **Ratios only in public.** Absolute share counts and price per share
   are never disclosed in `/api/v1/holding/cap-table/public`. The
   safety test `test_cap_table_public_is_amount_safe.py` blocks
   regressions.

2. **No phantom equity.** Every line is real equity, real options, or
   real warrants. No notional placeholders.

3. **Doctrine pinning.** Any change to the cap table is recorded
   alongside the doctrine version under which it was made.

4. **Capital Asset on every change.** Every cap-table change registers
   a Capital Asset entry of type `governance_rule` describing the
   change rationale. No description leaks counterparties.

## Changes

Append-only. Recorded in `data/cap_table.json` under `changes`. The
public surface aggregates ratios at the time of the request.

## Verification

- `tests/test_cap_table_public_is_amount_safe.py` — public projection
  has no SAR amount, no USD amount, no integer > 100 (ratios are
  fractions in 0..100; absolute share counts are typically thousands+).
- `tests/test_cap_table_ratios_sum_to_100.py` — the ratios sum to
  exactly 100.0%.
