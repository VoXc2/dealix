# Agent Control Doctrine

كل وكيل داخل Dealix له **بطاقة** وبحدود صلاحيات رقمية.

## مثال Agent Card

```json
{
  "agent_id": "AGT-REVENUE-001",
  "name": "RevenueAgent",
  "owner": "Dealix Revenue",
  "purpose": "Score accounts and recommend next actions",
  "allowed_inputs": ["client_uploaded_accounts", "approved_public_data"],
  "forbidden_actions": ["send_messages", "scrape_web", "cold_whatsapp"],
  "autonomy_level": 2,
  "approval_required_for": ["external_actions", "personal_data_outputs"],
  "audit_required": true
}
```

## مستويات الاستقلالية

0 Read · 1 Analyze · 2 Draft/Recommend · 3 Queue for approval · 4 Execute internal after approval · 5 External restricted · 6 Autonomous external **forbidden**

**قاعدة MVP:** مسموح 0–3 داخليًا؛ 4–5 لمؤسسات؛ 6 ممنوع.

**مراجع:** ضوابط وكلاء على نطاق واسع — [`../trust/AI_CONTROL_PLANE.md`](../trust/AI_CONTROL_PLANE.md) · [KPMG — agentic AI governance](https://www.kpmg.com/us/en/articles/2025/ai-governance-for-the-agentic-ai-era.html)

**الكود:** `endgame_os/agent_control.py` · `global_grade_os/agent_governance.py`.

**صعود:** [`ENDGAME_OPERATING_DOCTRINE.md`](ENDGAME_OPERATING_DOCTRINE.md)
