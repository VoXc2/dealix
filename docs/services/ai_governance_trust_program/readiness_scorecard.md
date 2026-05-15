# Readiness Scorecard

> **STATUS: Planned — Do Not Sell Yet.** This service is **not yet sellable**.
> It unlocks only after **≥3 documented proof packs** from lower-tier offers
> AND the readiness band below reaches `sellable` (≥85). Gates are defined in
> [`DEALIX_READINESS.md`](../../../DEALIX_READINESS.md).

Scores are computed in
[`auto_client_acquisition/enterprise_os/enterprise_readiness.py`](../../../auto_client_acquisition/enterprise_os/enterprise_readiness.py).
Each dimension is scored 0–100.

## Dimensions

| Dimension | Score (0–100) |
|---|---|
| Offer | 70 |
| Delivery | 48 |
| Product | 44 |
| Governance | 70 |
| Demo | 30 |
| Sales | 50 |
| Retainer | 30 |
| Scale | 26 |
| **Weighted total** | **≈ 49.5** |

## Bands

| Band | Range |
|---|---|
| blocked | < 70 |
| beta | 70–84 |
| sellable | 85–89 |
| premium | 90–94 |
| enterprise_ready | 95+ |

## Current Band: blocked

The weighted total of ≈49.5 places this service in the `blocked` band.

## Gating Rule

This service may be sold only when its band is **`sellable` or higher (≥85)**
AND at least 3 documented proof packs exist from lower-tier offers.

## Biggest Gaps

- **Scale (26)** — repeatable delivery across multiple clients not yet proven.
- **Demo (30)** — no shippable demo of the governance dashboard.
- **Retainer (30)** — post-program review motion not defined.

Closing Scale, Demo, and Retainer is the priority before any sale.

See also: [`offer.md`](offer.md) · [`delivery_checklist.md`](delivery_checklist.md).
