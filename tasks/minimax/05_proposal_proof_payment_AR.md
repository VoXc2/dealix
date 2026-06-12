# MiniMax Sub-prompt 05 — Proposal / Proof Pack / Payment OS (status binding, no rebuild)

> **Scope:** Document the existing revenue-execution chain: diagnostic → proposal → proof pack → pilot delivery → payment handoff → upsell → renewal.
> **Do not break:** `dealix/commercial/`, the `proposal_renderer`, the `claim_safety` rule, the `payment_pricing_safety` tests.
> **Branch:** `feature/minimax-factory-p0-hardening`

---

## 1. Objective

The full revenue chain already exists in code (`api/routers/commercial.py` exposes 13 endpoints, `dealix/commercial/` has the engines). The gap is the **one doc** that says:
- which endpoint produces which artifact,
- which approval gate stands in front of pricing and payment links,
- which safety test enforces no-ROI-claims.

This sub-prompt produces that doc.

---

## 2. Files to Create

### 2.1 `docs/commercial/REVENUE_EXECUTION_CHAIN_AR.md`

Sections:
1. **Chain overview (ASCII diagram)** — Diagnostic → Proposal → Proof Pack → Pilot → Payment Handoff → Upsell → Renewal.
2. **Endpoint table** — one row per endpoint in `api/routers/commercial.py`:
   - Method, path, what it produces, what approval gate sits in front, what evidence level is required.
3. **Approval gates** — `auto_client_acquisition/governance_os/approval_matrix.py` is the source of truth. Quote the relevant matrix entries.
4. **Pricing rules** — what is forbidden (no guaranteed ROI, no "100% increase", no fake case study). Cite the test: `pytest tests/test_commercial_claim_safety.py`.
5. **Payment link rule** — payment link generation requires `approval_required=true` and an admin key. Cite the test: `pytest tests/test_payment_pricing_safety.py`.
6. **Proof pack rule** — every `proof_pack` artifact must have `evidence_level ∈ L2..L5`. L0–L1 are stub-level and are not eligible for client delivery.
7. **Upsell gate** — upsell cannot fire before proof pack delivered AND ≥ 30 days since pilot start. Cite the rule.
8. **Renewal gate** — renewal cannot be auto-quoted. It produces a renewal draft that must be approved.

### 2.2 `docs/commercial/REVENUE_CHAIN_RISKS_AR.md` (optional, ≤ 120 lines)

A short risk register — top 5 risks the founder should monitor weekly:
1. Proposal sent without approval (signal: no entry in `approval_log` within 24h of `proposal_drafted`).
2. Proof pack with `evidence_level = L0` delivered to client.
3. Payment link sent before human approval.
4. Upsell fired before proof delivered.
5. Renewal quoted without renewal draft approval.

Each risk gets: signal, command to check, command to remediate.

### 2.3 `reports/revenue_execution/CHAIN_STATUS_LATEST.md` (stub if missing)

Snapshot:
- Last 10 proposals (id, client, status, approval_status).
- Last 5 proof packs (id, evidence_level, delivery_status).
- Last 5 payment handoffs (id, status, approval_id).
- Open upsell queue (count, top 3 by value).
- Open renewal queue (count, top 3 by value).

---

## 3. Constraints

- No code changes. Docs only.
- No live API calls. Snapshot can be hand-written for now; auto-writer is a separate sub-prompt.
- If a referenced endpoint or file does not exist, **say so**. Do not invent.
- Under 250 lines per doc.

---

## 4. Acceptance

```bash
test -f docs/commercial/REVENUE_EXECUTION_CHAIN_AR.md
make trust-gates
pytest tests/test_commercial_claim_safety.py -v --no-header -q
pytest tests/test_payment_pricing_safety.py -v --no-header -q
```
