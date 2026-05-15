"""System 29 — the Enterprise Sandbox Engine.

Simulation environments, canary rollouts, staged execution and replay — so a
new workflow can be exercised before it ever touches production.

A sandbox run is structurally incapable of a live action: every step is run
through a deterministic stub executor. There is no provider import here, so
`no_live_send` / `no_live_charge` hold by construction. Live-style action
types (send / charge) are explicitly recorded as blocked.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.control_plane_os.ledger import ControlEventType, emit
from auto_client_acquisition.sandbox_os.schemas import (
    CanaryRollout,
    ReplayResult,
    SandboxEnv,
    SandboxIsolation,
    SandboxRun,
    SandboxStep,
)

_MODULE = "sandbox_os"

# Action types that would reach a live provider in production. In the sandbox
# they are stubbed and explicitly recorded as blocked — never executed.
LIVE_ACTION_TYPES: frozenset[str] = frozenset(
    {
        "send",
        "send_message",
        "send_email",
        "send_whatsapp",
        "charge",
        "live_send",
        "live_charge",
        "capture_payment",
    }
)


class SandboxError(ValueError):
    """Raised on an invalid sandbox operation — never swallowed."""


def _stub_execute(step: SandboxStep) -> dict[str, Any]:
    """Deterministic stub executor. Never calls a real provider."""
    is_live = step.action_type in LIVE_ACTION_TYPES
    return {
        "step_id": step.step_id,
        "action_type": step.action_type,
        "simulated": True,
        "live_blocked": is_live,
        "outcome": "stub_ok",
        "input_keys": sorted(step.inputs.keys()),
    }


class SandboxEngine:
    """Creates sandboxes and runs simulations / canaries / replays."""

    def __init__(self) -> None:
        self._sandboxes: dict[str, SandboxEnv] = {}
        self._runs: dict[str, SandboxRun] = {}
        self._canaries: dict[str, CanaryRollout] = {}

    def create_sandbox(
        self, *, name: str, isolation: SandboxIsolation | str = SandboxIsolation.FULL
    ) -> SandboxEnv:
        sandbox = SandboxEnv(name=name, isolation=SandboxIsolation(isolation))
        self._sandboxes[sandbox.sandbox_id] = sandbox
        return sandbox

    def get_sandbox(self, sandbox_id: str) -> SandboxEnv | None:
        return self._sandboxes.get(sandbox_id)

    def simulate(
        self,
        *,
        workflow_id: str,
        steps: list[SandboxStep],
        sandbox_id: str | None = None,
    ) -> SandboxRun:
        """Simulate a workflow. Every step is stubbed — production is untouched."""
        if sandbox_id is None:
            sandbox = self.create_sandbox(name=f"auto-{workflow_id}")
            sandbox_id = sandbox.sandbox_id
        elif sandbox_id not in self._sandboxes:
            raise SandboxError(f"unknown sandbox: {sandbox_id}")

        results = [_stub_execute(step) for step in steps]
        run = SandboxRun(
            sandbox_id=sandbox_id,
            workflow_id=workflow_id,
            is_production=False,
            step_results=results,
            finished_at=datetime.now(UTC),
        )
        self._runs[run.run_id] = run
        emit(
            event_type=ControlEventType.SANDBOX_RUN,
            source_module=_MODULE,
            subject_type="workflow",
            subject_id=workflow_id,
            payload={
                "sandbox_id": sandbox_id,
                "steps": len(steps),
                "live_blocked": sum(1 for r in results if r["live_blocked"]),
            },
        )
        return run

    def get_run(self, run_id: str) -> SandboxRun | None:
        return self._runs.get(run_id)

    def canary(
        self, *, workflow_id: str, traffic_pct: float
    ) -> CanaryRollout:
        """Start a canary rollout — observation only, no production cutover."""
        rollout = CanaryRollout(
            workflow_id=workflow_id,
            traffic_pct=traffic_pct,
            health={"errors": 0, "observed": True},
        )
        self._canaries[rollout.rollout_id] = rollout
        emit(
            event_type=ControlEventType.CANARY_ROLLOUT,
            source_module=_MODULE,
            subject_type="workflow",
            subject_id=workflow_id,
            payload={"traffic_pct": traffic_pct},
        )
        return rollout

    def replay(self, source_run_id: str) -> ReplayResult:
        """Re-run a prior sandbox run and diff the step outcomes."""
        source = self._runs.get(source_run_id)
        if source is None:
            raise SandboxError(f"unknown sandbox run: {source_run_id}")
        steps = [
            SandboxStep(
                step_id=r["step_id"],
                action_type=r["action_type"],
                inputs={k: True for k in r.get("input_keys", [])},
            )
            for r in source.step_results
        ]
        replay_run = self.simulate(
            workflow_id=source.workflow_id, steps=steps, sandbox_id=source.sandbox_id
        )
        divergences: list[dict[str, Any]] = []
        for original, fresh in zip(source.step_results, replay_run.step_results):
            if original["outcome"] != fresh["outcome"]:
                divergences.append(
                    {
                        "step_id": original["step_id"],
                        "before": original["outcome"],
                        "after": fresh["outcome"],
                    }
                )
        emit(
            event_type=ControlEventType.SANDBOX_REPLAY,
            source_module=_MODULE,
            subject_type="sandbox_run",
            subject_id=source_run_id,
            payload={"divergences": len(divergences)},
        )
        return ReplayResult(
            source_run_id=source_run_id,
            replay_run_id=replay_run.run_id,
            divergences=divergences,
        )


_ENGINE: SandboxEngine | None = None


def get_sandbox_engine() -> SandboxEngine:
    """Return the process-scoped sandbox engine singleton."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SandboxEngine()
    return _ENGINE


def reset_sandbox_engine() -> None:
    """Test helper: drop the cached engine."""
    global _ENGINE
    _ENGINE = None


__all__ = [
    "LIVE_ACTION_TYPES",
    "ReplayResult",
    "SandboxEngine",
    "SandboxError",
    "get_sandbox_engine",
    "reset_sandbox_engine",
]
