# Governed Revenue Ops — Backend Domains, APIs & State Machine

**Status:** Canonical (Phase 2 of the repositioning rollout, 2026-05-16).
**Rollout record:** [`GOVERNED_REVENUE_OPS_REPOSITIONING_ROLLOUT.md`](GOVERNED_REVENUE_OPS_REPOSITIONING_ROLLOUT.md)

---

## 1. Domain manifest

| Domain | Responsibility | Code location |
|--------|----------------|---------------|
| clients | Client records, labels | (existing customer plane) |
| contacts | Client contacts | (existing) |
| market_proof | Market proof / case-safe summaries | `auto_client_acquisition/proof_engine/` |
| revenue_ops | Governed engagement state machine | `auto_client_acquisition/revenue_ops/` |
| diagnostics | Governed Revenue Ops Diagnostic engine | `auto_client_acquisition/revenue_ops/diagnostics.py` |
| evidence | Evidence event trail | `revenue_ops_engagements` router `_EVIDENCE` |
| approvals | State-machine transitions (founder approval) | `revenue_ops/state_machine.py` |
| billing | Invoice drafts (no charge) | `revenue_ops_engagements` router |
| board_decision | Board Decision Memo outputs | (catalog service `board_decision_memo`) |
| reports | Proof Pack assembly | `auto_client_acquisition/proof_engine/` |

## 2. API surface — `/api/v1/revenue-ops`

New router: `api/routers/revenue_ops_engagements.py`. Distinct from the legacy
autonomous-layers surface at `/api/v1/revenue-os` — this surface is the
governed-engagement surface for the 7-service catalog.

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/revenue-ops/diagnostics` | Create a Governed Revenue Ops Diagnostic engagement (state: `draft`) |
| POST | `/api/v1/revenue-ops/upload` | Attach a client CRM export |
| POST | `/api/v1/revenue-ops/score` | Re-run diagnostic scoring |
| GET | `/api/v1/revenue-ops/{id}/decision-passport` | Build a decision passport from findings |
| POST | `/api/v1/revenue-ops/{id}/follow-up-drafts` | Generate follow-up DRAFTS (never sent) |
| POST | `/api/v1/revenue-ops/evidence/events` | Append an evidence event |
| GET | `/api/v1/revenue-ops/{id}/evidence` | Read the evidence trail |
| POST | `/api/v1/revenue-ops/approvals` | Advance the engagement state machine |
| POST | `/api/v1/revenue-ops/invoices` | Create an invoice DRAFT (no charge) |
| GET | `/api/v1/revenue-ops/{id}` | Read the full engagement record |

There is **no `/send` endpoint** — by design. An external action requires an
explicit `approved` transition through `/approvals`.

The existing `/api/v1/revenue-os/*` (autonomous layers), `/api/v1/revenue-intelligence/*`
(governed intelligence MVP), and `/api/v1/decision-passport/*` surfaces are
**unchanged** — the new surface extends, it does not duplicate them.

## 3. Engagement state machine

`auto_client_acquisition/revenue_ops/state_machine.py`.

```
draft → approved → sent → used_in_meeting → scope_requested
      → invoice_sent → invoice_paid
```

| State | Meaning | Ladder |
|-------|---------|--------|
| draft | Internal artifact, not externally visible | — |
| approved | Founder approved — gate for any external action | — |
| sent | Delivered to client (manually / authorized channel) | — |
| used_in_meeting | Artifact used in a client meeting | L5 |
| scope_requested | Client requested a sprint/retainer scope | L6 |
| invoice_sent | Invoice draft issued | L7 candidate |
| invoice_paid | Invoice paid | L7 confirmed |

Rules enforced in code (and tested in
`tests/test_revenue_ops_engagement_state_machine.py`):
- `draft → sent` is **forbidden** — approval is mandatory before any send.
- No state may be skipped.
- `invoice_paid` is terminal.
- `approved → draft` is the single allowed rollback (rejection).

## 4. Doctrine guarantees

- Every response carries a `governance_decision` field.
- Follow-up drafts are `DRAFT_ONLY`; cold WhatsApp / LinkedIn automation /
  scraping requests are rejected with HTTP 403.
- Invoice endpoints create drafts only — no charge; Moyasar live mode is
  founder-controlled.
- Evidence events form the audit trail; no PII is stored in events.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
