"""Service catalog safety/compatibility tests.

The internal registry still carries historical/future catalogue entries for
planning compatibility, but current launch authority is separately enforced by
the commercial-runtime truth surface. These tests validate catalog safety
without treating policy/negation tokens in source code as positive marketing
claims.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load_registry():
    repo_root = Path(__file__).resolve().parent.parent
    schemas_path = repo_root / "auto_client_acquisition" / "service_catalog" / "schemas.py"
    spec_s = importlib.util.spec_from_file_location("_test_service_catalog_schemas", schemas_path)
    assert spec_s is not None and spec_s.loader is not None
    schemas_mod = importlib.util.module_from_spec(spec_s)
    sys.modules["_test_service_catalog_schemas"] = schemas_mod
    spec_s.loader.exec_module(schemas_mod)

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


def test_registry_has_exactly_17_offerings():
    assert len(OFFERINGS) == 17
    assert len(SERVICE_IDS) == 17
    tx = [o for o in OFFERINGS if o.customer_journey_stage == "transformation"]
    assert len(tx) == 10


def test_every_offering_has_complete_schema():
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
        for f in ["name_ar", "name_en", "kpi_commitment_ar", "kpi_commitment_en"]:
            assert d[f].strip(), f"{o.id}.{f} is empty"


def test_bilingual_names_present():
    for o in OFFERINGS:
        assert o.name_ar.strip()
        assert o.name_en.strip()
        assert o.name_ar != o.name_en


def test_no_positive_guarantee_language_in_customer_facing_catalog_fields():
    forbidden = [
        re.compile(r"\bguaranteed?\b", re.IGNORECASE),
        re.compile(r"\bguarantee\b", re.IGNORECASE),
        re.compile(r"نضمن"),
    ]
    for o in OFFERINGS:
        text_to_scan = " ".join([
            o.name_ar,
            o.name_en,
            o.kpi_commitment_ar,
            o.kpi_commitment_en,
            o.refund_policy_ar,
            o.refund_policy_en,
            *o.deliverables,
        ])
        for pat in forbidden:
            m = pat.search(text_to_scan)
            assert m is None, f"{o.id}: forbidden positive claim '{m.group(0)}'"

    repo_root = Path(__file__).resolve().parent.parent
    # Scan rendered/static customer-facing snapshots only. Source code is
    # allowed to contain prohibition tokens such as outcome_guarantee=None.
    for relative_path in (
        "apps/web/lib/service-catalog-snapshot.ts",
        "landing/assets/data/services-catalog.json",
    ):
        snapshot = (repo_root / relative_path).read_text(encoding="utf-8")
        for pat in forbidden:
            m = pat.search(snapshot)
            assert m is None, f"{relative_path}: forbidden positive claim '{m.group(0)}'"


def test_first_paid_motion_is_30_day_quote_only_pilot():
    pilot = get_offering("revenue_command_pilot_30d")
    assert pilot is not None
    assert pilot.name_en == "Revenue Command Pilot — 30 days"
    assert pilot.duration_days == 30
    assert pilot.price_sar == 0
    assert pilot.price_unit == "custom"
    assert pilot.commercial_status == "quote_only"
    assert get_offering("revenue_proof_sprint_499") is None


def test_action_modes_never_include_live_send_or_live_charge():
    forbidden_action_modes = {"live_send", "live_charge", "auto_send", "auto_charge"}
    for o in OFFERINGS:
        bad = set(o.action_modes_used) & forbidden_action_modes
        assert not bad, f"{o.id} uses forbidden action_mode(s): {bad}"


def test_every_offering_lists_relevant_hard_gates():
    required_gates = {"no_live_send", "no_live_charge", "no_fake_proof"}
    for o in OFFERINGS:
        missing = required_gates - set(o.hard_gates)
        assert not missing, f"{o.id} missing required hard_gates: {missing}"


def test_get_offering_lookup_works():
    assert get_offering("revenue_command_pilot_30d") is not None
    assert get_offering("free_mini_diagnostic") is not None
    assert get_offering("agency_partner_os") is not None
    assert get_offering("nonexistent_id") is None
    assert get_offering("") is None
    for o in OFFERINGS:
        assert o.id in SERVICE_IDS


def test_no_open_ended_outcome_or_free_work_promises():
    forbidden = [
        re.compile(r"work for free", re.IGNORECASE),
        re.compile(r"work until we do", re.IGNORECASE),
        re.compile(r"free months?", re.IGNORECASE),
        re.compile(r"نشتغل بدون مقابل"),
        re.compile(r"نواصل العمل حتى"),
        re.compile(r"اشتراكان مجانيان"),
        re.compile(r"شهر مجاني"),
        re.compile(r"\+20% reply-rate", re.IGNORECASE),
        re.compile(r"40%\+ of decision time", re.IGNORECASE),
        re.compile(r"\+٢٠٪"),
        re.compile(r"٤٠٪\+"),
    ]
    catalog_text = "\n".join(
        " ".join(
            (
                offering.kpi_commitment_ar,
                offering.kpi_commitment_en,
                offering.refund_policy_ar,
                offering.refund_policy_en,
            )
        )
        for offering in OFFERINGS
    )
    repo_root = Path(__file__).resolve().parent.parent
    public_snapshots = "\n".join(
        (repo_root / path).read_text(encoding="utf-8")
        for path in (
            "apps/web/lib/service-catalog-snapshot.ts",
            "landing/assets/data/services-catalog.json",
        )
    )
    for pattern in forbidden:
        assert pattern.search(catalog_text) is None, pattern.pattern
        assert pattern.search(public_snapshots) is None, pattern.pattern


def test_pilot_brief_source_explicitly_blocks_commitment_authority():
    source = Path("scripts/dealix_pilot_brief.py").read_text(encoding="utf-8")
    assert '"outcome_guarantee": None' in source
    assert '"external_send_allowed": False' in source
    assert '"execution_allowed": False' in source
    assert '"approval_required_for_commitment": True' in source
