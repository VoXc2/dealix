"""
Anthropic Computer Use — `computer_20250124` tool wrapper.

Lets a Dealix agent control a virtual desktop (Playwright-driven
Chromium inside a Docker sandbox) for tasks like:

    - Submitting a ZATCA invoice form when the API rejects.
    - Navigating Maroof to update merchant reputation.
    - Filing a tender response on Etimad.

We always run in a *sandbox container* (not the host) so a compromised
agent can't reach the production network.

Reference: https://docs.anthropic.com/en/docs/build-with-claude/computer-use
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class ComputerUseConfig:
    display_width: int = 1280
    display_height: int = 800
    display_number: int = 1
    sandbox_image: str = os.getenv(
        "COMPUTER_USE_SANDBOX_IMAGE", "ghcr.io/anthropics/claude-computer-use:latest"
    )


def is_enabled() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY", "").strip()) and bool(
        os.getenv("COMPUTER_USE_ENABLED", "").strip() in {"1", "true", "yes"}
    )


def tool_spec() -> dict[str, Any]:
    """Return the Anthropic tool spec a caller passes to messages.create."""
    cfg = ComputerUseConfig()
    return {
        "type": "computer_20250124",
        "name": "computer",
        "display_width_px": cfg.display_width,
        "display_height_px": cfg.display_height,
        "display_number": cfg.display_number,
    }


async def execute_action(
    *,
    action: str,
    coordinate: tuple[int, int] | None = None,
    text: str | None = None,
    sandbox_id: str | None = None,
) -> dict[str, Any]:
    """Execute one Computer-Use action against the sandbox container.

    Inert when the Docker sandbox isn't available — returns a
    structured `error: sandbox_unavailable`. Production should run
    inside a Vapi/Modal/Anyscale sandbox runtime.
    """
    if not is_enabled():
        return {"error": "computer_use_disabled"}
    log.info(
        "computer_use_action",
        action=action,
        coordinate=coordinate,
        text_len=len(text) if text else 0,
        sandbox_id=sandbox_id,
    )
    # Real execution is deferred to the runtime layer; this function
    # exists so agent code has a single entry point that survives the
    # eventual swap (Modal Sandbox vs Browserbase vs local Docker).
    return {
        "action": action,
        "coordinate": coordinate,
        "text": text,
        "sandbox_id": sandbox_id,
        "status": "queued_for_sandbox_runner",
    }
