# Approval Policy — Dealix Governance

**المرجع الاستراتيجي:** [`../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md`](../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md)  
**مصدر YAML:** [`../../dealix/config/approval_policy.yaml`](../../dealix/config/approval_policy.yaml)

## المبدأ

كل إجراء **خارجي** أو **مالي عالي المخاطر** أو **ادّعاء أمني/امتثالي** يمر عبر بوابة موافقة + أدلة مسبقة عند الحاجة.

## أنواع إجراءات (مثال)

| النوع | مستوى الخطورة | موافقة | يُنشئ أدلة | أدلة مطلوبة مسبقاً |
|--------|----------------|--------|------------|---------------------|
| external_message | medium | نعم | نعم | — |
| scope_send | high | نعم | نعم | scope_requested (أو ما يعادلها في النظام) |
| invoice_send | high | نعم | نعم | scope_approved |
| diagnostic_final | high | نعم | نعم | مراجعة داخلية |
| proof_pack_final | high | نعم | نعم | مراجعة داخلية |
| case_study_publish | high | نعم | نعم | موافقة عميل |
| security_claim | critical | نعم | نعم | **مصدر تقني/قانوني** |
| discount_request | medium/high | نعم | نعم | — |
| refund_request | high | نعم | نعم | — |
| affiliate_payout | high | نعم | نعم | invoice_paid |
| agent_tool_action | حسب الأداة | غالباً نعم | نعم | حسب سياسة الأداة |

## عقيدة التشغيل

Signal → Source → Approval → Action → Evidence → Decision → Value → Asset

## KPI حوكمة (مرجع)

امتثال موافقات ≈ 100% للإجراءات المشمولة · لا إرسال آلي عالي المخاطر · صفر تسامح مع ادّعاءات بلا مصدر.
