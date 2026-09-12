"""Sector Pack Governance — maturity ladder + publish gates for sector knowledge.

Sector packs are PATTERN knowledge: sector-level hypotheses that help ask better
diagnostic questions. They are never customer facts, never proof, never revenue.

COMMON_PATTERN != CUSTOMER_FACT.
Only packs that reach PUBLIC_READY (or later) with every quality gate passing may
be published. Everything else stays internal.
"""

from __future__ import annotations

import re
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_company_factory import SECTOR_INTEL

UNKNOWN = "UNKNOWN"

_ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
_FAKE_ROI_RE = re.compile(
    r"will save \d+%|guaranteed \d+%|نضمن|ستوفر \d+٪|\d+٪\s*توفير|توفير مؤكد",
    re.IGNORECASE,
)


class SectorPackMaturity(StrEnum):
    DRAFT = "draft"
    RESEARCHED = "researched"
    INTERNAL_READY = "internal_ready"
    VALIDATED = "validated"
    PUBLIC_READY = "public_ready"
    COMMERCIAL_SIGNAL = "commercial_signal"
    DELIVERY_PROVEN = "delivery_proven"


MATURITY_ORDER: tuple[SectorPackMaturity, ...] = (
    SectorPackMaturity.DRAFT,
    SectorPackMaturity.RESEARCHED,
    SectorPackMaturity.INTERNAL_READY,
    SectorPackMaturity.VALIDATED,
    SectorPackMaturity.PUBLIC_READY,
    SectorPackMaturity.COMMERCIAL_SIGNAL,
    SectorPackMaturity.DELIVERY_PROVEN,
)

PUBLISHABLE_MATURITY: frozenset[SectorPackMaturity] = frozenset(
    {
        SectorPackMaturity.PUBLIC_READY,
        SectorPackMaturity.COMMERCIAL_SIGNAL,
        SectorPackMaturity.DELIVERY_PROVEN,
    }
)


class QualityGate(StrEnum):
    SCHEMA = "schema"
    TRUTH = "truth"
    ARABIC = "arabic"
    ENGLISH = "english"
    SECTOR_RELEVANCE = "sector_relevance"
    USEFULNESS = "usefulness"
    SECURITY = "security"
    PRIVACY = "privacy"
    COST = "cost"
    MOBILE = "mobile"
    RTL = "rtl"
    ACCESSIBILITY = "accessibility"
    NO_FAKE_ROI = "no_fake_roi"


REQUIRED_GATES: tuple[QualityGate, ...] = tuple(QualityGate)

# Gates a pack must pass to be usable internally.
STRUCTURAL_GATES: tuple[QualityGate, ...] = (
    QualityGate.SCHEMA,
    QualityGate.TRUTH,
    QualityGate.ARABIC,
    QualityGate.ENGLISH,
    QualityGate.SECTOR_RELEVANCE,
    QualityGate.USEFULNESS,
    QualityGate.SECURITY,
    QualityGate.PRIVACY,
    QualityGate.COST,
    QualityGate.NO_FAKE_ROI,
)

# Extra gates required before anything may be published publicly.
PUBLICATION_GATES: tuple[QualityGate, ...] = (
    QualityGate.MOBILE,
    QualityGate.RTL,
    QualityGate.ACCESSIBILITY,
)


class PatternNotCustomerFactError(ValueError):
    """Raised when sector pattern knowledge is used as a customer fact."""


