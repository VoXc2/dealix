# AI Agent Decision Governance

أي قرار يخص **agents** يمر على بوابة أشد من المنتج العام.

## بوابة قبل إضافة وكيل

- غرض واضح  
- مالك واضح  
- أدوات مسموحة محددة  
- إجراءات ممنوعة واضحة  
- مستوى استقلالية ≤ 3 في MVP  
- تدقيق مطلوب  
- قاعدة إيقاف/إزالة موجودة  

**الكود:** `AgentDecisionGate` · `agent_decision_gate_passes` — `board_decision_os/agent_decision_gate.py`

## سياق الهوية والمساءلة

أبحاث حديثة حول **AI Identity** والفجوات في التعريف والتحقق لكيانات غير بشرية وغير حتمية — [arXiv:2604.23280](https://arxiv.org/abs/2604.23280)

## مثال قرار

```json
{
  "decision": "APPROVE_AGENT",
  "agent": "RevenueAgent",
  "autonomy_level": 2,
  "allowed_actions": ["score_accounts", "generate_drafts", "summarize"],
  "forbidden_actions": ["send_messages", "scrape_web", "cold_whatsapp"],
  "required_controls": ["audit_log", "approval_gate", "pii_redaction"]
}
```

**صعود:** [`BOARD_RISK_DECISIONS.md`](BOARD_RISK_DECISIONS.md)
