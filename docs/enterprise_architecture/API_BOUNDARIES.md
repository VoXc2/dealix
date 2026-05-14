# API Boundaries

Allowed flow:
```
data_os → governance_os → llm_gateway → proof_os → value_os → intelligence_os → command_os
```

Forbidden:
- `revenue_os` does not send external messages directly.
- `agent_os` does not bypass `governance_os`.
- `brain_os` does not answer without source registry.
- `client_os` does not display output without governance status.
- `proof_os` does not create case without proof score.
