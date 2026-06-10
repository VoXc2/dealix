# Agent Risk Score

## الأبعاد والأوزان

| البعد | الوزن |
|--------|-------|
| Data sensitivity | 20 |
| Tool risk | 20 |
| Autonomy level | 20 |
| External action exposure | 15 |
| Human oversight | 10 |
| Audit coverage | 10 |
| Business criticality | 5 |

## النطاقات

| النقاط | المستوى |
|--------|---------|
| 0–30 | low |
| 31–60 | medium |
| 61–80 | high |
| 81–100 | restricted / not allowed |

## الكود

`auto_client_acquisition/agentic_operations_os/agent_risk_score.py`
