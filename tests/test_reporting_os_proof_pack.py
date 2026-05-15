"""Reporting OS — proof pack facade."""

from __future__ import annotations

from auto_client_acquisition.reporting_os.proof_pack import (
    build_master_proof_pack_dict,
    build_proof_pack_dict,
    proof_pack_has_required_sections,
    proof_pack_master_complete,
    render_proof_pack_markdown,
)


def test_proof_pack_master_complete() -> None:
    master = build_master_proof_pack_dict(
        client={"name": "X"},
        service={"sku": "lead_intelligence_sprint"},
        problem={"statement": "messy leads"},
        inputs={"sources": "csv"},
        work_completed={"summary": "scored 50"},
        metrics={"accounts": 50},
        ai_outputs={"scores": True},
        governance={"approved": True},
        business_value={"category": "revenue"},
        next_step={"offer": "pilot"},
    )
    assert proof_pack_master_complete(master) is True
    md = render_proof_pack_markdown(master)
    assert "Proof Pack" in md
    assert "## Client" in md


def test_proof_pack_master_incomplete() -> None:
    assert proof_pack_master_complete({"client": {}}) is False


def test_proof_pack_requires_sections() -> None:
    ok = build_proof_pack_dict(
        inputs={"rows": 10},
        outputs={"ranked": 5},
        impact={"hours_saved": 2},
        next_actions=["schedule review"],
    )
    assert proof_pack_has_required_sections(ok) is True


def test_proof_pack_rejects_empty_actions() -> None:
    bad = build_proof_pack_dict(inputs={}, outputs={}, impact={}, next_actions=[])
    assert proof_pack_has_required_sections(bad) is False
