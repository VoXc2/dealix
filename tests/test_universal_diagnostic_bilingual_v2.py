"""Contracts for the bilingual universal free diagnostic (D0-D2 genuinely free).

Sector packs are pattern knowledge. Every number is either UNKNOWN or labelled
ESTIMATED with an explicit basis. Nothing here invents ROI, urgency, or facts.
"""
from __future__ import annotations

import re

from dealix.commercial.low_touch_products.diagnostic_product import (
    QUOTE_REQUIRED,
    DiagnosticProductEngine,
)
from dealix.commercial.sector_pack_governance import (
    SectorPackMaturity,
    SectorPackRegistry,
    first_wave_sectors,
)
from dealix.commercial.universal_diagnostic_factory import (
    FAMILIES,
    FAMILY_AR,
    FREE_DEPTHS,
    SECTOR_SURFACES,
    TRUTH_CLASS_ESTIMATED,
    TRUTH_CLASS_UNKNOWN,
    DiagnosticDepth,
    UniversalDiagnosticFactory,
)

ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
FAKE_ROI_RE = re.compile(
    r"will save \d+%|guaranteed \d+%|نضمن|ستوفر \d+٪|\d+٪\s*توفير|توفير مؤكد",
    re.IGNORECASE,
)

REQUESTED_SURFACES = {
    "logistics",
    "ports_marine",
    "construction",
    "real_estate",
    "retail",
    "ecommerce",
    "hospitality",
    "restaurants",
    "healthcare_operations",
    "clinics",
    "manufacturing",
    "industrial",
    "automotive",
    "education",
    "hr_recruitment",
    "professional_services",
    "accounting",
    "finance_operations",
    "legal_operations",
    "insurance_operations",
    "facilities",
    "maintenance",
    "field_services",
    "procurement",
    "warehousing",
    "distribution",
    "customer_service",
    "marketing",
    "technology_saas",
    "sme",
    "enterprise_operations",
}

CANONICAL_SECTORS = {
    "government_b2g",
    "construction_epc",
    "industrial_manufacturing",
    "logistics_supply_chain",
    "energy_utilities_oil_gas",
    "mining_metals",
    "real_estate_proptech",
    "healthcare",
    "finance_fintech_insurance",
    "retail_commerce_ecommerce",
    "tourism_hospitality",
    "professional_services",
    "technology_saas_si",
    "telecom_media_marketing",
    "education_training",
    "agriculture_food_water",
    "mobility_automotive",
    "export_import_rhq",
    "creative_sports_gaming",
    "associations_nonprofits",
}


def test_required_commercial_surfaces_are_covered() -> None:
    surface_ids = {surface.surface_id for surface in SECTOR_SURFACES}
    assert surface_ids >= REQUESTED_SURFACES, sorted(REQUESTED_SURFACES - surface_ids)


def test_every_surface_maps_to_a_canonical_sector_or_size_tier() -> None:
    for surface in SECTOR_SURFACES:
        assert surface.ar_name and ARABIC_RE.search(surface.ar_name)
        assert surface.en_name and surface.en_name.isascii()
        if surface.canonical_sector == "*":
            assert surface.company_size_hint in {"sme", "enterprise"}
        else:
            assert surface.canonical_sector in CANONICAL_SECTORS
        assert surface.primary_families
        assert set(surface.primary_families) <= set(FAMILY_AR)


def test_surface_alias_composes_canonical_sector_and_primary_families() -> None:
    factory = UniversalDiagnosticFactory()
    surface, families = factory.compose_for_surface(
        "clinics", buyer_role="coo", problem="support_backlog"
    )
    assert surface is not None
    assert surface.canonical_sector == "healthcare"
    ids = {family.family_id for family in families}
    assert ids & set(surface.primary_families)
    assert families and all(family.family_id in factory.families for family in families)


def test_size_only_surfaces_use_their_size_hint() -> None:
    factory = UniversalDiagnosticFactory()
    for surface_id, size in (("sme", "sme"), ("enterprise_operations", "enterprise")):
        surface, fams = factory.compose_for_surface(surface_id)
        assert surface is not None and surface.company_size_hint == size
        assert fams


def test_every_canonical_sector_has_a_dedicated_surface() -> None:
    from dealix.commercial.universal_diagnostic_factory import SECTOR_SURFACES

    factory = UniversalDiagnosticFactory()
    covered = factory.surface_coverage()
    missing = [sector for sector in CANONICAL_SECTORS if sector not in covered]
    assert not missing, missing
    by_sector: dict[str, list] = {}
    for surface in SECTOR_SURFACES:
        by_sector.setdefault(surface.canonical_sector, []).append(surface)
    for sector in sorted(CANONICAL_SECTORS):
        composed = False
        for surface in by_sector[sector]:
            _, families = factory.compose_for_surface(
                surface.surface_id,
                buyer_role="coo",
                depth=DiagnosticDepth.D2_FUNCTIONAL,
            )
            assert families, surface.surface_id
            if {family.family_id for family in families} & set(
                surface.primary_families
            ):
                composed = True
        assert composed, sector


