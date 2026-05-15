# Agentic Enterprise Platform — منصة المؤسسة الوكيلة

> **Status / الحالة:** Phase 0 landed — Governance Engine at Production depth; 11 engines registered as governed foundations.
> **Horizon / الأفق:** 3–5 year north-star. This does **not** re-sequence the 90-day commercial activation plan.
> **Canonical source / المرجع:** this document + `dealix/engines/registry.py` (the executable registry).

---

## 1. Vision — الرؤية

Models (Claude, Gemini, GLM, …) are converging toward commodity. The durable moat is **organizational
intelligence**: workflows, memory, governance, operational data, execution, and evaluation that compound
over time.

Dealix's north-star is to become the **operating system for digital labor** — the infrastructure layer on
which a company runs a hybrid human-agent workforce. The vision is expressed as **12 engines**. This is a
3–5 year horizon, not a single release.

The prime rule is unchanged and binds every engine:

> **AI explores → Deterministic systems execute → Humans approve.**

---

## 2. North-star vs. now — النجمة القطبية مقابل الآن

**The 12-engine vision is layered on top of the existing 90-day commercial activation plan. It does not
replace or re-sequence it.** `dealix/registers/90_day_execution.yaml` and the 5 paid offers remain the
active near-term priority. The engines are the substrate the commercial work compounds into — every paid
offer delivered today feeds one or more engines.

| 90-day offer | Feeds engine(s) |
|---|---|
| Free Mini Diagnostic (0 SAR) | Evaluation, Organizational Memory |
| Revenue Proof Sprint (499 SAR) | Workflow Orchestration, Execution, Governance |
| Data-to-Revenue Pack (1,500 SAR) | Organizational Memory, Organizational Graph |
| Growth Ops Monthly (2,999 SAR) | Digital Workforce, Workflow Orchestration, Observability |
| Executive Command Center (7,500 SAR) | Executive Intelligence, Governance, Transformation |

---

## 3. The 12 engines — المحركات الاثنا عشر

| # | Engine | Responsibility | Prime-rule role |
|---|---|---|---|
| 1 | Agent Runtime | Plan / reason / execute loop, memory, retries, delegation, escalation | AI explores |
| 2 | Workflow Orchestration | Event → reasoning → workflow → tool orchestration → approval routing → execution → retry → monitoring | Deterministic executes |
| 3 | Organizational Memory | Customer / workflow / executive / policy / company / operational memory | AI explores |
| 4 | **Governance** | Policy, approval, audit, explainability, compliance, risk — every action traceable & governed | Humans approve |
| 5 | Executive Intelligence | Bottlenecks, revenue leaks, briefs, forecasts, alerts | AI explores |
| 6 | Organizational Graph | Relationships across people / decisions / approvals / workflows / customers / risk / knowledge | AI explores |
| 7 | Execution | Actually executes operations (CRM, proposals, approvals) — always governed | Deterministic executes |
| 8 | Evaluation | Hallucination, grounding, execution success, escalation correctness, policy compliance, business impact | Humans approve |
| 9 | Observability | Traces, retries, failures, bottlenecks, policy violations, latency, token usage, agent health | Deterministic executes |
| 10 | Transformation | Maturity models, transformation frameworks, workflow redesign, AI operating models | AI explores |
| 11 | Digital Workforce | AI employees / supervisors / departments / performance / governance | Deterministic executes |
| 12 | Continuous Evolution | Feedback loops, workflow optimization, self-improvement | AI explores |

---

## 4. Gap analysis — تحليل الفجوة (honest status)

Each engine is a **governed facade over existing Dealix code** — not a rewrite. Status uses the
no-overclaim vocabulary (`Planned` / `Pilot` / `Partial` / `Production`). Only the Governance Engine is
`Production` in Phase 0.

