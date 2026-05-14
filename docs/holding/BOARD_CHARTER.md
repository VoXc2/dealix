# Board Charter — Dealix Group

## Authority

The Board of Directors:
- Approves major capital allocations (the `must_fund` overrides + any
  acquisition above 6 months of confirmed retainer revenue).
- Approves doctrine version bumps that are MAJOR (vX → vX+1).
- Approves BU KILL decisions (per `docs/holding/BU_KILL_RULES.md`).
- Appoints / replaces directors and advisory members.
- Reviews the Group Risk Register quarterly.

The Board does NOT:
- Run BU day-to-day operations (that is the BU owner's job).
- Approve individual customer engagements.
- Set sub-brand naming (those follow `SUB_BRAND_RULES.md`).
- Engage in outreach (the doctrine forbids automated outreach
  regardless of who initiates it).

## Cadence

| Cadence | Trigger | Output |
|---|---|---|
| Monthly | First Sunday | BU decision memos reviewed, capital allocation cycle |
| Quarterly | First Sunday of each quarter | Risk register review + annual-report mid-year mark |
| Annual | After fiscal year end | Annual report (`scripts/render_annual_report.py`) |
| On demand | Major change (kill / spinout / acquisition / doctrine major bump) | Decision memo + recorded vote |

## Committees

Three standing committees (chairs filled when the second + third
advisor seats are filled):

1. **Audit Committee** — owns the Group Risk Register, quarterly
   review, internal audit (see `INTERNAL_AUDIT.md`).
2. **Compensation Committee** — owns the option-pool allocation
   (`data/cap_table.json` reserved pool), hiring-trigger sign-off.
3. **Capital Allocation Committee** — owns the monthly `must_fund` /
   `should_test` / `hold` / `kill` cycle (the existing
   `board_decision_os/capital_allocation_board.py` engine).

## Proxy Rules

- Directors may not delegate votes outside the board.
- A recused director's vote does not count toward quorum.
- Quorum: ≥ 2 of 3 directors (when 3 seats filled).

## Public Disclosure

`GET /api/v1/holding/board` returns: name + role + independent flag.
Nothing else.

## Verification

- `tests/test_holding_endpoints.py` (PR11) — public board response
  contains only the 3 allowed fields.
- This document is referenced from `/api/v1/holding/board` response's
  `charter_path` field.
