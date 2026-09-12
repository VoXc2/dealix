"""Saudi Market Radar — official-source, freshness-bound research signals.

This is the existing canonical radar, not a second signal store. Every record is
research evidence only and is structurally forbidden from becoming consent,
relationship, pipeline or revenue. Dynamic counts (for example active Etimad
tenders) must be timestamped snapshots and are never hard-coded as durable fact.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"


class SignalSource(StrEnum):
    SDAIA_PDPL = "sdaia_pdpl"
    NCA_ECC = "nca_ecc"
    ZATCA = "zatca"
    ETIMAD = "etimad"
    MISA = "misa"
    MONSHAAT_JADEER = "monshaat_jadeer"
    SAMA = "sama"
    CST = "cst"
    MOH = "moh"
    REGA = "rega"
    GASTAT = "gastat"
    SAUDI_OPEN_DATA = "saudi_open_data"
    MINISTRY_COMMERCE = "ministry_commerce"
    CUSTOMER_SIGNAL = "customer_signal"


class RegulatorySignal(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    signal_id: str
    source: SignalSource
    source_url: str = UNKNOWN
    source_date: str = UNKNOWN
    retrieved_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    effective_date: str = UNKNOWN
    expiry_review_at: str = Field(
        default_factory=lambda: (datetime.now(UTC) + timedelta(days=90)).isoformat()
    )
    refresh_policy: str = "refresh_before_use"
    title_ar: str = UNKNOWN
    title_en: str = UNKNOWN
    scope: str = UNKNOWN
    affected_sectors: list[str] = Field(default_factory=list)
    affected_cells: list[str] = Field(default_factory=list)
    buyer_type: str = UNKNOWN
    problem: str = UNKNOWN
    trigger: str = UNKNOWN
    deadline: str = UNKNOWN
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    commercial_implication: str = UNKNOWN
    compliance_implication: str = UNKNOWN
    diagnostic_match: list[str] = Field(default_factory=list)
    offer_match: list[str] = Field(default_factory=list)
    evidence_strength: int = Field(default=1, ge=0, le=5)
    truth_class: str = "OBSERVED"
    counts_as_relationship: bool = False
    counts_as_consent: bool = False
    counts_as_pipeline: bool = False
    counts_as_revenue: bool = False
    tender_submission_allowed: bool = False

    def is_fresh(self) -> bool:
        try:
            expiry = datetime.fromisoformat(self.expiry_review_at.replace("Z", "+00:00"))
            return datetime.now(UTC) < expiry
        except Exception:
            return False


class SaudiMarketRadar:
    """Canonical in-memory official-source registry; callers persist elsewhere."""

    def __init__(self) -> None:
        self.signals: dict[str, RegulatorySignal] = {}

    def ingest(self, sig: RegulatorySignal) -> RegulatorySignal:
        self.signals[sig.signal_id] = sig
        return sig

    def zatca_wave25_signal(self) -> RegulatorySignal:
        return self.ingest(
            RegulatorySignal(
                signal_id="zatca_wave25_2026",
                source=SignalSource.ZATCA,
                source_url="https://zatca.gov.sa/en/MediaCenter/News/Pages/Wave25-E-invoicing.aspx",
                source_date="2026-07-24",
                retrieved_at=datetime.now(UTC).isoformat(),
                effective_date="2027-02-01",
                expiry_review_at=(datetime.now(UTC) + timedelta(days=30)).isoformat(),
                refresh_policy="official_source_monthly_and_before_customer_use",
                title_ar="زاتكا — المجموعة 25 لمرحلة الربط والتكامل",
                title_en="ZATCA Wave 25 — E-invoicing Integration Phase",
                scope=(
                    "Official Wave 25 criterion: VAT-subject revenue exceeded SAR 187,500 "
                    "in any of 2022, 2023, 2024 or 2025. ZATCA notifies targeted taxpayers; "
                    "customer applicability must be verified before any customer-specific claim."
                ),
                affected_sectors=["cross_sector"],
                buyer_type="finance/IT/operations",
                problem="fatoora_readiness",
                trigger="customer receives official Wave 25 notification or confirms applicability",
                deadline="2027-02-01 for notified Wave 25 taxpayers",
                confidence=0.98,
                commercial_implication="Free Fatoora readiness diagnostic -> customer-specific implementation/integration if qualified.",
                compliance_implication="Not tax/legal advice; no ZATCA certification or affiliation claim.",
                diagnostic_match=["Fatoora readiness", "systems/integration", "finance operations"],
                offer_match=["AI Company OS Setup", "Revenue Proof Sprint"],
                evidence_strength=5,
            )
        )

    def jadeer_supplier_signal(self) -> RegulatorySignal:
        return self.ingest(
            RegulatorySignal(
                signal_id="monshaat_jadeer_supplier_readiness",
                source=SignalSource.MONSHAAT_JADEER,
                source_url="https://www.monshaat.gov.sa/en/node/12778",
                retrieved_at=datetime.now(UTC).isoformat(),
                expiry_review_at=(datetime.now(UTC) + timedelta(days=60)).isoformat(),
                refresh_policy="official_source_every_60d_and_before_customer_use",
                title_ar="جدير — تأهيل المنشآت الصغيرة والمتوسطة",
                title_en="Jadeer — SME Supplier Prequalification",
                scope="Free Monsha'at service for SME prequalification and capability evidence for public/private procurement access.",
                affected_sectors=["cross_sector"],
                buyer_type="SME owner/procurement readiness owner",
                problem="supplier_readiness",
                trigger="supplier qualification or procurement readiness need",
                confidence=0.95,
                commercial_implication="Free supplier-readiness diagnostic; paid work only for customer-specific remediation/automation after qualification.",
                compliance_implication="No privileged access claim and no guarantee of qualification or procurement award.",
                diagnostic_match=["supplier readiness", "B2G readiness"],
                offer_match=["B2G Readiness Sprint", "Saudi Opportunity Snapshot"],
                evidence_strength=5,
            )
        )

    def sama_open_banking_signal(self) -> RegulatorySignal:
        return self.ingest(
            RegulatorySignal(
                signal_id="sama_open_banking_licensing_2026",
                source=SignalSource.SAMA,
                source_url="https://sama.gov.sa/en-US/MediaCenter/News/Pages/news-1135.aspx",
                source_date="2026-03-26",
                retrieved_at=datetime.now(UTC).isoformat(),
                expiry_review_at=(datetime.now(UTC) + timedelta(days=90)).isoformat(),
                refresh_policy="official_source_quarterly_and_before_financial-sector_use",
                title_ar="ساما — بدء ترخيص شركات الخدمات المصرفية المفتوحة",
                title_en="SAMA — Open Banking Licensing Commenced",
                scope="SAMA announced commencement of licensing fintech companies for open banking services following sandbox completion.",
                affected_sectors=["finance_fintech_insurance", "technology_saas_si"],
                buyer_type="compliance/product/technology",
                problem="regulated_integration_readiness",
                trigger="open banking product/integration or compliance change",
                confidence=0.98,
                commercial_implication="Free regulated AI/data/integration readiness diagnostic before any implementation scope.",
                compliance_implication="Only authorized institutions; customer consent/privacy and SAMA framework remain governing controls.",
                diagnostic_match=["AI/data/integration readiness", "risk/control"],
                offer_match=["AI Company OS Setup", "Revenue Proof Sprint"],
                evidence_strength=5,
            )
        )

    def cst_ai_adoption_signal(self) -> RegulatorySignal:
        return self.ingest(
            RegulatorySignal(
                signal_id="cst_ai_adoption_guide_2026",
                source=SignalSource.CST,
                source_url="https://www.cst.gov.sa/en/knowledge-center/reports/ai-adoption-guide-for-tech-companies",
                source_date="2026",
                retrieved_at=datetime.now(UTC).isoformat(),
                expiry_review_at=(datetime.now(UTC) + timedelta(days=90)).isoformat(),
                refresh_policy="official_source_quarterly",
                title_ar="CST — دليل تبني الذكاء الاصطناعي للشركات التقنية",
                title_en="CST — AI Adoption Guide for Technology Companies",
                scope="Readiness across context, data, infrastructure, skills/expertise and culture; includes internal, customer-facing and agentic AI use.",
                affected_sectors=["technology_saas_si", "telecom_media_marketing"],
                buyer_type="executive/technology/product",
                problem="ai_readiness",
                trigger="AI adoption or agent deployment initiative",
                confidence=0.95,
                commercial_implication="Free AI readiness diagnostic -> governed implementation only after customer-specific evidence.",
                compliance_implication="Treat guidance as readiness context, not a Dealix certification.",
                diagnostic_match=["AI readiness", "data readiness", "governance"],
                offer_match=["AI Company OS Setup", "Revenue Proof Sprint"],
                evidence_strength=5,
            )
        )

    def moh_sandbox_signal(self) -> RegulatorySignal:
        return self.ingest(
            RegulatorySignal(
                signal_id="moh_health_sandbox_2026",
                source=SignalSource.MOH,
                source_url="https://www.moh.gov.sa/en/ministry/mediacenter/news/pages/news-2026-07-08-001.aspx",
                source_date="2026-07-08",
                retrieved_at=datetime.now(UTC).isoformat(),
                expiry_review_at=(datetime.now(UTC) + timedelta(days=60)).isoformat(),
                refresh_policy="official_source_every_60d",
                title_ar="وزارة الصحة — Sandbox للابتكار الصحي",
                title_en="Ministry of Health — Health Innovation Sandbox",
                scope="Testing environment for digital health, AI, IoT, biotechnology and other innovative health solutions.",
                affected_sectors=["healthcare", "technology_saas_si"],
                buyer_type="innovation/technology/operations",
                problem="digital_health_validation",
                trigger="health innovation requires validation or deployment readiness",
                confidence=0.98,
                commercial_implication="Free health AI/readiness diagnostic; no clinical or regulatory approval claim.",
                compliance_implication="Sensitive health data and regulatory boundaries require explicit customer/authority evidence.",
                diagnostic_match=["AI readiness", "privacy/security", "delivery readiness"],
                offer_match=["AI Company OS Setup", "Revenue Proof Sprint"],
                evidence_strength=5,
            )
        )

    def rega_proptech_signal(self) -> RegulatorySignal:
        return self.ingest(
            RegulatorySignal(
                signal_id="rega_proptech_hub_sandbox_2026",
                source=SignalSource.REGA,
                source_url="https://rega.gov.sa/en/rega-services/platforms/saudi-proptech-hub/",
                retrieved_at=datetime.now(UTC).isoformat(),
                expiry_review_at=(datetime.now(UTC) + timedelta(days=60)).isoformat(),
                refresh_policy="official_source_every_60d",
                title_ar="هيئة العقار — مركز بروبتك والبيئة التنظيمية التجريبية",
                title_en="REGA — Saudi PropTech Hub & Regulatory Sandbox",
                scope="PropTech innovation/testing pathway under REGA supervision; program details and dates must be refreshed before acting.",
                affected_sectors=["real_estate_proptech", "technology_saas_si"],
                buyer_type="PropTech founder/innovation/operations",
                problem="proptech_regulatory_readiness",
                trigger="innovative real-estate model requires regulatory testing/readiness",
                confidence=0.95,
                commercial_implication="Free PropTech readiness diagnostic -> customer-specific implementation support if qualified.",
                compliance_implication="No guarantee of sandbox acceptance, licensing or market launch.",
                diagnostic_match=["digital readiness", "workflow automation", "privacy/security"],
                offer_match=["AI Company OS Setup", "Saudi Opportunity Snapshot"],
                evidence_strength=5,
            )
        )

    def etimad_tender_cell(
        self,
        tender_ref: str,
        issuer: str,
        sector: str,
        deadline: str,
        *,
        source_url: str = "https://tenders.etimad.sa/",
    ) -> RegulatorySignal:
        now = datetime.now(UTC)
        sig_id = f"etimad_{hashlib.sha256(tender_ref.encode()).hexdigest()[:8]}"
        return self.ingest(
            RegulatorySignal(
                signal_id=sig_id,
                source=SignalSource.ETIMAD,
                source_url=source_url,
                retrieved_at=now.isoformat(),
                effective_date=deadline,
                expiry_review_at=min(
                    now + timedelta(days=1),
                    datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                    if "T" in deadline
                    else now + timedelta(days=1),
                ).isoformat(),
                refresh_policy="refresh_daily_and_before_bid_decision",
                title_ar=f"منافسة اعتماد {tender_ref}",
                title_en=f"Etimad tender {tender_ref}",
                scope=f"Issuer {issuer}; sector {sector}; reference {tender_ref}. Verify live tender page for eligibility/documents/deadline.",
                affected_sectors=[sector],
                buyer_type="government/procurement",
                problem="tender_readiness",
                trigger="relevant tender discovered",
                deadline=deadline,
                confidence=0.7,
                commercial_implication="Research/readiness only: eligibility, documents, capacity, risk, effort and bid/no-bid recommendation.",
                compliance_implication="Tender submission is L5 and is never authorized by this record.",
                diagnostic_match=["B2G readiness", "supplier readiness"],
                offer_match=["B2G Readiness Sprint", "Saudi Opportunity Snapshot"],
                evidence_strength=3,
                tender_submission_allowed=False,
            )
        )

    def pdpl_signal(self) -> RegulatorySignal:
        now = datetime.now(UTC)
        return self.ingest(
            RegulatorySignal(
                signal_id="pdpl_direct_marketing_governance",
                source=SignalSource.SDAIA_PDPL,
                source_url="https://dgp.sdaia.gov.sa/",
                retrieved_at=now.isoformat(),
                expiry_review_at=(now + timedelta(days=90)).isoformat(),
                refresh_policy="official_source_quarterly_and_before_marketing_policy_change",
                title_ar="PDPL — حوكمة البيانات والتسويق المباشر",
                title_en="PDPL — Data Governance & Direct Marketing",
                scope="Consent/purpose/withdrawal/sender-identity controls; refresh exact legal requirements before customer-specific advice.",
                affected_sectors=["cross_sector"],
                buyer_type="privacy/compliance/marketing",
                problem="consent_and_direct_marketing_governance",
                trigger="direct marketing or personal-data processing workflow",
                confidence=0.9,
                commercial_implication="Consent-aware workflow and suppression governance; never cold WhatsApp by default.",
                compliance_implication="Not legal advice; exact applicability must be verified.",
                diagnostic_match=["privacy/PDPL", "channel governance"],
                offer_match=["AI Company OS Setup", "Revenue Proof Sprint"],
                evidence_strength=4,
            )
        )

    def misa_invest_saudi_signal(self) -> RegulatorySignal:
        """Keep the legacy method, but remove durable marketing statistics."""
        now = datetime.now(UTC)
        return self.ingest(
            RegulatorySignal(
                signal_id="misa_invest_saudi_market_access",
                source=SignalSource.MISA,
                source_url="https://misa.gov.sa/",
                retrieved_at=now.isoformat(),
                expiry_review_at=(now + timedelta(days=90)).isoformat(),
                refresh_policy="official_source_quarterly_and_before_market-entry-use",
                title_ar="وزارة الاستثمار — دخول السوق والفرص الاستثمارية",
                title_en="MISA — Saudi Market Entry & Investment Opportunities",
                scope="Official Saudi investment/market-entry context. Dynamic opportunity counts and incentives must be refreshed, never hard-coded here.",
                affected_sectors=["cross_sector"],
                buyer_type="foreign B2B/RHQ/market-entry decision maker",
                problem="saudi_market_entry",
                trigger="company evaluating Saudi market entry, RHQ or partner route",
                confidence=0.9,
                commercial_implication="Saudi Market Access diagnostic and buyer/partner/procurement mapping; no privileged-access claim.",
                compliance_implication="Licensing/incentive applicability is customer-specific and must be verified with official sources.",
                diagnostic_match=["market access", "buyer/partner mapping", "procurement readiness"],
                offer_match=["Saudi Market Access Sprint", "Partner / Distributor Desk", "Saudi Opportunity Snapshot"],
                evidence_strength=4,
            )
        )

    def seed_official_watchlist(self) -> list[RegulatorySignal]:
        return [
            self.zatca_wave25_signal(),
            self.jadeer_supplier_signal(),
            self.sama_open_banking_signal(),
            self.cst_ai_adoption_signal(),
            self.moh_sandbox_signal(),
            self.rega_proptech_signal(),
            self.pdpl_signal(),
            self.misa_invest_saudi_signal(),
        ]

    def list_fresh(self) -> list[RegulatorySignal]:
        return [signal for signal in self.signals.values() if signal.is_fresh()]

    def to_dict(self) -> dict[str, Any]:
        return {
            "signals": [signal.model_dump(mode="json") for signal in self.signals.values()],
            "fresh_count": len(self.list_fresh()),
            "research_counts_as_relationship": False,
            "research_counts_as_pipeline": False,
            "research_counts_as_revenue": False,
        }


__all__ = ["SaudiMarketRadar", "RegulatorySignal", "SignalSource", "UNKNOWN"]
