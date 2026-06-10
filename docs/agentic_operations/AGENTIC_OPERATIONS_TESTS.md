# Agentic Operations Tests

اختبارات العقود في `tests/` تربط الوثائق بالكود:

| الاختبار (مقترح) | الغرض |
|-------------------|--------|
| `test_agent_requires_identity_card` | هوية كاملة |
| `test_agent_requires_owner` | مالك إلزامي |
| `test_agent_autonomy_mvp_limit` | مستويات MVP 1–4 |
| `test_agent_forbidden_external_action` | لا تنفيذ خارجي |
| `test_agent_no_scraping_tool` | أدوات ممنوعة |
| `test_agent_no_cold_whatsapp` | قنوات |
| `test_agent_tool_permission_audited` | تغيير صلاحية = audit |
| `test_agent_output_requires_governance` | مخرج + حوكمة |
| `test_agent_handoff_required_for_pii` | PII → handoff |
| `test_agent_decommission_if_no_owner` | إيقاف بلا مالك |

**التنفيذ:** `tests/test_agentic_operations_os.py` (وحدات pytest بأسماء أعلاه حيث أمكن).

## الكود المرتبط

`auto_client_acquisition/agentic_operations_os/`
