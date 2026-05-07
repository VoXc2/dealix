"""Phase 11 — Case Study Engine tests.

Asserts:
- selection rules (evidence_level + consent + approval + redaction)
- narrative is bilingual + scrubbed for forbidden tokens
- consent_signature gate enforced (no approve without signed consent)
- candidate.is_publishable() only true after all gates pass
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


_GOOD_EVENT = {
    "event_id": "pe_good_1",
    "event_type": "DELIVERY_TASK_COMPLETED",
    "summary_ar": "Acme حقّق نجاحاً واضحاً",
    "summary_en": "Acme achieved a clear win",
    "evidence_level": "customer_confirmed",
    "approval_status": "approved",
    "consent_for_publication": True,
    "pii_redacted": True,
}
_WEAK_EVENT = {
    "event_id": "pe_weak_1",
    "event_type": "DELIVERY_TASK_COMPLETED",
    "summary_ar": "—",
    "summary_en": "—",
    "evidence_level": "observed",  # too weak
    "approval_status": "pending",
    "consent_for_publication": False,
    "pii_redacted": True,
}


def test_select_publishable_filters_correctly() -> None:
    from auto_client_acquisition.case_study_engine import select_publishable
    result = select_publishable([_GOOD_EVENT, _WEAK_EVENT])
    assert result["publishable_count"] == 1
    assert result["publishable"][0]["event_id"] == "pe_good_1"
    rejected = result["rejected"][0]
    assert "evidence_level_too_weak" in rejected["reasons"]
    assert "consent_not_granted" in rejected["reasons"]
    assert "not_approved" in rejected["reasons"]


def test_build_candidate_returns_pending_state(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from auto_client_acquisition.case_study_engine import build_candidate
    result = build_candidate(
        customer_handle="cs-test-1",
        events=[_GOOD_EVENT],
        sector="real_estate",
    )
    candidate = result["candidate"]
    assert candidate["customer_handle"] == "cs-test-1"
    assert candidate["consent_status"] == "not_requested"
    assert candidate["approval_status"] == "pending"
    assert candidate["redaction_status"] == "complete"
    # Forbidden tokens should be absent
    text = candidate["narrative_draft_ar"] + candidate["narrative_draft_en"]
    assert "نضمن" not in text
    assert "guaranteed" not in text.lower()
    assert "blast" not in text.lower()
    assert "scraping" not in text.lower()


def test_build_candidate_zero_publishable_raises(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from auto_client_acquisition.case_study_engine import build_candidate
    with pytest.raises(ValueError, match="no publishable"):
        build_candidate(
            customer_handle="cs-test-2",
            events=[_WEAK_EVENT],
            sector="real_estate",
        )


def test_approve_blocked_without_signed_consent(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from auto_client_acquisition.case_study_engine import (
        approve_candidate,
        build_candidate,
    )
    result = build_candidate(
        customer_handle="cs-test-3",
        events=[_GOOD_EVENT],
        sector="real_estate",
    )
    cid = result["candidate"]["candidate_id"]
    with pytest.raises(ValueError, match="signed consent"):
        approve_candidate(candidate_id=cid, approver="founder")


def test_full_lifecycle_request_sign_approve(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from auto_client_acquisition.case_study_engine import (
        approve_candidate,
        build_candidate,
        request_quote,
    )
    from auto_client_acquisition.proof_ledger.consent_signature import (
        record_signature,
    )
    # 1. Build candidate
    built = build_candidate(
        customer_handle="cs-lifecycle",
        events=[_GOOD_EVENT],
        sector="real_estate",
    )
    cid = built["candidate"]["candidate_id"]
    # 2. Request quote (creates consent signature)
    quote = request_quote(candidate_id=cid)
    sig_id = quote["consent_signature_id"]
    doc_hash = quote["document_hash"]
    # 3. Customer signs
    signed = record_signature(
        signature_id=sig_id,
        signed_by="Acme GM",
        confirmed_document_hash=doc_hash,
    )
    assert signed.status == "signed"
    # 4. Update the case study to reflect the signed consent
    from auto_client_acquisition.case_study_engine.builder import _INDEX
    _INDEX[cid].consent_status = "signed"
    # 5. Approve
    approval = approve_candidate(candidate_id=cid, approver="founder")
    assert approval["approval_status"] == "approved"
    assert approval["publishable_now"] is True


@pytest.mark.asyncio
async def test_candidate_endpoint(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/case-study/candidate", json={
            "events": [_GOOD_EVENT, _WEAK_EVENT],
        })
    body = r.json()
    assert body["candidate"] is True
    assert body["publishable_count"] == 1
    assert body["hard_gates"]["no_publish_without_consent"] is True


@pytest.mark.asyncio
async def test_build_endpoint(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/case-study/build", json={
            "customer_handle": "endpoint-test",
            "events": [_GOOD_EVENT],
            "sector": "real_estate",
        })
    assert r.status_code == 200
    body = r.json()
    assert body["candidate"]["customer_handle"] == "endpoint-test"
    assert body["publishable_count"] == 1


@pytest.mark.asyncio
async def test_library_endpoint_returns_list(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/case-study/library")
    assert r.status_code == 200
    body = r.json()
    assert "count" in body
    assert "entries" in body
    assert body["hard_gates"]["forbidden_tokens_scrubbed"] is True
