# إيقاع مراجعة ذاكرة الوثائق Dealix

**الغرض:** عدم ترك الفهرس والسجلات تتعفّن؛ ربط المراجعة بأدوات تحقق قابلة للتشغيل.

## الإيقاع

| الفترة | الإجراء |
|--------|---------|
| **أسبوعي** | مراجعة الوثائق الجديدة/المعدّلة في PRs الحديثة؛ التحقق من جملة الغرض (Sell / Deliver / Govern / Prove / Train / License / Fund / Archive). |
| **شهري** | تشغيل لقطة الفهرس + اختبارات الحوكمة + تحديث صفوف السجل عند تغيير canonical. |
| **ربع سنوي** | مراجعة **LEGACY / DEPRECATED** مقابل [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md)؛ تحديث [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md). |
| **نصف سنوي** | تحديث [DOCS_READING_PACKS_AR.md](DOCS_READING_PACKS_AR.md) (شريك / مستثمر / مشغّل). |

## الروتين الشهري (أوامر)

```bash
py -3 scripts/generate_docs_hub_snapshot.py
py -3 scripts/generate_holding_value_summary.py
py -3 scripts/validate_docs_governance.py
py -3 -m pytest tests/test_holding_value_deliverables.py tests/test_docs_governance_system.py tests/test_external_packs_registry.py tests/test_motion_packs.py tests/test_external_pack_safety.py -q --no-cov
```

يُنفَّذ نفس البوابة تلقائيًا في **CI** (`ci.yml` → Documentation governance gate).

## أسئلة شهرية (CEO / التشغيل)

1. ما الذي أصبح **CANONICAL** هذا الشهر؟
2. ما الذي انزل إلى **LEGACY** أو **DEPRECATED**؟
3. ما الذي استُخدم في **بيع** فعلي؟
4. ما الذي استُخدم في **تسليم**؟
5. ما الذي لم يعد يخدم ويمكن خفض ضجيجه؟
6. ما الذي يصلح كأصل **IP / ترخيص**؟

## شروط إعادة هيكلة لاحقة

لا تُنقل مجلدات الجذر بكثافة حتى:

1. [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md) مستقر لمدة شهرين على الأقل.
2. يوجد فاحص روابط (`broken links`) كعملية CI أو سكربت.
3. ملفات **LEGACY** مصنّفة في السياسة والسجل.
