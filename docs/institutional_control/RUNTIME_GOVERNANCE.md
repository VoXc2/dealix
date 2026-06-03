# Runtime Governance — الخندق المؤسسي

لا يكفي **policy PDF**؛ الحوكمة تعمل **أثناء التشغيل**. المخاطر تظهر في المسار والسياق — بيئة تنفيذ تحمي تدفق بيانات المستخدم — [arXiv:2604.19657](https://arxiv.org/abs/2604.19657)؛ مراقبة ممارسات البيانات للوكلاء — [AudAgent — arXiv:2511.07441](https://arxiv.org/abs/2511.07441).

## تدقيق وقت التشغيل

يفحص: source status · PII · allowed use · claim risk · channel risk · agent autonomy · approval requirement · **audit event**.

### مثال قرار

```json
{
  "decision": "DRAFT_ONLY",
  "risk_level": "medium",
  "reason": "Personal contact data exists but external action is not approved.",
  "matched_rules": ["external_action_requires_approval"],
  "audit_event_id": "AUD-001",
  "next_action": "human_review"
}
```

## سؤال العميل الجاد

ما البيانات؟ من وافق؟ ماذا حُظر؟ أين الدليل؟ ما المخاطر؟ ما الخطوة التالية؟

**الكود:** `governance_runtime_checklist_passes` · `evaluate_output_governance` — `institutional_control_os/governance_runtime.py`

**صعود:** [`../endgame/RUNTIME_GOVERNANCE_PRODUCT.md`](../endgame/RUNTIME_GOVERNANCE_PRODUCT.md) · [`INSTITUTIONAL_GOVERNANCE.md`](INSTITUTIONAL_GOVERNANCE.md)
