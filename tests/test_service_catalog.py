"""Service Catalog tests — Revenue Autopilot offer model.

Asserts the offering registry meets:
- Article 4: never includes 'live_send' or 'live_charge' in action_modes_used
- Article 8: KPI commitment language uses commitment phrasing, never "guaranteed"/"نضمن"
- Article 11: thin data registry (no business logic in tests)
- Pricing ladder: ascending for paid services
- Bilingual: every offering has both name_ar + name_en

Sandbox-safe — pure module imports, no api/security pyo3 cascade.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load_registry():
    """Load registry without importing api/* (avoids python-jose sandbox cascade)."""
    repo_root = Path(__file__).resolve().parent.parent

    # Pre-load schemas first (registry imports from it)
    schemas_path = repo_root / "auto_client_acquisition" / "service_catalog" / "schemas.py"
    spec_s = importlib.util.spec_from_file_location(
        "_test_service_catalog_schemas", schemas_path
    )
    assert spec_s is not None and spec_s.loader is not None
    schemas_mod = importlib.util.module_from_spec(spec_s)
    sys.modules["_test_service_catalog_schemas"] = schemas_mod
    spec_s.loader.exec_module(schemas_mod)

    # Now load registry, tricking it into using our pre-loaded schemas
    registry_path = repo_root / "auto_client_acquisition" / "service_catalog" / "registry.py"
    src = registry_path.read_text(encoding="utf-8")
    src = src.replace(
        "from auto_client_acquisition.service_catalog.schemas import ServiceOffering",
        "from _test_service_catalog_schemas import ServiceOffering",
    )
    ns: dict = {}
    exec(compile(src, str(registry_path), "exec"), ns)
    return ns, schemas_mod


_REGISTRY_NS, _SCHEMAS = _load_registry()
OFFERINGS = _REGISTRY_NS["OFFERINGS"]
SERVICE_IDS = _REGISTRY_NS["SERVICE_IDS"]
get_offering = _REGISTRY_NS["get_offering"]
list_offerings = _REGISTRY_NS["list_offerings"]


# ── Test 1 ────────────────────────────────────────────────────────────
def test_registry_has_exactly_5_offerings():
    """Article 11: catalog is the canonical 5 offerings (3 diagnostic tiers + 2 follow-ons)."""
    assert len(OFFERINGS) == 5, f"expected 5, got {len(OFFERINGS)}"
    assert len(SERVICE_IDS) == 5, "duplicate service_id in registry"


# ── Test 2 ────────────────────────────────────────────────────────────
def test_every_offering_has_complete_schema():
    """Every offering has all required fields populated (extra='forbid' ensures no rogue)."""
    required = {
        "id", "name_ar", "name_en", "price_sar", "price_unit", "duration_days",
        "deliverables", "kpi_commitment_ar", "kpi_commitment_en",
        "refund_policy_ar", "refund_policy_en", "action_modes_used",
        "hard_gates", "customer_journey_stage", "is_estimate",
    }
    for o in OFFERINGS:
        d = o.model_dump()
        missing = required - set(d.keys())
        assert not missing, f"offering {o.id} missing fields: {missing}"
        # Required strings non-empty
        for f in ["name_ar", "name_en", "kpi_commitment_ar", "kpi_commitment_en"]:
            assert d[f].strip(), f"{o.id}.{f} is empty"


# ── Test 3 ────────────────────────────────────────────────────────────
def test_bilingual_names_present():
    """Every offering must have Saudi-Arabic + English name (Article: Saudi-first)."""
    for o in OFFERINGS:
        assert o.name_ar.strip(), f"{o.id} missing Arabic name"
        assert o.name_en.strip(), f"{o.id} missing English name"
        assert o.name_ar != o.name_en, f"{o.id} ar==en (translation skipped)"


# ── Test 4 ────────────────────────────────────────────────────────────
def test_no_guaranteed_language_anywhere():
    """Article 8: forbidden tokens 'guaranteed', 'نضمن', 'ROI guaranteed'."""
    forbidden = [
        re.compile(r"\bguaranteed?\b", re.IGNORECASE),
        re.compile(r"\bguarantee\b", re.IGNORECASE),
        re.compile(r"نضمن"),
    ]
    for o in OFFERINGS:
        text_to_scan = " ".join([
            o.name_ar, o.name_en, o.kpi_commitment_ar, o.kpi_commitment_en,
            o.refund_policy_ar, o.refund_policy_en,
            *o.deliverables,
        ])
        for pat in forbidden:
            m = pat.search(text_to_scan)
            assert m is None, f"{o.id}: forbidden token '{m.group(0)}' present"


# ── Test 5 ────────────────────────────────────────────────────────────
def test_price_ladder_ascending_for_paid_one_time_services():
    """Diagnostic tiers: Starter (4,999) → Standard (9,999) → Executive (15,000)."""
    one_time_paid = [
        o for o in OFFERINGS if o.price_unit == "one_time" and o.price_sar > 0
    ]
    prices = [o.price_sar for o in one_time_paid]
    assert prices == sorted(prices), f"one-time prices not ascending: {prices}"
    starter = get_offering("diagnostic_starter_4999")
    standard = get_offering("diagnostic_standard_9999")
    executive = get_offering("diagnostic_executive_15000")
    assert starter is not None and standard is not None and executive is not None
    assert starter.price_sar < standard.price_sar < executive.price_sar


# ── Test 6 ────────────────────────────────────────────────────────────
def test_action_modes_never_include_live_send_or_live_charge():
    """Article 4: NO_LIVE_SEND + NO_LIVE_CHARGE immutable."""
    forbidden_action_modes = {"live_send", "live_charge", "auto_send", "auto_charge"}
    for o in OFFERINGS:
        modes = set(o.action_modes_used)
        bad = modes & forbidden_action_modes
        assert not bad, f"{o.id} uses forbidden action_mode(s): {bad}"


# ── Test 7 ────────────────────────────────────────────────────────────
def test_every_offering_lists_relevant_hard_gates():
    """Article 4: every offering must declare relevant hard gates explicitly."""
    required_gates = {
        "no_live_send",
        "no_live_charge",
        "no_fake_proof",
    }
    for o in OFFERINGS:
        declared = set(o.hard_gates)
        missing = required_gates - declared
        assert not missing, f"{o.id} missing required hard_gates: {missing}"


# ── Test 8 ────────────────────────────────────────────────────────────
def test_get_offering_lookup_works():
    """Helper function returns correct offering by id, None for unknown."""
    assert get_offering("diagnostic_starter_4999") is not None
    assert get_offering("revenue_intelligence_sprint") is not None
    assert get_offering("governed_ops_retainer") is not None
    assert get_offering("nonexistent_id") is None
    assert get_offering("") is None
    # SERVICE_IDS frozenset must match
    for o in OFFERINGS:
        assert o.id in SERVICE_IDS
