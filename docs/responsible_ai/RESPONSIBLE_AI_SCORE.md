# Dealix Responsible AI Score

كل عميل أو use case يمكن أن يأخذ **Responsible AI Score** (0–100) من سبعة أبعاد مرجّحة.

## الأبعاد والأوزان

| البعد | الوزن |
|--------|-------|
| Source clarity | 15 |
| Data sensitivity handling | 15 |
| Human oversight | 15 |
| Governance decision coverage | 15 |
| Auditability | 15 |
| Proof of value | 15 |
| Incident readiness | 10 |
| **المجموع** | **100** |

## القرار

| النطاق | المعنى |
|--------|--------|
| 85–100 | Responsible AI ready |
| 70–84 | Deploy with controls |
| 55–69 | Governance review required |
| <55 | Do not deploy |

## مثال (مرجعي)

```json
{
  "client": "Client A",
  "use_case": "Sales follow-up draft pack",
  "responsible_ai_score": 82,
  "decision": "Deploy with draft-only boundary and approval workflow"
}
```

## الكود

`auto_client_acquisition/responsible_ai_os/responsible_ai_score.py`
