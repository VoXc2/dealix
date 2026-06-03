# Evidence Graph

بدل سجلات منفصلة، Dealix تستهدف **Evidence Graph**: عقد (nodes) وروابط (edges) تُعيد بناء القصة كاملة.

## عقد (Nodes) — مرجعي

Client، Project، Source، Dataset، Agent، AI Run، Policy Check، Governance Decision، Human Review، Approval، Output، Proof Event، Value Event، Risk Event، Decision.

## علاقات (Edges) — مرجعي

- Source **used_by** AI Run  
- AI Run **produced** Output  
- Output **checked_by** Governance Decision  
- Governance Decision **requires** Approval  
- Approval **authorizes** Output  
- Output **supports** Proof Event  
- Proof Event **supports** Value Event  
- Risk Event **updates** Policy  
- Value Event **triggers** Board Decision  

## مثال JSON (مرجعي)

```json
{
  "source": "SRC-001",
  "used_by": "AIR-001",
  "produced": "OUT-001",
  "governed_by": "GOV-001",
  "reviewed_by": "REV-001",
  "supports": "PROOF-001",
  "created_value": "VAL-001"
}
```

## الكود

`auto_client_acquisition/evidence_control_plane_os/evidence_graph.py`
