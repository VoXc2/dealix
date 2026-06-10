from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class CompetitorStrength(str, Enum):
    DOMINANT = "dominant"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    EMERGING = "emerging"


class ThreatLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


@dataclass
class CompetitiveIntel:
    competitor_name: str
    strength: CompetitorStrength = CompetitorStrength.MODERATE
    market_share: float = 0.0
    key_features: list[str] = field(default_factory=list)
    advantages: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    recent_moves: list[str] = field(default_factory=list)
    pricing_tier: str = "mid"
    target_segment: str = "sme"
    last_scanned: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 0.7
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreatAssessment:
    overall_threat_level: ThreatLevel = ThreatLevel.MEDIUM
    threats: list[dict[str, Any]] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    competitive_landscape: str = ""
    assessed_at: datetime = field(default_factory=datetime.utcnow)


class CompetitiveIntelligence:
    COMPETITORS = ["salla", "zid", "salesforce", "hubspot", "local_crms"]

    def __init__(self):
        self._intel_cache: dict[str, CompetitiveIntel] = {}
        self._scan_log: list[dict[str, Any]] = []

    async def scan_competitor(self, name: str) -> CompetitiveIntel:
        name = name.lower().strip()
        if name not in self.COMPETITORS:
            raise ValueError(f"Unknown competitor '{name}'. Known: {self.COMPETITORS}")

        intel = self._build_intel(name)
        self._intel_cache[name] = intel
        self._scan_log.append({
            "competitor": name,
            "scanned_at": datetime.utcnow().isoformat(),
            "strength": intel.strength.value,
        })
        logger.info("Scanned competitor '%s' (strength: %s)", name, intel.strength.value)
        return intel

    async def generate_threat_assessment(self) -> ThreatAssessment:
        for comp in self.COMPETITORS:
            await self.scan_competitor(comp)

        threats = []
        opportunities = []
        recommendations = []

        dominant = [c for c in self._intel_cache.values() if c.strength == CompetitorStrength.DOMINANT]
        strong = [c for c in self._intel_cache.values() if c.strength == CompetitorStrength.STRONG]

        for comp in self._intel_cache.values():
            if comp.strength in (CompetitorStrength.DOMINANT, CompetitorStrength.STRONG):
                for adv in comp.advantages[:2]:
                    threats.append({
                        "competitor": comp.competitor_name,
                        "type": "advantage",
                        "detail": adv,
                        "threat_level": "high" if comp.strength == CompetitorStrength.DOMINANT else "medium",
                    })
                if comp.strength == CompetitorStrength.DOMINANT:
                    for move in comp.recent_moves[:2]:
                        threats.append({
                            "competitor": comp.competitor_name,
                            "type": "recent_move",
                            "detail": move,
                            "threat_level": "high",
                        })

        for comp in self._intel_cache.values():
            for weakness in comp.weaknesses:
                opportunities.append(
                    f"Capitalize on {comp.competitor_name}'s weakness: {weakness}"
                )
            for feature in comp.key_features:
                if "AI" in feature or "automation" in feature.lower():
                    opportunities.append(
                        f"Match or exceed {comp.competitor_name} on: {feature}"
                    )

        overall = await self._calculate_threat_level(threats)

        if dominant:
            recommendations.append("Prioritize differentiation from dominant competitors")
        if strong:
            recommendations.append("Target weaknesses of strong competitors with precision")
        recommendations.append("Accelerate AI-native differentiation vs traditional incumbents")
        recommendations.append("Focus on Saudi localization advantages over global players")
        recommendations.append("Build moat through data network effects from early customers")

        landscape = self._build_landscape_summary()

        return ThreatAssessment(
            overall_threat_level=overall,
            threats=threats,
            opportunities=opportunities,
            recommendations=recommendations,
            competitive_landscape=landscape,
        )

    async def get_intel(self, name: str) -> CompetitiveIntel | None:
        return self._intel_cache.get(name.lower().strip())

    async def get_all_intel(self) -> dict[str, CompetitiveIntel]:
        return dict(self._intel_cache)

    async def refresh_all(self) -> list[CompetitiveIntel]:
        results = []
        for comp in self.COMPETITORS:
            intel = await self.scan_competitor(comp)
            results.append(intel)
        return results

    async def compare_with(self, competitor_name: str) -> dict[str, Any]:
        intel = await self.scan_competitor(competitor_name)
        return {
            "competitor": competitor_name,
            "our_advantages": [
                "AI-native platform",
                "Saudi-first localization",
                "Fully autonomous agents",
                "End-to-end revenue OS",
                "Zero-touch onboarding",
            ],
            "their_advantages": intel.advantages,
            "opportunities": intel.weaknesses,
            "threats": intel.advantages[:3],
            "recommended_action": self._recommend_action(intel),
        }

    async def track_competitor_move(
        self,
        name: str,
        move: str,
    ) -> None:
        name = name.lower().strip()
        if name in self._intel_cache:
            self._intel_cache[name].recent_moves.append(move)
            if len(self._intel_cache[name].recent_moves) > 20:
                self._intel_cache[name].recent_moves = self._intel_cache[name].recent_moves[-20:]
        else:
            intel = await self.scan_competitor(name)
            intel.recent_moves.append(move)
        logger.info("Tracked move by %s: %s", name, move)

    async def _calculate_threat_level(
        self,
        threats: list[dict[str, Any]],
    ) -> ThreatLevel:
        high_threats = sum(1 for t in threats if t.get("threat_level") == "high")
        if high_threats >= 5:
            return ThreatLevel.CRITICAL
        if high_threats >= 2:
            return ThreatLevel.HIGH
        if high_threats >= 1:
            return ThreatLevel.MEDIUM
        return ThreatLevel.LOW

    def _build_intel(self, name: str) -> CompetitiveIntel:
        profile = self._competitor_profiles().get(name, {})
        return CompetitiveIntel(
            competitor_name=name,
            strength=CompetitorStrength(profile.get("strength", "moderate")),
            market_share=profile.get("market_share", 0.0),
            key_features=profile.get("key_features", []),
            advantages=profile.get("advantages", []),
            weaknesses=profile.get("weaknesses", []),
            recent_moves=profile.get("recent_moves", []),
            pricing_tier=profile.get("pricing_tier", "mid"),
            target_segment=profile.get("target_segment", "sme"),
        )

    def _build_landscape_summary(self) -> str:
        lines = ["Saudi Arabia Commercial AI Competitive Landscape", ""]
        for name, intel in self._intel_cache.items():
            lines.append(f"  {name.upper()}: {intel.strength.value} "
                         f"(share: {intel.market_share:.1f}%, segment: {intel.target_segment})")
        return "\n".join(lines)

    def _recommend_action(self, intel: CompetitiveIntel) -> str:
        if intel.strength == CompetitorStrength.DOMINANT:
            return "Avoid direct competition. Find underserved sub-segments."
        elif intel.strength == CompetitorStrength.STRONG:
            return "Target specific weaknesses with differentiated offering."
        elif intel.strength == CompetitorStrength.MODERATE:
            return "Compete head-to-head on AI-native capabilities."
        elif intel.strength == CompetitorStrength.WEAK:
            return "Target their customers with superior automation."
        return "Monitor and maintain differentiation."

    def _competitor_profiles(self) -> dict[str, dict[str, Any]]:
        return {
            "salla": {
                "strength": "strong",
                "market_share": 28.0,
                "key_features": [
                    "All-in-one e-commerce platform",
                    "Arabic-first interface",
                    "Local payment integrations",
                    "Mobile app builder",
                    "Shipping automation",
                ],
                "advantages": [
                    "Strong brand recognition in KSA",
                    "Large merchant base (50k+)",
                    "Local payment and shipping integrations",
                    "Arabic-first experience",
                ],
                "weaknesses": [
                    "Limited AI/automation capabilities",
                    "No autonomous sales agents",
                    "No revenue intelligence",
                    "Basic CRM functionality",
                    "Limited enterprise features",
                ],
                "recent_moves": [
                    "Expanded into logistics network",
                    "Launched Salla Payments",
                    "Opened venture studio for plugins",
                ],
                "pricing_tier": "mid",
                "target_segment": "sme",
            },
            "zid": {
                "strength": "moderate",
                "market_share": 15.0,
                "key_features": [
                    "Multi-channel commerce",
                    "Inventory management",
                    "Order fulfillment",
                    "Analytics dashboard",
                    "Mobile POS",
                ],
                "advantages": [
                    "Strong multi-channel capabilities",
                    "Good inventory management",
                    "Growing merchant base",
                ],
                "weaknesses": [
                    "Limited AI capabilities",
                    "No autonomous agent features",
                    "No predictive analytics",
                    "Weak CRM integration",
                    "Limited API ecosystem",
                ],
                "recent_moves": [
                    "Launched fulfillment network",
                    "Added buy-now-pay-later options",
                ],
                "pricing_tier": "mid",
                "target_segment": "sme",
            },
            "salesforce": {
                "strength": "dominant",
                "market_share": 22.0,
                "key_features": [
                    "Enterprise CRM",
                    "Sales Cloud",
                    "Marketing Cloud",
                    "Service Cloud",
                    "Einstein AI",
                    "AppExchange ecosystem",
                ],
                "advantages": [
                    "Global enterprise trust",
                    "Vast ecosystem and integrations",
                    "Mature AI (Einstein)",
                    "Strong enterprise sales motion",
                    "Comprehensive platform",
                ],
                "weaknesses": [
                    "Very expensive",
                    "Complex implementation",
                    "Not Saudi-localized",
                    "Requires dedicated admin",
                    "Overwhelming for SMBs",
                    "No native KSA compliance",
                ],
                "recent_moves": [
                    "Launched Einstein GPT",
                    "Acquired Slack and Tableau",
                    "Expanded Middle East data centers",
                ],
                "pricing_tier": "premium",
                "target_segment": "enterprise",
            },
            "hubspot": {
                "strength": "strong",
                "market_share": 18.0,
                "key_features": [
                    "Inbound marketing platform",
                    "Sales CRM",
                    "Content management",
                    "Marketing automation",
                    "Customer service hub",
                    "Operations hub",
                ],
                "advantages": [
                    "Excellent inbound marketing tools",
                    "User-friendly interface",
                    "Strong content management",
                    "Good free tier",
                    "Large app marketplace",
                ],
                "weaknesses": [
                    "Limited AI-native features",
                    "Not optimized for Saudi market",
                    "No Arabic-first experience",
                    "Limited local support",
                    "Expensive at scale",
                    "No autonomous agents",
                ],
                "recent_moves": [
                    "Launched Breeze AI features",
                    "Expanded CMS capabilities",
                    "Added smart CRM enhancements",
                ],
                "pricing_tier": "mid_premium",
                "target_segment": "mid_market",
            },
            "local_crms": {
                "strength": "weak",
                "market_share": 5.0,
                "key_features": [
                    "Basic contact management",
                    "Simple pipelines",
                    "Email integration",
                    "Basic reporting",
                ],
                "advantages": [
                    "Cheapest option",
                    "Local language support",
                    "Simple to use",
                ],
                "weaknesses": [
                    "No AI capabilities",
                    "No automation",
                    "Limited integrations",
                    "Poor scalability",
                    "No mobile apps",
                    "No analytics",
                ],
                "recent_moves": [
                    "Some adding basic WhatsApp integration",
                ],
                "pricing_tier": "budget",
                "target_segment": "micro",
            },
        }
