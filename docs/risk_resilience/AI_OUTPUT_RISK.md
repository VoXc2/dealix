# AI Output Risk

## مخاطر

دقة منخفضة · هلوسة · عربية تجارية ضعيفة · ادعاءات بلا أدلة · مخرجات بلا مصادر · توصيات غير مناسبة تجاريًا.

## ضوابط

Output schema validation · مراجعة بشرية · QA score · citations لـ Company Brain · unsupported-claim detector · Arabic business QA.

## قرار QA (0–100)

- ≥90 → client-ready  
- 80–89 → review  
- 70–79 → revise  
- <70 → reject  

**الكود:** `ai_output_qa_band` — `risk_resilience_os/risk_score.py`

## قواعد

```text
No source-less knowledge answer.
No unsupported business claim.
No client-facing AI output without QA.
```

**صعود:** [`AGENT_AUTONOMY_RISK.md`](AGENT_AUTONOMY_RISK.md)
