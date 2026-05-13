# وكيل التواصل الخارجي — منظومة تحقيق القيمة

**الطبقة:** L3 · منظومة تحقيق القيمة
**المالك:** رئيس الذكاء الاصطناعي
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [outreach_agent.md](./outreach_agent.md)

## السياق
يكتب وكيل التواصل الخارجي مسودات الرسائل مع حراس السلامة والادعاءات في
كل خطوة. ولا يرسل أبداً؛ يقترح فقط. هذا الفصل يبقي ديلكس منسجمة مع
الالتزامات العلنية في
`docs/growth/trust_page/what_we_do_not_do.md` ومع بنية القواعد في
`docs/DEALIX_OPERATING_CONSTITUTION.md`.

## بطاقة الوكيل

- **الدور:** يصيغ رسائل التواصل مع حراسة السلامة والادعاءات.
- **المدخلات المسموحة:** حسابات معتمدة، عرض، ICP، مكتبة نبرة القطاع.
- **المخرجات المسموحة:** مسودات متعددة موسومة بالقناة.
- **الممنوع:** إرسال الرسائل؛ وعود مضمونة؛ واتساب بارد؛ لينكدإن بارد؛
  انتحال الهوية؛ بيانات شخصية غير موثّقة.
- **الفحوصات المطلوبة:**
  - الحساب معتمد للتواصل؛
  - الادعاءات تجتاز قاعدة منع الضمانات؛
  - القناة تحترم حالة الموافقة؛
  - النبرة العربية تجتاز المراجعة للقنوات العربية.
- **مخطط الإخراج:** `OutreachDraftSet { account_id, channel, variants[],
  tone_label, safety_flags }`.
- **الاعتماد:** اعتماد بشري لكل مسودة قبل الاستخدام.

## قواعد القنوات

| Channel | Allowed | Notes |
|---|---|---|
| Email (business) | Yes | requires sender domain warm-up policy |
| LinkedIn DM | Conditional | only existing connections / consented |
| WhatsApp | No (cold) | only post-consent service messages |
| SMS | Conditional | regulated; needs consent record |

## الأنماط الخاطئة

- صياغات "نتائج مضمونة" أو "تحويل 100%".
- استخدام بيانات شخصية بلا مصدر معتمد.
- صياغات لقناة بلا موافقة.
- مخرجات نسخ ولصق جماعية بلا تنوّع نبرة.

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| Approved account + offer | OutreachDraftSet | Delivery owner | Per campaign |
| Tone library | Variant generation | Outreach Agent | Per draft |
| Compliance Guard verdict | Block / Edit / Allow | Compliance Guard | Per draft |

## المقاييس
- Claims Pass Rate — نسبة المسودات المجتازة قاعدة منع الضمانات.
- Tone QA Score — تقييم مراجع النبرة العربية.
- Channel Compliance Rate — نسبة احترام حالة الموافقة.
- Edit Distance — متوسط التحرير البشري قبل الإرسال.

## ذات صلة
- `docs/AI_STACK_DECISIONS.md` — اختيار النموذج
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — مجموعة التقييم
- `docs/EVALS_RUNBOOK.md` — تشغيل التقييمات
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — قواعد الحوكمة
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | مسودة أولى |
