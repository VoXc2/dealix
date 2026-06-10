"""Saudi / Tier-1 targeting surface for Revenue OS (re-exports stable entrypoints)."""

from __future__ import annotations

from auto_client_acquisition.revenue_os.saudi_targeting_profile import (
    SaudiTargetingProfile,
    anti_waste_violations_for_tier1_intake,
    assert_tier1_storage_allowed,
    build_local_discover_body,
    map_tier1_to_intake_lead_source,
    merge_targeting_into_discover_body,
    parse_tier1_lead_source,
)

__all__ = [
    "SaudiTargetingProfile",
    "anti_waste_violations_for_tier1_intake",
    "assert_tier1_storage_allowed",
    "build_local_discover_body",
    "map_tier1_to_intake_lead_source",
    "merge_targeting_into_discover_body",
    "parse_tier1_lead_source",
]
