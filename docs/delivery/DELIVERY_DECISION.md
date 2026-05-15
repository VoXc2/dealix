# Delivery Decision

No **client-facing** output ships unless this gate passes.

## Required

| Gate | Requirement |
|------|----------------|
| QA | Score ≥ **85** (or service-specific threshold documented) |
| Governance | Check passed — [`../governance/GOVERNANCE_DECISION.md`](../governance/GOVERNANCE_DECISION.md) |
| Proof | Proof pack exists for the engagement (`06_proof_pack.md` + annexes) |
| Next action | Explicit next step for the client (not “contact us”) |
| Hard fails | None (see below) |

Artifacts: `clients/<client>/delivery_approval.md`, [`../quality/OUTPUT_QA_SCORECARD.md`](../quality/OUTPUT_QA_SCORECARD.md).

## Hard fail (automatic block)

- PII leakage or unlawful processing
- Unsupported / fake proof
- Knowledge answer **without** source when source is required ([`DEALIX_STANDARD.md`](../company/DEALIX_STANDARD.md))
- Unsafe automation (cold WhatsApp, etc.) — [`../governance/FORBIDDEN_ACTIONS.md`](../governance/FORBIDDEN_ACTIONS.md)
- Guaranteed sales / revenue claims without defensible basis
- **No next action** — even a “beautiful” report is **blocked**

## Delivery outcomes

```text
Approved
Needs Revision
Blocked
```

## Rule

The client pays for a **clear decision**, not decoration. No next action → **Blocked**.
