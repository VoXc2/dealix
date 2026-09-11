"""Saudi Market Radar — official-source watchers for ZATCA/Etimad/MISA/PDPL/NCA.

Stores signals with provenance, supports cell impact mapping.
No hardcoding of regulatory facts forever; retrieval date and expiry tracked.
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
    SAUDI_OPEN_DATA = "saudi_open_data"
    MINISTRY_COMMERCE = "ministry_commerce"
    CUSTOMER_SIGNAL = "customer_signal"

class RegulatorySignal(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    signal_id: str
    source: SignalSource
    source_url: str = UNKNOWN
    retrieved_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    effective_date: str = UNKNOWN
    expiry_review_at: str = Field(default_factory=lambda: (datetime.now(UTC) + timedelta(days=90)).isoformat())
    title_ar: str = UNKNOWN
    title_en: str = UNKNOWN
    scope: str = UNKNOWN
    affected_sectors: list[str] = Field(default_factory=list)
    affected_cells: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    commercial_implication: str = UNKNOWN
    compliance_implication: str = UNKNOWN
    evidence_strength: int = Field(default=1, ge=0, le=5)

    def is_fresh(self) -> bool:
        try:
            expiry = datetime.fromisoformat(self.expiry_review_at.replace("Z", "+00:00"))
            return datetime.now(UTC) < expiry
        except Exception:
            return False

class SaudiMarketRadar:
    """Lightweight official-source registry — evidence-bound."""

    def __init__(self) -> None:
        self.signals: dict[str, RegulatorySignal] = {}

    def ingest(self, sig: RegulatorySignal) -> RegulatorySignal:
        self.signals[sig.signal_id] = sig
        return sig

    def zatca_wave25_signal(self) -> RegulatorySignal:
        # Official Wave 25 as market signal, not guaranteed demand
        now = datetime.now(UTC).isoformat()
        sig = RegulatorySignal(
            signal_id="zatca_wave25_2026",
            source=SignalSource.ZATCA,
            source_url="https://zatca.gov.sa",
            retrieved_at=now,
            effective_date="2026-06-01",
            title_ar="ZATCA Wave 25 إشارة سوقية للفوترة الإلكترونية",
            title_en="ZATCA Wave 25 market signal for e-invoicing",
            scope="Businesses exceeding threshold per official announcement; integration/readiness demand signal",
            affected_sectors=["finance_fintech_insurance", "technology_saas_si", "retail_commerce_ecommerce"],
            affected_cells=[],
            confidence=0.7,
            commercial_implication="e-invoicing readiness diagnostic, ERP integration assessment, workflow automation, data validation",
            compliance_implication="No ZATCA certification claim; readiness diagnostic only",
            evidence_strength=3,
        )
        return self.ingest(sig)

    def etimad_tender_cell(self, tender_ref: str, issuer: str, sector: str, deadline: str) -> RegulatorySignal:
        now = datetime.now(UTC).isoformat()
        sig_id = f"etimad_{hashlib.sha256(tender_ref.encode()).hexdigest()[:8]}"
        sig = RegulatorySignal(
            signal_id=sig_id,
            source=SignalSource.ETIMAD,
            source_url="https://etimad.sa",
            retrieved_at=now,
            effective_date=deadline,
            title_ar=f"مناقصة Etimad {tender_ref}",
            title_en=f"Etimad tender {tender_ref}",
            scope=f"Issuer {issuer}, sector {sector}, reference {tender_ref}",
            affected_sectors=[sector],
            confidence=0.6,
            commercial_implication="Tender intelligence cell — eligibility, partner requirement, bid effort, expected value",
            compliance_implication="Submission is L5, draft/readiness only",
            evidence_strength=2,
        )
        return self.ingest(sig)

    def pdpl_signal(self) -> RegulatorySignal:
        now = datetime.now(UTC).isoformat()
        return self.ingest(RegulatorySignal(
            signal_id="pdpl_governance_2026",
            source=SignalSource.SDAIA_PDPL,
            source_url="https://sdaia.gov.sa",
            retrieved_at=now,
            title_ar="PDPL حوكمة البيانات",
            title_en="PDPL Data Governance",
            scope="Consent, purpose, retention, withdrawal for direct marketing",
            affected_sectors=["technology_saas_si", "finance_fintech_insurance", "healthcare"],
            confidence=0.9,
            commercial_implication="Consent-first outreach, purpose limitation, no cold WhatsApp",
            compliance_implication="Direct marketing requires explicit consent",
            evidence_strength=4,
        ))

    def list_fresh(self) -> list[RegulatorySignal]:
        return [s for s in self.signals.values() if s.is_fresh()]

    def to_dict(self) -> dict[str, Any]:
        return {"signals": [s.model_dump(mode="json") for s in self.signals.values()], "fresh_count": len(self.list_fresh())}

__all__ = ["SaudiMarketRadar", "RegulatorySignal", "SignalSource", "UNKNOWN"]
