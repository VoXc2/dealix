"""Sector pack governance — maturity gates, Arabic-first coverage, pattern != customer fact."""

from __future__ import annotations

import pytest

from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_pack_governance import (
    PUBLICATION_GATES,
    STRUCTURAL_GATES,
    PatternNotCustomerFactError,
    QualityGate,
    SectorPackMaturity,
    SectorPackRegistry,
    build_pack,
    evaluate_gates,
    first_wave_sectors,
)


def test_all_canonical_sectors_have_internal_packs() -> None:
    registry = SectorPackRegistry()
    packs = registry.all()
    assert len(packs) == len(list(Sector))
    assert all(pack.maturity == SectorPackMaturity.INTERNAL_READY for pack in packs)
    assert all(not pack.structural_failures() for pack in packs)
    assert not any(pack.can_publish for pack in packs)


def test_arabic_is_first_class_for_every_sector() -> None:
    registry = SectorPackRegistry()
    for pack in registry.all():
        assert evaluate_gates(pack)[QualityGate.ARABIC] is True, pack.sector_id
        assert evaluate_gates(pack)[QualityGate.ENGLISH] is True, pack.sector_id
        assert pack.ar_name != pack.en_name, pack.sector_id


def test_publish_requires_publication_gates_and_all_quality_gates() -> None:
    registry = SectorPackRegistry()
    sector_id = Sector.TECHNOLOGY_SAAS_SI.value

    with pytest.raises(ValueError):
        registry.publish(sector_id, mobile_ready=False, rtl_ready=True, accessibility_checked=True)

    published = registry.publish(sector_id, mobile_ready=True, rtl_ready=True, accessibility_checked=True)
    assert published.maturity == SectorPackMaturity.PUBLIC_READY
    assert published.can_publish
    assert not published.gate_failures()
    assert len(PUBLICATION_GATES) == 3


def test_fake_roi_claim_blocks_publication() -> None:
    pack = build_pack(Sector.PROFESSIONAL_SERVICES)
    assert evaluate_gates(pack)[QualityGate.NO_FAKE_ROI] is True

    tainted = pack.model_copy(update={"pains": pack.pains + ["نضمن توفير 40% من التكاليف"]})
    assert evaluate_gates(tainted)[QualityGate.NO_FAKE_ROI] is False

    registry = SectorPackRegistry()
    registry._packs[tainted.sector_id] = tainted
    with pytest.raises(ValueError):
        registry.publish(
            tainted.sector_id,
            mobile_ready=True,
            rtl_ready=True,
            accessibility_checked=True,
        )


def test_missing_arabic_blocks_structural_readiness() -> None:
    pack = build_pack(Sector.HEALTHCARE).model_copy(update={"ar_name": "Healthcare Operations"})
    assert evaluate_gates(pack)[QualityGate.ARABIC] is False
    assert QualityGate.ARABIC in pack.structural_failures()


def test_pattern_knowledge_is_never_a_customer_fact() -> None:
    pack = build_pack(Sector.FINANCE_FINTECH_INSURANCE)
    assert pack.truth_class == "PATTERN"
    assert pack.is_customer_fact is False

    with pytest.raises(PatternNotCustomerFactError):
        pack.to_customer_context(evidence_ref="")

    context = pack.to_customer_context(evidence_ref="diag_evidence_123")
    assert context["truth_class"] == "PATTERN"
    assert context["is_customer_fact"] is False
    assert context["customer_evidence_ref"] == "diag_evidence_123"


def test_promotion_is_forward_only_and_gated() -> None:
    registry = SectorPackRegistry()
    sector_id = Sector.CONSTRUCTION_EPC.value

    with pytest.raises(ValueError):
        registry.promote(sector_id, SectorPackMaturity.RESEARCHED)

    validated = registry.promote(sector_id, SectorPackMaturity.VALIDATED)
    assert validated.maturity == SectorPackMaturity.VALIDATED

    with pytest.raises(ValueError):
        registry.promote(sector_id, SectorPackMaturity.PUBLIC_READY)

    with pytest.raises(ValueError):
        registry.promote(sector_id, SectorPackMaturity.VALIDATED)


def test_first_wave_covers_ten_governed_sectors() -> None:
    registry = SectorPackRegistry()
    wave = first_wave_sectors()
    assert len(wave) == 10
    for sector_id in wave:
        pack = registry.get(sector_id)
        assert pack.maturity == SectorPackMaturity.INTERNAL_READY
        assert pack.structural_failures() == []


def test_registry_summary_and_required_gates_are_singular() -> None:
    registry = SectorPackRegistry()
    summary = registry.summary()
    assert summary[SectorPackMaturity.INTERNAL_READY.value] == len(list(Sector))
    assert summary[SectorPackMaturity.PUBLIC_READY.value] == 0
    assert set(STRUCTURAL_GATES).isdisjoint(PUBLICATION_GATES)
    assert set(STRUCTURAL_GATES) | set(PUBLICATION_GATES) == set(QualityGate)
