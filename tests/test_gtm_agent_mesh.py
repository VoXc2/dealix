"""Smoke tests for GTM agent mesh."""

from __future__ import annotations

from dealix.commercial_ops.gtm_agent_mesh import (
    AGENT_MESH,
    EnrichmentAgent,
    LearningAgent,
    OutreachDraftAgent,
    ProofPackAgent,
    QualificationAgent,
    TargetingAgent,
    run_agent,
)


def test_agent_mesh_registry_has_six_agents() -> None:
    assert len(AGENT_MESH) == 6
    assert set(AGENT_MESH) == {
        "targeting",
        "enrichment",
        "outreach_draft",
        "qualification",
        "proof_pack",
        "learning",
    }


def test_all_agents_return_draft_only_envelope() -> None:
    sample_target = {
        "company": "Test Agency",
        "segment": "agency_wedge",
        "pain_hypothesis": "post-campaign follow-up gap",
        "channel": "linkedin_manual",
    }
    ctx = {"target": sample_target, "top_n": 3}
    for name in AGENT_MESH:
        out = run_agent(name, ctx)
        assert out["draft_only"] is True
        assert out["external_send"] is False
        assert isinstance(out["autonomy_level"], str)


def test_targeting_agent_smoke() -> None:
    out = TargetingAgent.run({"top_n": 2})
    assert out["agent"] == "targeting"
    assert "targets" in out


def test_enrichment_agent_smoke() -> None:
    out = EnrichmentAgent.run({"target": {"company": "Co", "contact": "x@y.sa"}})
    assert out["enriched"]["enriched_fields"]["company"] == "Co"


def test_outreach_draft_agent_smoke() -> None:
    out = OutreachDraftAgent.run(
        {"target": {"company": "Co", "pain_hypothesis": "needs proof", "channel": "email"}}
    )
    assert "draft_ar" in out
    assert "مسودة" in out["draft_ar"] or "Dealix" in out["draft_ar"]


def test_qualification_agent_rejects_doctrine_violation() -> None:
    out = QualificationAgent.run({"raw_request_text": "cold whatsapp blast all leads"})
    qual = out["qualification"]
    assert qual["decision"] == "reject"


def test_proof_pack_agent_smoke() -> None:
    out = ProofPackAgent.run({"customer_handle": "Acme"})
    assert out["proof_pack"]["customer_handle"] == "Acme"


def test_learning_agent_smoke() -> None:
    out = LearningAgent.run({"week_id": "2026-W21", "observations": ["won diagnostic"]})
    assert out["learning_report"]["week_id"] == "2026-W21"
