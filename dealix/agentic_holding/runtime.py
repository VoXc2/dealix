from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Iterable, Mapping, Sequence


GROUP_ROLES = (
    "president",
    "strategy-capital",
    "coo",
    "cto",
    "ai-automation",
    "cfo-economic-truth",
    "revenue",
    "growth",
    "delivery",
    "customer-success",
    "research-intelligence",
    "product",
    "data-analytics",
    "engineering",
    "security",
    "risk",
    "governance-compliance",
    "procurement-b2g",
    "partnerships",
    "talent-workforce",
    "brand-content",
    "qa-verification",
    "proof",
    "self-improvement",
)

SECTOR_ROLES = (
    "sector-ceo",
    "sector-strategy",
    "sector-market-intelligence",
    "sector-research",
    "sector-sales",
    "sector-business-development",
    "sector-diagnostic",
    "sector-solution-architect",
    "sector-product",
    "sector-delivery",
    "sector-customer-success",
    "sector-economics",
    "sector-procurement",
    "sector-b2g",
    "sector-compliance",
    "sector-content",
    "sector-distribution",
    "sector-partnerships",
    "sector-data",
    "sector-qa",
    "sector-proof",
    "sector-learning",
)

ARM_POD_ROLES = ("lead", "scout", "operator", "verifier")


class AgentLayer(StrEnum):
    GROUP = "group"
    SECTOR = "sector"
    ARM = "arm"
    SPECIALIST = "specialist"


@dataclass(frozen=True, slots=True)
class LogicalAgent:
    agent_id: str
    parent_id: str
    layer: AgentLayer
    role: str
    authority_scope: str = "L0-L4"
    sector: str | None = None
    arm_id: str | None = None
    legacy_owner_alias: str | None = None
    capabilities: tuple[str, ...] = ()


@dataclass(slots=True)
class AgentHierarchyRegistry:
    namespace_parents: dict[str, str | None] = field(default_factory=dict)
    namespace_kinds: dict[str, str] = field(default_factory=dict)
    agents: dict[str, LogicalAgent] = field(default_factory=dict)
    sector_ids: set[str] = field(default_factory=set)
    arm_ids: set[str] = field(default_factory=set)
    unmapped_arms: set[str] = field(default_factory=set)

    def register_namespace(
        self,
        namespace: str,
        *,
        kind: str,
        parent: str | None,
    ) -> None:
        existing_parent = self.namespace_parents.get(namespace)
        if namespace in self.namespace_parents and existing_parent != parent:
            raise ValueError(f"namespace parent drift: {namespace}")
        if parent is not None and parent not in self.namespace_parents:
            raise ValueError(f"orphan namespace parent: {parent}")
        self.namespace_parents[namespace] = parent
        self.namespace_kinds[namespace] = kind

    def register_agent(self, agent: LogicalAgent) -> None:
        if agent.parent_id not in self.namespace_parents:
            raise ValueError(f"orphan agent parent: {agent.parent_id}")
        if agent.agent_id in self.agents:
            raise ValueError(f"duplicate agent: {agent.agent_id}")
        self.agents[agent.agent_id] = agent

    def validate(self) -> list[str]:
        failures: list[str] = []
        for namespace, parent in self.namespace_parents.items():
            if parent is not None and parent not in self.namespace_parents:
                failures.append(f"orphan_namespace:{namespace}->{parent}")
        for agent in self.agents.values():
            if agent.parent_id not in self.namespace_parents:
                failures.append(f"orphan_agent:{agent.agent_id}->{agent.parent_id}")
        for arm_id in sorted(self.unmapped_arms):
            failures.append(f"unmapped_arm:{arm_id}")
        return failures

    def receipt(self) -> dict[str, Any]:
        by_layer = {layer.value: 0 for layer in AgentLayer}
        for agent in self.agents.values():
            by_layer[agent.layer.value] += 1
        arm_namespaces = sum(
            1 for kind in self.namespace_kinds.values() if kind == "arm_pod"
        )
        return {
            "architecture": "agentic_holding_sector_company_mesh",
            "logical_agents": len(self.agents),
            "group_roles": by_layer[AgentLayer.GROUP.value],
            "sector_agents": by_layer[AgentLayer.SECTOR.value],
            "arm_agents": by_layer[AgentLayer.ARM.value],
            "specialist_agents": by_layer[AgentLayer.SPECIALIST.value],
            "sector_companies": len(self.sector_ids),
            "distinct_arms": len(self.arm_ids),
            "arm_pods": arm_namespaces,
            "unmapped_arms": sorted(self.unmapped_arms),
            "orphan_failures": self.validate(),
        }


