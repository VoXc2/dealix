# محفظة النماذج — منظومة تحقيق القيمة

**الطبقة:** L3 · منظومة تحقيق القيمة
**المالك:** رئيس الذكاء الاصطناعي
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [MODEL_PORTFOLIO.md](./MODEL_PORTFOLIO.md)

## السياق
تشغّل ديلكس مهام كثيرة عبر عملاء كثيرين، واستخدام نموذج واحد لكل شيء هدر
وخطر. تحدّد محفظة النماذج مجموعة المهام القياسية ومعايير الاختيار وقواعد
التوجيه. وتكمل
`docs/AI_MODEL_ROUTING_STRATEGY.md` و
`docs/LLM_PROVIDERS_SETUP.md` و
`docs/AI_STACK_DECISIONS.md`.

## مجموعة المهام القياسية

- التصنيف.
- الاستخراج.
- التلخيص.
- التقييم.
- الكتابة التنفيذية بالعربية.
- إجابة الاسترجاع المعزّز (RAG).
- فحص الامتثال.
- توليد التقارير.

## معايير الاختيار

- الدقة على مجموعة تقييم خاصة بالمهمة.
- جودة العربية حين تنطبق.
- الكلفة لكل 1000 رمز / لكل نداء.
- زمن الاستجابة.
- طول السياق المطلوب.
- حساسية البيانات وموقف المزوّد.
- الموثوقية (الجهوزية، حدود المعدّل).

## التوجيه

| Task | Tier | Validation |
|---|---|---|
| simple classification | low-cost | schema check |
| outreach draft | mid | claims check |
| executive report | high | QA review |
| RAG answer | high + retrieval | citation check |
| compliance | high + rules | hard fail rules |

## انضباط المحفظة

- كل مهمة لها نموذج أساسي واحتياطي.
- كل نموذج مثبّت بإصدار.
- الكلفة وزمن الاستجابة يُتتبَّعان لكل نموذج/مهمة في برج التحكم.
- مراجعة ربع سنوية للمحفظة: تشذيب، ترقية، استبدال.

## الأنماط الخاطئة

- نموذج عملاق واحد لكل شيء بصرف النظر عن المهمة.
- تغيير النماذج بصمت بلا تقييم.
- توجيه المهام الحسّاسة إلى مزوّدين غير معتمدين.
- تجاهل جودة العربية لصالح مقاييس الإنجليزية.

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| Task taxonomy | Routing rules | Head of AI | Quarterly |
| Eval results | Promote / prune decision | Head of AI | Per change |
| Provider catalog | Approved provider list | Head of AI | Quarterly |
| Control Tower | Model performance telemetry | Head of AI | Continuous |

## المقاييس
- Cost per Task — متوسط الكلفة لكل مهمة قياسية.
- Latency P50 / P95 — بحسب المهمة والنموذج.
- Arabic Quality Score — للمهام العربية.
- Fallback Rate — نسبة المكالمات التي خدمها النموذج الاحتياطي.

## ذات صلة
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — استراتيجية التوجيه
- `docs/LLM_PROVIDERS_SETUP.md` — إعداد المزوّدين
- `docs/AI_STACK_DECISIONS.md` — قرارات المستوى الأعلى
- `docs/COST_OPTIMIZATION.md` — انضباط الكلفة
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | مسودة أولى |
