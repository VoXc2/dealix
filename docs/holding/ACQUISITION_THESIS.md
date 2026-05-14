# Acquisition Thesis — Dealix Group

## What Makes a Good Dealix Acquisition

A target is acquirable only when **all four** below are true. Any one
missing → reject.

1. **Doctrine compatibility.** The target's existing operations do not
   include any practice forbidden by `open-doctrine/11_NON_NEGOTIABLES.md`
   (scraping, cold-WhatsApp automation, LinkedIn automation,
   guaranteed-revenue claims, sourceless AI runs, agents without
   identity).

2. **Evidence inheritability.** The target's existing work can be
   re-anchored to Dealix's Proof Pack format. Targets whose value is
   "opaque expertise" without documentable evidence are rejected.

3. **Sector fit.** The target operates in (or has demonstrated demand
   from) a sector Dealix Group already serves OR a sector explicitly
   listed in the next year's theses (see annual report Section 9).

4. **Capital fit.** The target's price ≤ 18 months of the acquiring
   BU's confirmed retainer revenue (Article 8 confirmed only — no
   pipeline projections). Cash-only or cash+small-earnout. No
   stock-only deals.

## Explicit Non-Criteria

Dealix Group does **not** acquire to:

- Enter a market where a partner-led pilot has not yet proved demand.
- "Buy growth" — top-line acquisitions without margin proof.
- Pre-empt a competitor — defensive M&A is forbidden.
- Eliminate a small player — anti-competitive M&A is forbidden.
- Acquire customer lists.
- Acquire a brand with the intent of preserving its name as a primary
  brand (every acquired entity must follow the sub-brand rules: it
  becomes `Dealix <Function>` or it doesn't enter the group).

## Process Reference

See `MA_PLAYBOOK.md` for the staged process. See `BU_KILL_RULES.md`
for the inverse path (when to shut a BU down).

## Decision Authority

- Targets below 6 months of confirmed retainer revenue: founder + 1
  advisor sign-off.
- Targets above 6 months: full board memo + capital allocation board
  vote (`board_decision_os/capital_allocation_board.py`).

## Verification

- `tests/test_ma_playbook_lists_required_artifacts.py` ensures the
  M&A playbook enumerates every required artifact per stage.
- `tests/test_bu_kill_rules_match_unit_governance.py` ensures the
  kill rules in BU_KILL_RULES.md match the branches in
  `auto_client_acquisition/holding_os/unit_governance.py:evaluate_unit_decision()`.
