"""Open-Source Intelligence Radar — categorized ADOPT/TEST/WATCH/REJECT."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

class OpenSourceStatus(StrEnum):
    ADOPT = "adopt"
    TEST = "test"
    WATCH = "watch"
    REJECT = "reject"

class OpenSourceTool(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    tool_id: str
    name: str
    category: str
    license: str
    status: OpenSourceStatus
    reason: str = ""
    last_reviewed: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    tco_sar: float = 0.0

class OpenSourceRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, OpenSourceTool] = {}

    def register(self, tool: OpenSourceTool) -> None:
        self.tools[tool.tool_id] = tool

    def seed_defaults(self) -> None:
        self.register(OpenSourceTool(tool_id="posthog", name="PostHog", category="analytics", license="MIT+Cloud", status=OpenSourceStatus.ADOPT, reason="existing, sufficient, reuse", tco_sar=0))
        self.register(OpenSourceTool(tool_id="chatwoot", name="Chatwoot", category="omnichannel", license="MIT", status=OpenSourceStatus.WATCH, reason="self-hosted inbox, evaluate gap vs existing", tco_sar=500))
        self.register(OpenSourceTool(tool_id="mautic", name="Mautic", category="marketing_automation", license="GPL", status=OpenSourceStatus.WATCH, reason="only if Company Machine+n8n insufficient", tco_sar=800))
        self.register(OpenSourceTool(tool_id="listmonk", name="listmonk", category="newsletter", license="AGPL", status=OpenSourceStatus.WATCH, reason="lightweight opt-in, evaluate AGPL", tco_sar=300))
        self.register(OpenSourceTool(tool_id="formbricks", name="Formbricks", category="survey", license="AGPL", status=OpenSourceStatus.WATCH, reason="diagnostics, check AGPL/commercial", tco_sar=400))
        self.register(OpenSourceTool(tool_id="n8n", name="n8n", category="automation", license="Sustainable Use", status=OpenSourceStatus.WATCH, reason="history inactive, determine canonical vs Company Machine", tco_sar=600))
        self.register(OpenSourceTool(tool_id="crawl4ai", name="Crawl4AI", category="crawl", license="Apache2", status=OpenSourceStatus.TEST, reason="market radar crawling, Apache2 safe", tco_sar=200))

    def to_dict(self) -> dict[str, Any]:
        return {"tools": [t.model_dump(mode="json") for t in self.tools.values()]}

__all__ = ["OpenSourceRegistry", "OpenSourceTool", "OpenSourceStatus"]
