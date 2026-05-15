# Dealix Enterprise Maturity Operating System

> Goal: **The operating infrastructure layer for the agentic enterprise.**

This is the governing operating-model layer over Dealix. It does **not**
re-implement the 34 systems below — every system maps to existing modules
in `auto_client_acquisition/*`, `core/*`, `dealix/*`, `api/*`. This layer
**indexes, documents, scores, and gates** them.

## How to know you have arrived

Do not measure features. Measure organizational capability across ten
dimensions: observable, governable, evolvable, measurable, orchestrated, workflow_native, enterprise_safe, agent_ready, transformation_ready, continuously_improving.

Run the scorer:

```bash
python platform/readiness_model.py
```

It prints `DEALIX_ENTERPRISE_MATURITY_VERDICT` and a per-dimension score.

## The seven phases

### Phase 1 — Foundation Maturity

_Turn Dealix from a project into a platform._

| System | Path | Risk | Implemented by |
|--------|------|------|----------------|
| Platform Foundation | `platform/foundation` | high | auto_client_acquisition/enterprise_os, auto_client_acquisition/platform_v10 |
| Identity | `platform/identity` | critical | auto_client_acquisition/agent_identity_access_os, api/security |
| RBAC | `platform/rbac` | critical | auto_client_acquisition/agent_identity_access_os, api/security |
| Multi-Tenant Architecture | `platform/multi_tenant` | critical | auto_client_acquisition/customer_data_plane, auto_client_acquisition/data_os |
| Security | `platform/security` | critical | auto_client_acquisition/security_privacy, auto_client_acquisition/secure_agent_runtime_os |
| Deployment / Infrastructure-as-Code | `platform/deployment` | high | auto_client_acquisition/enterprise_rollout_os, scripts/infra |
| Observability | `platform/observability` | medium | auto_client_acquisition/observability_v10, auto_client_acquisition/observability_adapters |

### Phase 2 — Agentic Runtime Maturity

_Run a governed digital workforce, not prompt->response._

| System | Path | Risk | Implemented by |
|--------|------|------|----------------|
| Agent Catalog | `agents` | high | auto_client_acquisition/agents, auto_client_acquisition/ai_workforce_v10 |
| Agent Runtime | `platform/agent_runtime` | critical | auto_client_acquisition/agent_os, auto_client_acquisition/secure_agent_runtime_os |
| Tool Registry | `platform/tool_registry` | high | auto_client_acquisition/agent_os/tool_permissions.py, auto_client_acquisition/tool_guardrail_gateway |
| Agent Memory | `platform/agent_memory` | high | core/memory, auto_client_acquisition/revenue_memory |
| Escalation | `platform/escalation` | high | auto_client_acquisition/approval_center, auto_client_acquisition/governance_os/approval_matrix.py |

### Phase 3 — Workflow Orchestration Maturity

_Value comes from workflow redesign, not AI alone._

| System | Path | Risk | Implemented by |
|--------|------|------|----------------|
| Workflow Catalog | `workflows` | high | auto_client_acquisition/workflow_os, auto_client_acquisition/workflow_os_v10 |
| Workflow Engine | `platform/workflow_engine` | high | auto_client_acquisition/workflow_os, auto_client_acquisition/workflow_os_v10 |
| Orchestration | `platform/orchestration` | high | auto_client_acquisition/orchestrator, auto_client_acquisition/agentic_operations_os |
| Execution Engine | `platform/execution_engine` | high | auto_client_acquisition/execution_os, auto_client_acquisition/delivery_factory |

### Phase 4 — Organizational Memory Maturity

_Proprietary operational memory is the moat._

| System | Path | Risk | Implemented by |
|--------|------|------|----------------|
| Knowledge | `platform/knowledge` | medium | auto_client_acquisition/knowledge_os, auto_client_acquisition/company_brain |
| Retrieval | `platform/retrieval` | medium | auto_client_acquisition/intelligence_os, auto_client_acquisition/revenue_memory |
| Reranking | `platform/reranking` | low | auto_client_acquisition/intelligence_os, auto_client_acquisition/intelligence |
| Organizational Memory | `memory` | medium | auto_client_acquisition/revenue_memory, core/memory |

### Phase 5 — Governance Maturity

_Governance is runtime-enforced, not documentation._

| System | Path | Risk | Implemented by |
|--------|------|------|----------------|
| Governance | `governance` | critical | auto_client_acquisition/governance_os, dealix/governance |
| Policy Engine | `platform/policy_engine` | critical | auto_client_acquisition/governance_os/policy_registry.py, auto_client_acquisition/governance_os/policy_check.py |
| Approval Engine | `platform/approval_engine` | high | auto_client_acquisition/governance_os/approval_matrix.py, auto_client_acquisition/approval_center |
| Risk Engine | `platform/risk_engine` | high | auto_client_acquisition/risk_resilience_os, auto_client_acquisition/governance_os/runtime_decision.py |

### Phase 6 — Evaluation Maturity

_Nothing reaches production without evals._

| System | Path | Risk | Implemented by |
|--------|------|------|----------------|
| Retrieval Evals | `evals/retrieval` | medium | evals/lead_intelligence_eval.yaml, tests/governance |
| Hallucination Evals | `evals/hallucination` | high | evals/arabic_quality_eval.yaml, tests/governance |
| Workflow Execution Evals | `evals/workflow_execution` | high | evals/revenue_os_cases.jsonl, tests/governance |
| Agent Behavior Evals | `evals/agent_behavior` | high | evals/personal_operator_cases.jsonl, tests/governance |
| Governance Evals | `evals/governance` | critical | evals/governance_eval.yaml, tests/governance |
| Business Impact Evals | `evals/business_impact` | medium | evals/outreach_quality_eval.yaml, evals/company_brain_eval.yaml |

### Phase 7 — Continuous Evolution Maturity

_Systems that evolve safely, forever._

| System | Path | Risk | Implemented by |
|--------|------|------|----------------|
| Continuous Improvement | `continuous_improvement` | medium | auto_client_acquisition/learning_flywheel, auto_client_acquisition/self_growth_os |
| Releases | `releases` | high | auto_client_acquisition/enterprise_rollout_os |
| Changelogs | `changelogs` | low | CHANGELOG.md |
| Versions | `versions` | medium | auto_client_acquisition/enterprise_rollout_os |


## Operating rules

Every system ships: `architecture.md`, `readiness.md`, `observability.md`,
`rollback.md`, `metrics.md`, `risk_model.md`, `tests/`.
Every deployment: staged rollout + eval checks + observability verification +
rollback readiness.
Every workflow: retries + failure recovery + audit logging + approvals +
analytics.
Every agent: governance boundaries + memory isolation + tool permissions +
escalation rules + runtime validation.

Architecture principles: AI-first workflows; humans **above** the loop; governed
autonomy; event-driven orchestration; policy-enforced execution; continuous
evaluation; safe evolution.

_Generated by `scripts/build_platform_scaffold.py` — edit that, not the output._
