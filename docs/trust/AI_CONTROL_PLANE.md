# Dealix AI Control Plane

الشركات التي تشغّل AI بجدية تحتاج **control plane** — ليس مجرد نماذج.

## Components

1. Agent Registry  
2. LLM Gateway  
3. Prompt Registry  
4. Model Router  
5. Cost Guard  
6. Eval Runner  
7. AI Run Ledger  
8. Policy Engine  
9. Approval Engine  
10. Kill Switch (لاحقًا حسب النضج)  

## مثال سجل تشغيل (مرجعي)

```json
{
  "ai_run_id": "AIR-001",
  "agent": "RevenueAgent",
  "task": "score_accounts",
  "model_tier": "balanced",
  "prompt_version": "lead_scoring_v1",
  "inputs_redacted": true,
  "output_schema": "AccountScore",
  "governance_status": "approved_with_review",
  "qa_score": 91,
  "risk_level": "medium",
  "cost": 0.42
}
```

## Why it matters

توسع **agentic / multi-agent** AI يرفع مخاطر الامتثال والخصوصية والأداء — انظر [KPMG — AI governance for the agentic AI era](https://www.kpmg.com/us/en/articles/2025/ai-governance-for-the-agentic-ai-era.html) ومسوحات مثل [KPMG AI Quarterly Pulse](https://kpmg.com/us/en/articles/2025/ai-quarterly-pulse-survey.html).

**الكود:** `auto_client_acquisition/trust_os/ai_control_plane.py`

**مراجع تقنية:** [`../governance/AGENT_REGISTRY.md`](../governance/AGENT_REGISTRY.md) · [`../product/AI_RUN_PROVENANCE.md`](../product/AI_RUN_PROVENANCE.md)

**صعود:** [`ENTERPRISE_TRUST_PACK.md`](ENTERPRISE_TRUST_PACK.md)
