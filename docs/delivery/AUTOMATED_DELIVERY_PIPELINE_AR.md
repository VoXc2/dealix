# Automated Delivery Pipeline — خط التسليم

**الهدف:** بعد موافقة العميل، يتحرك التسليم في خط واضح. الأتمتة تكون في **التجهيز والتوجيه والتقارير**، وليست في الإرسال والالتزامات الخطرة (تبقى بموافقة بشرية).

- **Schema:** [`schemas/delivery_pipeline.schema.json`](../../schemas/delivery_pipeline.schema.json)
- **البيانات:** [`data/delivery/pipelines.jsonl`](../../data/delivery/pipelines.jsonl)
- **الحالة:** [`reports/delivery/DELIVERY_PIPELINE_STATUS.md`](../../reports/delivery/DELIVERY_PIPELINE_STATUS.md)

---

## 1. المراحل (stage)

```txt
interested
  → qualified
  → mini_proposal_ready
  → proposal_sent
  → payment_handoff
  → won
  → intake_required        ◄── بوابة: لا يبدأ التسليم قبل اكتمال الخمسة
  → delivery_started
  → first_output_ready
  → client_review
  → accepted
  → weekly_value_report
  → renewal_candidate
```

## 2. ما الذي يُؤتمت؟ وما الذي يُمنع؟

| يُؤتمت (تجهيز/توجيه/تقارير) | يبقى بموافقة بشرية |
|------------------------------|---------------------|
| إنشاء مجلد التسليم وقائمة intake | إرسال إيميلات خارجية |
| توليد مهام التسليم والقوالب | إرسال واتساب |
| توليد تقرير القيمة الأسبوعي (مسودة) | التسعير النهائي وروابط الدفع |
| تتبّع الإنجاز والعوائق | الالتزامات القانونية/العقود |
| تنبيه قائمة الموافقة | طلب API keys / بيانات حساسة |

## 3. المسار العام بعد الموافقة

```txt
Client agrees
→ إنشاء مجلد تسليم + intake checklist
→ توليد مهام التسليم + القوالب
→ أول تقرير قيمة (مسودة)
→ قائمة موافقة المؤسس
→ تتبّع الإنجاز
→ تقرير قيمة أسبوعي
```

تشغيل تقارير التسليم:

```bash
python3 scripts/generate_delivery_reports.py
```

---

## 4. القاعدة الأهم

> لا يبدأ التسليم (الانتقال إلى `delivery_started` وما بعده) قبل توفر **الخمسة**: النظام، Scope، المدخلات المطلوبة، success metric، مسؤول التسليم. التفاصيل في [DELIVERY_ACCEPTANCE_GATES_AR.md](DELIVERY_ACCEPTANCE_GATES_AR.md)، ويُفرَض آليًا بالفحص **C05**.
