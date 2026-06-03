"""LeadLoop — periodic lead batch processing runner."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any, Callable

import structlog

from dealix.hermes.config import HermesConfig, get_hermes_config
from dealix.hermes.registry import HermesRegistry

logger = structlog.get_logger(__name__)


class LeadLoop:
    """Processes batches of leads through the LeadIntelligenceAgent periodically.

    Usage::

        loop = LeadLoop(registry, config)
        result = await loop.run_once(leads=[...])
        await loop.run_forever(lead_source_fn=my_lead_poller)
    """

    def __init__(
        self,
        registry: HermesRegistry | None = None,
        config: HermesConfig | None = None,
    ) -> None:
        self._registry = registry or HermesRegistry.instance()
        self._config = config or get_hermes_config()
        self._stop_flag = False

    async def run_once(self, leads: list[dict[str, Any]]) -> dict[str, Any]:
        """Process a single batch of leads through LeadIntelligenceAgent.

        Parameters
        ----------
        leads:
            List of lead dicts. Each should include company, industry,
            revenue_sar, and employees.

        Returns
        -------
        dict
            Agent output with ranked leads and tier summary.
        """
        if not leads:
            return {"status": "no_leads", "processed": 0}

        started_at = datetime.now(UTC).isoformat()
        logger.info("lead_loop_batch_start", lead_count=len(leads))

        try:
            agent = self._registry.get("lead_intelligence")
            result = await agent.run(
                {"leads": leads, "goal": "Score and prioritise all leads"}
            )
        except KeyError:
            result = {
                "error": "lead_intelligence agent not registered",
                "status": "failed",
            }
        except Exception as exc:
            logger.error("lead_loop_batch_error", error=str(exc))
            result = {"error": str(exc), "status": "failed"}

        result["batch_started_at"] = started_at
        result["batch_lead_count"] = len(leads)
        logger.info("lead_loop_batch_complete", lead_count=len(leads))
        return result

    async def run_forever(
        self,
        lead_source_fn: Callable[[], list[dict[str, Any]]],
    ) -> None:
        """Poll lead_source_fn periodically and process new leads.

        Parameters
        ----------
        lead_source_fn:
            Callable returning a list of new leads. Called every
            ``config.hermes_loop_interval_seconds`` seconds.
        """
        self._stop_flag = False
        logger.info(
            "lead_loop_started",
            interval_seconds=self._config.hermes_loop_interval_seconds,
        )
        while not self._stop_flag:
            try:
                leads = lead_source_fn()
                if leads:
                    await self.run_once(leads)
                else:
                    logger.debug("lead_loop_no_new_leads")
            except Exception as exc:
                logger.error("lead_loop_poll_error", error=str(exc))
            await asyncio.sleep(self._config.hermes_loop_interval_seconds)

        logger.info("lead_loop_stopped")

    async def stop(self) -> None:
        """Signal the loop to stop after the current iteration."""
        self._stop_flag = True
        logger.info("lead_loop_stop_requested")


__all__ = ["LeadLoop"]
