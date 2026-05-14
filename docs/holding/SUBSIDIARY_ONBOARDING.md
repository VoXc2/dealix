# Subsidiary Onboarding — First 90 Days

Applies equally to a newly **spun-up** BU and an **acquired** BU.
Both pass through the same gates so the doctrine moat stays intact.

## Day 0

- BU registered in `data/business_units.json` (status `BUILD` or
  `PILOT`).
- Charter file exists at `docs/holding/units/<slug>.md`.
- Doctrine adoption certificate signed (from
  `partner-kit/DOCTRINE_ADOPTION_CHECKLIST.md`).
- Owner appointed and recorded in the registry.

## Days 1–30

- Trust Pack draft published from
  `partner-kit/TRUST_PACK_TEMPLATE.md`.
- First **Capital Asset** registered via
  `scripts/register_capital_asset.py` (asset_type `governance_rule`
  with description "onboarding capital seed").
- KPI published in the BU charter (1–3 KPIs, no more).
- BU monthly snapshot inputs identified (which signals will feed
  `unit_governance.py`).

## Days 31–60

- First **Proof Pack** drafted (even if a synthetic / migration
  example for newly-acquired BUs).
- Monthly snapshot exercise begins — `UnitMonthlySnapshot` instances
  captured manually until the data pipeline lights up.
- Group endorsement line + doctrine version anchor added to every
  BU-owned public surface.

## Days 61–90

- First **board memo** drafted via `scripts/draft_bu_decision_memo.py`
  for review at the next board cycle.
- BU appears on `landing/group.html` (rendered automatically because
  status is `BUILD` / `PILOT`).
- First **Value Ledger** entry (or for acquired BUs: re-anchored
  legacy value events to Dealix's Value Ledger).

## Gates

Any of the following blocks promotion from `BUILD` to `PILOT` or
`PILOT` to `SCALE`:

- Missing doctrine adoption certificate.
- Trust Pack not published.
- Zero Capital Assets registered.
- Owner record empty in `data/business_units.json`.

These gates mirror the conservative branches of
`auto_client_acquisition/holding_os/unit_governance.py:evaluate_unit_decision()`.

## Forbidden Shortcuts

- A BU may NOT take external action (send, publish, transact) before
  Days 1–30 gates are met.
- A BU may NOT publish a case study or sector claim before its first
  Proof Pack exists.
- A BU may NOT skip the board memo at Days 61–90; the verifier checks
  for memo file presence.

## Reference

- M&A path: see `MA_PLAYBOOK.md`.
- New-BU path: see `HOLDING_CHARTER.md` section "How To Add A BU".
- Kill path (opposite): see `BU_KILL_RULES.md`.
