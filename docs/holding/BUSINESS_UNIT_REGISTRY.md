# Business Unit Registry — Dealix Group

> Machine-readable source of truth: `data/business_units.json`.
> Status values (enum):
> `SCALE | BUILD | PILOT | HOLD | KILL | SPINOUT`
> Reuses `auto_client_acquisition/holding_os/unit_governance.py:UnitPortfolioDecision`.

This document is the **human-readable view** of the BU inventory. The
machine-readable JSON is the canonical source — re-render this document
when a BU is added or changes status.

## Active Operating Units

| Slug          | Name             | Status   | Owner    | KPI                                    | Doctrine | Charter                                  |
|---------------|------------------|----------|----------|----------------------------------------|----------|------------------------------------------|
| `core-os`     | Dealix Core OS   | `BUILD`  | founder  | MRR + Proof Packs per month            | v1.0.0   | `docs/holding/units/dealix-core-os.md`   |

## Piloted Units

_(none yet — register via `scripts/register_business_unit.py`)_

## On-Hold Units

_(none — the verifier blocks any HOLD without a documented reason)_

## Killed / Spun-Out Units

_(none — kill decisions require a board memo)_

## Planned Future Units (Not Yet Registered)

These names are reserved by Brand Architecture (PR13). They are **not**
operating units until registered:

- `Dealix Sprint Delivery` — would split out once sprint volume
  justifies a dedicated owner.
- `Dealix Trust Services` — audit / evidence productization.
- `Dealix Labs` — research / ventures (only after one operating BU is
  at `SCALE`).
- `Dealix Academy` — training / certification (only after a sector
  playbook has been used by ≥ 2 paying clients).

## How to Update

1. Run the register CLI with `--really-this-is-a-bu` and your change.
2. Run `python scripts/validate_business_units.py` (must exit 0).
3. Edit this document to reflect the registry.
4. Re-run the master verifier.

## Verification

- Every entry in `data/business_units.json` carries `entry_id`,
  `git_author`, `created_at`.
- `status` MUST be one of the `UnitPortfolioDecision` enum values.
- A KILL or HOLD entry MUST have a `reason` field.
- See `tests/test_business_unit_registry.py` for the locking checks.
