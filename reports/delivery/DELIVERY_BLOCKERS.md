# Dealix — Delivery Blockers
*Date: 2026-06-03 | Blocked pipelines: 2*

> القاعدة: لا يبدأ التسليم قبل توفر الخمسة: النظام، Scope، المدخلات المطلوبة، success metric، مسؤول التسليم.

| # | Company | System | Stage | Missing (Delivery Not Ready) | Listed Blockers |
|---|---------|--------|-------|------------------------------|-----------------|
| 1 | TrainMe KSA | WhatsApp Client OS | intake_required | required_inputs (متى يحتاج العميل تصعيداً لإنسان, سياسة الملفات والصلاحيات) | بانتظار سياسة الملفات والصلاحيات; بانتظار تحديد قواعد التصعيد لإنسان |
| 2 | TechVenture Partners | Executive Command OS | won | delivery_owner; required_inputs (مؤشرات المبيعات الحالية, مصادر العملاء, أهم المخاطر, شكل التقارير الحالية, المسؤولون الداخليون) | لم يُعيَّن مسؤول تسليم (delivery owner); النواقل المطلوبة غير مكتملة |

## Action per Blocker

### TrainMe KSA — WhatsApp Client OS → `Delivery Not Ready`
- **Stage:** intake_required
- **Missing:** required_inputs (متى يحتاج العميل تصعيداً لإنسان, سياسة الملفات والصلاحيات)
- **Action:** اجمع النواقص أعلاه قبل الانتقال إلى `delivery_started`.

### TechVenture Partners — Executive Command OS → `Delivery Not Ready`
- **Stage:** won
- **Missing:** delivery_owner, required_inputs (مؤشرات المبيعات الحالية, مصادر العملاء, أهم المخاطر, شكل التقارير الحالية, المسؤولون الداخليون)
- **Action:** اجمع النواقص أعلاه قبل الانتقال إلى `delivery_started`.

*Generated from data/delivery/pipelines.jsonl on 2026-06-03*
