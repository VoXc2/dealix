# Agent Identity Doctrine

كل agent داخل Dealix له **هوية كموظف**: بطاقة، مالك، غرض، مدخلات، أدوات، ممنوعات، استقلالية، موافقة، تدقيق.

## بطاقة مرجعية

```json
{
  "agent_id": "AGT-REV-001",
  "name": "RevenueAgent",
  "owner": "Dealix Revenue",
  "purpose": "Score accounts and recommend next actions",
  "allowed_inputs": ["client_uploaded_accounts", "approved_public_data"],
  "allowed_tools": ["score_accounts", "generate_draft", "create_summary"],
  "forbidden_actions": ["send_messages", "scrape_web", "cold_whatsapp", "linkedin_automation"],
  "autonomy_level": 2,
  "approval_required_for": ["external_actions", "personal_data_outputs"],
  "audit_required": true
}
```

## مستويات الاستقلالية

0 Read · 1 Analyze · 2 Draft/Recommend · 3 Queue · 4 داخلي بعد موافقة · 5 خارجي مقيد · **6 ممنوع تلقائيًا خارجيًا**

**MVP:** المستويات **0–3 فقط**؛ ما فوق يحتاج حوكمة enterprise وaudit وموافقات و incident response وصلاحيات صارمة.

**الكود:** `agent_identity_mvp_ok` — `institutional_scaling_os/agent_identity.py`

**صعود:** [`../institutional_control/AGENT_CONTROL_PLANE.md`](../institutional_control/AGENT_CONTROL_PLANE.md)
