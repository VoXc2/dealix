"""Thin sector-pack interface/registry. Plugs into existing truth layers.

No parallel service catalog: packs reference
auto_client_acquisition/vertical_playbooks + service_catalog by id only.
Seed: technology_saas, retail_hospitality, fatoora_sme.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SECTOR_PACK_VERSION = "1.0.0"


@dataclass(frozen=True)
class SectorPack:
    sector: str
    version: str = SECTOR_PACK_VERSION
    terminology_ar: tuple[str, ...] = ()
    terminology_en: tuple[str, ...] = ()
    intents: tuple[str, ...] = ()
    buyer_roles: tuple[str, ...] = ()
    common_problems: tuple[str, ...] = ()
    data_classes: tuple[str, ...] = ("public", "internal")
    regulatory_constraints: tuple[str, ...] = ()
    allowed_actions: tuple[str, ...] = ()
    restricted_actions: tuple[str, ...] = ()
    knowledge_sources: tuple[str, ...] = ()
    diagnostic_hooks: tuple[str, ...] = ()
    workflows: tuple[str, ...] = ()
    escalation_rules: tuple[str, ...] = ()
    acceptance_criteria: tuple[str, ...] = ()
    kpis: tuple[str, ...] = ()
    playbook_ref: str = ""
    catalog_refs: tuple[str, ...] = ("free_mini_diagnostic",)
    proof_metric: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "sector": self.sector,
            "version": self.version,
            "terminology_ar": list(self.terminology_ar),
            "terminology_en": list(self.terminology_en),
            "intents": list(self.intents),
            "buyer_roles": list(self.buyer_roles),
            "common_problems": list(self.common_problems),
            "data_classes": list(self.data_classes),
            "regulatory_constraints": list(self.regulatory_constraints),
            "allowed_actions": list(self.allowed_actions),
            "restricted_actions": list(self.restricted_actions),
            "knowledge_sources": list(self.knowledge_sources),
            "diagnostic_hooks": list(self.diagnostic_hooks),
            "workflows": list(self.workflows),
            "escalation_rules": list(self.escalation_rules),
            "acceptance_criteria": list(self.acceptance_criteria),
            "kpis": list(self.kpis),
            "playbook_ref": self.playbook_ref,
            "catalog_refs": list(self.catalog_refs),
            "proof_metric": self.proof_metric,
        }


_TECH_SAAS = SectorPack(
    sector="technology_saas",
    terminology_ar=("تفعيل", "تحويل trial إلى مدفوع", "زمن الوصول للقيمة"),
    terminology_en=("activation", "trial-to-paid", "time-to-value"),
    intents=("diagnostic_question", "onboarding", "technical_issue", "upgrade_question"),
    buyer_roles=("cto", "product_manager", "founder"),
    common_problems=("low trial-to-paid", "weak month-2 retention", "manual onboarding"),
    data_classes=("public", "internal"),
    regulatory_constraints=("PDPL consent for product analytics", "no scraping"),
    allowed_actions=("draft_onboarding_email", "prepare_diagnostic", "support_reply_draft"),
    restricted_actions=("send_cold_whatsapp", "auto_dm_linkedin", "fake_trial_users"),
    knowledge_sources=("official_public_site", "customer_provided_url", "internal_doc"),
    diagnostic_hooks=("trial_to_paid_rate", "time_to_first_value", "arabic_copy_check"),
    workflows=("inbound -> diagnose -> draft -> approval -> manual_send",),
    escalation_rules=("payment/refund/privacy -> founder", "guarantee ask -> founder"),
    acceptance_criteria=("draft_only without approval", "citations on every claim"),
    kpis=("trial_to_paid_conversion_delta", "reply_time_minutes_p50_delta"),
    playbook_ref="vertical_playbooks:saas",
    proof_metric="trial_to_paid_conversion_delta",
)

_RETAIL_HOSP = SectorPack(
    sector="retail_hospitality",
    terminology_ar=("حجوزات", "قائمة الانتظار", "تقييمات جوجل"),
    terminology_en=("bookings", "waitlist", "google reviews"),
    intents=("onboarding", "technical_issue", "proof_pack_question", "upgrade_question"),
    buyer_roles=("branch_manager", "owner", "marketing_lead"),
    common_problems=("slow inbound whatsapp reply", "lost leads", "no review strategy"),
    data_classes=("public", "internal"),
    regulatory_constraints=("PDPL consent for guest data", "no purchased phone lists"),
    allowed_actions=("draft_reply", "prepare_diagnostic", "follow_up_task"),
    restricted_actions=("send_cold_whatsapp", "buy_phone_lists", "scrape_local_directories"),
    knowledge_sources=("official_public_site", "customer_provided_url", "internal_doc"),
    diagnostic_hooks=("daily_whatsapp_volume", "avg_reply_time", "top_lead_source"),
    workflows=("inbound -> classify -> draft -> approval -> manual_reply",),
    escalation_rules=("angry_customer -> founder", "refund -> founder"),
    acceptance_criteria=("whatsapp inbound-only", "no auto-send"),
    kpis=("reply_time_minutes_p50_delta", "qualified_opportunities_per_pilot_week"),
    playbook_ref="vertical_playbooks:local_services",
    proof_metric="reply_time_minutes_p50_delta",
)

_FATOORA_SME = SectorPack(
    sector="fatoora_sme",
    terminology_ar=("فاتورة إلكترونية", "الربط مع هيئة الزكاة والضريبة", "إشعارات الفوترة"),
    terminology_en=("e-invoicing", "ZATCA integration", "billing notices"),
    intents=("billing", "payment", "connector_setup", "privacy_pdpl"),
    buyer_roles=("accountant", "owner", "ops_manager"),
    common_problems=("zatca onboarding confusion", "invoice disputes", "payment follow-up"),
    data_classes=("internal", "confidential"),
    regulatory_constraints=("ZATCA e-invoicing rules", "PDPL financial-data handling"),
    allowed_actions=("prepare_diagnostic", "support_reply_draft", "payment_reminder"),
    restricted_actions=("send_cold_whatsapp", "guaranteed_outcome_claim", "live_charge"),
    knowledge_sources=("official_public_site", "internal_doc", "crm_record"),
    diagnostic_hooks=("zatca_phase_check", "invoice_error_rate", "payment_delay_days"),
    workflows=("inbound -> verify -> draft -> approval -> manual_send",),
    escalation_rules=("payment/refund/privacy -> founder", "tax advice -> human expert"),
    acceptance_criteria=("no tax-advice claims without source", "draft_only finance text"),
    kpis=("invoice_error_rate_delta", "payment_delay_days_delta"),
    playbook_ref="vertical_playbooks:b2b_services",
    proof_metric="invoice_error_rate_delta",
)

_REGISTRY: dict[str, SectorPack] = {
    _TECH_SAAS.sector: _TECH_SAAS,
    _RETAIL_HOSP.sector: _RETAIL_HOSP,
    _FATOORA_SME.sector: _FATOORA_SME,
}


def list_sector_packs() -> list[dict[str, Any]]:
    return [p.to_dict() for p in _REGISTRY.values()]


def get_sector_pack(sector: str) -> dict[str, Any]:
    key = (sector or "").strip().lower()
    if key in _REGISTRY:
        return _REGISTRY[key].to_dict()
    # Safe fallback: never invent a sector — return closest generic + flag.
    fallback = _TECH_SAAS.to_dict()
    fallback["requested_sector"] = sector
    fallback["fallback"] = True
    return fallback


def is_known_sector(sector: str) -> bool:
    return (sector or "").strip().lower() in _REGISTRY
