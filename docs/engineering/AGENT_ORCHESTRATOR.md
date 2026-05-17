# Agent Orchestrator

How agents act inside Dealix Full Ops. Agents never call sensitive tools or
touch the outside world directly — every run passes the governance spine.

## The run contract

```
Event → Policy Check → Agent Selection → Tool Permission Check
      → Agent Run → Output Validation → Approval (if required)
      → Evidence Event → State Update
```

| Step | Responsibility | Backing module |
|---|---|---|
| Policy Check | classify A/R/S, evaluate rules | `dealix/trust/policy.py`, `governance_os/runtime_decision.py` |
| Tool Permission Check | confirm the agent may call the tool | `dealix/trust/tool_verification.py` |
| Output Validation | scan generated copy for forbidden claims | `governance_os/claim_safety.py`, `draft_gate.py` |
| Approval | route human-in-the-loop when required | `approval_center/` (`ApprovalStore`) |
| Evidence Event | append an immutable audit row | `auditability_os/audit_event.py` (`record_event`) |

## Agent permission model

Each agent declares what it `can` and `cannot` do. Drafting agents draft;
they never send, charge, approve, or mark-paid. Examples:

- An outreach drafting agent: `can` draft a message — `cannot` send it.
- A billing drafting agent: `can` draft an invoice — `cannot` send it or mark
  it paid.
- An affiliate compliance agent: `can` flag claims and block an asset —
  `cannot` approve a payout.

## Worked example — Affiliate OS

The `affiliate_os/` module shows the contract in code:

1. **Output Validation** — `asset_registry.review_asset_copy()` runs
   affiliate copy through `audit_claim_safety` + `runtime_decision.decide`
   before any asset is approved; a guaranteed-outcome claim returns `BLOCK`.
2. **Approval** — `payout_gate.request_payout()` opens an `ApprovalRequest`;
   the payout cannot settle until a human approves it.
3. **Evidence Event** — every intake, decision, commission, and payout writes
   a `record_event()` row to the audit ledger under the placeholder tenant
   `dealix_affiliate_ops`.

## Hard rules

- No autonomous external send. Ever.
- No guaranteed-outcome language in any agent output.
- Every high-risk action requires an approval and produces an evidence event.
- Agent runs are logged with the sources used and the policy result.
