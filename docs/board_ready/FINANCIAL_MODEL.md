# Financial Model

Five revenue lines + per-offer unit economics + per-category margin targets.

## 1. Revenue Lines

1. Diagnostics
2. Sprints
3. Retainers
4. Platform / Workspace (later)
5. Academy / Partners (later)

## 2. Unit Economics per Offer

- price
- delivery hours
- AI cost
- gross margin
- proof strength
- retainer conversion
- reuse assets created

## 3. Minimum margin targets

| Category | Min Margin |
| --- | ---: |
| Diagnostic | 75% |
| Sprint | 65–75% |
| Pilot | 55–70% |
| Retainer | 65% |
| Enterprise | 50–70% |
| Academy | 80% |
| Platform | 80% (mature) |

Enforced by `board_ready_os.financial_model.is_offer_healthy()`.

## 4. Board rule

> Do not scale an offer with weak gross margin, weak proof, or high scope creep.

## 5. The principle

> Unit economics is a board metric, not a finance hobby.
