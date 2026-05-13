# Dealix Sales Pipeline — Stages and Exit Criteria

11 stages from "Lead" to "Retainer Won". Each stage has an exit criterion;
no opportunity moves forward by feel.

| # | Stage | Exit criterion |
|---|-------|----------------|
| 1 | Lead | Company identified + contact path exists |
| 2 | Qualified | Qualification Score ≥ 60 (per `docs/sales/QUALIFICATION_SCORE.md`) |
| 3 | Discovery Scheduled | 30-min slot booked |
| 4 | Discovery Done | Pain + data/process + decision-maker captured in writing |
| 5 | Proposal Sent | SOW from `templates/sow/` sent; service + price + scope locked |
| 6 | Verbal Yes | Decision-maker says yes in writing (email/WhatsApp/Slack) |
| 7 | Paid | First invoice paid OR signed agreement |
| 8 | Delivery Started | `clients/<codename>/DELIVERY_COMMAND.md` opened; Stage 1 Discover entered |
| 9 | Proof Delivered | Stage 7 Prove complete; Proof Pack handed to customer |
| 10 | Retainer Offered | Renewal recommendation discussed in handoff session |
| 11 | Retainer Won | Retainer agreement signed |

## Movement rules

- An opportunity in any stage either advances (criterion met) or is **stalled** (criterion not met within stage-specific SLA). Stalled opportunities are reviewed weekly.
- Backward movement is allowed and tracked (e.g., Proposal Sent → Discovery Done means we missed something).
- An opportunity that never advances past Lead in 30 days is auto-archived.

## Stage SLAs

| Stage | SLA |
|-------|-----|
| Lead → Qualified | ≤ 5 business days |
| Qualified → Discovery Scheduled | ≤ 3 business days |
| Discovery Done → Proposal Sent | ≤ 2 business days |
| Proposal Sent → Verbal Yes / Lost | ≤ 7 business days |
| Verbal Yes → Paid | ≤ 14 business days |
| Paid → Delivery Started | ≤ 1 business day |
| Delivery Started → Proof Delivered | per SOW (7 / 10 / 21 days) |
| Proof Delivered → Retainer Offered | ≤ 7 days post-handoff |

## Conversion targets (per `docs/go-to-market/saudi_gtm_12m.md`)

- Outbound (200 accounts) → Demos (37) → Qualified (18) → Closes (7) in 90 days.
- Sprint → Retainer conversion target: 40% by Day 90.
- Retainer renewal target: ≥ 80% by 6 months.

## Weekly review

The CEO opens this pipeline in the Monday review and asks:
- Which stage has the most stalled opportunities?
- Which exit criterion is the most common blocker?
- What's the average days-in-stage?

## Cross-links

- `docs/sales/QUALIFICATION_SCORE.md`
- `docs/sales/sales_script.md`
- `docs/sales/objection_handling.md`
- `docs/go-to-market/saudi_gtm_12m.md`
- `docs/growth/CLIENT_JOURNEY.md`
- `templates/sow/`
