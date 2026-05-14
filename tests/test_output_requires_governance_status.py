"""Doctrine: every meaningful output carries a governance_decision envelope."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.adoption_os.adoption_score import (
    compute as compute_adoption_score,
)
from auto_client_acquisition.data_os.source_passport import SourcePassport
from auto_client_acquisition.proof_os.proof_pack import assemble
from auto_client_acquisition.value_os.monthly_report import generate as generate_monthly


@pytest.fixture(autouse=True)
def isolated_ledgers(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    yield


def _passport() -> SourcePassport:
    return SourcePassport(
        source_id="src_x",
        source_type="crm_export",
        owner="acme",
        allowed_use=("internal_analysis",),
        contains_pii=False,
        sensitivity="low",
        ai_access_allowed=True,
        external_use_allowed=False,
        retention_policy="90d",
    )


def test_proof_pack_has_governance_decision() -> None:
    pack = assemble(
        engagement_id="eng_1",
        customer_id="acme",
        source_passport=_passport(),
        dq_score=0.9,
        value_events=[],
        governance_events=[],
    )
    assert isinstance(pack.governance_decision, str)
    assert pack.governance_decision != ""


def test_monthly_value_report_has_governance_decision() -> None:
    report = generate_monthly(customer_id="acme")
    assert isinstance(report.governance_decision, str)
    assert report.governance_decision != ""


def test_adoption_score_has_governance_decision() -> None:
    score = compute_adoption_score(
        customer_id="acme",
        channels_enabled=2,
        integrations_connected=1,
        sectors_targeted=1,
        total_drafts_lifetime=10,
        logins_last_30d=5,
        drafts_approved_last_30d=3,
        replies_acted_on_last_30d=2,
    )
    assert isinstance(score.governance_decision, str)
    assert score.governance_decision != ""


def test_friction_aggregate_emits_governance_envelope_via_router() -> None:
    client = TestClient(app)
    resp = client.get("/api/v1/friction-log/acme")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "governance_decision" in body
    assert body["governance_decision"]
