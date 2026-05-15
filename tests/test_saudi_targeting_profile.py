"""SaudiTargetingProfile + discover/local body merge."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_os.saudi_targeting_profile import (
    SaudiTargetingProfile,
    build_local_discover_body,
    merge_targeting_into_discover_body,
)


def test_build_local_discover_body_minimal() -> None:
    p = SaudiTargetingProfile(industry_key="dental_clinic", city_key="riyadh")
    body = build_local_discover_body(p)
    assert body["industry"] == "dental_clinic"
    assert body["city"] == "riyadh"
    assert body.get("custom_query") is None or isinstance(body.get("custom_query"), str)


def test_build_local_discover_body_with_keywords() -> None:
    p = SaudiTargetingProfile(
        industry_key="logistics",
        city_key="jeddah",
        signal_keywords=["B2B", "تخزين"],
    )
    body = build_local_discover_body(p)
    assert "custom_query" in body
    assert "جدة" in body["custom_query"] or "Jeddah" in body["custom_query"]


def test_merge_explicit_industry_wins_over_profile() -> None:
    body = merge_targeting_into_discover_body(
        {
            "industry": "dental_clinic",
            "city": "riyadh",
            "targeting_profile": {
                "industry_key": "logistics",
                "city_key": "jeddah",
            },
        }
    )
    assert body["industry"] == "dental_clinic"
    assert body["city"] == "riyadh"


def test_merge_targeting_profile_only_fills_discover_fields() -> None:
    out = merge_targeting_into_discover_body(
        {"targeting_profile": {"industry_key": "dental_clinic", "city_key": "riyadh"}}
    )
    assert out["industry"] == "dental_clinic"
    assert out["city"] == "riyadh"
    assert "targeting_profile" not in out


def test_merge_raises_on_non_object_targeting_profile() -> None:
    with pytest.raises(ValueError, match="targeting_profile_must_be_object"):
        merge_targeting_into_discover_body({"targeting_profile": "bad"})
