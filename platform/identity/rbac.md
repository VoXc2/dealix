# RBAC Model — Revenue OS

## الأدوار الأساسية (النسخة الحالية)

1. `sales_operator`
   - تشغيل workflow
   - مراجعة المقترحات
   - لا يملك تنفيذ actions عالية المخاطر

2. `sales_approver`
   - الموافقة على الإجراءات عالية المخاطر
   - اعتماد التحديثات النهائية قبل التنفيذ

3. `tenant_admin`
   - إدارة السياسات والأدوار داخل tenant
   - الوصول لتقارير التدقيق والجاهزية

## Permission Model

كل صلاحية بصيغة:

`resource:action:scope`

أمثلة:

- `lead:read:tenant`
- `workflow:run:tenant`
- `crm:update:tenant`
- `approval:grant:tenant`

## قواعد الإلزام

- لا يوجد وصول بصلاحية عامة (`*`) في الإنتاج.
- صلاحيات التنفيذ الخارجي تتطلب policy gate.
- صلاحيات approval لا تُدمج مع دور التنفيذ التلقائي.

## فصل الواجبات (SoD)

- من يقترح action لا يعتمد نفس action في الحالات عالية المخاطر.
- approval يتطلب role مستقل أو user مختلف حسب policy.

## مصفوفة دور-إجراء (الحد الأدنى)

| Action | sales_operator | sales_approver | tenant_admin |
|-------|-----------------|----------------|--------------|
| Run lead workflow | Allow | Allow | Allow |
| Approve high-risk action | Deny | Allow | Allow |
| Execute CRM update (high risk) | Deny | Allow | Allow |
| View audit logs | Limited | Allow | Allow |
| Manage policy rules | Deny | Deny | Allow |
