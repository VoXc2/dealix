# Board Scorecards

Weights are implemented in `auto_client_acquisition/board_decision_os/board_scorecards.py` (single source of truth).

## Offer Scorecard (0–100 weighted)

| Dimension | Weight |
|-----------|-------:|
| Win rate | 15 |
| Gross margin | 15 |
| Proof strength | 20 |
| Retainer conversion | 20 |
| Repeatability | 15 |
| Governance safety | 10 |
| Productization signal | 5 |

**Band → decision**

| Total | Board read |
|------:|------------|
| 85–100 | Scale |
| 70–84 | Improve and sell |
| 55–69 | Pilot only |
| <55 | Hold / Kill |

## Client Scorecard (0–100 weighted)

| Dimension | Weight |
|-----------|-------:|
| Clear pain | 15 |
| Executive sponsor | 15 |
| Data readiness | 15 |
| Governance alignment | 15 |
| Adoption score | 15 |
| Proof score | 15 |
| Expansion potential | 10 |

**Band → decision**

| Total | Board read |
|------:|------------|
| 85–100 | Strategic account |
| 70–84 | Retainer-ready |
| 55–69 | Enablement needed |
| <55 | Avoid / diagnostic only |

## Productization Scorecard (0–100 weighted)

| Dimension | Weight |
|-----------|-------:|
| Repeated pain | 20 |
| Delivery hours saved | 20 |
| Revenue linkage | 20 |
| Risk reduction | 15 |
| Client pull | 15 |
| Build simplicity | 10 |

**Band → decision**

| Total | Board read |
|------:|------------|
| 85–100 | Build now |
| 70–84 | MVP |
| 55–69 | Template / manual |
| <55 | Hold |

## API

`POST /api/v1/board-decision-os/scorecards/offer` (and `/client`, `/productization`) with dimension scores **0–100** each.
