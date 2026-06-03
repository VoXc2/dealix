"""SprintLoop — 7-day Revenue Intelligence Sprint runner."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.config import HermesConfig, get_hermes_config
from dealix.hermes.memory import HermesMemory
from dealix.hermes.registry import HermesRegistry

logger = structlog.get_logger(__name__)


class SprintLoop:
    """Coordinates the 7-day Revenue Intelligence Sprint execution.

    Supports full sprint runs and resuming from a specific day.
    Sprint state is persisted in HermesMemory so sessions survive restarts.
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

    async def run_sprint(
        self,
        client_data: dict[str, Any],
        sprint_id: str,
    ) -> dict[str, Any]:
        """Run a full 7-day sprint from Day 1.

        Parameters
        ----------
        client_data:
            Client context dict including tenant_id, company_name, industry,
            records, monthly_data.
        sprint_id:
            Unique identifier for this sprint (used as memory session key).

        Returns
        -------
        dict
            Full sprint report with all 7 days of deliverables.
        """
        started_at = datetime.now(UTC).isoformat()
        await self._memory.store(sprint_id, "sprint_id", sprint_id)
        await self._memory.store(sprint_id, "started_at", started_at)
        await self._memory.store(sprint_id, "client_data", client_data)
        await self._memory.store(sprint_id, "current_day", 1)

        logger.info(
            "sprint_started",
            sprint_id=sprint_id,
            company=client_data.get("company_name", "unknown"),
        )

        try:
            agent = self._registry.get("sprint_orchestrator")
            result = await agent.run({**client_data, "sprint_id": sprint_id})
        except KeyError as exc:
            result = {"error": str(exc), "status": "failed", "sprint_id": sprint_id}
        except Exception as exc:
            logger.error("sprint_run_failed", sprint_id=sprint_id, error=str(exc))
            result = {"error": str(exc), "status": "failed", "sprint_id": sprint_id}

        await self._memory.store(sprint_id, "current_day", 7)
        await self._memory.store(sprint_id, "completed_at", datetime.now(UTC).isoformat())
        await self._memory.store(sprint_id, "final_result", result)

        logger.info("sprint_complete", sprint_id=sprint_id)
        return {
            "sprint_id": sprint_id,
            "started_at": started_at,
            "completed_at": datetime.now(UTC).isoformat(),
            "status": result.get("status", "complete"),
            "sprint_report": result.get("sprint_report", ""),
            "usage": result.get("usage", {}),
        }

    async def resume_sprint(
        self,
        sprint_id: str,
        day: int,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Resume a sprint from a specific day.

        Parameters
        ----------
        sprint_id:
            Sprint identifier to resume.
        day:
            Day number to resume from (1-7).
        context:
            Additional context to merge with stored sprint data.

        Returns
        -------
        dict
            Resumed sprint result from the specified day.
        """
        if not 1 <= day <= 7:
            return {"error": f"invalid_day: {day}. Must be 1-7.", "sprint_id": sprint_id}

        stored_client = await self._memory.get(sprint_id, "client_data", {})
        merged_input = {**stored_client, **context, "sprint_id": sprint_id, "resume_from_day": day}

        logger.info("sprint_resumed", sprint_id=sprint_id, from_day=day)

        try:
            agent = self._registry.get("sprint_orchestrator")
            result = await agent.run(merged_input)
        except KeyError as exc:
            result = {"error": str(exc), "status": "failed"}
        except Exception as exc:
            logger.error("sprint_resume_failed", sprint_id=sprint_id, error=str(exc))
            result = {"error": str(exc), "status": "failed"}

        await self._memory.store(sprint_id, "resumed_at", datetime.now(UTC).isoformat())
        await self._memory.store(sprint_id, "resume_day", day)

        return {
            "sprint_id": sprint_id,
            "resumed_from_day": day,
            "completed_at": datetime.now(UTC).isoformat(),
            "status": result.get("status", "complete"),
            "sprint_report": result.get("sprint_report", ""),
        }


__all__ = ["SprintLoop"]
