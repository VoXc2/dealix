# LLM Gateway — نية التصميم

لا يمر استدعاء نموذج لغوي من كل وحدة بشكل عشوائي. الهدف أن يمر عبر **بوابة موحّدة** تضمن:

- **model_catalog** — أي نماذج مسموحة لأي سياق
- **routing_policy** — اختيار النموذج حسب التكلفة والجودة
- **prompt_registry** — إصدارات prompts
- **cost_guard** — سقف تكلفة لكل مشروع/يوم
- **output_schema** — مخرجات قابلة للتحقق
- **redaction** — عدم إرسال PII خام للنموذج عند المنع
- **fallback_policy** — بدائل آمنة
- **run_log** — تتبع (بدون PII في السجلات)
- **eval_hook** — نقاط تقييم حتمية حيث تنطبق

## التنفيذ في الريبو اليوم

الطبقة القريبة من هذا المفهوم: [`auto_client_acquisition/llm_gateway_v10/`](../../auto_client_acquisition/llm_gateway_v10/) و[`tool_guardrail_gateway/`](../../auto_client_acquisition/tool_guardrail_gateway/) حيث يوجد.

الوثيقة هنا **نية معمارية**؛ التوسع يتم دون كسر مسارات المسودات والموافقات.
