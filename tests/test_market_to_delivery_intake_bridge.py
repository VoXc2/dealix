"""Handler boundary tests with injected sessions; not Postgres durability tests."""
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from api.routers import market_to_delivery_intake as router_module
from api.routers.market_to_delivery_intake import MarketToDeliveryIntakeBody
from db.models_commercial_intelligence import CommercialSignalRecord, CommercialSourceRecord


def _body(**overrides):
    payload = {
        "request_id": "mtd-test-001", "account_id": "account-1",
        "company_name": "Synthetic Company", "source_id": "source-1",
        "project_id": "construction-01", "problem": "Synthetic RFI handoff is slow.",
        "current_workflow": "Synthetic manual queue",
        "baseline": "Synthetic baseline supplied for preparation",
        "desired_outcome": "Measure response lead time", "constraints": "Synthetic test data only",
        "evidence_refs": [{"ref": "synthetic://fixture", "sha256": "a" * 64}],
        "data_authorized": True,
    }
    payload.update(overrides)
    return MarketToDeliveryIntakeBody.model_validate(payload)


def _source(**overrides):
    values = {"id": "source-1", "tenant_id": "tenant-a", "active": True,
              "policy_status": "approved", "kind": "client_provided", "freshness_days": 30}
    values.update(overrides)
    return SimpleNamespace(**values)


def _existing_for(body=None):
    body = body or _body()
    preparation = router_module.prepare(router_module._preparation_payload(body, "tenant-a"))
    return SimpleNamespace(
        id="sig-existing", evidence_level="l1_hypothesis",
        payload_json={
            "preparation_status": "DRAFT_PREPARED_FOR_REVIEW",
            "artifact_digest": preparation["artifact_digest"], "company_name": body.company_name,
            "request_digest": router_module.intake_request_fingerprint(body, "tenant-a"),
            "request_digest_version": router_module.REQUEST_SCHEMA,
        },
    )


class _Result:
    def __init__(self, record): self.record = record
    def scalars(self): return self
    def first(self): return self.record


class _Session:
    def __init__(self, *, source=None, existing=None, commit_error=None):
        self.source = source if source is not None else _source()
        self.existing = existing
        self.commit_error = commit_error
        self.added, self.statements = [], []
        self.commits = self.rollbacks = 0
    async def __aenter__(self): return self
    async def __aexit__(self, *_): return None
    async def get(self, model, record_id):
        return self.source if model is CommercialSourceRecord and record_id == "source-1" else None
    async def execute(self, statement):
        self.statements.append(statement)
        return _Result(self.existing)
    def add(self, record): self.added.append(record)
    async def commit(self):
        self.commits += 1
        if self.commit_error: raise self.commit_error
    async def rollback(self): self.rollbacks += 1


def _patch_session(monkeypatch, session):
    monkeypatch.setattr(router_module, "async_session_factory", lambda: lambda: session)


@pytest.mark.asyncio
async def test_intake_persists_only_l1_signal(monkeypatch):
    session = _Session()
    _patch_session(monkeypatch, session)
    result = await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id": "tenant-a"})
    assert result["status"] == "created"
    assert result["evidence_level"] == "l1_hypothesis"
    for key in ("relationship_created", "consent_created", "opportunity_created", "external_side_effect"):
        assert result[key] is False
    assert session.commits == 1
    assert len(session.added) == 1
    signal = session.added[0]
    assert isinstance(signal, CommercialSignalRecord)
    assert (signal.tenant_id, signal.account_id, signal.source_id) == ("tenant-a", "account-1", "source-1")
    assert signal.signal_type == "market_to_delivery_intake"
    assert signal.evidence_ref == "mtd://request/mtd-test-001"
    assert signal.confidence == 40
    for key in ("relationship_inferred", "consent_inferred", "opportunity_created"):
        assert signal.payload_json[key] is False
    assert signal.payload_json["diagnostic"]["evidence_refs"][0]["tenant_id"] == "tenant-a"
    assert signal.payload_json["request_digest"] == router_module.intake_request_fingerprint(_body(), "tenant-a")
    assert signal.payload_json["data_authority_evidence"] == "OPERATOR_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED"


@pytest.mark.asyncio
async def test_exact_replay_returns_existing_without_second_write(monkeypatch):
    session = _Session(existing=_existing_for())
    _patch_session(monkeypatch, session)
    result = await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id": "tenant-a"})
    assert result["status"] == "existing"
    assert result["signal_id"] == "sig-existing"
    assert session.added == [] and session.commits == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("change", [{"problem":"Changed requirement"}, {"company_name":"Other Company"}, {"estimated_cost_sar":"123"}])
