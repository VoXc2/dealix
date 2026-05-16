"""Governed Revenue & AI Operations tier — service catalog tests.

Asserts the 3 higher-tier offerings meet the same constitutional gates as the
core 7, and that adding them did NOT disturb the canonical `OFFERINGS` count.

- Article 4: never includes 'live_send'/'live_charge' in action_modes_used.
- Article 8: KPI/refund language uses commitment phrasing, never
  "guaranteed"/"نضمن".
- Bilingual: every offering has distinct name_ar + name_en.

Sandbox-safe — pure module imports via the same isolated loader as
``test_service_catalog.py`` (avoids the api/* python-jose cascade).
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load_registry():
    """Load registry without importing api/* (sandbox-safe)."""
    repo_root = Path(__file__).resolve().parent.parent

    schemas_path = (
        repo_root / "auto_client_acquisition" / "service_catalog" / "schemas.py"
    )
    spec_s = importlib.util.spec_from_file_location(
        "_test_governed_tier_schemas", schemas_path
    )
    assert spec_s is not None and spec_s.loader is not None
    schemas_mod = importlib.util.module_from_spec(spec_s)
    sys.modules["_test_governed_tier_schemas"] = schemas_mod
    spec_s.loader.exec_module(schemas_mod)

    registry_path = (
        repo_root / "auto_client_acquisition" / "service_catalog" / "registry.py"
    )
    src = registry_path.read_text(encoding="utf-8")
    src = src.replace(
        "from auto_client_acquisition.service_catalog.schemas import ServiceOffering",
        "from _test_governed_tier_schemas import ServiceOffering",
    )
    ns: dict = {}
    exec(compile(src, str(registry_path), "exec"), ns)  # noqa: S102
    return ns


_NS = _load_registry()
OFFERINGS = _NS["OFFERINGS"]
GOVERNED_TIER_OFFERINGS = _NS["GOVERNED_TIER_OFFERINGS"]
ALL_OFFERINGS = _NS["ALL_OFFERINGS"]
get_offering = _NS["get_offering"]
list_governed_tier = _NS["list_governed_tier"]

_EXPECTED_IDS = {
    "governed_revenue_ops_diagnostic",
    "revenue_intelligence_sprint",
    "governed_ops_retainer",
}


def test_core_ladder_still_exactly_7():
    """Adding the governed tier must NOT disturb the canonical 7."""
    assert len(OFFERINGS) == 7, f"expected 7 core offerings, got {len(OFFERINGS)}"


def test_governed_tier_has_exactly_3_offerings():
    assert len(GOVERNED_TIER_OFFERINGS) == 3
    assert len(list_governed_tier()) == 3
    assert len(ALL_OFFERINGS) == 10


def test_governed_tier_ids_unique_and_expected():
    ids = [o.id for o in GOVERNED_TIER_OFFERINGS]
    assert len(ids) == len(set(ids)), "duplicate id in governed tier"
    assert set(ids) == _EXPECTED_IDS


def test_governed_tier_all_marked_governed_revenue():
    for o in GOVERNED_TIER_OFFERINGS:
        assert o.tier == "governed_revenue", f"{o.id} has wrong tier: {o.tier}"


def test_governed_tier_no_guaranteed_language():
    """Article 8: forbidden tokens 'guaranteed', 'guarantee', 'نضمن'."""
    forbidden = [
        re.compile(r"\bguaranteed?\b", re.IGNORECASE),
        re.compile(r"\bguarantee\b", re.IGNORECASE),
        re.compile(r"نضمن"),
    ]
    for o in GOVERNED_TIER_OFFERINGS:
        text = " ".join(
            [
                o.name_ar,
                o.name_en,
                o.kpi_commitment_ar,
                o.kpi_commitment_en,
                o.refund_policy_ar,
                o.refund_policy_en,
                *o.deliverables,
            ]
        )
        for pat in forbidden:
            m = pat.search(text)
            assert m is None, f"{o.id}: forbidden token '{m.group(0)}' present"


def test_governed_tier_no_live_action_modes():
    """Article 4: NO live_send / live_charge / auto_send / auto_charge."""
    forbidden = {"live_send", "live_charge", "auto_send", "auto_charge"}
    for o in GOVERNED_TIER_OFFERINGS:
        bad = set(o.action_modes_used) & forbidden
        assert not bad, f"{o.id} uses forbidden action_mode(s): {bad}"


def test_governed_tier_required_hard_gates():
    required = {"no_live_send", "no_live_charge", "no_fake_proof"}
    for o in GOVERNED_TIER_OFFERINGS:
        missing = required - set(o.hard_gates)
        assert not missing, f"{o.id} missing required hard_gates: {missing}"


def test_governed_tier_bilingual_names():
    for o in GOVERNED_TIER_OFFERINGS:
        assert o.name_ar.strip(), f"{o.id} missing Arabic name"
        assert o.name_en.strip(), f"{o.id} missing English name"
        assert o.name_ar != o.name_en, f"{o.id} ar==en (translation skipped)"


def test_governed_tier_one_time_prices_ascending():
    one_time = [o for o in GOVERNED_TIER_OFFERINGS if o.price_unit == "one_time"]
    prices = [o.price_sar for o in one_time]
    assert prices == sorted(prices), f"governed one-time prices not ascending: {prices}"


def test_governed_tier_price_ceiling_consistent():
    """When a range is quoted, the ceiling must be >= the floor."""
    for o in GOVERNED_TIER_OFFERINGS:
        if o.price_sar_max is not None:
            assert o.price_sar_max >= o.price_sar, (
                f"{o.id}: price_sar_max {o.price_sar_max} < price_sar {o.price_sar}"
            )


def test_governed_tier_is_estimate():
    """Article 8: every numeric is an estimate, not a promise."""
    for o in GOVERNED_TIER_OFFERINGS:
        assert o.is_estimate is True, f"{o.id} must mark numbers as estimates"


def test_get_offering_finds_governed_tier():
    for service_id in _EXPECTED_IDS:
        assert get_offering(service_id) is not None
    # core ids still resolve; unknown still None
    assert get_offering("free_mini_diagnostic") is not None
    assert get_offering("nonexistent_id") is None
