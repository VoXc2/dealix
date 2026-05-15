# Dealix Enterprise Readiness Model (Revenue OS First)

## الهدف

هذا النموذج يحدد ما إذا كان Dealix أصبح "نظامًا تشغيليًا لا يمكن الاستغناء عنه" داخل شركة عميلة، بدل كونه مجرد طبقة AI تجريبية.

## مبدأ القرار

- لا نعتمد على كثرة الميزات.
- نعتمد على Workflow واحد حرج تشغيليًا يعمل باستمرار، بحوكمة، وبأثر مالي قابل للقياس.

## نطاق المرحلة الحالية

المرحلة الحالية تركز فقط على:

1. `sales_agent` واحد.
2. Workflow واحد: `lead_qualification`.
3. عزل متعدد المستأجرين (Tenant Isolation).
4. RBAC + Approval Gate + Audit Trail.
5. Observability + Eval + ROI reporting.

## طبقات الجاهزية (L0-L5)

### L0 — Prototype

- Demo يعمل محليًا.
- لا يوجد عزل tenants حقيقي.
- لا يوجد حوكمة تنفيذية كافية.

### L1 — Governed Single Tenant

- Tenant واحد يعمل end-to-end.
- جميع العمليات تحتوي `tenant_id`.
- Roleان أساسيان: `operator`, `approver`.
- قاعدة موافقة واحدة فعالة.

### L2 — Operational Embedding

- Workflow يعمل يوميًا مع فريق المبيعات.
- CRM sync يعمل (draft/approved mode).
- يوجد trace لكل تشغيل + metrics تشغيلية.

### L3 — Measurable Business Impact

- ROI report أسبوعي/شهري.
- Lead-to-meeting conversion baseline مقابل بعد التشغيل.
- زمن معالجة lead ينخفض بشكل موثق.

### L4 — Multi-Client Repeatability

- نفس الworkflow يعمل على 3 عملاء بدون كسر معماري.
- Playbooks ثابتة للتنصيب والتشغيل والتسليم.

### L5 — Enterprise Infrastructure Territory

- Reliability + governance + observability مستقرة.
- Rollback drill ناجح.
- Exec dashboard واضح وقابل للمراجعة.

## شروط النجاح التشغيلي (North-Star Acceptance)

النجاح يتحقق فقط عندما يعمل التالي معًا بدون chaos:

- 1 tenant
- 3 users
- 2 roles
- 1 workflow
- 1 agent
- 1 approval rule
- 1 CRM integration
- 1 observability trace
- 1 eval report
- 1 ROI report
- 1 rollback drill

## حالات الفشل التي تمنع الانتقال

- تنفيذ action خارجي بدون approval واضح.
- وصول بيانات tenant إلى tenant آخر.
- عدم توفر audit trail قابل للمراجعة.
- نجاح task لكن فشل governance compliance.
