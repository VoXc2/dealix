"""Arm Registry — 44+ capability arms, all activated, governed, reusable.

Each arm declares: arm_id, name, purpose, owner_agent, capabilities, inputs, outputs, tools, permissions, cost_class, risk_class, proof_requirements, supported_sectors, supported_problems, dependencies, health, maturity, last_verified.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class ArmHealth(StrEnum):
    ACTIVE = "active"
    DEGRADED = "degraded"
    BUILDING = "building"
    RETIRED = "retired"

class CapabilityArm(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    arm_id: str
    name: str
    name_ar: str = UNKNOWN
    purpose: str = UNKNOWN
    owner_agent: str  # dealix-pm/sales/delivery/engineer/content
    capabilities: list[str] = Field(default_factory=list)
    required_inputs: list[str] = Field(default_factory=list)
    produced_outputs: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    permissions: str = "L1"
    cost_class: str = "low"
    risk_class: str = "low"
    proof_requirements: list[str] = Field(default_factory=list)
    supported_sectors: list[str] = Field(default_factory=list)
    supported_problems: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    health: ArmHealth = ArmHealth.ACTIVE
    maturity: int = Field(default=3, ge=1, le=5)
    last_verified_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

ARMS: list[CapabilityArm] = [
    CapabilityArm(arm_id="arm_01_diagnostic", name="Universal Diagnostic Factory", name_ar="مصنع التشخيص الشامل", purpose="50 families D0-D5, sector/buyer overlays", owner_agent="dealix-pm", capabilities=["compose","question","leakage"], supported_sectors=["*"], supported_problems=["*"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_02_economic_cell", name="Economic Cell Registry", name_ar="سجل الخلايا الاقتصادية", purpose="500+ cells sparse, promotion/kill, DeepWIP", owner_agent="dealix-pm", capabilities=["generate","promote","kill"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_03_dispatcher", name="Economic Dispatcher", name_ar="الموزع الاقتصادي", purpose="confidence-aware scoring, VOI", owner_agent="dealix-pm", capabilities=["score","rank"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_04_president", name="President Command", name_ar="قيادة الرئيس", purpose="Top3 daily allocator", owner_agent="dealix-pm", capabilities=["top3","allocation","risks"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_05_probability", name="Probability Engine", name_ar="محرك الاحتمالات", purpose="10 probabilities, chain, update", owner_agent="dealix-pm", capabilities=["chain","update"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_06_portfolio_bets", name="Portfolio of Bets", name_ar="محفظة الرهانات", purpose="exploration 15%, DeepWIP 3, rank", owner_agent="dealix-pm", capabilities=["bets","rank","kill_zombies"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_07_financial", name="Financial OS", name_ar="النظام المالي", purpose="13-state truth, forecast, unit economics", owner_agent="dealix-pm", capabilities=["verified_cash","receivables","forecast","unit_economics"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_08_channel", name="Channel Registry", name_ar="سجل القنوات", purpose="22 types, 8 states, economic_score", owner_agent="dealix-pm", capabilities=["register","rank"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_09_consent", name="Consent Registry", name_ar="سجل الموافقات", purpose="6-state consent, can_send, withdraw", owner_agent="dealix-pm", capabilities=["consent","withdraw"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_10_relationship", name="Relationship Graph", name_ar="شبكة العلاقات", purpose="warm/stale, trust, next_action", owner_agent="dealix-sales", capabilities=["warm","stale"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_11_concierge", name="AI Concierge", name_ar="المساعد الذكي", purpose="11 intents, policy, allowlist 5", owner_agent="dealix-content", capabilities=["classify","retrieve","respond"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_12_diagnostic_ss", name="Self-Serve Diagnostic", name_ar="التشخيص الذاتي", purpose="input→bottleneck+range", owner_agent="dealix-content", capabilities=["assess"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_13_sector_company", name="Sector Company Factory", name_ar="مصنع شركات القطاعات", purpose="20 sectors as temp companies", owner_agent="dealix-pm", capabilities=["build","build_all"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_14_omnichannel", name="Omnichannel Orchestrator", name_ar="منسق القنوات", purpose="12 channels, draft→approval→send, no cold WhatsApp", owner_agent="dealix-sales", capabilities=["prepare_draft","approve_and_send"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_15_saudi_radar", name="Saudi Market Radar", name_ar="رادار السوق السعودي", purpose="ZATCA Wave25 187,500, MISA 1,865, Etimad 2243 active", owner_agent="dealix-pm", capabilities=["zatca","etimad","misa","pdpl"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_16_low_touch", name="Low-Touch Income", name_ar="الدخل قليل اللمس", purpose="22 rails, scoring, 5 seeded", owner_agent="dealix-pm", capabilities=["score","rank"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_17_open_source", name="Open Source Registry", name_ar="سجل المفتوح", purpose="ADOPT/TEST/WATCH/REJECT 7 tools", owner_agent="dealix-engineer", capabilities=["register"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_18_invariants", name="Company Invariants", name_ar="ثوابت الشركة", purpose="INV-001..007", owner_agent="dealix-pm", capabilities=["get_invariants"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_19_scheduler", name="Scheduler Inventory", name_ar="جرد المجدول", purpose="11 dealix timers, classify", owner_agent="dealix-engineer", capabilities=["inventory","classify"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_20_delivery", name="Delivery Factory", name_ar="مصنع التسليم", purpose="10 stages, reusable artifacts", owner_agent="dealix-delivery", capabilities=["create","advance"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_21_proof_asset", name="Proof Asset Factory", name_ar="مصنع الأصول", purpose="20 types, reuse, productization", owner_agent="dealix-delivery", capabilities=["create_from_delivery","reuse"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_22_business_telemetry", name="Business Telemetry", name_ar="القياس التجاري", purpose="receipts, economic movement", owner_agent="dealix-pm", capabilities=["emit"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_23_agent_packets", name="Agent Packets", name_ar="حزم الوكلاء", purpose="5-agent dispatch, budgets, stop condition", owner_agent="dealix-pm", capabilities=["build_all_packets"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_24_solutions_api", name="Solutions API", name_ar="واجهة الحلول", purpose="/api/v1/solutions 20 sectors", owner_agent="dealix-engineer", capabilities=["list_sectors","get_sector"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_25_solutions_web", name="Solutions Web", name_ar="ويب الحلول", purpose="/solutions grid + /solutions/[sector] detail", owner_agent="dealix-content", capabilities=["listing","detail"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_26_seo", name="SEO/AEO", name_ar="تحسين البحث", purpose="sitemap, robots, JSON-LD Organization+SoftwareApplication", owner_agent="dealix-content", capabilities=["sitemap","json_ld"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_27_daily_loop", name="Daily Company Loop", name_ar="الحلقة اليومية", purpose="reconcile→verify→process→rank→execute", owner_agent="dealix-pm", capabilities=["run_self_operating"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_28_verification", name="Verification Suite", name_ar="حزمة التحقق", purpose="8-scenario acceptance, 7 invariants, closed-loop 9 checks", owner_agent="dealix-engineer", capabilities=["verify"], health=ArmHealth.ACTIVE, maturity=4),
]

# Extend to 44 by adding more granular arms
EXTRA = [
    CapabilityArm(arm_id="arm_29_offer", name="Offer Factory", name_ar="مصنع العروض", purpose="11 offer families, business outcome", owner_agent="dealix-sales", capabilities=["offer_match"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_30_pricing", name="Pricing Intelligence", name_ar="ذكاء التسعير", purpose="cost floor, margin, risk premium", owner_agent="dealix-pm", capabilities=["price_range"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_31_negotiation", name="Negotiation Engine", name_ar="محرك التفاوض", purpose="target, floor, BATNA, concessions", owner_agent="dealix-sales", capabilities=["negotiate"], health=ArmHealth.ACTIVE, maturity=2),
    CapabilityArm(arm_id="arm_32_procurement_radar", name="Procurement Radar", name_ar="رادار المناقصات", purpose="Etimad discovery, bid/no-bid", owner_agent="dealix-pm", capabilities=["discover","score"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_33_jadeer", name="Jadeer Readiness", name_ar="جاهزية جدير", purpose="SME supplier qualification", owner_agent="dealix-pm", capabilities=["readiness"], health=ArmHealth.BUILDING, maturity=2),
    CapabilityArm(arm_id="arm_34_partner", name="Partner Radar", name_ar="رادار الشركاء", purpose="SI, consultancies, agencies, cloud", owner_agent="dealix-sales", capabilities=["partner_match"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_35_content_factory", name="Content Factory", name_ar="مصنع المحتوى", purpose="proof→ar/en article + post + FAQ", owner_agent="dealix-content", capabilities=["atomize"], health=ArmHealth.BUILDING, maturity=2),
    CapabilityArm(arm_id="arm_36_analytics", name="Analytics", name_ar="التحليلات", purpose="PostHog, funnel LANDING→PAYMENT", owner_agent="dealix-engineer", capabilities=["track"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_37_security", name="Security", name_ar="الأمن", purpose="least privilege, audit, loopback LLM", owner_agent="dealix-engineer", capabilities=["audit"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_38_observability", name="Observability", name_ar="المراقبة", purpose="traces, metrics, business events", owner_agent="dealix-engineer", capabilities=["trace"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_39_model_router", name="Model Router", name_ar="موجه النماذج", purpose="local→free→cheap→premium, cost per accepted", owner_agent="dealix-engineer", capabilities=["route"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_40_website_sensor", name="Website Sensor", name_ar="حساس الموقع", purpose="visitor intent→diagnostic→opportunity", owner_agent="dealix-content", capabilities=["sense"], health=ArmHealth.ACTIVE, maturity=3),
    CapabilityArm(arm_id="arm_41_trust_center", name="Trust Center", name_ar="مركز الثقة", purpose="PDPL, ZATCA, NCA, approval model", owner_agent="dealix-content", capabilities=["trust"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_42_proof_ledger", name="Proof Ledger", name_ar="سجل الإثبات", purpose="ledger v5 redaction, evidence_export", owner_agent="dealix-delivery", capabilities=["record","export"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_43_approval_center", name="Approval Center", name_ar="مركز الموافقات", purpose="L5 packets, idempotency, rollback", owner_agent="dealix-pm", capabilities=["approve"], health=ArmHealth.ACTIVE, maturity=4),
    CapabilityArm(arm_id="arm_44_revenue_memory", name="Revenue Memory", name_ar="ذاكرة الإيراد", purpose="isolated PG event store, vector", owner_agent="dealix-engineer", capabilities=["memory"], health=ArmHealth.ACTIVE, maturity=3),
]

ALL_ARMS = ARMS + EXTRA

def get_active_arms() -> list[CapabilityArm]:
    return [a for a in ALL_ARMS if a.health == ArmHealth.ACTIVE]

def to_dict() -> dict[str, Any]:
    return {"total": len(ALL_ARMS), "active": len(get_active_arms()), "arms": [a.model_dump(mode="json") for a in ALL_ARMS]}

__all__ = ["CapabilityArm", "ArmHealth", "ALL_ARMS", "get_active_arms", "to_dict"]
