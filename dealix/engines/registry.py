"""
The executable registry of Dealix's 12 engines.

This is the canonical, test-validated companion to
docs/agentic_operations/AGENTIC_ENTERPRISE_PLATFORM.md. Every engine's
`EngineSpec` lives here, and `dealix/registers/no_overclaim.yaml` mirrors
each engine's status.
"""

from __future__ import annotations

from dealix.engines.base import EngineSpec, EngineStatus


class EngineRegistry:
    """Validated registry of all engines in the platform."""

    def __init__(self, specs: list[EngineSpec]) -> None:
        self._specs: dict[str, EngineSpec] = {}
        for spec in specs:
            if spec.engine_id in self._specs:
                raise ValueError(f"Duplicate engine_id: {spec.engine_id}")
            self._specs[spec.engine_id] = spec
        numbers = sorted(s.number for s in specs)
        if numbers != list(range(1, len(specs) + 1)):
            raise ValueError(
                f"Engine numbers must be a gap-free 1..{len(specs)} sequence; got {numbers}"
            )

    def get(self, engine_id: str) -> EngineSpec:
        if engine_id not in self._specs:
            raise KeyError(f"Unknown engine: {engine_id}")
        return self._specs[engine_id]

    def all(self) -> list[EngineSpec]:
        return sorted(self._specs.values(), key=lambda s: s.number)

    def by_status(self, status: EngineStatus) -> list[EngineSpec]:
        return [s for s in self.all() if s.status == status]

    def __len__(self) -> int:
        return len(self._specs)

    def __contains__(self, engine_id: object) -> bool:
        return engine_id in self._specs


