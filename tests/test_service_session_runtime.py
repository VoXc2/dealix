"""Wave 13 Phase 3 — Service Session Runtime tests.

Asserts the orchestrator:
  - extends ServiceSessionRecord with new fields (Phase 3 extras)
  - tick() advances day counter only on active sessions
  - tick() raises ArtifactOverdueError when 2+ days w/o artifact
  - record_artifact() appends correctly
  - set_next_actions() populates bilingual fields

Sandbox-safe: imports only the orchestrator + schemas modules directly;
avoids api/security pyo3 cascade.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_modules():
    """Load schemas + orchestrator without triggering api/* imports."""
    repo_root = Path(__file__).resolve().parent.parent

    # full_ops_contracts/schemas.py is normal pydantic; safe to import.
    schemas_path = repo_root / "auto_client_acquisition" / "full_ops_contracts" / "schemas.py"
    spec_s = importlib.util.spec_from_file_location(
        "_test_w13_p3_full_ops_schemas", schemas_path
    )
    assert spec_s is not None and spec_s.loader is not None
    schemas_mod = importlib.util.module_from_spec(spec_s)
    sys.modules["_test_w13_p3_full_ops_schemas"] = schemas_mod
    sys.modules["auto_client_acquisition.full_ops_contracts.schemas"] = schemas_mod
    spec_s.loader.exec_module(schemas_mod)

    # orchestrator imports from schemas via package path; rely on sys.modules shim
    orch_path = repo_root / "auto_client_acquisition" / "service_sessions" / "orchestrator.py"
    spec_o = importlib.util.spec_from_file_location(
        "_test_w13_p3_orchestrator", orch_path
    )
    assert spec_o is not None and spec_o.loader is not None
    orch_mod = importlib.util.module_from_spec(spec_o)
    sys.modules["_test_w13_p3_orchestrator"] = orch_mod
    spec_o.loader.exec_module(orch_mod)

    return schemas_mod, orch_mod


_SCHEMAS, _ORCH = _load_modules()
ServiceSessionRecord = _SCHEMAS.ServiceSessionRecord
ArtifactOverdueError = _ORCH.ArtifactOverdueError
SessionNotRunningError = _ORCH.SessionNotRunningError
tick = _ORCH.tick
record_artifact = _ORCH.record_artifact
set_next_actions = _ORCH.set_next_actions
is_artifact_overdue = _ORCH.is_artifact_overdue


def _make_session(status: str = "active", day: int = 0) -> ServiceSessionRecord:
    return ServiceSessionRecord(
        session_id=f"sess_test_{day}",
        customer_handle="acme-real-estate",
        service_type="growth_proof_sprint",
        status=status,  # type: ignore[arg-type]
        day_number=day,
    )


# ── Test 1 ────────────────────────────────────────────────────────────
def test_schema_has_phase_3_fields():
    """Phase 3 added: service_offering_id, daily_artifacts, next_customer_action, next_founder_action, day_number."""
    rec = _make_session()
    d = rec.model_dump()
    for f in [
        "service_offering_id",
        "daily_artifacts",
        "next_customer_action",
        "next_founder_action",
        "day_number",
    ]:
        assert f in d, f"missing Phase 3 field: {f}"
    assert d["day_number"] == 0
    assert d["daily_artifacts"] == []


# ── Test 2 ────────────────────────────────────────────────────────────
def test_tick_advances_day_on_active_session():
    rec = _make_session(status="active", day=0)
    result = tick(rec)
    assert result.previous_day == 0
    assert result.new_day == 1
    assert rec.day_number == 1


# ── Test 3 ────────────────────────────────────────────────────────────
def test_tick_raises_on_non_active_session():
    for status in ["draft", "blocked", "complete", "delivered"]:
        rec = _make_session(status=status, day=1)  # type: ignore[arg-type]
        with pytest.raises(SessionNotRunningError):
            tick(rec)


# ── Test 4 ────────────────────────────────────────────────────────────
def test_tick_raises_artifact_overdue_when_2_days_behind():
    """Article 8: do NOT silently advance day counter without proof of work."""
    rec = _make_session(status="active", day=3)  # session on day 3
    # Last artifact was day 1 → 2-day gap → overdue
    record_artifact(rec, day_number=1, title_ar="مخرَج اليوم 1", title_en="Day 1 deliverable")
    assert is_artifact_overdue(rec) is True
    with pytest.raises(ArtifactOverdueError):
        tick(rec)


# ── Test 5 ────────────────────────────────────────────────────────────
def test_tick_does_not_raise_when_artifact_recent():
    rec = _make_session(status="active", day=2)
    record_artifact(rec, day_number=2, title_ar="مخرَج اليوم 2", title_en="Day 2 deliverable")
    assert is_artifact_overdue(rec) is False
    result = tick(rec)
    assert result.new_day == 3


# ── Test 6 ────────────────────────────────────────────────────────────
def test_record_artifact_appends_to_daily_artifacts():
    rec = _make_session(status="active", day=1)
    art = record_artifact(
        rec,
        artifact_id="art_001",
        artifact_type="proof_pack_section",
        title_ar="ملخص اليوم",
        title_en="Today's summary",
        customer_visible=True,
        status="approved",
    )
    assert art["artifact_id"] == "art_001"
    assert art["day_number"] == 1
    assert art["customer_visible"] is True
    assert art["status"] == "approved"
    assert len(rec.daily_artifacts) == 1
    assert rec.daily_artifacts[0]["artifact_id"] == "art_001"


# ── Test 7 ────────────────────────────────────────────────────────────
def test_set_next_actions_populates_bilingual_fields():
    rec = _make_session()
    set_next_actions(
        rec,
        customer_action_ar="اعتمد رسالة الاجتماع غداً",
        customer_action_en="Approve meeting message before tomorrow",
        founder_action_ar="جهّز الكلام الافتتاحي للمكالمة",
        founder_action_en="Prepare opening line for the call",
    )
    assert rec.next_customer_action == {
        "ar": "اعتمد رسالة الاجتماع غداً",
        "en": "Approve meeting message before tomorrow",
    }
    assert rec.next_founder_action == {
        "ar": "جهّز الكلام الافتتاحي للمكالمة",
        "en": "Prepare opening line for the call",
    }


# ── Test 8 ────────────────────────────────────────────────────────────
def test_session_offering_link_optional_and_typed():
    """service_offering_id is optional; when set, references service_catalog id."""
    rec = _make_session()
    assert rec.service_offering_id is None
    rec.service_offering_id = "diagnostic_starter"
    assert rec.service_offering_id == "diagnostic_starter"
    # Round-trip via model_dump
    d = rec.model_dump()
    assert d["service_offering_id"] == "diagnostic_starter"
