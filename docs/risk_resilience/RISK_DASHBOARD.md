# Risk Dashboard

يعرض (تشغيليًا): مخاطر مفتوحة · عالية الخطورة · حوادث حوكمة · إجراءات غير آمنة محظورة · أعلام PII · انتهاكات شركاء · إيراد سيء مرفوض · scope creep · proof ضعيف · مخاطر صلاحيات وكلاء.

## مثال قرار (JSON)

```json
{
  "risk": "Agent over-permission",
  "severity": "high",
  "signal": "RevenueAgent requested external sending tool",
  "decision": "deny tool; keep draft-only; add approval workflow"
}
```

**صعود:** [`SAUDI_RISK_LAYER.md`](SAUDI_RISK_LAYER.md)
