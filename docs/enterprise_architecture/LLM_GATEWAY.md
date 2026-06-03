# LLM Gateway — بوابة الذكاء الاصطناعي

## الهدف

كل استدعاء نموذج يمر عبر بوابة توفر: **توجيه النموذج**، **تسجيل التشغيل**، **حدود تكلفة**، **سياسات تخفيض/Redaction**، **ربط بالحوكمة**.

## قواعد Dealix

- **No AI call outside LLM Gateway** (في التصميم المستهدف؛ التنفيذ: `llm_gateway_v10`).
- **No prompt outside Prompt Registry** (توسع تدريجي عبر `prompt_registry` / كatalog المشروع).
- **No client-facing output without schema + governance + QA** (تكامل مع `governance_os` و`standards_os`).

## AI Run Ledger (مرجعي)

```json
{
  "ai_run_id": "AIR-001",
  "client_id": "CL-001",
  "project_id": "PRJ-001",
  "agent_id": "AGT-REV-001",
  "task": "score_accounts",
  "input_source_ids": ["SRC-001"],
  "redaction_applied": true,
  "prompt_version": "account_scoring_v1",
  "output_schema": "AccountScore",
  "model_route": "balanced_arabic_business",
  "governance_decision": "ALLOW_WITH_REVIEW",
  "qa_score": 91
}
```

## التنفيذ في الريبو

`auto_client_acquisition/llm_gateway_v10/` — يشمل `routing_policy.py`, `budget_policy.py`, `governance_shim.py`, `schemas.py`.

## معايير التوجيه (مرجعية)

نوع المهمة، مستوى المخاطر، حالة PII، جودة العربية، ميزانية التكلفة، زمن الاستجابة، صرامة المخطط (schema).

## روابط

- [GOVERNANCE_OS.md](GOVERNANCE_OS.md) — [PROOF_OS.md](PROOF_OS.md)