_SPECS: list[EngineSpec] = [
    EngineSpec(
        engine_id="agent_runtime",
        number=1,
        name_en="Agent Runtime Engine",
        name_ar="محرك تشغيل الوكلاء",
        responsibility="Plan / reason / execute loop, memory, retries, delegation, escalation.",
        capabilities=("plan", "reason", "execute", "memory", "retry", "delegate", "escalate"),
        status=EngineStatus.PARTIAL,
        wraps=(
            "auto_client_acquisition.secure_agent_runtime_os",
            "auto_client_acquisition.agent_os",
            "auto_client_acquisition.agentic_operations_os",
        ),
        governance_hooks=("policy.evaluate", "audit.append", "risk.snapshot"),
        roadmap_phase=1,
    ),
    EngineSpec(
        engine_id="workflow",
        number=2,
        name_en="Workflow Orchestration Engine",
        name_ar="محرك تنسيق سير العمل",
        responsibility=(
            "Event -> reasoning -> workflow selection -> tool orchestration -> "
            "approval routing -> execution -> retry -> monitoring."
        ),
        capabilities=("select_workflow", "orchestrate", "route_approval", "retry", "monitor"),
        status=EngineStatus.PARTIAL,
        wraps=("auto_client_acquisition.workflow_os_v10", "dealix.execution"),
        governance_hooks=("policy.evaluate", "approval.submit", "audit.append"),
        roadmap_phase=1,
    ),
    EngineSpec(
        engine_id="memory",
        number=3,
        name_en="Organizational Memory Engine",
        name_ar="محرك الذاكرة المؤسسية",
        responsibility=(
            "Customer / workflow / executive / policy / company / operational memory fabric."
        ),
        capabilities=(
            "customer_memory",
            "workflow_memory",
            "executive_memory",
            "policy_memory",
            "company_memory",
            "operational_memory",
        ),
        status=EngineStatus.PARTIAL,
        wraps=("dealix.intelligence", "dealix.contracts"),
        governance_hooks=("policy.evaluate", "audit.append"),
        roadmap_phase=2,
    ),
    EngineSpec(
        engine_id="governance",
        number=4,
        name_en="Governance Engine",
        name_ar="محرك الحوكمة",
        responsibility=(
            "Policy, approval, audit, explainability, compliance, and risk — "
            "every action traceable, auditable, governed, and explainable."
        ),
        capabilities=("policy", "approval", "audit", "explainability", "compliance", "risk"),
        status=EngineStatus.PRODUCTION,
        wraps=(
            "dealix.trust",
            "dealix.contracts",
            "auto_client_acquisition.compliance_os",
            "auto_client_acquisition.governance_os",
        ),
        governance_hooks=(
            "policy.evaluate",
            "approval.submit",
            "audit.append",
            "explainability.explain",
            "compliance.check",
            "risk.snapshot",
        ),
        roadmap_phase=0,
    ),
    EngineSpec(
        engine_id="executive",
        number=5,
        name_en="Executive Intelligence Engine",
        name_ar="محرك الذكاء التنفيذي",
        responsibility="Bottlenecks, revenue leaks, executive briefs, forecasts, alerts.",
        capabilities=("bottlenecks", "revenue_leaks", "briefs", "forecasts", "alerts"),
        status=EngineStatus.PARTIAL,
        wraps=("auto_client_acquisition.agentic_operations_os",),
        governance_hooks=("policy.evaluate", "audit.append"),
        roadmap_phase=2,
    ),
    EngineSpec(
        engine_id="graph",
        number=6,
        name_en="Organizational Graph Engine",
        name_ar="محرك الرسم البياني المؤسسي",
        responsibility=(
            "Relationships across people, decisions, approvals, workflows, "
            "customers, risks, and knowledge."
        ),
        capabilities=("add_node", "add_edge", "neighbors", "query"),
        status=EngineStatus.PILOT,
        wraps=(),  # net-new domain — in-memory Node/Edge store
        governance_hooks=("policy.evaluate", "audit.append"),
        roadmap_phase=3,
    ),
    EngineSpec(
        engine_id="execution",
        number=7,
        name_en="Execution Engine",
        name_ar="محرك التنفيذ",
        responsibility=(
            "Actually executes operations (CRM, proposals, approvals) — "
            "always behind governance and human approval."
        ),
        capabilities=("execute_action", "draft", "dispatch_governed"),
        status=EngineStatus.PARTIAL,
        wraps=("dealix.execution",),
        governance_hooks=("policy.evaluate", "approval.submit", "audit.append"),
        roadmap_phase=1,
    ),
    EngineSpec(
        engine_id="evaluation",
        number=8,
        name_en="Evaluation Engine",
        name_ar="محرك التقييم",
        responsibility=(
            "Hallucination, grounding, execution success, escalation correctness, "
            "policy compliance, business impact."
        ),
        capabilities=(
            "hallucination",
            "grounding",
            "execution_success",
            "escalation_correctness",
            "policy_compliance",
            "business_impact",
        ),
        status=EngineStatus.PARTIAL,
        wraps=("dealix.trust",),
        governance_hooks=("policy.evaluate", "audit.append"),
        roadmap_phase=2,
    ),
    EngineSpec(
        engine_id="observability",
        number=9,
        name_en="Observability Engine",
        name_ar="محرك المراقبة",
        responsibility=(
            "Traces, retries, failures, bottlenecks, policy violations, "
            "latency, token usage, agent health."
        ),
        capabilities=("traces", "failures", "policy_violations", "latency", "token_usage"),
        status=EngineStatus.PARTIAL,
        wraps=("dealix.trust", "dealix.contracts"),
        governance_hooks=("audit.append", "risk.snapshot"),
        roadmap_phase=2,
    ),
    EngineSpec(
        engine_id="transformation",
        number=10,
        name_en="Transformation Engine",
        name_ar="محرك التحول",
        responsibility=(
            "Maturity models, transformation frameworks, workflow redesign, "
            "governance roadmaps, AI operating models."
        ),
        capabilities=("maturity_model", "framework", "workflow_redesign", "operating_model"),
        status=EngineStatus.PILOT,
        wraps=("auto_client_acquisition.governance_os",),
        governance_hooks=("policy.evaluate", "audit.append"),
        roadmap_phase=3,
    ),
    EngineSpec(
        engine_id="digital_workforce",
        number=11,
        name_en="Digital Workforce Engine",
        name_ar="محرك القوى العاملة الرقمية",
        responsibility=(
            "AI employees, supervisors, departments, performance, and governance."
        ),
        capabilities=("ai_employee", "ai_department", "performance", "supervision"),
        status=EngineStatus.PARTIAL,
        wraps=("auto_client_acquisition.agentic_operations_os",),
        governance_hooks=("policy.evaluate", "approval.submit", "audit.append", "risk.snapshot"),
        roadmap_phase=2,
    ),
    EngineSpec(
        engine_id="evolution",
        number=12,
        name_en="Continuous Evolution Engine",
        name_ar="محرك التطور المستمر",
        responsibility="Feedback loops, workflow optimization, self-improvement.",
        capabilities=("feedback_loop", "optimize_workflow", "self_improve"),
        status=EngineStatus.PILOT,
        wraps=("auto_client_acquisition.friction_log",),
        governance_hooks=("policy.evaluate", "audit.append"),
        roadmap_phase=3,
    ),
]

ENGINE_REGISTRY = EngineRegistry(_SPECS)
