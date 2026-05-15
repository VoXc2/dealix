# Runtime Governance Product (Endgame)

**المنتج:** Governance Runtime — ليس PDF فقط، بل **قرارات وقت تشغيل**.

## مكوّنات

Policy Engine · PII Detection · Allowed Use Checker · Claim Safety Checker · Channel Risk Checker · Approval Engine · Audit Log · AI Run Ledger · Risk Index · Escalation Rules

## قرارات

ALLOW · ALLOW_WITH_REVIEW · DRAFT_ONLY · REQUIRE_APPROVAL · REDACT · BLOCK · ESCALATE

### مثال JSON

```json
{
  "decision": "REQUIRE_APPROVAL",
  "risk_level": "medium",
  "matched_rules": ["external_action_requires_approval"],
  "redactions": ["phone"],
  "audit_event_id": "AUD-001",
  "next_action": "human_review"
}
```

**المراجع:** مسار التنفيذ والسياسات — [arXiv:2603.16586](https://arxiv.org/abs/2603.16586) · [`../governance/GOVERNANCE_RUNTIME.md`](../governance/GOVERNANCE_RUNTIME.md)

**الكود:** `endgame_os/governance_product.py` — `GovernanceDecision` · `governance_runtime_maturity_score`.

**صعود:** [`ENDGAME_OPERATING_DOCTRINE.md`](ENDGAME_OPERATING_DOCTRINE.md)
