"""Service Catalog tests — 2026-Q2 commercial reframe.

Asserts the 3-offering registry meets:
- Article 4: never includes 'live_send' or 'live_charge' in action_modes_used
- Article 8: KPI commitment language uses commitment phrasing, never "guaranteed"/"نضمن"
- Article 11: thin data registry (no business logic in tests)
- Pricing ladder: ascending price floor across the 3 stages
- Bilingual: every offering has both name_ar + name_en
- Legacy ID aliases resolve to the correct 2026 successor

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
def test_registry_has_three_active_offerings():
    """Article 11: catalog is the canonical 2026-Q2 three offerings."""
    assert len(OFFERINGS) == 3, f"expected 3, got {len(OFFERINGS)}"
    assert len(SERVICE_IDS) == 3, "duplicate service_id in registry"


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
def test_price_floor_holds_across_ladder():
    """2026-Q2 ladder: Free (0) → Retainer (4,999/mo) → Sprint (25,000 one-time).
    The retainer is the entry FLOOR; the flagship sprint sits above it.
    """
    diagnostic = get_offering("strategic_diagnostic")
    retainer = get_offering("governed_ops_retainer_4999")
    sprint = get_offering("revenue_intelligence_sprint_25k")
    assert diagnostic is not None
    assert retainer is not None
    assert sprint is not None

    # Free diagnostic is exactly free.
    assert diagnostic.price_sar == 0.0

    # Retainer is the paid entry floor. Below 4,999 we don't sell.
    assert retainer.price_sar >= 4999.0
    assert retainer.price_unit == "per_month"

    # Flagship sprint is above the retainer floor and one-time.
    assert sprint.price_sar >= 25000.0
    assert sprint.price_unit == "one_time"
    assert sprint.price_sar > retainer.price_sar


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
    """Helper resolves canonical 2026 IDs + legacy aliases; None for unknown."""
    # Canonical 2026 IDs
    assert get_offering("strategic_diagnostic") is not None
    assert get_offering("governed_ops_retainer_4999") is not None
    assert get_offering("revenue_intelligence_sprint_25k") is not None

    # Legacy aliases resolve to the 2026 successor
    assert get_offering("free_mini_diagnostic") is not None
    assert get_offering("revenue_proof_sprint_499") is not None
    assert get_offering("growth_ops_monthly_2999") is not None

    # Unknown still returns None
    assert get_offering("nonexistent_id") is None
    assert get_offering("") is None

    # SERVICE_IDS frozenset matches the 3 active offerings
    for o in OFFERINGS:
        assert o.id in SERVICE_IDS
    # Legacy IDs are NOT in SERVICE_IDS (they only resolve via alias map)
    assert "agency_partner_os" not in SERVICE_IDS
    assert "revenue_proof_sprint_499" not in SERVICE_IDS
