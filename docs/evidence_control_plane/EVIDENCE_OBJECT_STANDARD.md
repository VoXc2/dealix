# Evidence Object Standard

كل دليل مهم في Dealix له **شكل موحد** (Evidence Object).

## الحقول (مرجع JSON)

```json
{
  "evidence_id": "EVD-001",
  "evidence_type": "governance_decision",
  "client_id": "CL-001",
  "project_id": "PRJ-001",
  "actor_type": "agent",
  "actor_id": "AGT-REV-001",
  "human_owner": "Revenue Owner",
  "source_ids": ["SRC-001"],
  "linked_artifacts": ["AIR-001", "OUT-001", "POL-001"],
  "summary": "Draft-only decision due to PII and no external approval.",
  "confidence": "high",
  "timestamp": "2026-05-14T10:00:00Z"
}
```

## القاعدة

**No critical action without Evidence Object.**

## الكود

`auto_client_acquisition/evidence_control_plane_os/evidence_object.py`
