# Client Handoff Automation — أتمتة التسليم بعد البيع

**الهدف:** عند موافقة العميل، يتحول العرض المصغّر إلى خط تسليم جاهز بلا عمل يدوي في التجهيز — مع إبقاء كل خطوة خطرة خلف موافقة بشرية.

---

## 1. ماذا يحدث عند «won»؟

```txt
Deal Won / Client agrees
→ إنشاء Delivery Pipeline (DP-xxx) من Mini Proposal (MP-xxx)
→ نسخ required_inputs من العرض إلى الخط (provided = false مبدئيًا)
→ توليد Intake Checklist (المدخلات المطلوبة للنظام)
→ عند اكتمال المدخلات: توليد Delivery Tasks (DT-xxx) + القوالب
→ أول تقرير قيمة (مسودة) + إدراج في قائمة الموافقة
→ تتبّع الإنجاز والعوائق في التقارير
```

## 2. الربط بين الكيانات

```txt
Mini Proposal (MP)  ─► Delivery Pipeline (DP)  ─► Delivery Tasks (DT)
                                  │
                                  └─► Weekly Value Report (WVR)
```

- `pipelines.jsonl` — خط لكل عميل، حالته ومدخلاته ومسؤوله.
- `tasks.jsonl` — مهام السبرنت، لكل مهمة `requires_approval` و`approved` (الإرسال يبقى خلف موافقة).
- `weekly_value_reports.jsonl` — تقارير القيمة الأسبوعية.

## 3. لا تبدأ المهام قبل المدخلات

> الخط لا ينتقل إلى `delivery_started` قبل اكتمال **الخمسة**. حتى ذلك الحين يبقى في `won` / `intake_required` ويظهر في [`DELIVERY_BLOCKERS.md`](../../reports/delivery/DELIVERY_BLOCKERS.md). هذا يمنع «تسليمًا ناقصًا».

## 4. ما الذي يبقى يدويًا/بموافقة؟

```txt
- روابط الدفع والتسعير النهائي
- إرسال أي رسالة خارجية (بريد/واتساب)
- طلب API keys أو ملفات حساسة (يُمنع تخزين الأسرار)
- العقود والالتزامات
- نشر case study
```

## 5. التقارير التشغيلية

| التقرير | المصدر |
|---------|--------|
| [DELIVERY_PIPELINE_STATUS.md](../../reports/delivery/DELIVERY_PIPELINE_STATUS.md) | `pipelines.jsonl` |
| [DELIVERY_BLOCKERS.md](../../reports/delivery/DELIVERY_BLOCKERS.md) | `pipelines.jsonl` |
| [WEEKLY_VALUE_REPORT_QUEUE.md](../../reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md) | `weekly_value_reports.jsonl` |

```bash
python3 scripts/generate_delivery_reports.py
```
