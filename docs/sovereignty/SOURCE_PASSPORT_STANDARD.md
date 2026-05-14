# Source Passport Standard

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

**قواعد:** No allowed use → internal analysis فقط · PII + external بدون أساس → redact/block · إجراء خارجي → موافقة.

**السياق السعودي:** منظومة حوكمة بيانات وطنية (مثل **SDAIA**، **NDMO**) تجعل جواز المصدر **وسيلة بيعية** — [NDMO](https://www.ndmo.gov.sa).

**الكود:** `SourcePassport` · `source_passport_valid_for_ai` — `sovereignty_os/source_passport_standard.py`

**صعود:** [`../architecture/SOURCE_PASSPORT.md`](../architecture/SOURCE_PASSPORT.md) · [`OPERATING_SOVEREIGNTY.md`](OPERATING_SOVEREIGNTY.md)
