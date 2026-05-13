# Dealix Enterprise Architecture & Operating System Blueprint

> Dealix is not an AI agency. It is an AI Operations OS. Every module has a job, every event has a log, every decision has evidence, every client has a workspace.

Layer 22 consolidated doctrine.

## 1. Architecture thesis

Every AI output passes:

```
Source Passport → Data Classification → LLM Gateway → Governance Runtime →
QA → Approval → Audit Event → Proof Event → Value Event → Board Decision
```

## 2. System Map

```
auto_client_acquisition/
  core_os/        data_os/         governance_os/  llm_gateway/
  agent_os/       workflow_os/     revenue_os/     brain_os/
  proof_os/       value_os/        capital_os/     client_os/
  intelligence_os/ command_os/    trust_os/        risk_os/
  standards_os/   ecosystem_os/
```

Plus the doctrine packages:

```
endgame_os/  global_grade_os/  command_control_os/  sovereignty_os/
strategic_control_os/  operating_manual_os/  institutional_control_os/
institutional_scaling_os/  board_ready_os/  proof_architecture_os/
value_capture_os/  ecosystem_os/  adoption_os/  enterprise_rollout_os/
intelligence_compounding_os/  operating_finance_os/  board_decision_os/
risk_resilience_os/  compliance_trust_os/  operating_rhythm_os/
strategic_resilience_os/  responsible_ai_os/  client_maturity_os/
```

## 3. Core OS — entities + events

Entities: Client, Project, Workspace, User, Agent, DataSource, Workflow, Output, Approval, AuditEvent, ProofEvent, ValueEvent, CapitalAsset, Decision, Risk.

Universal event: `{event_id, event_type, actor_type, actor_id, client_id, project_id, timestamp, payload}`.

## 4. Allowed flow

```
data_os → governance_os
governance_os → llm_gateway
llm_gateway → proof_os
proof_os → value_os
value_os → intelligence_os
intelligence_os → command_os
```

## 5. Forbidden flows

- `revenue_os` does not directly send external messages.
- `agent_os` does not bypass `governance_os`.
- `brain_os` does not answer without source registry.
- `client_os` does not display output without governance status.
- `proof_os` does not create case without proof score.

## 6. MVP build order — 10 steps

1. core_os events/entities.
2. data_os Source Passport + import preview.
3. governance_os runtime_decision.
4. revenue_os account_scoring + draft_pack.
5. proof_os proof_pack + proof_score.
6. value_os value_ledger.
7. capital_os capital_ledger.
8. command_os simple CEO dashboard.
9. client_os minimal workspace.
10. trust_os trust_pack.

Do not start: marketplace, academy portal, white-label, deep integrations, autonomous agents, complex RBAC.

## 7. Tests required

```
tests/test_no_source_passport_no_ai.py
tests/test_pii_external_requires_approval.py
tests/test_no_cold_whatsapp.py
tests/test_no_linkedin_automation.py
tests/test_no_scraping_engine.py
tests/test_no_guaranteed_claims.py
tests/test_output_requires_governance_status.py
tests/test_proof_pack_required.py
tests/test_agent_autonomy_mvp_limit.py
tests/test_case_study_requires_verified_value.py
```

## 8. The closing sentence

> Dealix becomes an AI Operations OS when the architecture itself forces quality: no data without a passport, no AI without the gateway, no output without governance, no external action without approval, no claim without proof, no project without a capital asset.
