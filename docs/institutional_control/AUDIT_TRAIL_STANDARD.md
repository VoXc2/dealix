# Audit Trail Standard

## ما يسأل عنه العميل الكبير

من استخدم البيانات؟ أي agent؟ أي prompt/model؟ من وافق؟ ما القرار؟ ما الدليل؟

## حدث تدقيق (مثال)

```json
{
  "audit_event_id": "AUD-001",
  "actor_type": "agent",
  "actor_id": "AGT-REV-001",
  "human_owner": "Dealix Revenue",
  "action": "score_accounts",
  "dataset_id": "DS-001",
  "source_id": "SRC-001",
  "policy_decision": "ALLOW_WITH_REVIEW",
  "approval_required": false,
  "timestamp": "2026-05-14T10:00:00Z"
}
```

## أهداف التغطية (اتجاه enterprise)

- تسجيل عمليات AI ذات الصلة · قرارات الحوكمة · ربط مخرجات العميل بأحداث تدقيق · موافقات الإجراءات الخارجية

**الكود:** `AuditEvent` · `audit_event_complete` — `institutional_control_os/audit_trail.py`

**صعود:** [`../product/AI_RUN_PROVENANCE.md`](../product/AI_RUN_PROVENANCE.md) · [`INSTITUTIONAL_GOVERNANCE.md`](INSTITUTIONAL_GOVERNANCE.md)
