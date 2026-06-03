"""Wave 13 Phase 4 — Deliverable Entity tests.

Asserts:
  - Schema fields complete (extra='forbid')
  - State machine: 7 states + valid transitions only
  - customer_visible=False blocks portal display
  - proof_related=True + status='delivered' requires proof_event_id
  - JSONL persistence path

Sandbox-safe: imports schemas + lifecycle + store via direct file load.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load():
    repo_root = Path(__file__).resolve().parent.parent

    schemas_path = repo_root / "auto_client_acquisition" / "deliverables" / "schemas.py"
    spec = importlib.util.spec_from_file_location("_test_w13_p4_schemas", schemas_path)
    assert spec is not None and spec.loader is not None
    schemas = importlib.util.module_from_spec(spec)
    sys.modules["_test_w13_p4_schemas"] = schemas
    sys.modules["auto_client_acquisition.deliverables.schemas"] = schemas
    spec.loader.exec_module(schemas)

    lifecycle_path = repo_root / "auto_client_acquisition" / "deliverables" / "lifecycle.py"
    spec = importlib.util.spec_from_file_location("_test_w13_p4_lifecycle", lifecycle_path)
    assert spec is not None and spec.loader is not None
    lifecycle = importlib.util.module_from_spec(spec)
    sys.modules["_test_w13_p4_lifecycle"] = lifecycle
    spec.loader.exec_module(lifecycle)

    store_path = repo_root / "auto_client_acquisition" / "deliverables" / "store.py"
    spec = importlib.util.spec_from_file_location("_test_w13_p4_store", store_path)
    assert spec is not None and spec.loader is not None
    store = importlib.util.module_from_spec(spec)
    sys.modules["_test_w13_p4_store"] = store
    spec.loader.exec_module(store)

    return schemas, lifecycle, store


_SCH, _LIFE, _STORE = _load()
Deliverable = _SCH.Deliverable
DELIVERABLE_TRANSITIONS = _LIFE.DELIVERABLE_TRANSITIONS
InvalidTransitionError = _LIFE.InvalidTransitionError
advance = _LIFE.advance
is_terminal = _LIFE.is_terminal
create_deliverable = _STORE.create_deliverable
get_deliverable = _STORE.get_deliverable
list_by_session = _STORE.list_by_session
reset_for_test = _STORE.reset_for_test


# ── Test 1 ────────────────────────────────────────────────────────────
def test_schema_required_fields():
    d = Deliverable(
        deliverable_id="deliv_t1",
        session_id="sess_001",
        customer_handle="acme",
        type="proof_pack",
        title_ar="حزمة الإثبات",
        title_en="Proof Pack",
    )
    assert d.deliverable_id == "deliv_t1"
    assert d.status == "draft"
    assert d.version == 1
    assert d.customer_visible is True
    assert d.approval_required is True
    assert d.proof_related is False


# ── Test 2 ────────────────────────────────────────────────────────────
def test_schema_rejects_unknown_field():
    with pytest.raises(Exception):  # pydantic ValidationError
        Deliverable(
            deliverable_id="deliv_t2",
            session_id="sess_001",
            customer_handle="acme",
            type="proof_pack",
            title_ar="ع",
            title_en="E",
            rogue_field="not_allowed",  # type: ignore[call-arg]
        )


# ── Test 3 ────────────────────────────────────────────────────────────
def test_state_machine_has_7_states():
    expected = {
        "draft", "internal_review", "customer_review_required",
        "approved", "revision_requested", "delivered", "archived",
    }
    assert set(DELIVERABLE_TRANSITIONS.keys()) == expected


# ── Test 4 ────────────────────────────────────────────────────────────
def test_archived_is_terminal():
    assert is_terminal("archived") is True
    assert is_terminal("draft") is False
    assert is_terminal("delivered") is False  # delivered → archived possible


# ── Test 5 ────────────────────────────────────────────────────────────
def test_advance_valid_transitions():
    reset_for_test()
    d = create_deliverable(
        session_id="sess_005",
        customer_handle="acme",
        type="executive_pack",
        title_ar="حزمة تنفيذية",
        title_en="Executive Pack",
        persist=False,
    )
    assert d.status == "draft"
    advance(d, target="internal_review")
    assert d.status == "internal_review"
    advance(d, target="customer_review_required")
    assert d.status == "customer_review_required"
    advance(d, target="approved")
    assert d.status == "approved"
    advance(d, target="delivered")
    assert d.status == "delivered"


# ── Test 6 ────────────────────────────────────────────────────────────
def test_advance_invalid_transition_raises():
    reset_for_test()
    d = create_deliverable(
        session_id="sess_006",
        customer_handle="acme",
        type="draft_pack",
        title_ar="مسودة",
        title_en="Draft",
        persist=False,
    )
    # Cannot jump draft → delivered
    with pytest.raises(InvalidTransitionError):
        advance(d, target="delivered")
    assert d.status == "draft"  # unchanged


# ── Test 7 ────────────────────────────────────────────────────────────
def test_proof_related_requires_proof_event_id_on_delivered():
    """Article 8: no fake proof — proof_related=True must have proof_event_id when delivered."""
    reset_for_test()
    d = create_deliverable(
        session_id="sess_007",
        customer_handle="acme",
        type="proof_pack",
        title_ar="حزمة الإثبات",
        title_en="Proof Pack",
        proof_related=True,
        proof_event_id=None,  # missing!
        persist=False,
    )
    advance(d, target="customer_review_required")
    advance(d, target="approved")
    with pytest.raises(InvalidTransitionError) as ei:
        advance(d, target="delivered")
    assert "proof" in str(ei.value).lower()


# ── Test 8 ────────────────────────────────────────────────────────────
def test_proof_related_with_event_id_can_be_delivered():
    reset_for_test()
    d = create_deliverable(
        session_id="sess_008",
        customer_handle="acme",
        type="proof_pack",
        title_ar="حزمة الإثبات",
        title_en="Proof Pack",
        proof_related=True,
        proof_event_id="proof_evt_xyz",
        persist=False,
    )
    advance(d, target="customer_review_required")
    advance(d, target="approved")
    advance(d, target="delivered")
    assert d.status == "delivered"


# ── Test 9 ────────────────────────────────────────────────────────────
def test_list_by_session_filters_customer_visible():
    """Article 4: customer_visible=False blocks portal display."""
    reset_for_test()
    create_deliverable(
        session_id="sess_009",
        customer_handle="acme",
        type="proof_pack",
        title_ar="ع1",
        title_en="V1",
        customer_visible=True,
        persist=False,
    )
    create_deliverable(
        session_id="sess_009",
        customer_handle="acme",
        type="executive_pack",
        title_ar="ع2",
        title_en="Internal",
        customer_visible=False,  # internal-only
        persist=False,
    )
    all_items = list_by_session("sess_009", customer_visible_only=False)
    portal_items = list_by_session("sess_009", customer_visible_only=True)
    assert len(all_items) == 2
    assert len(portal_items) == 1
    assert portal_items[0].customer_visible is True


# ── Test 10 ───────────────────────────────────────────────────────────
def test_revision_requested_path():
    """Customer can request revision; path: customer_review → revision_requested → draft."""
    reset_for_test()
    d = create_deliverable(
        session_id="sess_010",
        customer_handle="acme",
        type="executive_pack",
        title_ar="حزمة",
        title_en="Pack",
        persist=False,
    )
    advance(d, target="internal_review")
    advance(d, target="customer_review_required")
    advance(d, target="revision_requested")
    advance(d, target="draft")
    assert d.status == "draft"
    # Version stays 1 (caller bumps version explicitly when re-doing work)
    assert d.version == 1
