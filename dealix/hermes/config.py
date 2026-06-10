"""Hermes system configuration via environment variables."""

from __future__ import annotations

import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class HermesConfig(BaseSettings):
    """Configuration for the Hermes agent system.

    All values can be overridden via environment variables with the HERMES_ prefix.
    The API key falls back to ANTHROPIC_API_KEY if HERMES_API_KEY is not set.
    """

    hermes_api_key: str = Field(
        default="",
        description="Anthropic API key for Hermes. Falls back to ANTHROPIC_API_KEY.",
    )
    hermes_model: str = Field(
        default="claude-opus-4-8",
        description="Primary model for complex reasoning tasks.",
    )
    hermes_fast_model: str = Field(
        default="claude-haiku-4-5-20251001",
        description="Fast, cheap model for classification and simple tasks.",
    )
    hermes_max_tokens: int = Field(default=8192, ge=256, le=65536)
    hermes_max_tool_rounds: int = Field(default=20, ge=1, le=50)
    hermes_loop_interval_seconds: int = Field(default=300, ge=10)
    hermes_cost_budget_usd: float = Field(default=5.0, ge=0.0)

    # MiniMax (secondary provider — OpenAI-compatible, high-volume daily tasks)
    minimax_api_key: str = Field(default="", description="MiniMax API key.")
    minimax_model: str = Field(default="MiniMax-Text-01", description="MiniMax model for daily batch tasks.")
    minimax_base_url: str = Field(default="https://api.minimaxi.chat/v1", description="MiniMax API base URL.")
    minimax_daily_outreach_enabled: bool = Field(default=True, description="Enable daily outreach loop.")
    minimax_outreach_max_per_day: int = Field(default=20, ge=1, le=100, description="Max outreach drafts per day.")

    model_config = {"env_prefix": "", "case_sensitive": False, "extra": "ignore"}

    def effective_api_key(self) -> str:
        """Return HERMES_API_KEY if set, otherwise fall back to ANTHROPIC_API_KEY."""
        if self.hermes_api_key:
            return self.hermes_api_key
        return os.environ.get("ANTHROPIC_API_KEY", "")

    def effective_minimax_key(self) -> str:
        """Return MINIMAX_API_KEY from config or env."""
        if self.minimax_api_key:
            return self.minimax_api_key
        return os.environ.get("MINIMAX_API_KEY", "")


@lru_cache(maxsize=1)
def get_hermes_config() -> HermesConfig:
    """Return the singleton HermesConfig instance."""
    return HermesConfig()


__all__ = ["HermesConfig", "get_hermes_config"]
