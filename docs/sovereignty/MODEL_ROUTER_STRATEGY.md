# Model Router Strategy

لا **استدعاء مباشر** لمزود واحد: كل طلب يمر بـ task type · risk · sensitivity · تكلفة · جودة · لغة · زمن استجابة.

**قرارات:** cheap / balanced / premium / rules-only (عند **high risk + PII** → مسار rules + حجز حتى جواز مصدر واضح).

### مثال

```json
{
  "task": "draft_outreach",
  "risk_level": "medium",
  "contains_pii": true,
  "language": "ar",
  "required_quality": "high",
  "decision": "premium_model_with_redaction_and_human_review"
}
```

**المنطق:** Dealix تبيع **governed outcome** لا «مخرج نموذج» خام.

**الكود:** `ModelRouterContext` · `route_model_decision` — `sovereignty_os/model_router_strategy.py`

**صعود:** [`../architecture/CORE_OS.md`](../architecture/CORE_OS.md) · [`OPERATING_SOVEREIGNTY.md`](OPERATING_SOVEREIGNTY.md)
