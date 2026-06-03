# عقد مخرجات الوكلاء التجاريين

نفس الحقول الإلزامية في `AGENT_OUTPUT_CONTRACT_AR.md` مع ثوابت تجارية إضافية:

- كل عرض يحمل `product_id` مطابق للكتالوج، و`qualified_opportunity=true`.
- السعر يُذكر **كنطاق** فقط ما لم توجد `price_approved_by_human=true`.
- تسليم الدفع يحمل `approved_by_human=true` و`qualified=true` قبل التنفيذ.
- الصفقة المربوحة تحمل `delivery_handoff=true` و`customer_success_handoff=true`.
- التجديد يحمل `delivered_value=true` و`delivery_completed=true`.

## مثال (عرض)

```json
{
  "agent": "Proposal Agent",
  "summary": "مسودة عرض P1 لعميل مؤهَّل",
  "business_impact": "احتمال إغلاق ضمن النطاق المتوقع — بدون ضمانات",
  "files_touched": ["company_os/revenue/proposals.json"],
  "evidence_level": "internal_data",
  "risk_level": "high",
  "approval_required": true,
  "product_id": "P1_SPRINT",
  "qualified_opportunity": true,
  "price_range": "2,500 - 7,500 SAR",
  "tests_checks_run": ["pytest tests/test_proposal_maps_to_product_catalog.py"],
  "rollback": "revert proposals.json change",
  "next_founder_action": "اعتماد السعر النهائي والموافقة على الإرسال"
}
```
