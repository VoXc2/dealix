"""WatchdogLoop — continuous health monitoring for the Hermes system."""

from __future__ import annotations

import asyncio
import os
from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.config import HermesConfig, get_hermes_config
from dealix.hermes.registry import HermesRegistry

logger = structlog.get_logger(__name__)

_EXPECTED_AGENTS = [
    "lead_intelligence",
    "revenue_intelligence",
    "sprint_orchestrator",
    "diagnostic_agent",
    "data_architect",
    "managed_ops",
    "sales_intelligence",
    "market_intel",
    "company_brain",
    "governance",
]


class WatchdogLoop:
    """Monitors Hermes system health: agent registration, API key, and tool imports.

    Usage::

        watchdog = WatchdogLoop(registry, config)
        status = await watchdog.run_once()
        await watchdog.run_forever()
    """

    def __init__(
        self,
        registry: HermesRegistry | None = None,
        config: HermesConfig | None = None,
    ) -> None:
        self._registry = registry or HermesRegistry.instance()
        self._config = config or get_hermes_config()
        self._stop_flag = False

    async def run_once(self) -> dict[str, Any]:
        """Execute one health check cycle.

        Checks:
        - All 10 expected agents are registered.
        - API key is configured.
        - Tool modules are importable.

        Returns
        -------
        dict
            Health status with checks, warnings, and overall status.
        """
        checks: dict[str, Any] = {}
        warnings: list[str] = []
        errors: list[str] = []

        # Check agent registry
        registered = self._registry.list_agents()
        missing_agents = [a for a in _EXPECTED_AGENTS if a not in registered]
        checks["agent_registry"] = {
            "registered_count": len(registered),
            "expected_count": len(_EXPECTED_AGENTS),
            "missing": missing_agents,
            "ok": len(missing_agents) == 0,
        }
        if missing_agents:
            warnings.append(f"Missing agents: {missing_agents}")

        # Check API key
        api_key = self._config.effective_api_key()
        api_key_ok = bool(api_key)
        checks["api_key"] = {
            "configured": api_key_ok,
            "source": "HERMES_API_KEY" if os.environ.get("HERMES_API_KEY") else (
                "ANTHROPIC_API_KEY" if os.environ.get("ANTHROPIC_API_KEY") else "none"
            ),
        }
        if not api_key_ok:
            warnings.append("No API key configured — LLM calls will return mock data.")

        # Check tool module imports
        tool_imports: dict[str, bool] = {}
        tool_modules = [
            "dealix.hermes.tools.crm_tools",
            "dealix.hermes.tools.data_tools",
            "dealix.hermes.tools.scoring_tools",
            "dealix.hermes.tools.analysis_tools",
            "dealix.hermes.tools.saudi_tools",
        ]
        for mod in tool_modules:
            try:
                __import__(mod)
                tool_imports[mod.split(".")[-1]] = True
            except ImportError as exc:
                tool_imports[mod.split(".")[-1]] = False
                errors.append(f"Import failed: {mod}: {exc}")

        checks["tool_modules"] = {
            "results": tool_imports,
            "all_ok": all(tool_imports.values()),
        }

        # Overall health
        if errors:
            overall = "critical"
        elif warnings:
            overall = "degraded"
        else:
            overall = "healthy"

        result = {
            "status": overall,
            "checked_at": datetime.now(UTC).isoformat(),
            "checks": checks,
            "warnings": warnings,
            "errors": errors,
        }
        logger.info("watchdog_health_check", status=overall, warnings=len(warnings), errors=len(errors))
        return result

    async def run_forever(self) -> None:
        """Run health checks continuously.

        Sleeps for ``config.hermes_loop_interval_seconds`` between checks.
        Call :meth:`stop` to exit gracefully.
        """
        self._stop_flag = False
        logger.info(
            "watchdog_loop_started",
            interval_seconds=self._config.hermes_loop_interval_seconds,
        )
        while not self._stop_flag:
            try:
                status = await self.run_once()
                if status["status"] != "healthy":
                    logger.warning(
                        "watchdog_unhealthy",
                        status=status["status"],
                        warnings=status["warnings"],
                        errors=status["errors"],
                    )
            except Exception as exc:
                logger.error("watchdog_check_failed", error=str(exc))
            await asyncio.sleep(self._config.hermes_loop_interval_seconds)

        logger.info("watchdog_loop_stopped")

    async def stop(self) -> None:
        """Signal the watchdog to stop after the current check."""
        self._stop_flag = True
        logger.info("watchdog_stop_requested")


__all__ = ["WatchdogLoop"]
