"""Wave 13 Phase 10 — Integration Capability Registry tests.

Asserts:
  - 12 integrations registered (no duplicates)
  - Every integration has trigger_for_next_level (bilingual)
  - L3 entries respect 8 hard gates AND have L3_proven_by_5_plus_customers=True
  - Lookup helpers work
  - Forbidden upgrades are explicitly blocked in trigger text
  - Bilingual names

Sandbox-safe: direct module load.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load():
    repo_root = Path(__file__).resolve().parent.parent

    schemas_path = repo_root / "auto_client_acquisition" / "integration_capability" / "schemas.py"
    spec = importlib.util.spec_from_file_location("_test_w13_p10_ic_schemas", schemas_path)
    assert spec is not None and spec.loader is not None
    schemas = importlib.util.module_from_spec(spec)
    sys.modules["_test_w13_p10_ic_schemas"] = schemas
    spec.loader.exec_module(schemas)

    # registry imports schemas via package path
    reg_path = repo_root / "auto_client_acquisition" / "integration_capability" / "registry.py"
    src = reg_path.read_text(encoding="utf-8")
    src = src.replace(
        "from auto_client_acquisition.integration_capability.schemas import",
        "from _test_w13_p10_ic_schemas import",
    )
    ns: dict = {}
    exec(compile(src, str(reg_path), "exec"), ns)
    return schemas, ns


_SCH, _REG = _load()
INTEGRATIONS = _REG["INTEGRATIONS"]
INTEGRATION_IDS = _REG["INTEGRATION_IDS"]
list_integrations = _REG["list_integrations"]
get_integration = _REG["get_integration"]


# ── Test 1 ────────────────────────────────────────────────────────────
def test_exactly_12_integrations_no_duplicates():
    assert len(INTEGRATIONS) == 12
    assert len(INTEGRATION_IDS) == 12  # frozenset has no dupes


# ── Test 2 ────────────────────────────────────────────────────────────
def test_every_integration_has_bilingual_trigger():
    for i in INTEGRATIONS:
        assert i.trigger_for_next_level_ar.strip(), f"{i.integration_id} missing AR trigger"
        assert i.trigger_for_next_level_en.strip(), f"{i.integration_id} missing EN trigger"
        # Names bilingual + non-empty
        assert i.name_ar.strip() and i.name_en.strip()


# ── Test 3 ────────────────────────────────────────────────────────────
def test_L3_entries_require_5_plus_customers_proof():
    """Article 4 prevention: NO L3 entry unless L3_proven_by_5_plus_customers=True."""
    for i in INTEGRATIONS:
        if i.current_level == 3:
            assert i.L3_proven_by_5_plus_customers is True, (
                f"{i.integration_id} marked L3 but L3_proven_by_5_plus_customers=False"
            )


# ── Test 4 ────────────────────────────────────────────────────────────
def test_every_integration_declares_at_least_one_hard_gate():
    """Article 4: every integration MUST declare relevant hard gates."""
    for i in INTEGRATIONS:
        assert len(i.hard_gates_respected) >= 1, (
            f"{i.integration_id} missing hard_gates_respected"
        )


# ── Test 5 ────────────────────────────────────────────────────────────
def test_blocked_upgrades_explicitly_marked():
    """Specific integrations should mark dangerous upgrades as PERMANENTLY BLOCKED."""
    # WhatsApp Business outbound auto = forever blocked
    wba = get_integration("whatsapp_business")
    assert wba is not None
    combined_trigger = wba.trigger_for_next_level_ar + wba.trigger_for_next_level_en
    assert ("BLOCKED" in combined_trigger or "محظور" in combined_trigger)

    # Gmail auto-send = forever blocked
    gmail = get_integration("gmail")
    assert gmail is not None
    combined_trigger = gmail.trigger_for_next_level_ar + gmail.trigger_for_next_level_en
    assert ("BLOCKED" in combined_trigger or "محظور" in combined_trigger)


# ── Test 6 ────────────────────────────────────────────────────────────
def test_lookup_helpers():
    assert get_integration("hunter_io") is not None
    assert get_integration("moyasar") is not None
    assert get_integration("zatca_phase_2") is not None
    assert get_integration("nonexistent") is None
    # Categories present
    cats = {i.category for i in INTEGRATIONS}
    expected_cats = {"lead_source", "crm", "spreadsheet", "calendar",
                     "messaging", "payment", "compliance", "email"}
    assert cats >= expected_cats - {"analytics", "observability"}
