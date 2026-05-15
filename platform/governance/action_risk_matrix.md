# Action Risk Matrix

## خط سير إلزامي لكل Action

`risk score -> policy check -> approval check -> execution -> audit log`

## مستويات المخاطر

- **L0 (Informational)**: قراءة/تحليل فقط.
- **L1 (Low)**: إنشاء draft داخلي.
- **L2 (Medium)**: تعديل بيانات داخلية للـ tenant.
- **L3 (High)**: تحديثات CRM أو تواصل خارجي مهيأ للإرسال.
- **L4 (Critical)**: أي إرسال خارجي مباشر أو تغيير واسع النطاق.

## مصفوفة القرار

| Risk Level | Policy Check | Human Approval | Execution Mode |
|-----------|--------------|----------------|----------------|
| L0 | Required | No | Auto |
| L1 | Required | Optional by tenant policy | Auto |
| L2 | Required | Usually required | Guarded auto |
| L3 | Required | Mandatory | Manual/approved only |
| L4 | Required | Mandatory + 2nd control (if enabled) | Never auto |

## قواعد Dealix غير القابلة للتفاوض

- لا إرسال cold WhatsApp تلقائي.
- لا إرسال LinkedIn DM تلقائي.
- لا إرسال Gmail خارجي بدون موافقة صريحة.
- لا إنشاء Calendar event خارجي بدون موافقة صريحة.

## متطلبات السجل التدقيقي (Audit)

لكل action يجب حفظ:

- `action_id`
- `tenant_id`
- `actor_id`
- `risk_level`
- `policy_result`
- `approval_ref` (عند الحاجة)
- `execution_result`
- `timestamp`

## حالات المنع الفوري

- risk level غير معروف.
- policy غير قابل للتقييم.
- missing approval في L3/L4.