def _field(obj: Any, name: str, default: Any) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def build_registry(
    sector_ids: Sequence[str],
    arms: Iterable[Any],
) -> AgentHierarchyRegistry:
    sectors = tuple(dict.fromkeys(str(value) for value in sector_ids if str(value)))
    registry = AgentHierarchyRegistry()
    registry.register_namespace("dealix", kind="holding", parent=None)
    registry.register_namespace("dealix.group", kind="group", parent="dealix")

    for role in GROUP_ROLES:
        registry.register_agent(
            LogicalAgent(
                agent_id=f"dealix.group.{role}",
                parent_id="dealix.group",
                layer=AgentLayer.GROUP,
                role=role,
            )
        )

    for sector in sectors:
        sector_ns = f"dealix.{sector}"
        registry.sector_ids.add(sector)
        registry.register_namespace(sector_ns, kind="sector_company", parent="dealix")
        for role in SECTOR_ROLES:
            registry.register_agent(
                LogicalAgent(
                    agent_id=f"{sector_ns}.{role}",
                    parent_id=sector_ns,
                    layer=AgentLayer.SECTOR,
                    role=role,
                    sector=sector,
                )
            )

    sector_set = set(sectors)
    for arm in arms:
        arm_id = str(_field(arm, "arm_id", "")).strip()
        if not arm_id:
            raise ValueError("arm_id is required")
        registry.arm_ids.add(arm_id)
        raw_supported = _field(arm, "supported_sectors", []) or []
        supported = {str(value) for value in raw_supported}
        if not supported or "*" in supported:
            applicable = sector_set
        else:
            applicable = supported & sector_set
        if not applicable:
            registry.unmapped_arms.add(arm_id)
            continue
        owner_alias = str(_field(arm, "owner_agent", "")).strip() or None
        capabilities = tuple(str(value) for value in (_field(arm, "capabilities", []) or []))
        for sector in sorted(applicable):
            sector_ns = f"dealix.{sector}"
            arm_ns = f"{sector_ns}.{arm_id}"
            registry.register_namespace(arm_ns, kind="arm_pod", parent=sector_ns)
            for role in ARM_POD_ROLES:
                registry.register_agent(
                    LogicalAgent(
                        agent_id=f"{arm_ns}.{role}",
                        parent_id=arm_ns,
                        layer=AgentLayer.ARM,
                        role=role,
                        sector=sector,
                        arm_id=arm_id,
                        legacy_owner_alias=owner_alias,
                        capabilities=capabilities,
                    )
                )

    return registry


def build_current_registry() -> AgentHierarchyRegistry:
    from dealix.commercial.arm_registry import get_active_arms
    from dealix.commercial.sector_company_factory import SectorCompanyFactory

    sector_ids = [company.sector.value for company in SectorCompanyFactory().build_all()]
    return build_registry(sector_ids, get_active_arms())


@dataclass(frozen=True, slots=True)
class ResourceSnapshot:
    cpu_load: float
    available_ram_mb: int
    swap_pressure: float
    disk_io_pressure: float
    provider_quota_fraction: float
    model_quota_fraction: float
    worktree_slots: int
    incident_state: str = "normal"
    cpu_count: int | None = None

    def __post_init__(self) -> None:
        for name in (
            "cpu_load",
            "swap_pressure",
            "disk_io_pressure",
            "provider_quota_fraction",
            "model_quota_fraction",
        ):
            value = float(getattr(self, name))
            if value < 0 or value > 1:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.available_ram_mb < 0 or self.worktree_slots < 0:
            raise ValueError("resource counts cannot be negative")
        if self.cpu_count is not None and self.cpu_count < 1:
            raise ValueError("cpu_count must be at least 1 when provided")


@dataclass(frozen=True, slots=True)
class WorkItem:
    work_id: str
    agent_id: str
    expected_economic_value: float
    risk: float
    cost_pressure: float = 0.0
    repo_writer: bool = False
    requires_paid_model: bool = False
    material_external_effect: bool = False
    requires_model: bool = False

    def __post_init__(self) -> None:
        for name in ("expected_economic_value", "risk", "cost_pressure"):
            value = float(getattr(self, name))
            if value < 0 or value > 100:
                raise ValueError(f"{name} must be between 0 and 100")