async def test_changed_payload_conflicts(monkeypatch, change):
    session = _Session(existing=_existing_for())
    _patch_session(monkeypatch, session)
    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(_body(**change), current_user={"tenant_id":"tenant-a"})
    assert error.value.status_code == 409
    assert error.value.detail == "market_to_delivery_request_id_payload_conflict"
    assert not session.added and session.commits == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("source_change,expected", [
    ({"tenant_id":"tenant-b"},404), ({"active":False},404),
    ({"policy_status":"blocked"},409), ({"policy_status":"review_required"},409),
    ({"policy_status":"research_only"},409), ({"policy_status":"unrecognized"},409),
    ({"kind":"public_registry"},409),
])
async def test_ineligible_source_is_rejected_before_preparation(monkeypatch, source_change, expected):
    session = _Session(source=_source(**source_change))
    _patch_session(monkeypatch, session)
    def no_prepare(_): raise AssertionError("ineligible source reached preparation")
    monkeypatch.setattr(router_module, "prepare", no_prepare)
    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id":"tenant-a"})
    assert error.value.status_code == expected
    assert not session.added


@pytest.mark.asyncio
async def test_no_data_attestation_no_persistence(monkeypatch):
    session = _Session()
    _patch_session(monkeypatch, session)
    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(_body(data_authorized=False), current_user={"tenant_id":"tenant-a"})
    assert error.value.status_code == 422 and not session.added


def test_body_cannot_self_assert_consent_or_approval():
    for key in ("consent", "auto_approve", "tenant_id"):
        payload = _body().model_dump(); payload[key] = True
        with pytest.raises(ValidationError): MarketToDeliveryIntakeBody.model_validate(payload)


@pytest.mark.asyncio
async def test_failed_commit_returns_503_not_prepared_success(monkeypatch):
    session = _Session(commit_error=RuntimeError("synthetic db unavailable"))
    _patch_session(monkeypatch, session)
    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id":"tenant-a"})
    assert error.value.status_code == 503
    assert error.value.detail == "market_to_delivery_intake_not_persisted"
    assert session.rollbacks == 1


@pytest.mark.asyncio
async def test_replay_does_not_invoke_new_preparation_engine(monkeypatch):
    session = _Session(existing=_existing_for())
    _patch_session(monkeypatch, session)
    def forbidden_prepare(_): raise AssertionError("replay invoked newer engine/catalog")
    monkeypatch.setattr(router_module, "prepare", forbidden_prepare)
    result = await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id":"tenant-a"})
    assert result["status"] == "existing" and session.commits == 0


@pytest.mark.asyncio
async def test_replay_still_checks_revoked_source(monkeypatch):
    session = _Session(existing=_existing_for(), source=_source(active=False))
    _patch_session(monkeypatch, session)
    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id":"tenant-a"})
    assert error.value.status_code == 404 and session.commits == 0


@pytest.mark.asyncio
async def test_legacy_exact_artifact_replay_does_not_backfill(monkeypatch):
    existing = _existing_for(); del existing.payload_json["request_digest"]
    session = _Session(existing=existing)
    _patch_session(monkeypatch, session)
    result = await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id":"tenant-a"})
    assert result["status"] == "existing"
    assert "request_digest" not in existing.payload_json and session.commits == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("field", ["company_name", "artifact_digest"])
async def test_incomplete_legacy_replay_fails_closed(monkeypatch, field):
    existing = _existing_for(); del existing.payload_json["request_digest"]; existing.payload_json.pop(field)
    session = _Session(existing=existing)
    _patch_session(monkeypatch, session)
    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id":"tenant-a"})
    assert error.value.status_code == 409
    assert error.value.detail == "market_to_delivery_legacy_request_requires_review"


@pytest.mark.asyncio
async def test_unknown_digest_version_fails_closed(monkeypatch):
    existing = _existing_for(); existing.payload_json["request_digest_version"] = "unsupported"
    session = _Session(existing=existing)
    _patch_session(monkeypatch, session)
    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id":"tenant-a"})
    assert error.value.status_code == 409


class _RaceSession(_Session):
    async def execute(self, statement):
        self.statements.append(statement)
        return _Result(self.existing if self.rollbacks else None)


@pytest.mark.asyncio
@pytest.mark.parametrize("changed", [False, True])
async def test_unique_constraint_race_checks_intent(monkeypatch, changed):
    winner = _existing_for(_body(company_name="Race changed company") if changed else _body())
    session = _RaceSession(existing=winner, commit_error=IntegrityError("synthetic", {}, Exception("conflict")))
    _patch_session(monkeypatch, session)
    if changed:
        with pytest.raises(HTTPException) as error:
            await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id":"tenant-a"})
        assert error.value.status_code == 409
    else:
        result = await router_module.persist_market_to_delivery_intake(_body(), current_user={"tenant_id":"tenant-a"})
        assert result["status"] == "existing"
    assert session.commits == 1 and session.rollbacks == 1


@pytest.mark.asyncio
async def test_lookup_and_write_share_normalized_account(monkeypatch):
    session = _Session(); _patch_session(monkeypatch, session)
    await router_module.persist_market_to_delivery_intake(
        _body(account_id=" account-1 ", source_id=" source-1 "), current_user={"tenant_id":"tenant-a"})
    params = session.statements[0].compile().params
    assert "account-1" in params.values() and " account-1 " not in params.values()
    assert session.added[0].account_id == "account-1"


@pytest.mark.asyncio
@pytest.mark.parametrize("user", [{}, {"tenant_id":1}, {"tenant_id":"x/y"}])
async def test_invalid_authenticated_tenant_denied(user):
    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(_body(), current_user=user)
    assert error.value.status_code == 403
