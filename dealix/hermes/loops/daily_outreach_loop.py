"""DailyOutreachLoop — runs CustomerAcquisitionAgent every 24 hours.

Produces outreach drafts queued for founder approval. Never auto-sends.
"""
from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.config import HermesConfig, get_hermes_config
from dealix.hermes.registry import HermesRegistry

logger = structlog.get_logger(__name__)

_24H = 86400


class DailyOutreachLoop:
    """Runs the CustomerAcquisitionAgent daily and queues drafts for approval."""

    def __init__(
        self,
        registry: HermesRegistry | None = None,
        config: HermesConfig | None = None,
    ) -> None:
        self._registry = registry or HermesRegistry.instance()
        self._config = config or get_hermes_config()
        self._running = False

    async def run_once(self, leads: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        """Run one daily acquisition cycle. Returns summary."""
        try:
            agent = self._registry.get("customer_acquisition")
        except KeyError:
            logger.warning("daily_outreach_loop_no_agent")
            return {"status": "skipped", "reason": "customer_acquisition agent not registered"}

        input_data = {
            "leads": leads or [],
            "max_drafts": self._config.minimax_outreach_max_per_day,
            "date": datetime.now(UTC).isoformat(),
        }
        logger.info("daily_outreach_loop_start", leads=len(input_data["leads"]))
        result = await agent.run(input_data)
        logger.info("daily_outreach_loop_done", drafts=result.get("drafts_queued", 0))
        return result

    async def run_forever(self, lead_source_fn: Any | None = None) -> None:
        """Run the daily loop until stop() is called."""
        self._running = True
        logger.info("daily_outreach_loop_started", interval_hours=24)
        while self._running:
            leads: list[dict[str, Any]] = []
            if lead_source_fn is not None:
                try:
                    leads = await lead_source_fn() if asyncio.iscoroutinefunction(lead_source_fn) else lead_source_fn()
                except Exception as exc:
                    logger.warning("daily_outreach_loop_lead_source_error", error=str(exc))
            try:
                await self.run_once(leads=leads)
            except Exception as exc:
                logger.error("daily_outreach_loop_error", error=str(exc))
            await asyncio.sleep(_24H)

    def stop(self) -> None:
        """Stop the loop after the current cycle completes."""
        self._running = False
        logger.info("daily_outreach_loop_stopped")


__all__ = ["DailyOutreachLoop"]
