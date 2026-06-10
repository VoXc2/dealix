# Governance Runtime — منتج التنفيذ (Dominance Layer)

**طبقة تنفيذ:** حوكمة وقت التشغيل كـ **منتج تشغيل** لا «قسم امتثال» فقط.

**مرجع مؤسسي موسّع:** [`../enterprise/GOVERNANCE_RUNTIME_PRODUCT.md`](../enterprise/GOVERNANCE_RUNTIME_PRODUCT.md) · [`../trust/ENTERPRISE_TRUST_PACK.md`](../trust/ENTERPRISE_TRUST_PACK.md)

---

## لماذا خطّ أعمال؟

عند تسريع نشر AI تبقى **أمن البيانات والخصوصية والامتثال** من أعلى المخاوف لدى القيادات — انظر تغطية [TechRadar لمسوحات KPMG عن حمايات الأمن أثناء سباق نشر AI](https://www.techradar.com/pro/ai-is-no-longer-a-future-concept-but-an-operational-reality-new-kpmg-report-claims-firms-are-racing-to-deploy-ai-but-need-to-ensure-they-have-the-right-security-protections).

---

## مثال مخرجات (مرجعي)

```json
{
  "decision": "REQUIRE_APPROVAL",
  "risk_level": "medium",
  "matched_rules": ["external_action_requires_approval"],
  "redactions": ["phone"],
  "audit_event_id": "AUD-001",
  "next_action": "human_review"
}
```

## مكونات

Policy Engine · PII Detection · Allowed Use Checker · Claim Safety Checker · Channel Risk Checker · Approval Engine · Audit Log · AI Run Ledger · Escalation Rules  

**صعود:** [`AI_CONTROL_PLANE.md`](AI_CONTROL_PLANE.md) · [`ENTERPRISE_READINESS_LADDER.md`](ENTERPRISE_READINESS_LADDER.md)
