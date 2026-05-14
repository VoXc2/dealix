# Privacy-by-Runtime

الخصوصية **ليست docs فقط** — يجب أن تكون **runtime**.

**مرجع:** مراقبة ممارسات بيانات الوكلاء أثناء التنفيذ — [AudAgent — arXiv:2511.07441](https://arxiv.org/abs/2511.07441).

## مسار كل مهمة AI

```text
Source Passport
→ PII Detector
→ Allowed Use Checker
→ Redaction
→ Policy Decision
→ Audit Event
→ Approval Requirement
```

## مثال قرار

```json
{
  "input_contains_pii": true,
  "allowed_use": ["internal_analysis", "draft_only"],
  "external_use_allowed": false,
  "decision": "DRAFT_ONLY",
  "required_action": "human_review_before_any_external_use"
}
```

**الكود:** `privacy_runtime_outcome` — `institutional_scaling_os/privacy_runtime.py`

**صعود:** [`../institutional_control/RUNTIME_GOVERNANCE.md`](../institutional_control/RUNTIME_GOVERNANCE.md)
