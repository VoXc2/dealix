# AI Output QA Standard

**معيار الجودة للمخرجات:** [`../quality/QUALITY_STANDARD_V1.md`](../quality/QUALITY_STANDARD_V1.md) · [`../quality/QA_REVIEW_PROCESS.md`](../quality/QA_REVIEW_PROCESS.md)

## أبعاد QA

accuracy · source support · schema validity · Arabic quality · business usefulness · governance status · claim safety · actionability.

## Arabic QA

clarity · executive tone · Saudi business fit · no exaggeration · no literal translation · no guaranteed claims.

## قرار الدرجة

- **QA ≥ 90:** client-ready  
- **80–89:** review  
- **70–79:** revise  
- **‏‏<70:** reject  

## القاعدة

```text
No client-facing AI output without QA.
```

**الكود:** `ai_output_qa_band` — `standards_os/agent_control_standard.py`

**بوابة:** [`../company/SERVICE_READINESS_GATE.md`](../company/SERVICE_READINESS_GATE.md)

**صعود:** [`DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md`](DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md)