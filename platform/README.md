# Platform Control Map — Self-Evolving Agentic Enterprise

This directory is the execution scaffold for the 15 dominance systems.

## System map

| # | System | Primary module | Required subpaths |
|---|--------|----------------|-------------------|
| 1 | Organizational Operating Fabric | `platform/operating_fabric/` | `event_mesh`, `context_engine`, `organizational_state` |
| 2 | Agentic BPM | `platform/agentic_bpm/` | `process_awareness`, `workflow_reasoning`, `explainability` |
| 3 | Digital Workforce | `platform/digital_workforce/` | `agent_org_chart`, `agent_performance`, `agent_supervision` |
| 4 | Governed Autonomy | `platform/runtime_governance/` | `tool_fencing`, `escalation`, `write_staging`, `reversibility` |
| 5 | Operational Memory | `platform/memory_fabric/` | `lineage`, `retrieval`, `reranking`, `citations` |
| 6 | Execution Dominance | `platform/execution_engine/` | `orchestration`, `queues`, `compensation_logic`, `recovery_engine` |
| 7 | Executive Intelligence | `platform/executive_intelligence/` | `forecasting`, `organizational_insights` |
| 8 | Observability Dominance | `platform/tracing/` + `observability/` | `metrics`, `alerts`, `incident_tracking` |
| 9 | Evaluation Dominance | `evals/` | `hallucination`, `retrieval`, `workflow_execution`, `governance`, `business_impact`, `operational_efficiency` |
| 10 | Continuous Evolution | `continuous_improvement/` | `releases`, `changelogs`, `versions` |
| 11 | Transformation Engine | `transformation/` | `maturity_model.md`, `operating_model.md`, `workflow_redesign.md`, `adoption_framework.md`, `ai_governance_rollout.md` |
| 12 | Organizational Graph | `platform/organizational_graph/` | `relationship_engine`, shared `context_engine` |
| 13 | Trust Engine | `platform/trust_engine/` | `explainability`, `accountability`, `reversibility` |
| 14 | Strategic Intelligence | `platform/market_intelligence/` | `strategic_reasoning`, `risk_forecasting` |
| 15 | Self-Evolving Enterprise | `platform/self_improvement/` | `feedback_loops`, `optimization`, `adaptive_orchestration` |

## Runtime invariants

1. No external action without policy gate and trace.
2. No high-risk write without staging and reversibility.
3. No workflow autonomy outside process boundaries.
4. No release promotion without eval and governance gates.
5. No executive recommendation without evidence lineage.

## Integration contract with existing Dealix modules

- Use existing OS modules under `auto_client_acquisition/` as domain logic sources.
- Use `api/` for governed entry points and decision passport enforcement.
- Use `evals/` for release gating evidence.
- Use `observability/` for incident reconstruction and rollback intelligence.
