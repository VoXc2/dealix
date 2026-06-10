"""HermesOrchestrator — supervisor-pattern multi-agent coordinator."""

from __future__ import annotations

import asyncio
import json
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.config import HermesConfig, get_hermes_config
from dealix.hermes.engine import HermesEngine, build_tool_schema
from dealix.hermes.memory import HermesMemory
from dealix.hermes.registry import HermesRegistry

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Pipeline definitions
# ---------------------------------------------------------------------------

def _identity(output: dict[str, Any], _previous: dict[str, Any]) -> dict[str, Any]:
    """Pass the previous output through unchanged."""
    return output


def _make_pipeline(steps: list[tuple[str, Callable[..., dict[str, Any]]]]) -> list[tuple[str, Any]]:
    return steps


_PIPELINES: dict[str, list[tuple[str, Any]]] = {
    "revenue_sprint": [
        ("diagnostic_agent", lambda inp, _prev: inp),
        ("data_architect", lambda inp, prev: {**inp, "diagnostic": prev}),
        ("revenue_intelligence", lambda inp, prev: {**inp, "data_pack": prev}),
        ("sprint_orchestrator", lambda inp, prev: {**inp, "revenue_analysis": prev}),
    ],
    "lead_qualification": [
        ("lead_intelligence", lambda inp, _prev: inp),
        ("sales_intelligence", lambda inp, prev: {**inp, "lead_results": prev}),
    ],
    "free_diagnostic": [
        ("diagnostic_agent", lambda inp, _prev: inp),
    ],
    "managed_ops_weekly": [
        ("managed_ops", lambda inp, _prev: inp),
        ("revenue_intelligence", lambda inp, prev: {**inp, "ops_report": prev}),
    ],
    "data_pack_build": [
        ("data_architect", lambda inp, _prev: inp),
        ("governance", lambda inp, prev: {**inp, "data_pack": prev}),
    ],
}

_SUPERVISOR_SYSTEM = """\
You are the Dealix Supervisor Agent. You orchestrate a team of specialist agents to achieve goals.

Available agents (call by exact name):
{agent_list}

Given a goal, decide which agent to call next and what input to pass.
When the goal is fully achieved, output: {{"done": true, "summary": "..."}}
Otherwise output: {{"next_agent": "<name>", "input": {{...}}, "reason": "..."}}

Be decisive. Each step should meaningfully advance toward the goal.
"""


