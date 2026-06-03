"""RevenueLoop — periodic revenue intelligence cycle runner."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.config import HermesConfig, get_hermes_config
from dealix.hermes.orchestrator import HermesOrchestrator

logger = structlog.get_logger(__name__)


class RevenueLoop:
    """Runs the revenue intelligence pipeline on a periodic schedule.

    Usage::

        loop = RevenueLoop(orchestrator, config)
        await loop.run_once("tenant_123")
        # or:
        await loop.run_forever("tenant_123")
    """

    def __init__(
        self,
        orchestrator: HermesOrchestrator,
        config: HermesConfig | None = None,
    ) -> None:
        self._orchestrator = orchestrator
        self._config = config or get_hermes_config()
        self._stop_flag = False

    async def run_once(self, tenant_id: str) -> dict[str, Any]:
        """Execute one complete revenue intelligence cycle.

        Parameters
        ----------
        tenant_id:
            Tenant to run the cycle for.

        Returns
        -------
        dict
            Pipeline result with cycle metadata.
        """
        started_at = datetime.now(UTC).isoformat()
        logger.info("revenue_loop_cycle_start", tenant_id=tenant_id, started_at=started_at)

        input_data = {
            "tenant_id": tenant_id,
            "period": datetime.now(UTC).strftime("%B %Y"),
            "cycle_type": "automated_weekly",
        }

        result = await self._orchestrator.run_pipeline(
            pipeline_name="managed_ops_weekly",
            input_data=input_data,
        )

        result["cycle_started_at"] = started_at
        result["cycle_tenant"] = tenant_id
        logger.info(
            "revenue_loop_cycle_complete",
            tenant_id=tenant_id,
            steps=result.get("steps_completed", 0),
        )
        return result

    async def run_forever(self, tenant_id: str) -> None:
        """Run the revenue intelligence cycle indefinitely.

        Sleeps for ``config.hermes_loop_interval_seconds`` between cycles.
        Call :meth:`stop` to exit the loop gracefully.

        Parameters
        ----------
        tenant_id:
            Tenant to run cycles for.
        """
        self._stop_flag = False
        logger.info(
            "revenue_loop_started",
            tenant_id=tenant_id,
            interval_seconds=self._config.hermes_loop_interval_seconds,
        )
        while not self._stop_flag:
            try:
                await self.run_once(tenant_id)
            except Exception as exc:
                logger.error("revenue_loop_cycle_error", tenant_id=tenant_id, error=str(exc))
            await asyncio.sleep(self._config.hermes_loop_interval_seconds)

        logger.info("revenue_loop_stopped", tenant_id=tenant_id)

    async def stop(self) -> None:
        """Signal the loop to stop after the current cycle completes."""
        self._stop_flag = True
        logger.info("revenue_loop_stop_requested")


__all__ = ["RevenueLoop"]
