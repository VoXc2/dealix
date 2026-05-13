# Dealix Operating Ledger

> **Rule**: If it is not in a ledger, it does not exist operationally.
> 
> The Operating Ledger is Dealix's source of truth across 8 dimensions.
> Every request, decision, output, risk, and learning is logged. Without
> ledgers you forget; with ledgers you compound.

## The 8 ledgers

| # | Ledger | What it captures | Location |
|---|--------|------------------|----------|
| 1 | Request Ledger | Every inbound (sales, client, feature, governance, support, partner, enterprise) | `docs/ledgers/REQUEST_LEDGER.md` |
| 2 | Decision Ledger | Every non-trivial decision with evidence + risk + owner | `docs/ledgers/DECISION_LEDGER.md` |
| 3 | Client Ledger | Every customer, current status, revenue, health, next step | `docs/ledgers/CLIENT_LEDGER.md` |
| 4 | Delivery Ledger | Every customer-facing output shipped, QA-scored | `docs/ledgers/DELIVERY_LEDGER.md` |
| 5 | Governance Ledger | Every risk event, approval, block, redaction | `docs/ledgers/GOVERNANCE_LEDGER.md` |
| 6 | Proof Ledger | Every measured before/after outcome, by proof type | `docs/ledgers/PROOF_LEDGER.md` |
| 7 | Learning Ledger | Every insight captured at project close | `docs/ledgers/LEARNING_LEDGER.md` |
| 8 | Product Ledger | Every feature candidate with score + decision | `docs/ledgers/PRODUCT_LEDGER.md` |

## How the 8 ledgers feed the Control Plane

```
Request Ledger ─┐
Decision Ledger ┤
Client Ledger   ├──→ Control Plane ──→ Weekly Operating Review
Delivery Ledger ┤                       (CEO decisions)
Governance      ┤
Proof Ledger    ┤
Learning        ┤
Product Ledger ─┘
```

The Control Plane (`docs/company/CONTROL_PLANE.md`) reads from the ledgers
and produces the weekly answers: what to sell, what to block, what to build,
what to upsell, what to publish.

## Operating rule per ledger

- **Every entry has a date and an owner**.
- **No retroactive editing**. Mistakes are followed by a new dated entry.
- **Weekly review**: founder/CEO walks every ledger for new entries.
- **Monthly close**: count entries per ledger; identify which ledger is under-filled (signal of a missing operating habit).

## Markdown-table form is the MVP

In Phase 2, ledgers move into the event store (`auto_client_acquisition/revenue_memory/event_store.py`) for queryable, immutable, audit-grade storage. For now, markdown tables in `docs/ledgers/` are sufficient and zero-friction.

## Owner & cadence

- **Owner**: CEO oversees; HoCS owns Client + Delivery + Governance + Proof + Learning; CRO owns Request; HoP owns Product; HoLegal owns Governance.
- **Cadence**: daily 15-min triage; weekly operating review consumes the ledgers.

## Cross-links

- `docs/company/CONTROL_PLANE.md` — reads from these ledgers
- `docs/company/CLOSED_LOOP_EXECUTION.md` — the 11-station loop that feeds the ledgers
- `docs/company/COMPOUNDING_SYSTEM.md` — the 6 assets that get logged
- `docs/company/DECISION_OPERATING_SYSTEM.md` — what decisions log to Decision Ledger
- `docs/company/DEALIX_OPERATING_KERNEL.md` — the runtime
