from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_commercial_factory import (
    CANONICAL_OFFERS,
    FREE,
    SectorCommercialFactory,
)


def test_all_canonical_sectors_have_exactly_one_commercial_pack() -> None:
    factory = SectorCommercialFactory()
    packs = factory.build_all()

    assert len(packs) == len(Sector) == 20
    assert {pack.sector_id for pack in packs} == {sector.value for sector in Sector}
    assert len({pack.sector_id for pack in packs}) == 20


def test_sector_packs_are_bilingual_free_and_use_canonical_offers() -> None:
    packs = SectorCommercialFactory().build_all()

    for pack in packs:
        assert pack.arabic_name.strip()
        assert pack.english_name.strip()
        assert pack.diagnostic_price == FREE
        assert pack.offer_matches
        assert set(pack.offer_matches) <= CANONICAL_OFFERS
        assert pack.diagnostic_modules[0] == "UNIVERSAL_CORE"
        assert pack.official_sources


def test_public_market_signals_never_become_commercial_truth() -> None:
    packs = SectorCommercialFactory().build_all()
    signals = [signal for pack in packs for signal in pack.current_signals]

    assert signals
    for signal in signals:
        assert signal.truth_class == "OBSERVED"
        assert signal.counts_as_relationship is False
        assert signal.counts_as_consent is False
        assert signal.counts_as_pipeline is False
        assert signal.counts_as_revenue is False


def test_coverage_receipt_fails_closed_semantically() -> None:
    receipt = SectorCommercialFactory().coverage_receipt()

    assert receipt == {
        "canonical_sectors": 20,
        "sectors_covered": 20,
        "coverage_percent": 100,
        "all_diagnostics_free": True,
        "duplicates": 0,
        "canonical_offers_only": True,
        "research_never_pipeline": True,
    }
