# أسئلة مشتريات · أمن · RFP — إجابات جاهزة (Dealix)

**الحالة:** مسودة داخلية — راجع محامياً قبل إرسال RFP رسمي  
**آخر تحديث:** 2026-05-18

---

## A) الشركة والمنتج

| سؤال | إجابة |
|------|--------|
| ما هو Dealix؟ | Revenue OS عربي أولاً: ذاكرة إيرادات، Decision Passport، وكلاء بموافقة بشرية. |
| هل CRM؟ | لا — يكمّل CRM؛ يركز على قرار وإثبات وأتمتة محكومة. |
| من يستخدمه؟ | مؤسسون وفرق إيراد B2B في السعودية/GCC (وكالات، SaaS مبكر). |

---

## B) الأمان والوصول

| سؤال | إجابة |
|------|--------|
| مصادقة API | Admin API key · جلسات تطبيق حسب النشر |
| تشفير نقل | TLS 1.2+ |
| تشفير تخزين | at-rest حسب مزود DB (Railway/AWS) |
| سجل تدقيق | Revenue events + middleware على مسارات PII |
| pentest | حسب خطة enterprise — غير معلن علناً حتى إتمام |

---

## C) PDPL والخصوصية

| سؤال | إجابة |
|------|--------|
| الأدوار | عميل Controller لبيانات عملائه؛ Dealix Processor |
| DPA | [`docs/DPA_DEALIX_FULL.md`](../DPA_DEALIX_FULL.md) / pilot template |
| DSAR | 30 يوم هدف — [`PDPL_DATA_SUBJECT_REQUEST_SOP.md`](../PDPL_DATA_SUBJECT_REQUEST_SOP.md) |
| خرق | runbook + `integrations/pdpl.py` |
| DPO | عند عميل مؤسسي #1 — قالب appointment |
| إخطار SDAIA | **لا تلتزم بصياغة 72h في RFP دون محامٍ** |

---

## D) الإقامة ونقل البيانات

| سؤال | إجابة |
|------|--------|
| أين DB؟ | **يُملأ per contract** — انظر ملحق INFRA |
| نسخ احتياطي | region منفصل مُوثّق |
| LLM | US محتمل — إفصاح + تقليل PII |
| نقل عبر الحدود | بنود DPA + قائمة subprocessors |
| حذف عند الإنهاء | محو/إرجاع حسب DPA |

**ملحق:** [`INFRA_HOSTING_REGION_RUBRIC_AR.md`](INFRA_HOSTING_REGION_RUBRIC_AR.md)

---

## E) AI والامتثال التشغيلي

| سؤال | إجابة |
|------|--------|
| إرسال تلقائي؟ | لا واتساب بارد · لا LinkedIn auto · لا Gmail خارجي بدون موافقة |
| تدريب على بيانات العميل؟ | لا بيع بيانات؛ معالجة لخدمة العقد فقط |
| قرارات آلية | يمكن مراجعة بشرية — حق الاعتراض في DSAR SOP |
| مستوى أدلة | L0–L5 — لا تسويق تحت L4 |

---

## F) التوفر والاستمرارية

| سؤال | إجابة افتراضية (عدّل في Enterprise SLA) |
|------|------------------------------------------|
| RPO | ≤ 24h |
| RTO | ≤ 4h (هدف داخلي) |
| نسخ | يومي |
| منطقة DR | نفس region أو GCC ثانوي — حسب خيار الاستضافة |

---

## G) تكاملات

| سؤال | إجابة |
|------|--------|
| HubSpot | عند Truth Matrix أخضر + token |
| Calendly | webhooks + booking |
| Moyasar | دفع SAR |
| Webhooks | generic للأنظمة الأخرى |

---

## H) مرفقات نموذجية لـ RFP

1. [`MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`](MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md) (داخلي — استخرج فقرات للعميل)
2. `landing/privacy-policy.html`
3. `landing/sub-processors.html`
4. ملحق INFRA مملوء (خارج git)
5. Sample Proof Pack (إن متوفر)

---

## I) أسئلة يجب توجيهها للعميل

| سؤال | لماذا |
|------|-------|
| هل تشترط إقامة KSA فقط أم GCC؟ | يحدد خيار C/D |
| من Controller لبيانات leads؟ | DPA roles |
| هل LLM خارجي مقبول؟ | بنود عقد |
| حجم PII في CRM؟ | DPIA |
