# Dealix — Governed Revenue & AI Operations (قرار تنفيذي)

## التموضع المعتمد

- **EN:** Dealix — Governed Revenue & AI Operations
- **AR:** Dealix شركة تشغيل إيراد وذكاء اصطناعي محكوم بالأدلة والموافقات وقياس القيمة.

## نجم الشمال

- **Governed Value Decisions Created**  
  عدد القرارات التشغيلية/الإيرادية التي تحتوي:
  1) مصدر واضح، 2) موافقة موثقة، 3) أثر قابل للقياس، 4) Evidence trail.

## تسلسل الشركة

1. Service-led
2. Software-assisted
3. Evidence-led
4. Retainer-backed
5. Platform later

## سلّم العروض (الأولوية التجارية)

1. Governed Revenue Ops Diagnostic
2. Revenue Intelligence Sprint
3. Governed Ops Retainer
4. Trust Pack Lite (عند إشارة أمن/امتثال)
5. Board Decision Memo (للقيادة)

## آلة الحالة الصارمة (Evidence Levels)

- `prepared_not_sent` = L2
- `sent` = L4
- `replied_interested` = L4
- `meeting_booked` = L4
- `used_in_meeting` = L5
- `scope_requested` = L6
- `pilot_intro_requested` = L6
- `invoice_sent` = L7_candidate
- `invoice_paid` = L7_confirmed

### قواعد إلزامية

- لا `sent` بدون `founder_confirmed=true`.
- لا L5 بدون `used_in_meeting`.
- لا L6 بدون `scope_requested` أو `pilot_intro_requested`.
- لا L7 confirmed بدون payment.
- لا claim revenue قبل `invoice_paid`.

## KPIs التشغيل الأساسية (لا تضخيم مؤشرات)

- `sent_count`
- `reply_count`
- `meeting_count`
- `scope_requested_count`
- `invoice_sent_count`
- `invoice_paid_count`
- `retainer_opportunity_count`

## سياسة No-Build

أي ميزة جديدة تُبنى فقط إذا تحقق واحد على الأقل:

- workflow يدوي تكرر 3 مرات
- طلب عميل صريح
- تقليل خطر حقيقي
- تسريع تسليم مدفوع
- فتح retainer

## التفعيل داخل المنتج

التمثيل البرمجي الرسمي موجود في:

- `auto_client_acquisition/service_catalog/governed_revenue_ai_ops.py`
- `GET /api/v1/services/governed-operating-model`

هذا يضمن أن التموضع ليس نصًا تسويقيًا فقط، بل سطح تشغيل قابل للاستهلاك في الواجهة واللوحات.
