# Event Model — نموذج الأحداث التشغيلي

**القاعدة:** أحداث مهمة **ليست** مجرد صف في جدول — تبني audit · proof ledger · analytics · automation · client timeline · AI control tower.

## أحداث أساسية

`project_created` · `dataset_uploaded` · `data_quality_scored` · `pii_detected` · `governance_checked` · `account_scored` · `draft_generated` · `approval_required` · `approval_granted` · `proof_event_created` · `report_delivered` · `capital_asset_created` · `feature_candidate_created` · `retainer_recommended`

## مثال

```json
{
  "event_type": "governance_checked",
  "project_id": "PRJ-001",
  "decision": "REQUIRE_APPROVAL",
  "risk_level": "medium",
  "audit_event_id": "AUD-001",
  "created_at": "2026-05-13T12:00:00Z"
}
```

**سياسات التتبع:** [`../product/PRODUCT_TELEMETRY.md`](../product/PRODUCT_TELEMETRY.md) · [`../governance/AUDIT_LOG_POLICY.md`](../governance/AUDIT_LOG_POLICY.md)
