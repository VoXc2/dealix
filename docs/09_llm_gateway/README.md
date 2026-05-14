# طبقة LLM Gateway

## كل استدعاء AI يمر عبر

model router، prompt registry، schema validator، redaction، cost guard، eval hook، AI run ledger.

## Model Routing

حسب: نوع المهمة، المخاطر، PII، جودة عربية، ميزانية تكلفة، زمن استجابة، صرامة المخطط.

## قواعد

- No AI call outside LLM Gateway.
- No prompt outside Prompt Registry.
- No client output without schema + governance + QA.

## تنفيذ

- `auto_client_acquisition/llm_gateway_v10/`، `docs/enterprise_architecture/LLM_GATEWAY.md`

## روابط

- [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
