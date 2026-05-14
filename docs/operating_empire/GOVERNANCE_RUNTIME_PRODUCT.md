# Governance Runtime Product (Empire Layer)

**ملخص تنفيذي:** حوكمة الوكلاء **وقت التشغيل** تعتمد على مسار التنفيذ وليس تعليمات ثابتة فقط — [Runtime assurance for agents (arXiv:2603.16586)](https://arxiv.org/abs/2603.16586).

**تفاصيل المنتج:** [`../dominance/GOVERNANCE_RUNTIME_PRODUCT.md`](../dominance/GOVERNANCE_RUNTIME_PRODUCT.md) · [`../enterprise/GOVERNANCE_RUNTIME_PRODUCT.md`](../enterprise/GOVERNANCE_RUNTIME_PRODUCT.md)

## مكونات

Policy Engine · PII Detection · Allowed Use Checker · Claim Safety Checker · Channel Risk Checker · Approval Engine · Audit Log · AI Run Ledger · Risk Index · Escalation Rules  

## مثال قرار JSON

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

**صعود:** [`OPERATING_EMPIRE_BLUEPRINT.md`](OPERATING_EMPIRE_BLUEPRINT.md)
