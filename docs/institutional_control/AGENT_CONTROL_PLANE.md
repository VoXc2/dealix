# Agent Control Plane

كل agent **كموظف افتراضي محكوم**: بطاقة، أدوات، ممنوعات، مستوى استقلالية، موافقة، سجل.

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

**قاعدة MVP:** **0–3 فقط** في البداية.

**مراجع:** بيئات تنفيذ تحمي تدفق بيانات المستخدم — [arXiv:2604.19657](https://arxiv.org/abs/2604.19657).

**الكود:** `agent_control_plane_card_valid` — `institutional_control_os/agent_control_plane.py`

**صعود:** [`../trust/AI_CONTROL_PLANE.md`](../trust/AI_CONTROL_PLANE.md) · [`../endgame/AGENT_CONTROL_DOCTRINE.md`](../endgame/AGENT_CONTROL_DOCTRINE.md)
