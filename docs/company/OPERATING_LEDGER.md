# Dealix Operating Ledger

The **Operating Ledger** is the source of truth for Dealix execution: if it is not recorded, it is not managed—and what is not managed does not scale.

**Mature AI organizations** tend to select initiatives for **business value** and **technical feasibility**, invest in **governance** and **engineering discipline**, and a substantial share of high-maturity leaders report measuring **impact, ROI, and risks** in tangible ways ([Gartner — AI maturity and project longevity](https://www.gartner.com/en/newsroom/press-releases/2025-06-30-gartner-survey-finds-forty-five-percent-of-organizations-with-high-artificial-intelligence-maturity-keep-artificial-intelligence-projects-operational-for-at-least-three-years)).

## Ledger types

| # | Ledger | File | What it records |
|---|--------|------|-----------------|
| 1 | **Request** | [`../ledgers/REQUEST_LEDGER.md`](../ledgers/REQUEST_LEDGER.md) | Every inbound ask |
| 2 | **Decision** | [`../ledgers/DECISION_LEDGER.md`](../ledgers/DECISION_LEDGER.md) | Material choices |
| 3 | **Client** | [`../ledgers/CLIENT_LEDGER.md`](../ledgers/CLIENT_LEDGER.md) | Accounts + state |
| 4 | **Delivery** | [`../ledgers/DELIVERY_LEDGER.md`](../ledgers/DELIVERY_LEDGER.md) | Client-facing outputs |
| 5 | **Governance** | [`../ledgers/GOVERNANCE_LEDGER.md`](../ledgers/GOVERNANCE_LEDGER.md) | Risks, approvals, blocks |
| 6 | **Proof** | [`../ledgers/PROOF_LEDGER.md`](../ledgers/PROOF_LEDGER.md) | Evidence of impact |
| 7 | **Learning** | [`../ledgers/LEARNING_LEDGER.md`](../ledgers/LEARNING_LEDGER.md) | Post-project insight |
| 8 | **Product** | [`../ledgers/PRODUCT_LEDGER.md`](../ledgers/PRODUCT_LEDGER.md) | Feature candidates + build calls |

## Rule

```text
If it is not in a ledger, it does not exist operationally.
```

## Control plane

[`CONTROL_PLANE.md`](CONTROL_PLANE.md) aggregates ledgers into **this week’s** sell / block / build / publish calls.

## Related

- [`CLOSED_LOOP_EXECUTION.md`](CLOSED_LOOP_EXECUTION.md)
- [`DECISION_OPERATING_SYSTEM.md`](DECISION_OPERATING_SYSTEM.md)
- Client workbench logs: `clients/<client>/<project>/04_governance_log.md`
