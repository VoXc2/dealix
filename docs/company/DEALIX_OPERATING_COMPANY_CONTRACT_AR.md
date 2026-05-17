# Dealix Operating Company Contract (Governed Acceleration)

هذا المستند يربط الرؤية التشغيلية الكبرى بـ **عقد تنفيذي داخل الكود** بدلاً من بقائها كنص نظري فقط.

المرجع البرمجي:

- `auto_client_acquisition/orchestrator/operating_company_contract.py`
- `auto_client_acquisition/orchestrator/policies.py`

## المعادلة التشغيلية

Dealix = AI-native Revenue Ops + Governance Infrastructure + Proof Pack Factory + Service-to-Platform Engine + GCC Trust Layer.

القاعدة الثابتة:

**No autonomous chaos. Governed acceleration.**

سلسلة القرار الإلزامية:

Signal → Source → Risk → Approval → Action → Evidence → Decision → Value → Asset

## ما الذي تم ترميزه (Codified) داخل العقد؟

1. **المصانع السبعة** كنماذج تشغيلية واضحة:
   - Demand Factory
   - Trust Factory
   - Sales Factory
   - Delivery Factory
   - Proof Factory
   - Product Learning Factory
   - Governance Factory

2. **اللوبات التسعة** (Market Signal, Founder Trust, Proof Funnel, Sales Conversion, Delivery, Upsell, Partner, Governance, Productization).

3. **Taxonomy للأحداث** موحّد للأحداث التجارية والتشغيلية (مثل: `lead_captured`, `scope_sent`, `invoice_paid`, `proof_pack_sent`).

4. **State Machine** موحّد لمراحل الفرصة من `new_lead` إلى `closed_won/closed_lost`.

5. **قواعد لا تُكسر (Event Guards)** مثل:
   - لا `message_sent` بدون `message_approved`.
   - لا `invoice_paid` بدون `payment_proof_ref`.
   - لا `diagnostic_started` قبل `invoice_paid`.
   - لا `proof_pack_sent` قبل `founder_reviewed=true`.
   - لا `case_study_approved` بدون `client_permission=true`.

6. **Approval Matrix قابلة للاستدعاء برمجياً**:
   - `send_scope` و `send_invoice` تتطلب موافقة بشرية.
   - `start_delivery` يتطلب دليل دفع.
   - `security_claim` و `publish_case_study` و `final_diagnostic` محكومة بالموافقة.
   - `agent_tool_action` يتطلب موافقة عند مخاطر متوسطة فأعلى.

## لماذا هذا مهم؟

- يمنع تضخم حالات الإيراد أو التسليم بلا دليل.
- يجعل كل قرار قابل للتدقيق (audit-ready).
- يحول التشغيل اليومي إلى أصول قابلة للتحويل لاحقاً إلى playbooks ثم modules.

## أولويات التفعيل التالية (Execution Hooks)

1. ربط `validate_event(...)` على بوابة كتابة الأحداث في الـ ledger.
2. توحيد `action_id` في الـ APIs التنفيذية (`send_scope`, `send_invoice`, `start_delivery`...).
3. إظهار مخالفات العقد داخل Dashboard (Approval Center + Evidence Ledger).
4. استخراج تقارير أسبوعية من المخالفات كمدخل مباشر لتحسين السياسات.
