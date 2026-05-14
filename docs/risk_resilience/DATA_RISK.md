# Data Risk

## مخاطر

مصادر غير واضحة · بيانات بلا allowed-use واضح · PII في الملفات · خلط عملاء · استخدام خارجي بلا موافقة.

## ضوابط

Source Passport · Allowed Use Registry · PII Detection · Data Retention · **No Source Passport = no AI use** · **External use = approval required**

## مثال Source Passport (مفاهيمي)

```json
{
  "source_id": "SRC-001",
  "source_type": "client_upload",
  "owner": "client",
  "allowed_use": ["internal_analysis", "draft_only"],
  "contains_pii": true,
  "sensitivity": "medium",
  "ai_access_allowed": true,
  "external_use_allowed": false,
  "retention_policy": "project_duration"
}
```

## قرارات تشغيلية

Unknown source → **BLOCK** external use.  
PII + allowed use غير واضح → **REDACT** أو **BLOCK**.  
رفع عميل + draft-only → **DRAFT_ONLY**.

**صعود:** [`PRIVACY_RISK.md`](PRIVACY_RISK.md)
