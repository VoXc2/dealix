# Board of Directors — Dealix Group

> Public surface: `GET /api/v1/holding/board`.
> Machine-readable: `data/board_of_directors.json`.

## Roster (Initial)

| Name      | Role            | Independent | Notes |
|-----------|-----------------|:-----------:|-------|
| Founder   | Chair, Director | No          | Operates the holding day-to-day. |
| Reserved  | Advisor (open)  | Yes (when filled) | Domain: Saudi B2B services / governance. |
| Reserved  | Advisor (open)  | Yes (when filled) | Domain: finance / capital allocation. |

## Independence Rules

- A director is "independent" only if they hold no equity-class
  position above 0% and no executive role at any operating BU.
- Reserved advisory seats are filled by board memo. Acceptance is
  recorded in `data/board_of_directors.json`.

## Conflict Rules

- A director with a financial conflict (e.g., portfolio overlap with
  a target acquisition) recuses from the relevant vote.
- All recusals are recorded in the corresponding meeting memo.

## Replacement

A board seat can be vacated only by:
- voluntary resignation (recorded in writing),
- a board memo invoking the suspension policy in
  `docs/40_partners/PARTNER_SUSPENSION_POLICY.md` adapted for
  directors,
- or expiry of a fixed-term advisory appointment.

## Public Disclosure

`/api/v1/holding/board` returns only **name + role + independent
flag**. No emails, no phone numbers, no addresses (locked by
`tests/test_holding_endpoints.py` in PR11 plus a new check in PR15).
