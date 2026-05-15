# Readiness Scorecard

> **Status: Planned — Do Not Sell Yet.** This service is **not yet sellable**. It unlocks only after **≥3 documented proof packs** from lower-ladder offers **and** passing the `DEALIX_READINESS.md` gates.

## How this is computed

Eight dimensions are each scored 0–100, then combined into a weighted total by `auto_client_acquisition/enterprise_os/enterprise_readiness.py`.

## Current scores

| Dimension | Score (0–100) |
|---|---|
| Offer | 70 |
| Delivery | 40 |
| Product | 36 |
| Governance | 56 |
| Demo | 26 |
| Sales | 48 |
| Retainer | 32 |
| Scale | 22 |
| **Weighted total** | **≈ 44.0** |

## Bands

| Band | Range |
|---|---|
| blocked | < 70 |
| beta | 70–84 |
| sellable | 85–89 |
| premium | 90–94 |
| enterprise_ready | 95+ |

**Current band: blocked.**

## Gating rule

The service may be sold only when the weighted total reaches band **sellable (≥85)** or higher. At ≈44.0 it is **blocked**.

## Biggest gaps

- **Demo (26)** — no repeatable, evidence-backed demonstration exists yet.
- **Scale (22)** — delivery cannot yet run across multiple concurrent enterprise clients.
- **Product (36)** — signal layer and approval queue are not production-hardened.

Closing Demo, Scale, and Product is the priority path out of the blocked band. Cross-reference: `DEALIX_READINESS.md` · `dealix/registers/no_overclaim.yaml` · [`offer.md`](offer.md).
