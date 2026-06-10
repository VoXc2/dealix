# Capability Maturity Model

Each **client capability** is scored **Level 0–5**. Use the same lens across the seven capabilities in [`CAPABILITY_OPERATING_MODEL.md`](CAPABILITY_OPERATING_MODEL.md).

## Levels

| Level | Name | Meaning |
|------:|------|---------|
| **0** | Absent | لا عملية واضحة، لا بيانات، لا مالك، لا مقياس |
| **1** | Manual | العمل يدوي ومتذبذب |
| **2** | Structured | عملية موثقة + مالك + مدخلات معروفة |
| **3** | AI-assisted | AI يساعد: مسودات، تقييم، تقارير، تلخيص |
| **4** | Governed AI workflow | AI مدمج مع **موافقات**، QA، سجلات، قياس |
| **5** | Optimized operating system | القدرة **متكررة**، مقاسة، محسّنة، وجزء منها **self-serve** حيث ينطبق |

## Example — Revenue capability

```text
L0: leads مبعثرة بلا تعريف موحد
L1: فريق مبيعات يتابع يدويًا
L2: مراحل pipeline موثقة + مصدر البيانات معروف
L3: AI يقيّم/يرتب + يولّد مسودات (بعد الموافقة)
L4: تسجيل + موافقات + تقارير جودة + hygiene لـ CRM
L5: Monthly AI RevOps OS — لوحة، proof، تحسين مستمر
```

## Sales language

> “نرفع **Revenue Capability** من L1 إلى L3 خلال Sprint، ثم L4 في Pilot، ثم نتجه نحو L5 مع الـ retainer إذا أثبتتم الجدية.”

Log levels in [`../clients/_TEMPLATE/CAPABILITY_ROADMAP.md`](../clients/_TEMPLATE/CAPABILITY_ROADMAP.md) (copy per client).
