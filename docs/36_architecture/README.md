# Architecture — الحزم وحدود API وأولوية MVP

## شجرة الحزم (مرجعية)

الهدف التنظيمي: `core_os`، `data_os`، `governance_os`، `llm_gateway`، `agent_os`، `workflow_os`، `revenue_os`، `brain_os`، `proof_os`، `value_os`، `capital_os`، `client_os`، `intelligence_os`، `command_os`، `trust_os`، `risk_os`، `standards_os`، `ecosystem_os`، `saudi_layer` — **التعيين الفعلي للمسارات** في `docs/enterprise_architecture/SYSTEM_MAP.md`.

## حدود API (ممنوع)

- `revenue_os` لا يرسل رسائل خارجية مباشرة.
- `agent_os` لا يتجاوز `governance_os`.
- `brain_os` لا يجيب بلا source registry.
- `client_os` لا يعرض مخرجات بلا governance status.
- `proof_os` لا ينشئ case بلا proof score.

## أولوية تنفيذ MVP (مراحل)

1. Core + Trust MVP: data/governance/llm/revenue/proof/value.  
2. Commercial MVP: diagnostic، sprint، draft pack، proof، client summary، trust pack.  
3. Retainer MVP: monthly value report، health، proof timeline، cadence، adoption review.  
4. Agent-safe MVP: identity، permissions، auditability card، runtime policy، kill switch، agent tests.  
5. Enterprise MVP: AI run ledger، evidence graph، approval engine، compliance report، trust dashboard، audit export.

## روابط

- [SYSTEM_MAP.md](../enterprise_architecture/SYSTEM_MAP.md)، [API_BOUNDARIES.md](../enterprise_architecture/API_BOUNDARIES.md)، [MVP_BUILD_ORDER.md](../enterprise_architecture/MVP_BUILD_ORDER.md)، [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