def _family_has_arabic(family_id: str) -> bool:
    name = FAMILY_AR.get(family_id, "")
    return bool(name) and bool(ARABIC_RE.search(name))


def test_arabic_first_questions_have_english_parity() -> None:
    factory = UniversalDiagnosticFactory()
    for family in FAMILIES:
        assert _family_has_arabic(family.family_id), family.family_id
        for locale in ("ar", "en"):
            questions = factory.generate_questions(family, locale=locale)
            assert len(questions) == 2
            for question in questions:
                assert question["text_ar"] and question["text_en"]
                if locale == "ar":
                    assert ARABIC_RE.search(question["question_text"])
                else:
                    assert question["question_text"].isascii()
                assert question["truth_class"] in {"PATTERN", "ESTIMATED"}


def test_no_invented_estimates_without_caller_basis() -> None:
    factory = UniversalDiagnosticFactory()
    leakage = factory.economic_leakage(
        [{"finding": "manual handoff delays", "evidence": "interview"}]
    )
    assert leakage
    item = leakage[0]
    assert item["truth_class"] == TRUTH_CLASS_UNKNOWN
    assert item["annual_frequency"] == "UNKNOWN"
    assert item["time_per_event"] == "UNKNOWN"
    assert item["is_measured_fact"] is False


def test_estimate_label_requires_basis() -> None:
    factory = UniversalDiagnosticFactory()
    labelled = factory.economic_leakage(
        [
            {
                "finding": "manual handoff delays",
                "evidence": "system_export",
                "annual_frequency": 12,
                "time_per_event": "2h",
                "estimate_basis": "system_export_jira",
                "annual_hours": 24,
            }
        ]
    )
    item = labelled[0]
    assert item["truth_class"] == TRUTH_CLASS_ESTIMATED
    assert "تقدير" in item["estimate_label_ar"]
    assert "ESTIMATED" in item["estimate_label_en"]
    assert item["is_measured_fact"] is False


def test_value_estimate_never_invents_without_cost_basis() -> None:
    factory = UniversalDiagnosticFactory()
    labelled = factory.economic_leakage(
        [
            {
                "finding": "manual handoff delays",
                "evidence": "system_export",
                "annual_frequency": 12,
                "time_per_event": "2h",
                "estimate_basis": "system_export_jira",
                "annual_hours": 24,
            }
        ]
    )
    unknown = factory.value_estimate(labelled)
    assert unknown["truth_class"] == TRUTH_CLASS_UNKNOWN
    assert unknown["value_range_sar"] == "UNKNOWN"

    estimated = factory.value_estimate(labelled, hourly_cost_sar=100)
    assert estimated["truth_class"] == TRUTH_CLASS_ESTIMATED
    low = estimated["value_range_sar"]["low"]
    high = estimated["value_range_sar"]["high"]
    assert 0 < low < high
    assert estimated["is_measured_fact"] is False


def test_all_diagnostic_depths_are_free() -> None:
    factory = UniversalDiagnosticFactory()
    assert FREE_DEPTHS == frozenset(DiagnosticDepth)
    for depth in DiagnosticDepth:
        assert factory.is_free(depth)
        assert depth in FREE_DEPTHS

def test_generated_diagnostic_text_has_no_fake_roi() -> None:
    factory = UniversalDiagnosticFactory()
    texts = [surface.ar_name for surface in SECTOR_SURFACES]
    texts += [surface.en_name for surface in SECTOR_SURFACES]
    for family in FAMILIES:
        texts.append(family.name)
        texts.extend(
            question["text_ar"] + " " + question["text_en"]
            for question in factory.generate_questions(family, locale="ar")
        )
    assert not [text for text in texts if FAKE_ROI_RE.search(text)]


def test_first_wave_sector_packs_are_internal_ready() -> None:
    registry = SectorPackRegistry()
    for sector_id in first_wave_sectors():
        pack = registry.get(sector_id)
        assert pack.maturity == SectorPackMaturity.INTERNAL_READY, sector_id
        assert not pack.structural_failures(), (sector_id, pack.structural_failures())
        assert pack.can_publish is False
    assert len(first_wave_sectors()) >= 10
