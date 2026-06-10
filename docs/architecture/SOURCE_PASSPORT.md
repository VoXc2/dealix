# Source Passport — جواز سفر المصدر

**Dealix source-centric:** كل دفعة بيانات/lot لها **مصدر**، **استخدام مسموح**، **PII**، **احتفاظ**، **علاقة** قبل أي AI أو تسليم خارجي.

## مخطط JSON مرجعي

```json
{
  "source_id": "SRC-001",
  "source_type": "customer_upload",
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

## الأسئلة التي يجب أن يجيب عليها النظام

- من أين جاءت البيانات؟  
- هل نستخدمها لهذا الغرض؟  
- هل فيها PII؟  
- هل نرسلها خارجًا؟  
- هل ندخلها نموذجًا؟  

**مرجع امتثال:** [`../data/DATA_READINESS_STANDARD.md`](../data/DATA_READINESS_STANDARD.md) · [`../ledgers/SOURCE_REGISTRY.md`](../ledgers/SOURCE_REGISTRY.md) · كود: `auto_client_acquisition/data_os/source_attribution.py` · [`trust_os` (جواز ككائن)](../trust/DATA_TRUST_ARCHITECTURE.md) · `auto_client_acquisition/trust_os/source_passport.py`

## Gate

انظر [`../company/SERVICE_READINESS_GATE.md`](../company/SERVICE_READINESS_GATE.md) — **Gate C — Data**.
