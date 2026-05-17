"""Full Ops 2.0 — multi-step outreach sequence engine."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.outreach_sequence import (
    SEQUENCES,
    compute_next_step,
    get_sequence,
    list_sequences,
)


# ── sequence definitions ─────────────────────────────────────────


def test_named_sequences_exist() -> None:
    for name in ("warm_linkedin", "proof_pack_download", "partner", "webinar"):
        assert name in SEQUENCES


def test_list_sequences_returns_ordered_steps() -> None:
    seqs = list_sequences()
    assert seqs
    for s in seqs:
        offsets = [step["day_offset"] for step in s["steps"]]
        assert offsets == sorted(offsets)


def test_every_step_requires_approval() -> None:
    # DOCTRINE — no step may auto-send; all must route to approval.
    for seq in SEQUENCES.values():
        for step in seq.steps:
            assert step.requires_approval is True


def test_no_cold_whatsapp_channel_in_sequences() -> None:
    for seq in SEQUENCES.values():
        for step in seq.steps:
            assert "whatsapp" not in step.channel.lower()


def test_get_sequence_case_insensitive() -> None:
    assert get_sequence("WARM_LINKEDIN") is not None
    assert get_sequence("does_not_exist") is None


# ── next-step computation ────────────────────────────────────────


def test_first_step_due_on_enrollment_day() -> None:
    res = compute_next_step(
        sequence_name="warm_linkedin",
        lead_id="lead1",
        enrolled_on="2026-05-01",
        completed_steps=0,
        as_of="2026-05-01",
    )
    assert res.has_pending_step is True
    assert res.next_step is not None
    assert res.next_step["step_number"] == 1
    assert res.next_step["requires_approval"] is True


def test_step_not_due_before_offset() -> None:
    res = compute_next_step(
        sequence_name="warm_linkedin",
        lead_id="lead1",
        enrolled_on="2026-05-01",
        completed_steps=1,  # step 2 has day_offset 3
        as_of="2026-05-02",
    )
    assert res.has_pending_step is False
    assert res.next_step is None


def test_step_due_after_offset_elapsed() -> None:
    res = compute_next_step(
        sequence_name="warm_linkedin",
        lead_id="lead1",
        enrolled_on="2026-05-01",
        completed_steps=1,
        as_of="2026-05-05",  # 4 days >= step 2 offset 3
    )
    assert res.has_pending_step is True
    assert res.next_step["step_number"] == 2


def test_sequence_complete_when_all_steps_done() -> None:
    seq = get_sequence("partner")
    assert seq is not None
    res = compute_next_step(
        sequence_name="partner",
        lead_id="lead1",
        enrolled_on="2026-05-01",
        completed_steps=len(seq.steps),
        as_of="2026-09-01",
    )
    assert res.has_pending_step is False
    assert "complete" in res.reason_en.lower()


def test_unknown_sequence_returns_no_step() -> None:
    res = compute_next_step(
        sequence_name="nope",
        lead_id="lead1",
        enrolled_on="2026-05-01",
    )
    assert res.has_pending_step is False


def test_invalid_enrollment_date_handled() -> None:
    res = compute_next_step(
        sequence_name="webinar",
        lead_id="lead1",
        enrolled_on="not-a-date",
    )
    assert res.has_pending_step is False


# ── router endpoints ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_router_list_sequences() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/outreach/sequences")
    body = r.json()
    assert body["status"] == "ok"
    assert any(s["name"] == "webinar" for s in body["sequences"])
    assert body["doctrine"] == "sequences_prepare_drafts_only_no_auto_send"


@pytest.mark.asyncio
async def test_router_next_step_returns_draft_instruction() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/outreach/sequences/next-step",
            json={
                "sequence": "proof_pack_download",
                "lead_id": "lead42",
                "enrolled_on": "2026-05-01",
                "completed_steps": 0,
                "as_of": "2026-05-01",
            },
        )
    body = r.json()
    assert body["has_pending_step"] is True
    assert body["next_step"]["requires_approval"] is True
    assert body["next_step"]["prepare_only"] is True


@pytest.mark.asyncio
async def test_router_next_step_validates_required_fields() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/outreach/sequences/next-step",
            json={"sequence": "webinar"},
        )
    assert r.status_code == 400
