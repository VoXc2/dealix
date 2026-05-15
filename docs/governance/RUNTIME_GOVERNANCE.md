# Runtime Governance

Canonical check list + rule examples: [`GOVERNANCE_RUNTIME.md`](GOVERNANCE_RUNTIME.md).

Governance must run **during execution**, not only as a policy PDF. As **agentic** patterns spread, organizations need **controls on data access, allowed actions, monitoring**, and **human oversight** when scaling agents ([TechRadar — scaling agentic AI safely](https://www.techradar.com/pro/how-enterprises-can-safely-scale-agentic-ai)).

## Runtime checks (minimum)

1. **Data source** check — lawful basis + permitted use  
2. **PII** check — minimize, flag, redact  
3. **Permission** check — mirror user/workspace RBAC ([`PERMISSION_MIRRORING.md`](PERMISSION_MIRRORING.md))  
4. **Output claim** check — no unsupported guarantees  
5. **External action** check — channel policy; approval if not draft-only  
6. **Approval requirement** — per [`APPROVAL_MATRIX.md`](APPROVAL_MATRIX.md)  
7. **Audit log** write — for sensitive paths ([`AUDIT_LOG_POLICY.md`](AUDIT_LOG_POLICY.md))  
8. **Proof event** write — tie to proof pack / delivery ledger when client-visible  

## Rule

Every **AI-assisted** workflow must pass runtime governance **before** client delivery or **before** any non-draft external effect.

## Runtime decision outcomes

```text
Allow
Allow with review
Require approval
Redact
Block
Escalate
```

**Future:** enforce as middleware on AI/tool routes ([`MANAGEMENT_API_SPEC.md`](../product/MANAGEMENT_API_SPEC.md)).