class HermesOrchestrator:
    """Supervisor-pattern multi-agent coordinator.

    Supports predefined pipelines, parallel execution, and a goal-driven
    supervisor loop where the LLM decides which agent to invoke next.
    """

    def __init__(
        self,
        registry: HermesRegistry | None = None,
        memory: HermesMemory | None = None,
        config: HermesConfig | None = None,
    ) -> None:
        self._registry = registry or HermesRegistry.instance()
        self._memory = memory or HermesMemory()
        self._config = config or get_hermes_config()
        self._engine = HermesEngine(config=self._config)

    # ------------------------------------------------------------------
    # Predefined pipelines
    # ------------------------------------------------------------------

    async def run_pipeline(
        self,
        pipeline_name: str,
        input_data: dict[str, Any],
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Execute a named pipeline as a sequence of agent steps.

        Parameters
        ----------
        pipeline_name:
            One of: revenue_sprint, lead_qualification, free_diagnostic,
            managed_ops_weekly, data_pack_build.
        input_data:
            Input dict passed to the first agent; subsequent agents receive
            merged data including prior outputs.
        session_id:
            Optional session identifier for memory persistence.

        Returns
        -------
        dict
            Final output from the last pipeline step plus full step history.
        """
        if pipeline_name not in _PIPELINES:
            return {
                "error": f"unknown_pipeline: {pipeline_name!r}",
                "available_pipelines": list(_PIPELINES.keys()),
            }

        sid = session_id or str(uuid.uuid4())
        steps = _PIPELINES[pipeline_name]
        step_history: list[dict[str, Any]] = []
        previous_output: dict[str, Any] = {}
        current_input = input_data

        logger.info("pipeline_started", pipeline=pipeline_name, session_id=sid, steps=len(steps))

        for i, (agent_name, input_mapper) in enumerate(steps):
            step_input = input_mapper(current_input, previous_output)
            await self._memory.store(sid, f"step_{i}_input", step_input)

            try:
                agent = self._registry.get(agent_name)
                step_output = await agent.run(step_input)
            except KeyError as exc:
                logger.warning("pipeline_agent_missing", agent=agent_name, error=str(exc))
                step_output = {"error": str(exc), "agent": agent_name}
            except Exception as exc:
                logger.error("pipeline_step_failed", agent=agent_name, error=str(exc))
                step_output = {"error": str(exc), "agent": agent_name}

            await self._memory.store(sid, f"step_{i}_output", step_output)
            step_history.append(
                {
                    "step": i,
                    "agent": agent_name,
                    "status": step_output.get("status", "unknown"),
                }
            )
            previous_output = step_output
            current_input = {**input_data, **step_output}

        logger.info("pipeline_complete", pipeline=pipeline_name, session_id=sid)
        return {
            "pipeline": pipeline_name,
            "session_id": sid,
            "steps_completed": len(step_history),
            "step_history": step_history,
            "final_output": previous_output,
            "completed_at": datetime.now(UTC).isoformat(),
        }

    # ------------------------------------------------------------------
    # Parallel execution
    # ------------------------------------------------------------------

    async def run_parallel_agents(
        self,
        agent_names: list[str],
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Run multiple agents concurrently and merge their results.

        Parameters
        ----------
        agent_names:
            List of agent names to run in parallel.
        input_data:
            Input dict passed to all agents.

        Returns
        -------
        dict
            Merged results keyed by agent name, plus a summary.
        """
        async def _run_one(name: str) -> tuple[str, dict[str, Any]]:
            try:
                agent = self._registry.get(name)
                result = await agent.run(input_data)
                return name, result
            except KeyError as exc:
                return name, {"error": str(exc), "agent": name}
            except Exception as exc:
                logger.error("parallel_agent_failed", agent=name, error=str(exc))
                return name, {"error": str(exc), "agent": name}

        logger.info("parallel_run_started", agents=agent_names)
        results = await asyncio.gather(*[_run_one(n) for n in agent_names])

        merged: dict[str, Any] = {}
        errors: list[str] = []
        for name, result in results:
            merged[name] = result
            if "error" in result:
                errors.append(name)

        logger.info("parallel_run_complete", agents=len(results), errors=len(errors))
        return {
            "results": merged,
            "agents_run": agent_names,
            "errors": errors,
            "completed_at": datetime.now(UTC).isoformat(),
        }

    # ------------------------------------------------------------------
    # Supervisor loop
    # ------------------------------------------------------------------

    async def run_supervisor_loop(
        self,
        goal: str,
        available_agents: list[str],
        max_iterations: int = 10,
    ) -> dict[str, Any]:
        """Goal-driven supervisor loop — LLM decides which agent to call next.

        Parameters
        ----------
        goal:
            Natural language description of what to achieve.
        available_agents:
            Agent names the supervisor may invoke.
        max_iterations:
            Maximum number of agent calls before forcing a summary.

        Returns
        -------
        dict
            Final synthesis, steps taken, and usage metrics.
        """
        agent_list_str = "\n".join(
            f"- {name}: {self._describe_agent(name)}" for name in available_agents
        )
        system = _SUPERVISOR_SYSTEM.format(agent_list=agent_list_str)

        steps_taken: list[dict[str, Any]] = []
        context: dict[str, Any] = {"goal": goal}
        total_tokens = 0

        for iteration in range(max_iterations):
            # Ask supervisor which agent to call next
            history_str = json.dumps(steps_taken, indent=2, default=str)
            user_msg = (
                f"Goal: {goal}\n\n"
                f"Steps taken so far ({iteration}):\n{history_str}\n\n"
                f"Context: {json.dumps(context, default=str)[:2000]}\n\n"
                "What is the next step? Output JSON only."
            )

            messages = [{"role": "user", "content": user_msg}]
            final_text, _ = await self._engine.run_agent_loop(
                system=system,
                messages=messages,
                tools=[],
                max_rounds=1,
            )
            total_tokens += self._engine.last_usage.total_tokens

            # Parse supervisor decision
            try:
                decision = self._extract_json(final_text)
            except Exception:
                decision = {"done": True, "summary": final_text}

            if decision.get("done"):
                logger.info(
                    "supervisor_loop_complete",
                    iterations=iteration + 1,
                    reason="goal_achieved",
                )
                return {
                    "status": "complete",
                    "goal": goal,
                    "iterations": iteration + 1,
                    "steps_taken": steps_taken,
                    "summary": decision.get("summary", ""),
                    "context": context,
                    "total_tokens": total_tokens,
                    "completed_at": datetime.now(UTC).isoformat(),
                }

            next_agent = decision.get("next_agent", "")
            agent_input = decision.get("input", {})

            if next_agent not in available_agents:
                logger.warning("supervisor_invalid_agent", agent=next_agent)
                break

            try:
                agent = self._registry.get(next_agent)
                agent_output = await agent.run({**context, **agent_input})
            except Exception as exc:
                agent_output = {"error": str(exc), "agent": next_agent}

            step = {
                "iteration": iteration,
                "agent": next_agent,
                "reason": decision.get("reason", ""),
                "status": agent_output.get("status", "unknown"),
            }
            steps_taken.append(step)
            context[f"step_{iteration}_{next_agent}"] = agent_output

        logger.warning("supervisor_loop_max_iterations", max_iterations=max_iterations)
        return {
            "status": "max_iterations_reached",
            "goal": goal,
            "iterations": max_iterations,
            "steps_taken": steps_taken,
            "summary": f"Reached {max_iterations} iterations without explicit completion.",
            "total_tokens": total_tokens,
            "completed_at": datetime.now(UTC).isoformat(),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _describe_agent(self, name: str) -> str:
        try:
            agent = self._registry.get(name)
            return agent.description
        except KeyError:
            return "unknown agent"

    @staticmethod
    def _extract_json(text: str) -> dict[str, Any]:
        """Extract the first JSON object from a text string."""
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in text.")
        return json.loads(text[start:end])


__all__ = ["HermesOrchestrator"]
