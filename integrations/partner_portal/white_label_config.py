"""
White Label Configuration — manages white-label instances for partners.
تكوين العلامة البيضاء — يدير حالات العلامة البيضاء للشركاء.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class Theme:
    primary_color: str = "#1a1a2e"
    secondary_color: str = "#e94560"
    accent_color: str = "#0f3460"
    font_family_ar: str = "Cairo, sans-serif"
    font_family_en: str = "Inter, sans-serif"
    logo_url: str = ""
    favicon_url: str = ""
    custom_css: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "accent_color": self.accent_color,
            "font_family_ar": self.font_family_ar,
            "font_family_en": self.font_family_en,
            "logo_url": self.logo_url,
            "favicon_url": self.favicon_url,
        }


@dataclass
class WLConfig:
    partner_id: str
    subdomain: str
    company_name_ar: str
    company_name_en: str
    theme: Theme | None = None
    custom_domain: str = ""
    locale: str = "ar"
    features: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "partner_id": self.partner_id,
            "subdomain": self.subdomain,
            "company_name_ar": self.company_name_ar,
            "company_name_en": self.company_name_en,
            "theme": self.theme.to_dict() if self.theme else None,
            "custom_domain": self.custom_domain,
            "locale": self.locale,
            "features": self.features,
        }


@dataclass
class WLInstance:
    id: str
    partner_id: str
    subdomain: str
    company_name_ar: str
    company_name_en: str
    custom_domain: str = ""
    theme: Theme = field(default_factory=Theme)
    status: str = "active"
    locale: str = "ar"
    features: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "partner_id": self.partner_id,
            "subdomain": self.subdomain,
            "company_name_ar": self.company_name_ar,
            "company_name_en": self.company_name_en,
            "custom_domain": self.custom_domain,
            "theme": self.theme.to_dict(),
            "status": self.status,
            "locale": self.locale,
            "features": self.features,
            "created_at": self.created_at.isoformat(),
        }


class WhiteLabelConfig:
    def __init__(self):
        self._instances: dict[str, WLInstance] = {}
        self.log = logger.bind(component="white_label_config")

    async def create(self, partner_id: str, config: WLConfig) -> WLInstance:
        instance = WLInstance(
            id=generate_id("wl"),
            partner_id=partner_id,
            subdomain=config.subdomain,
            company_name_ar=config.company_name_ar,
            company_name_en=config.company_name_en,
            custom_domain=config.custom_domain,
            theme=config.theme or Theme(),
            locale=config.locale,
            features=config.features,
            status="active",
        )
        self._instances[instance.id] = instance
        self.log.info(
            "white_label_created",
            id=instance.id,
            partner_id=partner_id,
            subdomain=config.subdomain,
        )
        return instance

    async def get_domain(self, partner_id: str) -> str:
        for instance in self._instances.values():
            if instance.partner_id == partner_id:
                if instance.custom_domain:
                    return f"https://{instance.custom_domain}"
                return f"https://{instance.subdomain}.dealix.ai"
        raise ValueError(f"No white-label instance found for partner {partner_id}")

    async def apply_theme(self, partner_id: str, theme: Theme) -> None:
        for instance in self._instances.values():
            if instance.partner_id == partner_id:
                instance.theme = theme
                self.log.info("theme_applied", partner_id=partner_id)
                return
        raise ValueError(f"No white-label instance found for partner {partner_id}")

    def get_instance(self, partner_id: str) -> WLInstance | None:
        for instance in self._instances.values():
            if instance.partner_id == partner_id:
                return instance
        return None

    def get_instance_by_id(self, instance_id: str) -> WLInstance | None:
        return self._instances.get(instance_id)

    def list_instances(self) -> list[WLInstance]:
        return list(self._instances.values())

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_instances": len(self._instances),
            "active": sum(1 for i in self._instances.values() if i.status == "active"),
            "with_custom_domain": sum(1 for i in self._instances.values() if i.custom_domain),
        }
