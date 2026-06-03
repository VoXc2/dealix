"""Phase 6 — Proof Ledger extensions (file storage + consent + pack)."""
from __future__ import annotations

import base64

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.proof_ledger.consent_signature import (
    decline,
    hash_document,
    is_consent_valid,
    record_signature,
    request_consent,
)
from auto_client_acquisition.proof_ledger.file_storage import store_attachment
from auto_client_acquisition.proof_ledger.pack_assembly import assemble_proof_pack


# ── file_storage ──────────────────────────────────────────────
def test_store_attachment_round_trip(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = store_attachment(
        customer_handle="acme",
        event_id="pe_test_1",
        filename="report.pdf",
        mime_type="application/pdf",
        data=b"%PDF-1.4 fake content",
    )
    assert result["bytes"] == len(b"%PDF-1.4 fake content")
    assert result["uri"].startswith("file://")
    assert "data/proof_attachments/acme/pe_test_1/report.pdf" in result["uri"]


def test_store_attachment_rejects_oversize(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="too large"):
        store_attachment(
            customer_handle="acme",
            event_id="pe_test_2",
            filename="big.pdf",
            mime_type="application/pdf",
            data=b"x" * (11 * 1024 * 1024),
        )


def test_store_attachment_rejects_bad_mime(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="mime_type"):
        store_attachment(
            customer_handle="acme",
            event_id="pe_test_3",
            filename="bad.exe",
            mime_type="application/x-executable",
            data=b"\x4d\x5a",
        )


def test_store_attachment_strips_path_traversal(tmp_path, monkeypatch) -> None:
    """Path traversal segments are stripped via basename; file lands in
    the customer dir, not the parent."""
    monkeypatch.chdir(tmp_path)
    result = store_attachment(
        customer_handle="acme",
        event_id="pe_test_4",
        filename="../../etc/passwd",
        mime_type="text/plain",
        data=b"safe",
    )
    # File should be inside the customer/event dir — never outside
    assert "data/proof_attachments/acme/pe_test_4/passwd" in result["uri"]
    assert "/etc/" not in result["uri"]


def test_store_attachment_rejects_invalid_handle(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="customer_handle"):
        store_attachment(
            customer_handle="bad handle/with/slash",
            event_id="pe_test_5",
            filename="x.txt",
            mime_type="text/plain",
            data=b"x",
        )


# ── consent_signature ──────────────────────────────────────────
def test_consent_request_then_sign(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    narrative = "Acme reduced response time from 2 hours to 30 minutes."
    sig = request_consent(
        customer_handle="acme",
        scope="single_pack",
        narrative=narrative,
    )
    assert sig.status == "requested"
    assert sig.document_hash == hash_document(narrative)

    signed = record_signature(
        signature_id=sig.signature_id,
        signed_by="Sami Al-Foulan, GM",
        confirmed_document_hash=sig.document_hash,
    )
    assert signed.status == "signed"
    assert signed.signed_at is not None


def test_consent_signature_rejects_hash_mismatch(tmp_path, monkeypatch) -> None:
    """Cannot sign for narrative A then publish narrative B."""
    monkeypatch.chdir(tmp_path)
    sig = request_consent(
        customer_handle="acme",
        scope="single_pack",
        narrative="Original narrative.",
    )
    with pytest.raises(ValueError, match="document_hash mismatch"):
        record_signature(
            signature_id=sig.signature_id,
            signed_by="Sami",
            confirmed_document_hash="wronghash" + "0" * 56,
        )


def test_is_consent_valid_only_when_signed_and_matching(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    narrative = "Some narrative."
    sig = request_consent(
        customer_handle="acme", scope="single_event", narrative=narrative,
    )
    # Not yet signed
    assert is_consent_valid(signature_id=sig.signature_id, narrative=narrative) is False
    record_signature(
        signature_id=sig.signature_id,
        signed_by="Sami",
        confirmed_document_hash=sig.document_hash,
    )
    # Now signed and matching
    assert is_consent_valid(signature_id=sig.signature_id, narrative=narrative) is True
    # Different narrative still false
    assert is_consent_valid(signature_id=sig.signature_id, narrative="Other") is False


def test_consent_decline_blocks_signing(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    sig = request_consent(customer_handle="acme", scope="single_event", narrative="x")
    declined = decline(signature_id=sig.signature_id, declined_by="Sami")
    assert declined.status == "declined"
    with pytest.raises(ValueError, match="cannot re-sign"):
        record_signature(
            signature_id=sig.signature_id,
            signed_by="Sami",
            confirmed_document_hash=sig.document_hash,
        )


# ── pack_assembly ──────────────────────────────────────────────
_SIGNED_EVENT = {
    "event_id": "pe_signed",
    "event_type": "DELIVERY_TASK_COMPLETED",
    "summary_ar": "تسليم ناجح",
    "summary_en": "Successful delivery",
    "evidence_level": "customer_confirmed",
    "approval_status": "approved",
    "consent_for_publication": True,
}
_PENDING_EVENT = {
    "event_id": "pe_pending",
    "event_type": "DELIVERY_TASK_COMPLETED",
    "summary_ar": "—",
    "summary_en": "—",
    "evidence_level": "observed",
    "approval_status": "pending",
    "consent_for_publication": False,
}


def test_assemble_internal_only_includes_all(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    pack = assemble_proof_pack(
        customer_handle="acme",
        events=[_SIGNED_EVENT, _PENDING_EVENT],
        audience="internal_only",
    )
    assert pack["cover"]["event_count"] == 2
    assert pack["cover"]["publishable_count"] == 1
    assert len(pack["events"]) == 2  # internal includes everything
    assert pack["safety_summary"] == "internal_only_default"


def test_assemble_external_publishable_only_signed(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    pack = assemble_proof_pack(
        customer_handle="acme",
        events=[_SIGNED_EVENT, _PENDING_EVENT],
        audience="external_publishable",
    )
    assert pack["cover"]["publishable_count"] == 1
    assert len(pack["events"]) == 1  # only signed
    assert pack["events"][0]["event_id"] == "pe_signed"
    assert pack["safety_summary"] == "publishable_consent_required"


def test_assemble_external_with_zero_publishable_raises(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="zero publishable"):
        assemble_proof_pack(
            customer_handle="acme",
            events=[_PENDING_EVENT],
            audience="external_publishable",
        )


# ── HTTP endpoints ─────────────────────────────────────────────
@pytest.mark.asyncio
async def test_attachments_endpoint_round_trip(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/proof-ledger/attachments", json={
            "customer_handle": "acme",
            "event_id": "pe_http_1",
            "filename": "screen.png",
            "mime_type": "image/png",
            "data_base64": base64.b64encode(b"\x89PNG fake").decode(),
        })
    assert r.status_code == 200
    assert r.json()["stored"] is True
    assert r.json()["guardrails"]["max_bytes"] == 10 * 1024 * 1024


@pytest.mark.asyncio
async def test_consent_request_endpoint(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/proof-ledger/consent/request", json={
            "customer_handle": "acme",
            "scope": "single_pack",
            "narrative": "We helped Acme close 5 deals.",
        })
    assert r.status_code == 200
    sig = r.json()["signature"]
    assert sig["status"] == "requested"
    assert sig["customer_handle"] == "acme"


@pytest.mark.asyncio
async def test_pack_build_endpoint_internal(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/proof-ledger/pack/build", json={
            "customer_handle": "acme",
            "events": [_SIGNED_EVENT, _PENDING_EVENT],
            "audience": "internal_only",
        })
    assert r.status_code == 200
    body = r.json()
    assert body["cover"]["event_count"] == 2
    assert body["pack_id"].startswith("pack_")
