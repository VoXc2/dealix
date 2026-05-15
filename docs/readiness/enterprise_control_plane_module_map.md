# Enterprise Control Plane — Module Map

خريطة الوحدات الحقيقية لطبقة التحكم المؤسسية / Canonical map of the real
control-plane modules.

## Why this document exists

An earlier hardening draft was written against modules named
`control_plane_os`, `agent_mesh_os`, `assurance_contract_os`,
`runtime_safety_os`, `value_engine_os`, `self_evolving_os`, `sandbox_os`.
**None of those exist in this repository.** The control-plane capability is
real but lives under different names. This file is the single reference that
maps the intended concepts to the actual modules, so every follow-up sprint
targets real code instead of inventing parallel layers.

Rule: **harden the existing modules — do not create new top-level `*_os`
layers.**

## Concept → real module(s)

| Concept | Real module(s) | Role | Known gaps |
|---|---|---|---|
| Control Plane | `auto_client_acquisition/evidence_control_plane_os/`, `auto_client_acquisition/institutional_control_os/` | Evidence graph, accountability map, compliance index, gap detection; `governance_runtime.py`, `agent_control_plane.py`, `incident_response.py`, `audit_trail.py` | In-memory / JSONL state; no relational `control_events` / `workflow_runs` tables |
| Agent Mesh | `auto_client_acquisition/agent_os/`, `secure_agent_runtime_os/`, `agent_identity_access_os/` | Agent registry, agent cards, autonomy levels, tool permissions, identity & access, runtime states | `test_secure_agent_runtime.py` is stale (imports `RuntimeState`; module exports `AgentRuntimeState`) |
| Assurance Contracts | `auto_client_acquisition/governance_os/` (`policy_check.py`, `policy_registry.py`, `approval_matrix.py`), `compliance_trust_os/approval_engine.py` | Policy checks, approval matrix, forbidden actions, channel policy, runtime governance vocabulary (`GovernanceDecision`) | No first-class "assurance contract" object; concept is spread across policy modules |
| Runtime Safety | `auto_client_acquisition/secure_agent_runtime_os/`, `reliability_os/` | Kill switches, deployment rings, context/data/tool boundaries, prompt integrity, risk memory | — |
| Human-AI oversight / Approval Gate | `auto_client_acquisition/approval_center/` | `ApprovalStore`, `ApprovalRequest`, `FounderRuleEngine` (fail-closed founder rules) | In-memory store; `customer_id` optional, no enforced `tenant_id` |
| Value Engine | `auto_client_acquisition/value_os/`, `value_capture_os/` | Value ledger (tiered: estimated/observed/verified/client_confirmed), monthly value report | Ledger is in-memory MVP; sibling ledgers (friction, capital) are JSONL-backed |
| Self-Evolving | `auto_client_acquisition/self_growth_os/` | Proof snippet engine and growth loop | — |
| Sandbox / Canary | *No direct module.* `secure_agent_runtime_os/deployment_rings.py` is the nearest primitive | — | A sandbox/canary rollout module does not exist; flagged for a future sprint |

## Governance vocabulary

`governance_os/runtime_decision.py` exposes `GovernanceDecision` (re-exported
from `compliance_trust_os/approval_engine.py`) and two transformer functions:
`governance_decision_from_policy_check`, `governance_decision_from_passport_ai_gate`.
There is **no `decide()` function** — the earlier draft assumed one. The
disabled `api/routers/data_os.py` is the only caller that expects `decide()`.

## Verification

`scripts/verify_enterprise_control_plane.sh` is the one-command gate for this
map: it compiles the modules above, imports the API, runs ruff over the
control-plane scope, and runs the green control-plane test suites. CI enforces
it via `.github/workflows/enterprise-control-plane.yml`.
