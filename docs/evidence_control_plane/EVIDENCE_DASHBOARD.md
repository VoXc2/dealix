# Evidence Dashboard

اللوحة لا تعرض أرقامًا فقط؛ تعرض **فجوات الثقة** (Evidence gaps).

## محاور العرض

- Evidence Coverage %  
- Source Passport Coverage  
- AI Run Ledger Coverage  
- Policy Check Coverage  
- Human Review Coverage  
- Approval Linkage  
- Proof Linkage  
- Value Linkage  
- Risk Events  
- **Open Evidence Gaps**  

## أهم مقياس

**Evidence Coverage %** (مبسّط):

`critical events with required evidence / total critical events`

## العتبات

| النطاق | المعنى |
|--------|--------|
| < 70% | fragile |
| 70–84% | usable internally |
| 85–94% | client-ready |
| 95–100% | enterprise-ready |

## الكود

`auto_client_acquisition/evidence_control_plane_os/evidence_dashboard.py`
