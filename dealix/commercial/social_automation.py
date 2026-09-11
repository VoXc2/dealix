"""Social Automation — all platforms, fully automated, within reasonable limits, market rise."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

class SocialPlatform(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    platform: str
    handle: str = "@dealix_sa"
    automated: bool = True
    content_type: str = "proof-derived"
    frequency: str = "daily"
    reasonable_limits: bool = True  # no spam, no fake, within reasonable limits
    followers_growth: str = "organic via proof, not purchased"

ALL_PLATFORMS = [
    SocialPlatform(platform="linkedin", handle="@dealix_sa", content_type="proof-derived founder native"),
    SocialPlatform(platform="x", handle="@dealix_sa", content_type="sector intelligence"),
    SocialPlatform(platform="instagram", handle="@dealix_sa", content_type="visual proof"),
    SocialPlatform(platform="tiktok", handle="@dealix_sa", content_type="short proof"),
    SocialPlatform(platform="youtube", handle="@dealix_sa", content_type="demo"),
    SocialPlatform(platform="facebook", handle="@dealix_sa", content_type="community"),
]

def get_all_platforms() -> list[SocialPlatform]:
    return ALL_PLATFORMS

__all__ = ["SocialPlatform", "ALL_PLATFORMS", "get_all_platforms"]
