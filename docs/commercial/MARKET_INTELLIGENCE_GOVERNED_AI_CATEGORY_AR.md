# فئة «AI للإيرادات بحوكمة» — Trust Plane وتمييز Dealix

**آخر تحديث:** 2026-05-18

---

## 1) تعريف الفئة (للمشتري)

**Governed Revenue AI:** أنظمة تُعدّ مسودات قرار وإجراءات إيرادية، وتنفّذ خارجياً **فقط** بعد موافقة بشرية، مع **سجل تدقيق** و**مستوى أدلة** قبل الإنفاق على قنوات.

**ليس:** شات بوت يرسل آلاف الرسائل · CRM + GPT wrapper · تنبؤ بلا مصدر.

---

## 2) اتجاه السوق 2025–2026

| إشارة | ماذا يبيع السوق | مواءمة Dealix |
|-------|----------------|---------------|
| منصات governed execution | approval + audit | Safe Agent Runtime |
| ضغط امتثال | PDPL + contactability | Compliance OS |
| تخويف من AI outbound | سياسات شركات | NO_COLD_WHATSAPP في الكود |
| RevOps tooling | pipeline hygiene | anti-waste API |

**أمثلة فئة (لا تُذكر في عروض العملاء):** Tektonic، Orcaworks — [روابط في خطة الاستخبارات]

---

## 3) Trust Plane — أربع طبقات

| طبقة | آلية Dealix | تحقق |
|------|-------------|--------|
| Policy | doctrine + commercial_ops | `tests/test_commercial_doctrine.py` |
| Draft | queue approval | `/ops/approvals` |
| Evidence | L0–L5 | `decision-passport/evidence-levels` |
| Execute | يدوي بعد موافقة | لا auto-send خارجي |

---

## 4) Decision Passport — للمهندس والمبيعات

| عنصر | وصف | API |
|------|-----|-----|
| Golden chain | سلسلة قرار مرجعية | `GET .../golden-chain` |
| Evidence levels | L0–L5 | `GET .../evidence-levels` |
| Lead intake | جواز مع lead | `POST /api/v1/leads` |
| Anti-waste | لا تسويق تحت L4 | `POST .../anti-waste/check` |

**جملة للعميل:** «كل إجراء خارجي يحمل: القرار، الدليل، الموافق، وما لم يُسمح به.»

---

## 5) أسئلة المشتري التقنية (10)

| # | سؤال | إجابة مختصرة |
|---|------|--------------|
| 1 | هل ترسلون واتساب بارد؟ | لا — مسودة فقط |
| 2 | هل LinkedIn آلي؟ | لا |
| 3 | هل Gmail يُرسل وحده؟ | لا بدون موافقة |
| 4 | أين سجل التدقيق؟ | Revenue Memory + middleware |
| 5 | كيف تقللون PII للـ LLM؟ | redaction + سياسة موجهات |
| 6 | من Controller؟ | العميل لبيانات عملائه؛ Dealix Processor |
| 7 | قائمة المعالجين؟ | sub-processors.html |
| 8 | حق المحو؟ | DSAR SOP + pdpl.py |
| 9 | مستوى أدلة التسويق؟ | لا حملة عامة تحت L4 |
| 10 | تكامل HubSpot؟ | حسب Truth Matrix — أخضر فقط |

**تفصيل RFP:** [`MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md`](MARKET_INTELLIGENCE_PROCUREMENT_FAQ_AR.md)

---

## 6) مقارنة سريعة (جدول عرض)

| | CRM + ChatGPT | Sales engagement | Dealix |
|--|---------------|------------------|--------|
| موافقة قبل إرسال | يدوي خارجي | جزئي | مدمج |
| أدلة قرار | لا | لا | Decision Passport |
| سياق سعودي/عربي | عام | عام | أولاً |
| PDPL في التصميم | لاحق | لاحق | من البداية |
| تسعير محلي | USD غالباً | USD | SAR ladder |

---

## 7) مسارات منتج للتعزيز (بدون كود هنا)

1. عرض Evidence level في UI Founder لكل صفقة نشطة.
2. تقرير أسبوعي «إجراءات مرفوضة بسبب anti-waste».
3. تصدير Decision Passport PDF للعميل (Proof Pack).

---

## 8) روابط

- [`MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`](MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md)
- [`POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md`](POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md)
- AGENTS.md — non-negotiables
