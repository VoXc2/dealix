# Agent OS — هوية وكلاء الذكاء الاصطناعي

## الهدف

كل وكيل له **بطاقة** (غرض، مدخلات مسموحة، أدوات، ممنوعات، مستوى استقلالية، موافقات مطلوبة، تدقيق).

## Agent Card (مرجعي)

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

## مستويات الاستقلالية في الـ MVP

| المستوى | المعنى |
|---------|--------|
| 0 | قراءة |
| 1 | تحليل |
| 2 | مسودة / توصية |
| 3 | طابور للموافقة |

لا تفعّل مستويات أعلى من 3 في المؤسسات إلا مع ضوابط enterprise كاملة.

## التنفيذ في الريبو

- `auto_client_acquisition/ai_workforce/` — سجل الوكلاء، orchestrator، تكلفة.
- `auto_client_acquisition/agent_governance/` — حوكمة الوكلاء.
- سقف الـ MVP: `auto_client_acquisition/standards_os/agent_control_standard.py` (`MVP_AUTONOMY_LEVEL_MAX = 3`).

## روابط

- [RISK_OS.md](RISK_OS.md) — [TESTS_REQUIRED.md](TESTS_REQUIRED.md)
