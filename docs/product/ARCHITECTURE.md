# Dealix Architecture

## Layers

1. Frontend
2. API
3. Service OS modules
4. AI Gateway
5. Governance
6. Data layer
7. Observability
8. Integrations

## Core modules (repo mapping)

| Name in docs | Python packages |
|--------------|------------------|
| Strategy OS | `strategy_os` |
| Data OS | `data_os`, `revenue_data_intake` |
| Revenue OS | `revenue_os` |
| Customer OS | `support_os`, customer inbox routers |
| Operations OS | `workflow_os_v10`, `delivery_factory`, `bottleneck_radar` |
| Knowledge OS | `knowledge_os` (facade), `company_brain_mvp`, `support_os/knowledge_answer.py` |
| Governance OS | `governance_os`, `compliance_os` |
| Reporting OS | `reporting_os`, `executive_reporting` |
| Delivery OS | `delivery_os`, `service_sessions` |

See [`../commercial/CODE_MAP_OS_TO_MODULES_AR.md`](../commercial/CODE_MAP_OS_TO_MODULES_AR.md).
