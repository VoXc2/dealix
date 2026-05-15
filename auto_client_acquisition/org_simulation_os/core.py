"""System 32 — the Organizational Simulation Engine.

Simulates workflows, failures, approval load, scale and incidents *before*
deployment, so failure modes surface in prediction rather than in production.

Workflow and failure scenarios delegate execution to `sandbox_os` — they never
touch production. Incident scenarios use the operational memory graph
(`org_graph_os`) to predict cascading impact. This engine produces predictions
and recommendations only.
"""

from __future__ import annotations

from auto_client_acquisition.control_plane_os.ledger import ControlEventType, emit
from auto_client_acquisition.org_graph_os.core import GraphError, get_org_graph
from auto_client_acquisition.org_simulation_os.schemas import (
    ScenarioKind,
    SimulationResult,
    SimulationScenario,
)
from auto_client_acquisition.sandbox_os.core import get_sandbox_engine
from auto_client_acquisition.sandbox_os.schemas import SandboxStep

_MODULE = "org_simulation_os"


class SimulationError(ValueError):
    """Raised on an invalid simulation request — never swallowed."""


class OrgSimulator:
    """Predicts organizational outcomes by simulating scenarios."""

    def __init__(self) -> None:
        self._results: dict[str, SimulationResult] = {}

    def simulate(self, scenario: SimulationScenario) -> SimulationResult:
        """Run a scenario and return its predicted outcome."""
        dispatch = {
            ScenarioKind.WORKFLOW.value: self._simulate_workflow,
            ScenarioKind.FAILURE.value: self._simulate_failure,
            ScenarioKind.APPROVAL.value: self._simulate_approval,
            ScenarioKind.SCALE.value: self._simulate_scale,
            ScenarioKind.INCIDENT.value: self._simulate_incident,
        }
        handler = dispatch.get(str(scenario.kind))
        if handler is None:  # pragma: no cover — guarded by the enum
            raise SimulationError(f"unknown scenario kind: {scenario.kind}")
        result = handler(scenario)
        self._results[scenario.scenario_id] = result
        emit(
            event_type=ControlEventType.SIMULATION_RUN,
            source_module=_MODULE,
            subject_type="simulation",
            subject_id=scenario.scenario_id,
            payload={"kind": str(scenario.kind), "risk_score": result.risk_score},
        )
        return result

    def get_result(self, scenario_id: str) -> SimulationResult | None:
        return self._results.get(scenario_id)

    def list_scenarios(self) -> list[str]:
        return sorted(self._results.keys())

    # ── per-kind handlers ────────────────────────────────────────
    def _build_steps(self, scenario: SimulationScenario) -> list[SandboxStep]:
        raw_steps = scenario.parameters.get("steps", [])
        return [
            SandboxStep(
                step_id=str(s.get("step_id", f"s{i}")),
                action_type=str(s.get("action_type", "noop")),
                inputs=dict(s.get("inputs", {})),
            )
            for i, s in enumerate(raw_steps)
        ]

    def _simulate_workflow(self, scenario: SimulationScenario) -> SimulationResult:
        workflow_id = str(scenario.parameters.get("workflow_id", "unknown"))
        run = get_sandbox_engine().simulate(
            workflow_id=workflow_id, steps=self._build_steps(scenario)
        )
        return SimulationResult(
            scenario_id=scenario.scenario_id,
            kind=ScenarioKind.WORKFLOW,
            predicted_outcomes=run.step_results,
            bottlenecks=[],
            risk_score=0.1,
            recommendation="workflow simulated cleanly — safe to canary",
        )

    def _simulate_failure(self, scenario: SimulationScenario) -> SimulationResult:
        workflow_id = str(scenario.parameters.get("workflow_id", "unknown"))
        fail_step = str(scenario.parameters.get("fail_step", ""))
        run = get_sandbox_engine().simulate(
            workflow_id=workflow_id, steps=self._build_steps(scenario)
        )
        bottlenecks = [fail_step] if fail_step else ["unspecified_step"]
        return SimulationResult(
            scenario_id=scenario.scenario_id,
            kind=ScenarioKind.FAILURE,
            predicted_outcomes=run.step_results,
            bottlenecks=bottlenecks,
            risk_score=0.6,
            recommendation=f"add rollback + retry around step(s): {', '.join(bottlenecks)}",
        )

    def _simulate_approval(self, scenario: SimulationScenario) -> SimulationResult:
        pending = int(scenario.parameters.get("pending_count", 0))
        capacity = max(1, int(scenario.parameters.get("approver_capacity", 1)))
        backlog = max(0, pending - capacity)
        risk = min(1.0, round(backlog / (capacity * 5 or 1), 3))
        bottlenecks = ["approval_backlog"] if backlog else []
        return SimulationResult(
            scenario_id=scenario.scenario_id,
            kind=ScenarioKind.APPROVAL,
            predicted_outcomes=[{"pending": pending, "capacity": capacity, "backlog": backlog}],
            bottlenecks=bottlenecks,
            risk_score=risk,
            recommendation=(
                "add approver capacity or batch approvals"
                if backlog
                else "approval throughput is sufficient"
            ),
        )

    def _simulate_scale(self, scenario: SimulationScenario) -> SimulationResult:
        current = float(scenario.parameters.get("current_load", 0))
        target = float(scenario.parameters.get("target_load", 0))
        ratio = target / current if current > 0 else float("inf")
        overloaded = ratio > 3.0
        risk = min(1.0, round((ratio - 1.0) / 10.0, 3)) if current > 0 else 1.0
        return SimulationResult(
            scenario_id=scenario.scenario_id,
            kind=ScenarioKind.SCALE,
            predicted_outcomes=[{"current_load": current, "target_load": target, "ratio": ratio if current > 0 else None}],
            bottlenecks=["capacity"] if overloaded else [],
            risk_score=max(0.0, risk),
            recommendation=(
                "provision capacity before scaling"
                if overloaded
                else "scale target is within safe bounds"
            ),
        )

    def _simulate_incident(self, scenario: SimulationScenario) -> SimulationResult:
        incident_id = str(scenario.parameters.get("incident_id", ""))
        if not incident_id:
            raise SimulationError("incident scenario requires an 'incident_id' parameter")
        try:
            impact = get_org_graph().incident_impact(incident_id)
        except GraphError as exc:
            raise SimulationError(str(exc)) from exc
        affected = len(impact.affected) + len(impact.related_workflows)
        risk = min(1.0, round(0.2 + 0.1 * affected, 3))
        return SimulationResult(
            scenario_id=scenario.scenario_id,
            kind=ScenarioKind.INCIDENT,
            predicted_outcomes=[impact.model_dump(mode="json")],
            bottlenecks=impact.related_workflows,
            risk_score=risk,
            recommendation=(
                f"contain {len(impact.related_workflows)} workflow(s); "
                f"{len(impact.resulting_risks)} downstream risk(s) predicted"
            ),
        )


_SIMULATOR: OrgSimulator | None = None


def get_org_simulator() -> OrgSimulator:
    """Return the process-scoped organizational simulator singleton."""
    global _SIMULATOR
    if _SIMULATOR is None:
        _SIMULATOR = OrgSimulator()
    return _SIMULATOR


def reset_org_simulator() -> None:
    """Test helper: drop the cached simulator."""
    global _SIMULATOR
    _SIMULATOR = None


__all__ = [
    "OrgSimulator",
    "SimulationError",
    "get_org_simulator",
    "reset_org_simulator",
]
