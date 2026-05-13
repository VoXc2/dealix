# Strategic Bets Framework

## Rule

Each month: **1–3 bets only**. Everything else is backlog with explicit “not now”.

## Bet types

- Revenue Bet
- Product Bet
- Trust Bet
- Distribution Bet
- Enterprise Bet
- Venture Bet

## Examples

**Revenue Bet:** Double down on Revenue Intelligence Sprint for B2B services.

**Product Bet:** Build Proof Pack Generator because it repeats across every sprint.

**Trust Bet:** Ship Agent Registry + AI Run Ledger before enterprise pilots.

## Validation

`auto_client_acquisition/board_decision_os/strategic_bets.py` enforces max bets and non-empty rationale.

## API

`POST /api/v1/board-decision-os/strategic-bets/validate`
