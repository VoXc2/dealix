# خط التسليم الآلي (Delivery Pipeline)

عندما يصبح الحساب «won»، يبدأ خط تسليم واضح — لكنه **لا يتقدّم خطوة قبل اكتمال
مدخلات العميل**.

## المراحل

```
intake → build → review → handoff → value_report → closed
```

`intake` لا يتحول إلى `build` إلا عندما `inputs_received = true`.

## المخرجات

- `data/delivery/pipelines.jsonl` — خطوط التسليم.
- `data/delivery/acceptance_gates.jsonl` — بوابات القبول لكل سبرنت.
- `data/delivery/weekly_value_reports.jsonl` — تقارير القيمة الأسبوعية.
- `data/delivery/tasks.jsonl` — مهام التنفيذ.

## بنية خط التسليم

| الحقل | المعنى |
| --- | --- |
| `client`, `selected_system`, `sprint_id` | العميل والنظام والسبرنت |
| `scope` | النطاق المحدد |
| `required_inputs` | مدخلات لازمة للبدء |
| `success_metric` | مؤشر نجاح قابل للقياس |
| `acceptance_criteria` | معايير القبول |
| `owner` | المسؤول |
| `stage`, `inputs_received` | المرحلة وحالة المدخلات |

## بوابة جاهزية التسليم

يفشل الخط إذا: لا نظام، لا نطاق، لا مدخلات، لا مؤشر نجاح، لا معايير قبول، لا
مسؤول، أو بدأ التنفيذ قبل استلام المدخلات. التطبيق:
`scripts/checks/check_delivery_gate.py`.

## تقرير القيمة الأسبوعي

كل عميل نشط يحصل على تقرير أسبوعي بمؤشرات وأدلة وخطوات تالية — هو ما يثبت القيمة
ويبرر التجديد.
