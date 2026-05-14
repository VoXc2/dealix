# Source Passport Standard (Institutional)

**قاعدة:** No Source Passport = no AI use.

### مثال

```json
{
  "source_id": "SRC-001",
  "source_type": "client_upload",
  "owner": "client",
  "allowed_use": ["internal_analysis", "draft_only"],
  "contains_pii": true,
  "sensitivity": "medium",
  "relationship_status": "existing_relationship",
  "retention_policy": "project_duration",
  "ai_access_allowed": true,
  "external_use_allowed": false
}
```

**قواعد:** لا allowed use واضح → تحليل داخلي فقط · PII + أساس غامض → redact/block · إجراء خارجي → موافقة · مصدر مجهول → لا outreach.

**سياق PDPL / شفافية:** فجوات في إعلان عناصر الخصوصية في عينات تجارة إلكترونية سعودية — [arXiv:2602.18616](https://arxiv.org/abs/2602.18616).

**مرجع Canonical:** [`../sovereignty/SOURCE_PASSPORT_STANDARD.md`](../sovereignty/SOURCE_PASSPORT_STANDARD.md) · الكود: `sovereignty_os` + `institutional_control_os/source_passport.py`

**صعود:** [`INSTITUTIONAL_GOVERNANCE.md`](INSTITUTIONAL_GOVERNANCE.md)
