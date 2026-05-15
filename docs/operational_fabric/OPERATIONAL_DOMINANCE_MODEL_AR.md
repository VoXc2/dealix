# DEALIX OPERATIONAL DOMINANCE MODEL — التنفيذ المؤسسي (Systems 26–35)

هذه الوثيقة تربط الـ blueprint التشغيلي بطبقة تنفيذ فعلية داخل الكود.

## لماذا ليس `/platform/...` حرفيًا؟

في Python، إنشاء مجلد top-level باسم `platform` يسبّب تعارضًا مباشرًا مع مكتبة Python القياسية `platform` وقد يكسر الاستيراد عبر المشروع.

لذلك تم اعتماد مسار آمن:

- `auto_client_acquisition/operational_fabric_os/`

مع الحفاظ على نفس المفهوم التشغيلي لكل نظام.

## خريطة الأنظمة 26–35 إلى الملفات المنفذة

### System 26 — Organizational Control Plane

- `/platform/control_plane` → `operational_fabric_os/control_plane.py`
- `/platform/operational_routing` → داخل `control_plane.py` (`reroute_workflow`)
- `/platform/state_coordination` → داخل `control_plane.py` (checkpoints + rollback state)
- `/platform/global_orchestration` → داخل `control_plane.py` (`observe_workflow`)

### System 27 — Agent Mesh Infrastructure

- `/platform/agent_mesh` → `operational_fabric_os/agent_mesh.py`
- `/platform/agent_discovery` → داخل `agent_mesh.py` (`discover`)
- `/platform/capability_registry` → داخل `agent_mesh.py` (`AgentDescriptor.capabilities`)
- `/platform/inter_agent_protocols` → boundary/governance primitives في `AgentDescriptor`
- `/platform/agent_routing` → داخل `agent_mesh.py` (`route`)

### System 28 — Assurance Contract Engine

- `/platform/assurance_contracts` → `operational_fabric_os/assurance_contracts.py`
- `/platform/execution_contracts` → `AssuranceContract.allow_execute`
- `/platform/rollback_contracts` → `AssuranceContract.rollback_required`
- `/platform/governance_contracts` → `AssuranceContract.governance_policy`

### System 29 — Enterprise Sandbox Engine

- `/platform/sandbox` → `operational_fabric_os/sandbox_engine.py`
- `/platform/simulation` → `SandboxExecutionPlan.simulation_passed`
- `/platform/canary_rollouts` → `promote_from_canary`
- `/platform/replay_engine` → `SandboxExecutionPlan.replay_ready`

### System 30 — Operational Memory Graph

- `/platform/org_graph` → `operational_fabric_os/operational_memory_graph.py`
- `/platform/dependency_graph` → typed edges (`GraphEdge.relation`)
- `/platform/relationship_engine` → `OperationalMemoryGraph.related`
- `/platform/context_graph` → `OperationalMemoryGraph.incident_context`

### System 31 — Enterprise Safety Engine

- `/platform/runtime_safety` → `operational_fabric_os/runtime_safety.py`
- `/platform/circuit_breakers` → `RuntimeSafetyState.circuit_open`
- `/platform/kill_switches` → `activate_kill_switch`
- `/platform/execution_limits` → `RuntimeSafetyPolicy.execution_limit`

### System 32 — Organizational Simulation Engine

- `/platform/org_simulation` → `operational_fabric_os/org_simulation.py`
- `/platform/workflow_simulation` → `run_release_simulation(...).checks["workflow_simulation"]`
- `/platform/failure_simulation` → `run_release_simulation(...).checks["failure_simulation"]`
- `/platform/load_simulation` → `run_release_simulation(...).checks["load_simulation"]`

### System 33 — Human-AI Operating Model

- `/platform/human_ai_operating_model` → `operational_fabric_os/human_ai_model.py`
- `/platform/escalation` → `OversightDecision.requires_approval`
- `/platform/delegation` → `evaluate_human_ai_request`
- `/platform/approval_center` → `OversightDecision.mode == "human_supervised"`

### System 34 — Business Value Engine

- `/platform/value_engine` → `operational_fabric_os/business_value_engine.py`
- `/platform/roi_tracking` → `ValueSnapshot.roi`
- `/platform/impact_analysis` → `ValueSnapshot.revenue_impact` + `csat_delta`
- `/platform/efficiency_metrics` → `ValueSnapshot.efficiency_gain_pct` + `execution_speed_gain_pct`

### System 35 — Self-Evolving Enterprise Fabric

- `/platform/self_evolving_fabric` → `operational_fabric_os/self_evolving_fabric.py`
- `/platform/meta_learning` → `recommend_evolution`
- `/platform/meta_orchestration` → evolution gate reasons
- `/platform/continuous_optimization` → `continuous_optimization_ready`
