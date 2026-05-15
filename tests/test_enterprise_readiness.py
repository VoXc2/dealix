"""Enterprise tier — readiness scorecard tests."""

from __future__ import annotations

from auto_client_acquisition.enterprise_os.enterprise_readiness import (
    ENTERPRISE_READINESS,
    ReadinessBand,
    ReadinessScores,
    compute_readiness_score,
    get_readiness,
    is_sellable,
    list_readiness,
    score_band,
)

_ALL_100 = ReadinessScores(100, 100, 100, 100, 100, 100, 100, 100)
_ALL_0 = ReadinessScores(0, 0, 0, 0, 0, 0, 0, 0)


def test_weights_sum_to_one() -> None:
    assert compute_readiness_score(_ALL_100) == 100.0
    assert compute_readiness_score(_ALL_0) == 0.0


def test_score_clamped_to_range() -> None:
    score = compute_readiness_score(ReadinessScores(80, 80, 80, 80, 80, 80, 80, 80))
    assert 0.0 <= score <= 100.0


def test_score_band_thresholds() -> None:
    assert score_band(69) == ReadinessBand.BLOCKED
    assert score_band(70) == ReadinessBand.BETA
    assert score_band(84) == ReadinessBand.BETA
    assert score_band(85) == ReadinessBand.SELLABLE
    assert score_band(89) == ReadinessBand.SELLABLE
    assert score_band(90) == ReadinessBand.PREMIUM
    assert score_band(94) == ReadinessBand.PREMIUM
    assert score_band(95) == ReadinessBand.ENTERPRISE_READY


def test_is_sellable_matches_band() -> None:
    assert not is_sellable(69)
    assert not is_sellable(84)
    assert is_sellable(85)
    assert is_sellable(95)


def test_every_enterprise_service_has_readiness() -> None:
    reports = list_readiness()
    assert len(reports) == len(ENTERPRISE_READINESS) == 5
    for sid in ENTERPRISE_READINESS:
        report = get_readiness(sid)
        assert report is not None
        assert report.service_id == sid
        assert report.band == score_band(report.total)


def test_enterprise_tier_starts_not_sellable() -> None:
    """Honest Planned status: nothing in the tier is sellable yet."""
    for report in list_readiness():
        assert not report.sellable, report.service_id
        assert report.band == ReadinessBand.BLOCKED, report.service_id


def test_get_readiness_unknown_returns_none() -> None:
    assert get_readiness("not_a_service") is None
