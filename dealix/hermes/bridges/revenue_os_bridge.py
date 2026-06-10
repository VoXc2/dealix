"""RevenueOSBridge — ربط Hermes بـ Revenue OS signals"""

from __future__ import annotations

from typing import Any, Optional

import structlog

from dealix.hermes.orchestrators.wave_orchestrator import WAVE_CONFIGS

logger = structlog.get_logger(__name__)


class MarketSignal:
    """Lightweight signal model matching dealix.commercial.market_intelligence.MarketSignal."""

    def __init__(
        self,
        signal_id: str,
        sector: str,
        signal_type: str,
        title_ar: str,
        title_en: str,
        description_ar: str,
        description_en: str,
        urgency: str = "MEDIUM",
        opportunity_ar: str = "",
        opportunity_en: str = "",
        source_type: str = "hermes_wave",
        requires_decision_passport: bool = False,
        action_type: str = "",
    ) -> None:
        self.signal_id = signal_id
        self.sector = sector
        self.signal_type = signal_type
        self.title_ar = title_ar
        self.title_en = title_en
        self.description_ar = description_ar
        self.description_en = description_en
        self.urgency = urgency
        self.opportunity_ar = opportunity_ar
        self.opportunity_en = opportunity_en
        self.source_type = source_type
        self.requires_decision_passport = requires_decision_passport
        self.action_type = action_type


class RevenueOSBridge:
    """ربط Hermes بـ Revenue OS signals — يحول نتائج Waves إلى إشارات قابلة للتنفيذ"""

    _instance: RevenueOSBridge | None = None

    @classmethod
    def instance(cls) -> RevenueOSBridge:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def wave_to_signal(self, wave_id: str, result: dict) -> Optional[MarketSignal]:
        """Convert wave completion to a Revenue OS MarketSignal."""
        signal_map = {
            "wave_3_distribution": self._distribution_to_signal,
            "wave_4_intelligence": self._intelligence_to_signal,
            "wave_7_saudi": self._saudi_to_signal,
            "wave_8_gulf": self._gulf_to_signal,
            "wave_9_ops": self._ops_to_signal,
        }
        handler = signal_map.get(wave_id)
        if handler:
            signal = await handler(result)
            logger.info("wave_converted_to_signal", wave_id=wave_id, signal_id=signal.signal_id)
            return signal

        logger.debug("no_signal_handler_for_wave", wave_id=wave_id)
        return None

    async def signal_to_wave_action(self, signal: MarketSignal) -> Optional[str]:
        """Convert a Revenue OS signal to a Hermes wave action."""
        if signal.requires_decision_passport:
            logger.info("signal_requires_passport", signal_id=signal.signal_id)
            return None
        logger.info("signal_mapped_to_action", signal_id=signal.signal_id, action=signal.action_type)
        return signal.action_type

    async def _distribution_to_signal(self, result: dict) -> MarketSignal:
        """Wave 3 completion → distribution signal."""
        return MarketSignal(
            signal_id=f"wave3_dist_{result.get('timestamp', 'now')}",
            sector="all",
            signal_type="distribution",
            title_ar="إشارة توزيع: مكاين التصريف جاهزة",
            title_en="Distribution Signal: 4 Engines Ready",
            description_ar="اكتملت موجات التوزيع الأربعة الكبرى — جاهزون للانطلاق",
            description_en="All 4 distribution engines completed — ready for launch",
            urgency="HIGH",
            opportunity_ar="تفعيل جميع قنوات التوزيع",
            opportunity_en="Activate all distribution channels",
            action_type="activate_distribution",
            requires_decision_passport=True,
        )

    async def _intelligence_to_signal(self, result: dict) -> MarketSignal:
        """Wave 4 completion → AI intelligence signal."""
        return MarketSignal(
            signal_id=f"wave4_ai_{result.get('timestamp', 'now')}",
            sector="all",
            signal_type="intelligence",
            title_ar="إشارة ذكاء: الذكاء الصناعي مكتمل",
            title_en="Intelligence Signal: AI Layer Complete",
            description_ar="اكتملت طبقة الذكاء الصناعي — جاهزون للتوسع الذكي",
            description_en="AI superintelligence layer complete — ready for smart scaling",
            urgency="HIGH",
            opportunity_ar="تفعيل التوسع الذكي القائم على RAG",
            opportunity_en="Activate RAG-based smart expansion",
            action_type="enable_ai_layer",
            requires_decision_passport=False,
        )

    async def _saudi_to_signal(self, result: dict) -> MarketSignal:
        """Wave 7 completion → Saudi market signal."""
        return MarketSignal(
            signal_id=f"wave7_sa_{result.get('timestamp', 'now')}",
            sector="saudi",
            signal_type="market_entry",
            title_ar="إشارة سوق: الطبقة السعودية جاهزة",
            title_en="Market Signal: Saudi Layer Ready",
            description_ar="اكتملت طبقة السعودية العميقة — جاهزون للسوق السعودي",
            description_en="Deep Saudi layer complete — ready for Saudi market",
            urgency="HIGH",
            opportunity_ar="بدء الحملات التسويقية السعودية",
            opportunity_en="Start Saudi marketing campaigns",
            action_type="enter_saudi_market",
            requires_decision_passport=False,
        )

    async def _gulf_to_signal(self, result: dict) -> MarketSignal:
        """Wave 8 completion → Gulf expansion signal."""
        return MarketSignal(
            signal_id=f"wave8_gulf_{result.get('timestamp', 'now')}",
            sector="gulf",
            signal_type="expansion",
            title_ar="إشارة توسع: الخليج جاهز",
            title_en="Expansion Signal: Gulf Ready",
            description_ar="اكتملت طبقة التوسع الخليجي — جاهزون لدخول 5 أسواق",
            description_en="Gulf expansion layer complete — ready for 5 markets",
            urgency="MEDIUM",
            opportunity_ar="التوسع في الإمارات وقطر والكويت والبحرين وعُمان",
            opportunity_en="Expand into UAE, Qatar, Kuwait, Bahrain, Oman",
            action_type="expand_gulf",
            requires_decision_passport=True,
        )

    async def _ops_to_signal(self, result: dict) -> MarketSignal:
        """Wave 9 completion → ops excellence signal."""
        return MarketSignal(
            signal_id=f"wave9_ops_{result.get('timestamp', 'now')}",
            sector="internal",
            signal_type="operational",
            title_ar="إشارة تشغيل: التميز التنفيذي مكتمل",
            title_en="Ops Signal: Executive Excellence Ready",
            description_ar="اكتملت طبقة التميز التشغيلي — النظام يعمل بكامل طاقته",
            description_en="Executive ops excellence layer complete — system at full power",
            urgency="MEDIUM",
            opportunity_ar="تفعيل التشغيل الذاتي الكامل",
            opportunity_en="Activate full autonomous operations",
            action_type="enable_autonomous_ops",
            requires_decision_passport=False,
        )

    async def get_wave_signal_map(self) -> dict[str, str]:
        """Return mapping of wave IDs to their signal types."""
        return {
            "wave_3_distribution": "distribution",
            "wave_4_intelligence": "intelligence",
            "wave_7_saudi": "market_entry",
            "wave_8_gulf": "expansion",
            "wave_9_ops": "operational",
        }


__all__ = ["MarketSignal", "RevenueOSBridge"]
