# Account Intelligence OS — نظام ذكاء الحسابات

*القلب التشغيلي لـ Dealix Intelligence-to-Revenue Factory.*
*آخر تحديث: 2026-06-03*

---

## الهدف

تحويل Dealix من «مصنع 400 إيميل» إلى **مصنع استحواذ وتسليم أعمال يومي**:

```txt
اكتشاف شركات → تحليل عام → تحديد الألم → اختيار النظام المناسب
→ استخراج قنوات التواصل العامة → تحديد الدور المستهدف → إيميل مخصّص
→ سكربت اتصال → Mini Proposal → متابعة → تسليم → تقرير قيمة
```

كل شركة تصبح **Account Intelligence Pack** — ملف بيع كامل يجيب:

```txt
من الشركة؟ ماذا تعمل؟ كيف نتواصل معها؟ من الدور المناسب؟
ما الألم المحتمل؟ أي نظام يناسبها؟ ماذا نرسل؟ ماذا نقول بالاتصال؟
ما العرض المختصر؟ وإذا وافقت، ماذا نسلّم؟
```

---

## ماذا يقدر النظام؟ (Capability Honesty)

### يقدر بقوة
```txt
البحث عن الشركة · قراءة الموقع العام · معرفة القطاع/المدينة/الدولة ·
استنتاج الخدمات · تحديد قنوات التواصل العامة المنشورة · تحديد الدور الأنسب ·
استنتاج الألم المحتمل · اختيار نظام واحد · كتابة إيميل مخصّص · تجهيز Call Brief
· تجهيز Mini Proposal · تجهيز Delivery Pack
```

### يقدر أحيانًا (حسب توفّر البيانات العامة)
```txt
إيجاد هاتف عام من الموقع/Google Business · بريد عام (info@/sales@) ·
أسماء من صفحات الفريق/أخبار عامة · وظائف منشورة تدل على ألم · إشارات توسّع
```

### لا يُضمَن دائمًا (لذلك Evidence Levels)
```txt
رقم مباشر لصاحب القرار · بريد شخصي موثوق · ألم داخلي غير منشور ·
ميزانية الشركة · مشاكل حقيقية بلا دليل
```

> الفصل بين «يقدر» و«لا يُضمَن» هو سبب وجود **Evidence Levels** و**Contact Confidence**:
> لا نكتب ما لا نتحقق منه كحقيقة.

---

## المكوّنات (Architecture)

```txt
docs/systems/DEALIX_FIVE_SYSTEMS_AR.md        ← مصدر الحقيقة للأنظمة الخمسة
docs/account_intelligence/                     ← العقد + الأدلة + التقييم + التشغيل
docs/contacts/                                 ← سياسة + مصفوفة + قنوات + ثقة التواصل
docs/proposals/MINI_PROPOSAL_FACTORY_AR.md     ← مصنع العروض المختصرة
docs/delivery/DELIVERY_AUTOMATION_READINESS_AR.md ← جاهزية التسليم عند الفوز
docs/finance/STARTER_SPRINT_MARGIN_MODEL_AR.md ← نموذج الهامش
docs/security/EXTERNAL_CONTENT_UNTRUSTED_AR.md ← المحتوى الخارجي غير موثوق
schemas/                                       ← عقود البيانات (JSON Schema)
data/                                          ← الباقات + القنوات + الاكتشاف + العروض
reports/                                       ← التقارير + قيادة المؤسس
scripts/validate_account_intelligence.py       ← بوابة الجودة (17 فحصًا)
```

---

## كل باقة = 10 طبقات

```txt
1. Company Intelligence      6. Personalized Email Draft
2. Contact Targeting         7. Call Brief
3. Client Need Card          8. Follow-up Sequence
4. Recommended System        9. Mini Proposal Angle
5. Public Contact Channels   10. Delivery Readiness + Next Action
```

---

## بوابة الجودة (Quality Gate)

كل باقة تمر بـ 17 فحصًا في `scripts/validate_account_intelligence.py`:
schema validation، وجود نظام موصى، تطابق الدور، عدم اختلاق التواصل، معالجة غياب
التواصل، لغة احتمالية في L0/L1، منع الادعاءات الجازمة والضمانات، منع Re:/Fwd،
منع تسريب الأسماء الداخلية، صحة العروض المختصرة، اكتمال قيادة المؤسس، وأمان
المحتوى الخارجي.

> النتيجة الحالية: **17/17 ✅** (راجع `reports/account_intelligence/ACCOUNT_PACK_QUALITY_REVIEW.md`).
