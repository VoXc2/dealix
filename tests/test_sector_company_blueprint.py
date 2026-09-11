"""Contracts for the Saudi sector taxonomy + sector company blueprints (ONE Dealix)."""
from __future__ import annotations

import re

from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_company_blueprint import (
    MATURITY_LADDER,
    build_all_blueprints,
    build_blueprint,
    portfolio_index,
)
from dealix.commercial.sector_taxonomy import (
    ISIC_SECTIONS,
    coverage,
    taxonomy_for,
)

FAKE_ROI_RE = re.compile(
    r"will save \d+%|guaranteed \d+%|نضمن|ستوفر \d+٪|\d+٪\s*توفير|توفير مؤكد",
    re.IGNORECASE,
)


def test_every_sector_is_mapped_at_isic_section_level() -> None:
    report = coverage()
    assert report["sectors_with_isic_section"] == report["sectors_total"] == 20
    assert report["sectors_missing_isic_section"] == []
    assert report["isic_mapping_status"].startswith("ISIC_REV4_SECTION_LEVEL")


def test_known_isic_section_mappings_are_correct() -> None:
    assert taxonomy_for(Sector.CONSTRUCTION_EPC).isic_sections == ["F"]
    assert taxonomy_for(Sector.HEALTHCARE).isic_sections == ["Q"]
    assert taxonomy_for(Sector.FINANCE_FINTECH_INSURANCE).isic_sections == ["K"]
    assert taxonomy_for(Sector.LOGISTICS_SUPPLY_CHAIN).isic_sections == ["H"]
    assert taxonomy_for(Sector.EDUCATION_TRAINING).isic_sections == ["P"]
    assert taxonomy_for(Sector.TECHNOLOGY_SAAS_SI).isic_sections == ["J"]
    for reference in [taxonomy_for(sector) for sector in Sector]:
        assert set(reference.isic_sections) <= set(ISIC_SECTIONS)
        assert reference.validation_required is True
        assert reference.is_customer_fact is False


def test_blueprints_preserve_canonical_sector_ids_and_are_pattern_only() -> None:
    blueprints = build_all_blueprints()
    assert len(blueprints) == 20
    assert {blueprint.sector_id for blueprint in blueprints} == {sector.value for sector in Sector}
    for blueprint in blueprints:
        assert blueprint.truth_class == "PATTERN"
        assert blueprint.is_customer_fact is False
        assert blueprint.ar_name and blueprint.en_name
        assert 0 < blueprint.completeness_pct <= 100
        assert blueprint.regulator_validation_status == "REQUIRES_OFFICIAL_VERIFICATION"


def test_maturity_never_exceeds_governed_pack_level() -> None:
    for blueprint in build_all_blueprints():
        assert blueprint.maturity_status in MATURITY_LADDER
        assert MATURITY_LADDER.index(blueprint.maturity_status) <= MATURITY_LADDER.index("INTERNAL_READY")


def test_scores_are_unknown_not_invented() -> None:
    blueprint = build_blueprint(Sector.HEALTHCARE)
    assert blueprint.economic_score == "UNKNOWN"
    assert blueprint.market_score == "UNKNOWN"
    assert blueprint.delivery_readiness == "UNKNOWN"
    assert blueprint.proof_readiness == "UNKNOWN"
    assert blueprint.digital_maturity == "UNKNOWN"
    assert blueprint.ai_maturity == "UNKNOWN"


def test_buyer_and_problem_cells_are_deterministic_patterns() -> None:
    blueprint = build_blueprint(Sector.GOVERNMENT_B2G)
    assert blueprint.buyers
    assert any(cell.segment == "b2g" for cell in blueprint.buyers)
    assert blueprint.problem_cells
    for cell in blueprint.problem_cells:
        assert cell.truth_class == "PATTERN"
        assert cell.evidence_status == "UNKNOWN"
        assert cell.diagnostic_families


def test_blueprint_text_has_no_fake_roi() -> None:
    for blueprint in build_all_blueprints():
        payload = str(blueprint.to_dict())
        assert not FAKE_ROI_RE.search(payload), blueprint.sector_id


def test_portfolio_index_summarizes_without_inflating_status() -> None:
    index = portfolio_index()
    assert index["sectors_total"] == 20
    assert index["truth_class"] == "PATTERN"
    assert index["is_customer_fact"] is False
    assert index["avg_completeness_pct"] > 0
    assert sum(index["by_maturity"].values()) == 20
    assert "MARKET_TEST_READY" not in index["by_maturity"]
