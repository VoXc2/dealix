"""Pydantic v2 schemas for the per-customer CompanyBrain v6."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

FORBIDDEN_CHANNELS: tuple[str, ...] = (
    "cold_whatsapp",
    "linkedin_automation",
    "scrape_web",
)


class BuildRequest(BaseModel):
    """Inbound request — describes a SPECIFIC CUSTOMER, not Dealix."""

    model_config = ConfigDict(extra="forbid")

    company_handle: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    region: str = "ksa"
    current_channels: list[str] = Field(default_factory=list)
    allowed_channels: list[str] = Field(default_factory=list)
    blocked_channels: list[str] = Field(default_factory=list)
    tone_preference: str = "professional"
    language_preference: str = "ar"
    pain_points: list[str] = Field(default_factory=list)
    growth_goal: str = ""


class CompanyBrainV6(BaseModel):
    """Per-customer brain snapshot — composed from a BuildRequest."""

    model_config = ConfigDict(extra="forbid")

    company_handle: str
    sector: str
    region: str
    offer: str
    icp: str
    current_channels: list[str] = Field(default_factory=list)
    allowed_channels: list[str] = Field(default_factory=list)
    blocked_channels: list[str] = Field(default_factory=list)
    tone_preference: str = "professional"
    language_preference: str = "ar"
    pain_points: list[str] = Field(default_factory=list)
    growth_goal: str = ""
    service_recommendation: str = "growth_starter"
    risk_profile: dict[str, Any] = Field(default_factory=dict)
    next_best_action: str = ""
    evidence_ids: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

    def as_markdown(self) -> str:
        """Bilingual markdown summary — safe phrasing only.

        Customer-facing render intentionally omits the raw blocked-channel
        token list (it can contain technical names like ``cold_whatsapp``);
        instead we surface a count + the policy statement.
        """
        allowed_render = ", ".join(self.allowed_channels) or "—"
        n_blocked = len(self.blocked_channels)
        lines = [
            f"# CompanyBrain — {self.company_handle}",
            "",
            f"- **Sector / القطاع:** {self.sector}",
            f"- **Region / المنطقة:** {self.region}",
            f"- **Offer / العرض:** {self.offer}",
            f"- **ICP / العميل المستهدف:** {self.icp}",
            f"- **Tone / النبرة:** {self.tone_preference}",
            f"- **Language / اللغة:** {self.language_preference}",
            "",
            "## Channels / القنوات",
            f"- allowed / المسموح: {allowed_render}",
            f"- blocked count / عدد المحظور: {n_blocked}",
            "",
            "## Recommendation / التوصية",
            f"- service: `{self.service_recommendation}`",
            f"- next action: {self.next_best_action}",
            "",
            "_All outbound steps are gated by founder approval._",
            "_جميع الخطوات الخارجيّة تتطلّب موافقة المؤسس._",
        ]
        return "\n".join(lines)
