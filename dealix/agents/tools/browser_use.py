"""
Browser-Use — Playwright + LLM agent for autonomous web tasks.

We use the `browser-use` PyPI package when installed; otherwise we
expose a `dry_run` that prints the plan without running a browser so
the surrounding code is import-safe.

Used by the market-researcher skill to crawl a target company's
website + LinkedIn snippet for hiring signals.

Reference: https://github.com/browser-use/browser-use
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class BrowseResult:
    success: bool
    output: str
    artefacts: list[str]  # screenshot / PDF paths
    error: str | None = None


def is_enabled() -> bool:
    return bool(os.getenv("BROWSER_USE_ENABLED", "").strip() in {"1", "true", "yes"})


async def browse(
    *,
    task: str,
    start_url: str,
    headless: bool = True,
    dry_run: bool = False,
) -> BrowseResult:
    if dry_run or not is_enabled():
        log.info("browser_use_dry_run", task=task[:80], start_url=start_url)
        return BrowseResult(
            success=False,
            output=f"(dry-run) would browse {start_url} for: {task}",
            artefacts=[],
            error="dry_run" if dry_run else "browser_use_disabled",
        )
    try:
        from browser_use import Agent  # type: ignore
        from browser_use.browser import Browser  # type: ignore
    except ImportError:
        log.warning("browser_use_sdk_not_installed")
        return BrowseResult(
            success=False,
            output="",
            artefacts=[],
            error="browser_use_sdk_not_installed",
        )

    # The real SDK takes an LLM client; we expect the caller to pass it
    # via `llm` kwarg. For now we initialise with the env defaults.
    try:
        import anthropic  # type: ignore

        client = anthropic.AsyncAnthropic()
        async with Browser(headless=headless) as browser:
            agent = Agent(task=task, llm=client, browser=browser)
            result = await agent.run(max_steps=15)
        return BrowseResult(
            success=True,
            output=str(result.final_result or ""),
            artefacts=list(getattr(result, "screenshots", []) or []),
        )
    except Exception as exc:
        log.exception("browser_use_failed", task=task[:80])
        return BrowseResult(success=False, output="", artefacts=[], error=str(exc))