@dataclass(frozen=True, slots=True)
class RuntimeBudget:
    worker_slots: int
    writer_slots: int
    paid_model_allowed: bool
    model_capacity_available: bool


@dataclass(frozen=True, slots=True)
class DispatchPlan:
    selected: tuple[WorkItem, ...]
    rejected: dict[str, str]
    budget: RuntimeBudget

    def receipt(self) -> dict[str, Any]:
        return {
            "selected": [item.work_id for item in self.selected],
            "rejected": self.rejected,
            "worker_slots": self.budget.worker_slots,
            "writer_slots": self.budget.writer_slots,
            "paid_model_allowed": self.budget.paid_model_allowed,
            "model_capacity_available": self.budget.model_capacity_available,
        }


@dataclass(frozen=True, slots=True)
class ResourceGovernor:
    max_workers: int = 12
    max_repo_writers: int = 2
    paid_spill_allowed: bool = False
    conservative_cpu_count: int = 4

    def budget(self, snapshot: ResourceSnapshot) -> RuntimeBudget:
        host_capacity = snapshot.cpu_count or self.conservative_cpu_count
        workers = max(1, min(max(1, self.max_workers), max(1, host_capacity)))
        if snapshot.incident_state.lower() == "critical":
            workers = 1
        elif snapshot.incident_state.lower() != "normal":
            workers = min(workers, 2)
        if snapshot.cpu_load >= 0.90 or snapshot.available_ram_mb < 1024 or snapshot.swap_pressure >= 0.80:
            workers = min(workers, 1)
        elif snapshot.cpu_load >= 0.75 or snapshot.available_ram_mb < 2048 or snapshot.swap_pressure >= 0.60:
            workers = min(workers, 3)
        if snapshot.disk_io_pressure >= 0.90:
            workers = min(workers, 2)
        model_capacity_available = not (
            snapshot.provider_quota_fraction <= 0.02
            and snapshot.model_quota_fraction <= 0.02
        )
        if not model_capacity_available:
            workers = min(workers, 2)
        writers = min(max(0, snapshot.worktree_slots), self.max_repo_writers, workers)
        return RuntimeBudget(
            worker_slots=workers,
            writer_slots=writers,
            paid_model_allowed=self.paid_spill_allowed,
            model_capacity_available=model_capacity_available,
        )


class AgentDispatcher:
    def __init__(self, governor: ResourceGovernor | None = None) -> None:
        self.governor = governor or ResourceGovernor()

    @staticmethod
    def _score(item: WorkItem) -> float:
        return (
            2.0 * item.expected_economic_value
            - 1.0 * item.risk
            - 0.75 * item.cost_pressure
        )

    def dispatch(
        self,
        items: Sequence[WorkItem],
        *,
        registry: AgentHierarchyRegistry,
        snapshot: ResourceSnapshot,
    ) -> DispatchPlan:
        failures = registry.validate()
        if failures:
            raise ValueError(f"registry validation failed: {failures}")
        budget = self.governor.budget(snapshot)
        rejected: dict[str, str] = {}
        eligible: list[WorkItem] = []
        for item in items:
            if item.agent_id not in registry.agents:
                rejected[item.work_id] = "unknown_agent"
            elif item.material_external_effect:
                rejected[item.work_id] = "exact_action_authority_required"
            elif item.requires_paid_model and not budget.paid_model_allowed:
                rejected[item.work_id] = "paid_spill_blocked"
            elif item.requires_model and not budget.model_capacity_available:
                rejected[item.work_id] = "model_quota_exhausted"
            else:
                eligible.append(item)
        eligible.sort(key=self._score, reverse=True)

        selected: list[WorkItem] = []
        writers = 0
        for item in eligible:
            if len(selected) >= budget.worker_slots:
                rejected[item.work_id] = "worker_capacity"
                continue
            if item.repo_writer:
                if writers >= budget.writer_slots:
                    rejected[item.work_id] = "worktree_capacity"
                    continue
                writers += 1
            selected.append(item)
        return DispatchPlan(tuple(selected), rejected, budget)
