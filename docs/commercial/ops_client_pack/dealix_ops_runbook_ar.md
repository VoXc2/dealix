# Dealix — Ops Runbook جاهز للتنفيذ

## الهدف
تحويل Phase MAX من عرض تقني إلى آلة تشغيل تجارية: عرض، ديمو، إثبات، Scope، Invoice، ثم Proof Pack.

## الحزمة التي تقدمها في المحادثة
1. Executive Deck: `dealix_ops_sales_kit_ar.pptx`
2. Live Demo: `/ar/business-now#strategy`
3. Proof Pack Sample: Evidence Ledger + Decision Passport + Value Report
4. Diagnostic Scope: inputs / outputs / timeline / price / acceptance criteria
5. Approval Policy: لا إرسال خارجي ولا case study ولا invoice live بدون موافقة

## التشغيل مرة واحدة
```bash
bash scripts/run_business_now.sh
```
افتح: `/ar/business-now#strategy` مع API على `:8000`.

## مسار المحادثة
### أول 30 ثانية
Dealix helps teams turn AI experimentation and revenue operations into governed, measurable workflows — with source clarity, approval boundaries, evidence trails, and proof of value.

### سؤال discovery
Where do AI experiments or revenue workflows currently create ambiguity, risk, or wasted follow-up?

### ديمو 12 دقيقة
1. افتح `/ar/business-now#strategy`
2. شغّل simulate حسب القطاع/المدينة/الميزانية
3. اعرض focus الحالي بصدق
4. افتح GTM أول 10
5. افتح Sales Script
6. اعرض Proof demo
7. اختم بـ Diagnostic Scope

## العرض الأول الذي تبيعه
**Governed Revenue Ops Diagnostic**

السعر المقترح:
- 4,999–9,999 SAR كبداية
- 15,000 SAR للعميل الأقوى أو النطاق الأوسع

## مخرجات التشخيص
- Revenue Workflow Map
- Source Quality Review
- Pipeline Risk Map
- Follow-up Gap Analysis
- Decision Passport
- Proof-of-Value Opportunities
- Recommended Sprint / Retainer

## قواعد عدم الهزل
- لا revenue قبل invoice_paid
- لا L5 قبل used_in_meeting
- لا L6 قبل scope_requested
- لا إرسال خارجي بدون founder_confirmed=true
- لا تبني feature جديدة قبل تكرار workflow ثلاث مرات
- أي score تجريبي يبقى `is_estimate: true`

## 72 ساعة القادمة
### اليوم 1
شغّل النظام، افتح الصفحة، جهّز screenshots، وثبت الرسالة.

### اليوم 2
اختر 5 warm contacts فقط. أرسل يدوياً. سجّل `sent` فقط بعد الإرسال.

### اليوم 3
صنّف الردود: interested / objection / wrong_segment / referral / silence.

## قرار الإغلاق
إذا العميل مهتم: لا تعرض المنصة كاملة. اعرض Diagnostic Scope فقط.

الجملة الختامية:
إذا كان هذا يعكس مشكلة عندكم، التشخيص المدفوع يحولها إلى workflow محكوم وقابل للقياس خلال أسبوعين.
