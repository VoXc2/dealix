# Productization Decision

Turn manual work into **durable assets** before you call it “product.”

## Rule — productize only if

- Repeated **at least 3 times** (or paid for twice with same shape)
- **Reduces delivery time** materially
- **Improves quality or governance**
- Supports **more than one client** (or one client + clear horizontal reuse)
- Can be **tested** / verified (eval, script, pytest)

See also [`BUILD_DECISION.md`](BUILD_DECISION.md).

## Decision outcomes

```text
Template      — docs + checklist only
Script        — internal automation
Internal tool — operator-facing
Client feature — in product surface
SaaS module   — packaged, billed, SLAs
Ignore        — one-off; document why
```

## Record

Update [`FEATURE_BACKLOG.md`](FEATURE_BACKLOG.md) and [`../company/FEATURE_CANDIDATE_LOG.md`](../company/FEATURE_CANDIDATE_LOG.md).