| # | Engine | Wraps (existing code) | Status |
|---|---|---|---|
| 1 | Agent Runtime | `auto_client_acquisition.secure_agent_runtime_os`, `agent_os`, `agentic_operations_os` | Partial |
| 2 | Workflow Orchestration | `auto_client_acquisition.workflow_os_v10`, `dealix.execution` (`GovernedPipeline`) | Partial |
| 3 | Organizational Memory | `dealix.intelligence`, `dealix.contracts` | Partial |
| 4 | **Governance** | `dealix.trust` (policy/approval/audit), `dealix.contracts`, `auto_client_acquisition.compliance_os`, `governance_os` | **Production** |
| 5 | Executive Intelligence | `auto_client_acquisition.agentic_operations_os.agentic_operations_board` | Partial |
| 6 | Organizational Graph | net-new (in-memory `Node`/`Edge`/`Relationship`) | Pilot |
| 7 | Execution | `dealix.execution` (`GovernedPipeline`) | Partial |
| 8 | Evaluation | `dealix.trust.tool_verification` | Partial |
| 9 | Observability | `dealix.contracts.audit_log`, `dealix.trust.audit` | Partial |
| 10 | Transformation | `auto_client_acquisition.governance_os` (policy registry) | Pilot |
| 11 | Digital Workforce | `auto_client_acquisition.agentic_operations_os` (agent identity/lifecycle/permissions) | Partial |
| 12 | Continuous Evolution | `auto_client_acquisition.friction_log` | Pilot |

The 11 non-Governance engines land as **real, registered facades**: discoverable in the registry, wired to
verify their foundation modules import, and with unbuilt capabilities raising `PlannedCapabilityError`
(loud failure — never a fake result). They are honest foundations, not throwaway stubs.

---

## 5. Engine architecture standard — معيار البنية

Every engine conforms to one shared contract (`dealix/engines/base.py`):

- **`EngineSpec`** — immutable record: `engine_id`, `number` (1–12), bilingual name, responsibility,
  `capabilities`, `status`, `wraps` (importable modules it composes), `governance_hooks`, `roadmap_phase`.
- **`governance_hooks` is required non-empty** — operationalizes the `no_unbounded_agents` non-negotiable.
  No engine may act outside the Governance Engine's reach.
- **`BaseEngine`** — every engine implements `_domain_report()`; `status_report()` additionally verifies
  every `wraps` module imports.
- **`PlannedCapabilityError`** — registered-but-unbuilt capability fails loudly (`no_silent_failures`).
- **`EngineRegistry`** (`dealix/engines/registry.py`) — the 12 specs, validated for unique IDs and a
  gap-free 1–12 numbering. Discoverable at `GET /api/v1/governance-engine/engines`.

---

## 6. Phased roadmap — خارطة الطريق

- **Phase 0 (this branch):** engine registry + `BaseEngine` contract; Governance Engine to Production
  depth (policy, approval, audit, explainability, compliance, risk) with API + tests; 11 engines
  registered as governed foundations.
- **Phase 1+:** fill each engine's `Planned` capabilities one engine at a time, prioritized by which
  90-day offer they unblock. No engine fill-in is allowed to block the commercial plan.

---

## 7. Doctrine & no-overclaim binding — الالتزام بالعقيدة

The 11 non-negotiables apply to every engine as acceptance gates:

- `no_unbounded_agents` — every `EngineSpec` declares non-empty `governance_hooks` (enforced in
  `EngineSpec.__post_init__` and by `tests/test_no_ungoverned_engine.py`).
- `no_silent_failures` — unbuilt capabilities raise `PlannedCapabilityError`, never fake a result.
- `no_unaudited_changes` — the Governance Engine appends an `AuditEntry` for every evaluation.
- `no_live_send` / `no_live_charge` — no engine touches an external send/charge path; the engine layer is
  read-only and audit-emitting.

Every engine's status is mirrored in `dealix/registers/no_overclaim.yaml`. Nothing is described as
complete beyond the Governance Engine.

---

## 8. Cross-references — مراجع

- `docs/ARCHITECTURE_LAYER_MAP.md` — canonical module map.
- `dealix/masters/trust_fabric_spec.md` — policy / approval / audit fabric (reused by Engine 4).
- `dealix/masters/execution_fabric_spec.md` — durable workflow fabric (Engine 2 target).
- `dealix/masters/constitution.md` — binding rules.
- `dealix/engines/registry.py` — the executable, test-validated registry of all 12 engines.