class SectorPack(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sector_id: str
    sector: Sector | None = None
    ar_name: str = UNKNOWN
    en_name: str = UNKNOWN
    workflows: list[str] = Field(default_factory=list)
    pains: list[str] = Field(default_factory=list)
    systems: list[str] = Field(default_factory=list)
    kpis: list[str] = Field(default_factory=list)
    automation_areas: list[str] = Field(default_factory=list)
    ai_areas: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    proof_requirements: list[str] = Field(default_factory=list)
    question_modules: list[str] = Field(default_factory=list)
    delivery_templates: list[str] = Field(default_factory=list)
    maturity: SectorPackMaturity = SectorPackMaturity.DRAFT
    cost_class: str = "low"
    mobile_ready: bool = False
    rtl_ready: bool = False
    accessibility_checked: bool = False
    truth_class: str = "PATTERN"
    is_customer_fact: bool = False

    def text_fields(self) -> list[str]:
        values: list[str] = [self.ar_name, self.en_name, self.sector_id]
        for items in (
            self.workflows,
            self.pains,
            self.systems,
            self.kpis,
            self.automation_areas,
            self.ai_areas,
            self.risks,
            self.proof_requirements,
            self.question_modules,
            self.delivery_templates,
        ):
            values.extend(items)
        return values

    def structural_failures(self) -> list[QualityGate]:
        gates = evaluate_gates(self)
        return [gate for gate in STRUCTURAL_GATES if not gates[gate]]

    def gate_failures(self) -> list[QualityGate]:
        return [gate for gate, ok in evaluate_gates(self).items() if not ok]

    @property
    def can_publish(self) -> bool:
        return self.maturity in PUBLISHABLE_MATURITY and not self.gate_failures()

    def to_customer_context(self, *, evidence_ref: str) -> dict[str, Any]:
        if not evidence_ref:
            raise PatternNotCustomerFactError(
                "Sector pack is pattern knowledge; customer-specific context requires an evidence_ref"
            )
        return {
            "sector_id": self.sector_id,
            "ar_name": self.ar_name,
            "en_name": self.en_name,
            "question_modules": list(self.question_modules),
            "delivery_templates": list(self.delivery_templates),
            "truth_class": "PATTERN",
            "is_customer_fact": False,
            "customer_evidence_ref": evidence_ref,
        }


def _has_arabic(value: str) -> bool:
    return bool(value) and value != UNKNOWN and bool(_ARABIC_RE.search(value))


def _looks_like_pii(value: str) -> bool:
    return bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+|\+?\d{9,}", value or ""))


def evaluate_gates(pack: SectorPack) -> dict[QualityGate, bool]:
    texts = pack.text_fields()
    schema_pass = bool(pack.sector_id) and all(
        field.strip() for field in (pack.ar_name, pack.en_name)
    )
    truth_pass = pack.truth_class == "PATTERN" and pack.is_customer_fact is False
    arabic_pass = _has_arabic(pack.ar_name)
    english_pass = bool(pack.en_name) and pack.en_name != UNKNOWN and pack.en_name.isascii()
    relevance_pass = bool(pack.workflows) and bool(pack.pains)
    usefulness_pass = bool(pack.question_modules) and bool(pack.delivery_templates) and bool(pack.automation_areas)
    privacy_pass = not any(_looks_like_pii(text) for text in texts)
    return {
        QualityGate.SCHEMA: schema_pass,
        QualityGate.TRUTH: truth_pass,
        QualityGate.ARABIC: arabic_pass,
        QualityGate.ENGLISH: english_pass,
        QualityGate.SECTOR_RELEVANCE: relevance_pass,
        QualityGate.USEFULNESS: usefulness_pass,
        QualityGate.SECURITY: True,
        QualityGate.PRIVACY: privacy_pass,
        QualityGate.COST: pack.cost_class in {"low", "medium", "high"},
        QualityGate.MOBILE: pack.mobile_ready,
        QualityGate.RTL: pack.rtl_ready,
        QualityGate.ACCESSIBILITY: pack.accessibility_checked,
        QualityGate.NO_FAKE_ROI: not any(_FAKE_ROI_RE.search(text) for text in texts),
    }


def build_pack(sector: Sector) -> SectorPack:
    intel = SECTOR_INTEL.get(sector, {})
    problems = list(intel.get("problems", []))
    workflows = list(intel.get("workflows", []))
    offers = list(intel.get("offers", []))
    pack = SectorPack(
        sector_id=sector.value,
        sector=sector,
        ar_name=str(intel.get("ar", UNKNOWN)),
        en_name=str(intel.get("en", UNKNOWN)),
        workflows=workflows,
        pains=problems,
        systems=[],
        kpis=[],
        automation_areas=[f"automate::{workflow}" for workflow in workflows],
        ai_areas=[f"ai::{problem}" for problem in problems[:3]],
        risks=list(intel.get("compliance", [])),
        proof_requirements=[f"proof::{workflow}" for workflow in workflows],
        question_modules=[f"q::{problem}" for problem in problems],
        delivery_templates=[f"template::{offer}" for offer in offers],
        cost_class="low",
        mobile_ready=False,
        rtl_ready=False,
        accessibility_checked=False,
    )
    if not pack.structural_failures():
        pack.maturity = SectorPackMaturity.INTERNAL_READY
    return pack


class SectorPackRegistry:
    """One governed registry over the canonical sector intelligence."""

    def __init__(self) -> None:
        self._packs: dict[str, SectorPack] = {
            sector.value: build_pack(sector) for sector in Sector
        }

    def get(self, sector_id: str) -> SectorPack:
        return self._packs[sector_id]

    def all(self) -> list[SectorPack]:
        return list(self._packs.values())

    def by_maturity(self, maturity: SectorPackMaturity) -> list[SectorPack]:
        return [pack for pack in self._packs.values() if pack.maturity == maturity]

    def promote(self, sector_id: str, target: SectorPackMaturity) -> SectorPack:
        pack = self._packs[sector_id]
        if MATURITY_ORDER.index(target) <= MATURITY_ORDER.index(pack.maturity):
            raise ValueError(f"promotion must move forward: {pack.maturity} -> {target}")
        failures = pack.gate_failures() if target in PUBLISHABLE_MATURITY else pack.structural_failures()
        if failures:
            raise ValueError(f"cannot promote {sector_id} to {target}: failing gates {failures}")
        promoted = pack.model_copy(update={"maturity": target})
        self._packs[sector_id] = promoted
        return promoted

    def publish(self, sector_id: str, *, mobile_ready: bool, rtl_ready: bool, accessibility_checked: bool) -> SectorPack:
        pack = self._packs[sector_id].model_copy(
            update={
                "mobile_ready": mobile_ready,
                "rtl_ready": rtl_ready,
                "accessibility_checked": accessibility_checked,
            }
        )
        if pack.gate_failures():
            raise ValueError(f"cannot publish {sector_id}: failing gates {pack.gate_failures()}")
        promoted = pack.model_copy(update={"maturity": SectorPackMaturity.PUBLIC_READY})
        self._packs[sector_id] = promoted
        return promoted

    def summary(self) -> dict[str, int]:
        summary = {maturity.value: 0 for maturity in MATURITY_ORDER}
        for pack in self._packs.values():
            summary[pack.maturity.value] += 1
        return summary


def first_wave_sectors() -> list[str]:
    """Highest-value Saudi-first sectors for the first governed wave."""
    return [
        Sector.TECHNOLOGY_SAAS_SI.value,
        Sector.PROFESSIONAL_SERVICES.value,
        Sector.FINANCE_FINTECH_INSURANCE.value,
        Sector.HEALTHCARE.value,
        Sector.CONSTRUCTION_EPC.value,
        Sector.LOGISTICS_SUPPLY_CHAIN.value,
        Sector.REAL_ESTATE_PROPTECH.value,
        Sector.RETAIL_COMMERCE_ECOMMERCE.value,
        Sector.EDUCATION_TRAINING.value,
        Sector.GOVERNMENT_B2G.value,
    ]


__all__ = [
    "SectorPackMaturity",
    "MATURITY_ORDER",
    "PUBLISHABLE_MATURITY",
    "QualityGate",
    "REQUIRED_GATES",
    "STRUCTURAL_GATES",
    "PUBLICATION_GATES",
    "PatternNotCustomerFactError",
    "SectorPack",
    "evaluate_gates",
    "build_pack",
    "SectorPackRegistry",
    "first_wave_sectors",
]
