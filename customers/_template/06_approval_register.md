# 06 — Approval & Authority Register / سجل الموافقات والصلاحيات

> Durable account-level log for material actions. Internal analysis/drafting may
> run autonomously within current policy. Customer/external, financial, legal,
> production, DNS/DB/secret, tender, or destructive effects require the matching
> current action-bound authority and evidence gates.

| # | Date | Action | Requested by | Authority source | Action hash / idempotency | Expiry | Decision | Provider / effect receipt | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | `dealix-sales/delivery/pm/content/engineer` | | | | `approve / hold / reject` | | |

## Standing rules / قواعد ثابتة
- **L0 Observe / L1 Analyze / L2 Draft / L3 Internal Execute / bounded L4 Repo Execute:** may run autonomously when current policy permits, reversible, tenant-safe, and receipt-backed.
- **Material external effects:** customer send, public publish, spend/payment/refund, binding legal/commercial commitment, tender submission, merge main, production/DNS/material DB/secret mutation, and destructive deletion require action-specific authority.
- An old/blanket approval never authorizes a new payload. Bind approval to the current payload/action hash, authority source, expiry, and idempotency key.
- Relationship/consent/suppression/sender-health/channel-policy gates remain independent of commercial approval.
- Provider acceptance ≠ delivered; record delivery/failure receipt separately.
