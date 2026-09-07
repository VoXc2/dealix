from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from api.routers import market_to_delivery_intake as router_module
from api.routers.market_to_delivery_intake import MarketToDeliveryIntakeBody
from db.models_commercial_intelligence import CommercialSignalRecord, CommercialSourceRecord


def _body(**overrides):
    payload = {
        "request_id": "mtd-test-001",
        "account_id": "account-1",
        "company_name": "Synthetic Company",
        "source_id": "source-1",
        "project_id": "construction-01",
        "problem": "Synthetic RFI handoff is slow.",
        "current_workflow": "Synthetic manual queue",
        "baseline": "Synthetic baseline supplied for preparation",
        "desired_outcome": "Measure response lead time",
        "constraints": "Synthetic test data only",
        "evidence_refs": [{"ref": "synthetic://fixture", "sha256": "a" * 64}],
        "data_authorized": True,
    }
    payload.update(overrides)
    return MarketToDeliveryIntakeBody.model_validate(payload)


def _source(**overrides):
    values = {
        "id": "source-1",
        "tenant_id": "tenant-a",
        "active": True,
        "policy_status": "approved",
        "kind": "client_provided",
        "freshness_days": 30,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def _artifact_digest(body=None):
    body = body or _body()
    preparation = router_module.prepare(
        router_module._preparation_payload(body, "tenant-a")
    )
    return preparation["artifact_digest"]


def _existing_for(body=None):
    return SimpleNamespace(
        id="sig-existing",
        evidence_level="l1_hypothesis",
        payload_json={
            "preparation_status": "DRAFT_PREPARED_FOR_REVIEW",
            "artifact_digest": _artifact_digest(body),
        },
    )


class _Scalars:
    def __init__(self, record):
        self.record = record

    def first(self):
        return self.record


class _Result:
    def __init__(self, record):
        self.record = record

    def scalars(self):
        return _Scalars(self.record)


class _Session:
    def __init__(self, *, source=None, existing=None, commit_error=None):
        self.source = source if source is not None else _source()
        self.existing = existing
        self.commit_error = commit_error
        self.added = []
        self.commits = 0
        self.rollbacks = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        return None

    async def get(self, model, record_id):
        if model is CommercialSourceRecord and record_id == "source-1":
            return self.source
        return None

    async def execute(self, _statement):
        return _Result(self.existing)

    def add(self, record):
        self.added.append(record)

    async def commit(self):
        self.commits += 1
        if self.commit_error:
            raise self.commit_error

    async def rollback(self):
        self.rollbacks += 1


def _patch_session(monkeypatch, session):
    monkeypatch.setattr(router_module, "async_session_factory", lambda: lambda: session)


@pytest.mark.asyncio
async def test_intake_persists_only_l1_signal(monkeypatch):
    session = _Session()
    _patch_session(monkeypatch, session)

    result = await router_module.persist_market_to_delivery_intake(
        _body(),
        current_user={"id": "sales-user", "tenant_id": "tenant-a"},
    )

    assert result["status"] == "created"
    assert result["evidence_level"] == "l1_hypothesis"
    assert result["relationship_created"] is False
    assert result["consent_created"] is False
    assert result["opportunity_created"] is False
    assert result["external_side_effect"] is False
    assert session.commits == 1

    signals = [item for item in session.added if isinstance(item, CommercialSignalRecord)]
    assert len(signals) == 1
    signal = signals[0]
    assert signal.tenant_id == "tenant-a"
    assert signal.account_id == "account-1"
    assert signal.source_id == "source-1"
    assert signal.signal_type == "market_to_delivery_intake"
    assert signal.evidence_ref == "mtd://request/mtd-test-001"
    assert signal.evidence_level == "l1_hypothesis"
    assert signal.confidence == 40
    assert signal.payload_json["relationship_inferred"] is False
    assert signal.payload_json["consent_inferred"] is False
    assert signal.payload_json["opportunity_created"] is False
    assert signal.payload_json["diagnostic"]["evidence_refs"][0]["tenant_id"] == "tenant-a"


@pytest.mark.asyncio
async def test_exact_replay_returns_existing_without_second_write(monkeypatch):
    existing = _existing_for()
    session = _Session(existing=existing)
    _patch_session(monkeypatch, session)

    result = await router_module.persist_market_to_delivery_intake(
        _body(),
        current_user={"tenant_id": "tenant-a"},
    )

    assert result["status"] == "existing"
    assert result["signal_id"] == "sig-existing"
    assert session.added == []
    assert session.commits == 0


@pytest.mark.asyncio
async def test_changed_payload_under_same_request_id_conflicts(monkeypatch):
    existing = _existing_for()
    session = _Session(existing=existing)
    _patch_session(monkeypatch, session)

    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(
            _body(problem="Changed synthetic requirement under same request id."),
            current_user={"tenant_id": "tenant-a"},
        )

    assert error.value.status_code == 409
    assert error.value.detail == "market_to_delivery_request_id_payload_conflict"
    assert session.added == []
    assert session.commits == 0


@pytest.mark.asyncio
async def test_source_is_tenant_scoped(monkeypatch):
    session = _Session(source=_source(tenant_id="tenant-b"))
    _patch_session(monkeypatch, session)

    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(
            _body(),
            current_user={"tenant_id": "tenant-a"},
        )

    assert error.value.status_code == 404
    assert error.value.detail == "tenant_intake_source_not_found"
    assert not session.added


@pytest.mark.asyncio
async def test_blocked_source_fails_closed(monkeypatch):
    session = _Session(source=_source(policy_status="blocked"))
    _patch_session(monkeypatch, session)

    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(
            _body(), current_user={"tenant_id": "tenant-a"}
        )

    assert error.value.status_code == 409
    assert error.value.detail == "blocked_source_cannot_accept_intake"


@pytest.mark.asyncio
async def test_public_research_source_cannot_masquerade_as_customer_intake(monkeypatch):
    session = _Session(source=_source(kind="public_registry"))
    _patch_session(monkeypatch, session)

    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(
            _body(), current_user={"tenant_id": "tenant-a"}
        )

    assert error.value.status_code == 409
    assert error.value.detail == "source_kind_not_eligible_for_customer_intake"


@pytest.mark.asyncio
async def test_data_authority_is_required_but_does_not_create_consent(monkeypatch):
    session = _Session()
    _patch_session(monkeypatch, session)

    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(
            _body(data_authorized=False),
            current_user={"tenant_id": "tenant-a"},
        )

    assert error.value.status_code == 422
    assert not session.added


def test_body_cannot_self_assert_consent_or_approval():
    payload = _body().model_dump()
    payload["consent"] = True
    with pytest.raises(ValidationError):
        MarketToDeliveryIntakeBody.model_validate(payload)

    payload = _body().model_dump()
    payload["auto_approve"] = True
    with pytest.raises(ValidationError):
        MarketToDeliveryIntakeBody.model_validate(payload)


@pytest.mark.asyncio
async def test_persistence_failure_is_503_and_rolls_back(monkeypatch):
    session = _Session(commit_error=RuntimeError("synthetic db unavailable"))
    _patch_session(monkeypatch, session)

    with pytest.raises(HTTPException) as error:
        await router_module.persist_market_to_delivery_intake(
            _body(), current_user={"tenant_id": "tenant-a"}
        )

    assert error.value.status_code == 503
    assert error.value.detail == "market_to_delivery_intake_not_persisted"
    assert session.rollbacks == 1
