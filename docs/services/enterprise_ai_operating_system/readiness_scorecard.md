# Readiness Scorecard

> **Status: Planned — Do Not Sell Yet.** This service is **not yet sellable**. It unlocks only after **≥3 documented proof packs** from lower-tier offers **and** passing the `DEALIX_READINESS.md` gates.

The scorecard rates 8 dimensions, each 0–100, computed in `auto_client_acquisition/enterprise_os/enterprise_readiness.py`. The weighted total maps to a readiness band.

## Current scores

| Dimension | Score (0–100) |
|---|---|
| Offer | 72 |
| Delivery | 42 |
| Product | 38 |
| Governance | 58 |
| Demo | 28 |
| Sales | 52 |
| Retainer | 34 |
| Scale | 24 |
| **Weighted total** | **≈ 46.2** |
| **Band** | **blocked** |

## Bands

| Band | Weighted total |
|---|---|
| blocked | < 70 |
| beta | 70–84 |
| sellable | 85–89 |
| premium | 90–94 |
| enterprise_ready | 95+ |

## Gating rule

The service may only be sold when its band is **≥ sellable (≥ 85)**. At a weighted total of ≈ 46.2 the band is **blocked**, so the service stays under "Do Not Sell Yet".

## Biggest gaps

In priority order, the dimensions blocking readiness are:

- **Scale (24)** — Scale Plan playbook and rollout sequencing not proven
- **Demo (28)** — no end-to-end demo or reference walkthrough
- **Retainer (34)** — monthly optimization cycle not yet operationalized
- **Product (38)** — Company Brain and agent layer not hardened

Closing these, plus the ≥3 proof packs requirement, is the path to a sellable band.

See also: [`offer.md`](offer.md) · [`../../27_delivery_playbooks/ENTERPRISE_AI_TRANSFORMATION_DELIVERY_PLAYBOOK.md`](../../27_delivery_playbooks/ENTERPRISE_AI_TRANSFORMATION_DELIVERY_PLAYBOOK.md).
