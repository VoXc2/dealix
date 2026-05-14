# حزمة الخدمة — الحد الأدنى (12) وWorld-Class (15)

## World-Class — 15 عنصراً

لا تُعتبر خدمة **عالمية المستوى** حتى تُغطّى هذه العناصر في الوثائق والتسليم والمكالمات:

| # | العنصر | ملاحظات |
|---|--------|---------|
| 1 | Promise | الوعد الواحد الواضح |
| 2 | Target customer | لمن بالضبط |
| 3 | Pain | ألم محدد |
| 4 | Inputs | ما يجب أن يزودنا به العميل |
| 5 | Scope | ما يُنجز وما يُستبعد |
| 6 | Deliverables | قائمة مخرجات ملزمة |
| 7 | Timeline | مدة واضحة |
| 8 | Price | نطاق سعر أو سعر ثابت |
| 9 | Not included | ما لا يشمله العرض |
| 10 | Delivery process | مراحل التسليم (مربوطة بـ Dealix Method) |
| 11 | QA checklist | جودة، عربي، ادعاءات، مصادر |
| 12 | Governance checklist | PII، أساس، إرسال، audit |
| 13 | Report template | تقرير تنفيذي |
| 14 | Proof pack | إثبات مدخلات/معالجة/مخرجات/أثر/خطوة تالية |
| 15 | Upsell path | pilot / retainer / enterprise |

المنهجية: [`DEALIX_METHOD_AR.md`](DEALIX_METHOD_AR.md).  
الرؤية طويلة المدى: [`DEALIX_AI_OS_LONG_TERM_AR.md`](DEALIX_AI_OS_LONG_TERM_AR.md).

### مثال: Company Brain Sprint

| العنصر | محتوى مختصر |
|--------|--------------|
| Promise | تحويل ملفات الشركة إلى مساعد داخلي بمصادر |
| Pain | معرفة مبعثرة، أسئلة متكررة، بطء مبيعات |
| Inputs | PDF/DOCX، FAQs، سياسات، عروض، كتالوج، صلاحيات |
| Deliverables | جرد وثائق، قاعدة قابلة للبحث، Q&A، اقتباسات، قواعد وصول، eval، سير تحديث |
| QA | إجابة بمصدر؛ لا مصدر = لا إجابة؛ أحدث مصدر؛ جودة عربي/إنجليزي؛ لا تسرّب وثائق مقيدة |
| Upsell | Monthly Brain Management، Sales Knowledge، Policy Assistant، Enterprise Brain |

---

## الحد الأدنى في الريبو اليوم (12 ملفاً + مثال)

للتوافق مع التحقق الآلي [`scripts/verify_service_files.py`](../../scripts/verify_service_files.py) و`readiness >= 80`، يجب أن يتوفر على الأقل:

| # | العنصر | أين في الريبو |
|---|--------|----------------|
| 1 | Offer | `docs/services/<name>/offer.md` (أقسام Promise / Price / … السبعة) |
| 2 | Scope | `scope.md` |
| 3 | Price | داخل `offer.md` |
| 4 | Duration | داخل `offer.md` |
| 5 | Intake | `intake.md` أو ما يعادله حسب الخدمة |
| 6 | Data/File Request | `data_request.md` أو ما يعادله |
| 7 | Delivery Checklist | `delivery_checklist.md` |
| 8 | QA Checklist | `qa_checklist.md` |
| 9 | Product Module | موثّق في [`MODULE_MAP.md`](../product/MODULE_MAP.md) + كود |
| 10 | Report Template | `report_template.md` أو ما يعادله |
| 11 | Proof Pack | `proof_pack_template.md` |
| 12 | Upsell Path | `upsell.md` |

**إضافة احترافية:** `sample_output.md` — مثال مخرج للعرض والـ demo.

### سد الفجوة 12 → 15

- **Promise / Target / Pain:** غطّها في `offer.md` (أقسام Promise و Best for + وصف الألم في Intake أو Offer).  
- **Inputs:** `data_request.md` أو `intake.md`.  
- **Delivery process:** `delivery_checklist.md` + ربط صريح بمراحل Method في مقدمة الملف.  
- **Governance checklist:** [`../governance/GOVERNANCE_SERVICE_CHECKS_AR.md`](../governance/GOVERNANCE_SERVICE_CHECKS_AR.md) + قسم أو ملف `governance_notes.md` لاحقاً إذا لزم.

التحقق الآلي يفحص الملفات + هيكل `offer.md`؛ توسيع الـ15 يبقى مسؤولية تحرير الوثائق حتى نضيف فحوصات إضافية اختيارية.
