# نمو الإيرادات في 10 أيام / Grow Revenue Sprint
## Lead Intelligence Sprint — Customer-Facing Offer Page

---

## المشكلة / The Problem

**AR:** عندك آلاف السجلات في Excel أو CRM، لكن لا أحد يعرف من **يجب التواصل معه الآن**. الفرق المبيعات تصرف ساعات يوميًا في فلترة Sheets يدويًا، التكرارات تُضاع، البيانات بدون مصادر موثّقة، والمسودات بالعربي تخرج بمستوى أقل من الإنجليزي. النتيجة: pipeline ضعيف، اجتماعات قليلة، رسائل تواصل غير مقنعة.

**EN:** Thousands of records in Excel or CRM, but no one knows **who to contact first**. Reps lose hours filtering sheets manually, duplicates are hidden, sources are unverified, and Arabic outreach drafts are visibly weaker than English. The result: thin pipeline, few meetings, unconvincing messages.

---

## الوعد / The Promise

**AR:** خلال **10 أيام عمل**، نحوّل بياناتك المبعثرة إلى:
- **50 حسابًا سعوديًا مرتّبًا** حسب احتمالية الإغلاق (شرائح A/B/C/D واضحة).
- **10 إجراءات فورية** مع رسائل بيلينغوال جاهزة للإرسال (بعد موافقتك).
- **تقرير تنفيذي** يعرضه CEO في اجتماع المجلس القادم.

**EN:** In **10 business days**, we turn messy data into:
- **Top 50 ranked Saudi accounts** by close probability (clear A/B/C/D bands).
- **10 immediate actions** with bilingual outreach drafts ready to send (after your approval).
- An **executive report** the CEO can show in the next board meeting.

---

## ما تستلمه / What You Receive (Deliverables)

| البند / Deliverable | التفاصيل / Detail |
|---|---|
| 1. مجموعة بيانات نظيفة | حتى 5,000 سجل، مع Data Quality Score من Dealix |
| 2. أعلى 50 حسابًا | مع شريحة A/B/C/D + تفسير لكل تصنيف |
| 3. أعلى 10 إجراءات | مع مالك مقترح + موعد + قيمة متوقعة (SAR) |
| 4. مسودات تواصل بيلينغوال | 10 مسودات مع تذييل PDPL المادة 13 |
| 5. Mini CRM | لوحة Kanban بـ Stages مرتّبة |
| 6. تقرير تنفيذي بيلينغوال | 18 صفحة PDF/PPT — جاهز للعرض |
| 7. جلسة تسليم 60 دقيقة | مسجّلة، مع QA كامل |
| 8. حزمة إثبات | KPIs قبل/بعد لإعادة الاستخدام داخليًا |

---

## السعر والشروط / Price & Terms

| البند | القيمة |
|---|---|
| **السعر الثابت / Fixed price** | **SAR 9,500** (ضريبة القيمة المضافة 15% خارج السعر) |
| **المدة / Timeline** | 10 أيام عمل |
| **الدفع / Payment** | Net 14، 100% عند التسليم |
| **عقد / Contract** | SOW جاهز للتوقيع — 4 صفحات |
| **ضمان / Guarantee** | Data Quality Score ≥ 80 أو نُعيد المعالجة بدون رسوم إضافية |

---

## غير مشمول (Not Included)

لكي لا توجد مفاجآت، نوضّح ما **لا** يشمله Sprint:
- **لا نُرسل أي رسالة تواصل نيابةً عنك.** كل إرسال يحتاج موافقتك الصريحة.
- لا نقوم بـ web scraping ولا LinkedIn automation ولا cold WhatsApp.
- لا نضمن "اجتماعات" أو "صفقات" — نضمن جودة البيانات والترتيب فقط.
- لا تكامل CRM مخصص (يُتاح في مشروع منفصل).
- لا نشترك ببيانات من مزودين خارجيين على حسابنا.
- **لا ادعاءات غير موثّقة** في أي مسودة (مرشَّحة آليًا).

---

## مناسب لـ / Best For

- شركات B2B سعودية في BFSI أو Retail أو Healthcare أو Logistics.
- فرق مبيعات بين 5 و50 مندوبًا.
- مَن لديه CRM (Salesforce / HubSpot / Zoho / Excel) لكن البيانات مبعثرة.
- مَن يريد **تقرير تنفيذي جاهز للعرض على المجلس**، وليس مجرد ملفًا.

---

## كيف تبدو النتيجة / What the Output Looks Like

> "From 5,000 messy records to SAR 6.4M ranked pipeline in 10 days."

شاهد نموذج تقرير تنفيذي حقيقي (بيانات اصطناعية): `docs/services/lead_intelligence_sprint/sample_output.md`

---

## ضمانات الجودة / Quality Guarantees

| البند | القيمة |
|---|---|
| Data Quality Score بعد التنظيف | ≥ 80 (أو إعادة معالجة مجانية) |
| PDPL Art. 13/14 footer | على 100% من المسودات |
| الادعاءات المحظورة | 0 (تمر بـ `forbidden_claims.py`) |
| PII auto-redaction | 100% (تمر بـ `pii_detector.py`) |
| Bilingual quality parity | AR ≥ EN (لا فرق ملحوظ) |
| تغطية audit log | 100% من الأحداث في `event_store` |

---

## مسار الترقية / Upgrade Path

بعد Sprint، تختار:

1. **Sprint v2** بسعر SAR 14,000 — توسيع إلى Top 100 + 20 مسودة إضافية + 2 رحلة email.
2. **Monthly RevOps Retainer** بسعر **SAR 18,000/شهريًا** — تنظيف مستمر + إعادة تصنيف + 20 مسودة بيلينغوال شهريًا + 4 ساعات استشارية أسبوعيًا + ورشة QBR ربعيًا.

---

## خطوة البدء / Call to Action

**AR:** 25 دقيقة معك لنتأكد أن Sprint مناسب لبياناتك. لا التزام. اطلب الموعد بكلمة واحدة: **"ابدأ"** ردًا على أي بريد من Dealix، أو احجز مباشرة عبر الرابط أدناه.

**EN:** 25 minutes to confirm the Sprint fits your data. No commitment. Reply **"start"** to any Dealix email, or book a slot directly below.

> **احجز جلستك / Book your slot:** [calendly.com/dealix/grow-revenue-sprint](#)
> **أو راسلنا / Or email:** sales@dealix.me

---

## روابط ذات صلة / Related links

- [نموذج تقرير تنفيذي / Sample executive report](../../services/lead_intelligence_sprint/sample_output.md)
- [نطاق الخدمة / Scope](../../services/lead_intelligence_sprint/scope.md)
- [نموذج طلب البيانات / Data intake form](../../services/lead_intelligence_sprint/intake.md)
- [حزمة الإثبات / Proof pack template](../../services/lead_intelligence_sprint/proof_pack_template.md)
- [سيناريو المبيعات / Sales script](../sales_script.md)
- [إجابات الاعتراضات / Objection handling](../objection_handling.md)

---

*Dealix · sales@dealix.me · `service_id: lead_intelligence_sprint` · SAR 9,500 · 10 أيام عمل*
