# AI Run Provenance

Every client-facing AI output must include provenance.

## Provenance fields

- ai_run_id  
- agent_id  
- model  
- prompt_version  
- input_sources  
- redaction_status  
- governance_status  
- qa_score  
- human_reviewer  
- output_version  
- delivered_at  

## Rule

No provenance → no delivery.

## Why

Traceability: when the client asks where a recommendation came from, the answer is knowable.

See: [`AI_RUN_LEDGER.md`](../ledgers/AI_RUN_LEDGER.md).
