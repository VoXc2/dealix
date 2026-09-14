from __future__ import annotations

from pathlib import Path

from dealix.commercial.delix_service_preparation import DelixServicePreparation, RESEARCH_ONLY
from dealix.commercial.economic_cell import Sector
from dealix.commercial.large_scale_sector_execution import LargeScaleSectorExecutor
from dealix.commercial.saudi_sector_targeting import SaudiSectorTargetingEngine

ROOT = Path(__file__).resolve().parents[1]


def _first_sector() -> Sector:
    return next(iter(Sector))


def test_service_preparation_does_not_mint_relationship_or_fixed_roster() -> None:
    sector = _first_sector()
    packet = DelixServicePreparation().prepare_for_person(
        "UNVERIFIED_RESEARCH_SUBJECT",
        sector,
        "UNVERIFIED_RESEARCH_COMPANY",
    )
    assert packet["commercial_status"] == RESEARCH_ONLY
    assert packet["communication"]["status"] == "DRAFT_ONLY"
    assert packet["communication"]["live_send_allowed"] is False
    assert packet["relationship_evidence_ref"] is None
    assert packet["consent_evidence_ref"] is None
    assert packet["truth_firewall"] == {
        "research_is_relationship": False,
        "public_contact_is_consent": False,
        "draft_is_sent": False,
        "quote_is_revenue": False,
    }
    logical_agents = packet["logical_agents"]
    assert logical_agents
    assert all(agent.startswith(f"dealix.{sector.value}.") for agent in logical_agents)
    assert "dealix-pm" not in logical_agents


def test_service_preparation_verify_is_registry_derived_and_zero_synthetic_relationships() -> None:
    receipt = DelixServicePreparation().verify()
    assert receipt["sectors"] == len(tuple(Sector))
    assert receipt["logical_agents"] > 5
    assert receipt["orphan_failures"] == []
    assert receipt["synthetic_relationships_created"] == 0
    assert receipt["live_outbound_authority"] is False
    assert receipt["fixed_five_authority"] is False
    assert receipt["global_deepwip3_authority"] is False


def test_large_scale_compatibility_surface_is_research_only() -> None:
    result = LargeScaleSectorExecutor().execute_sector(_first_sector(), people=1000)
    assert result.people_targeted == 0
    assert result.research_scope_requested == 1000
    assert result.relationship_count == 0
    assert result.consent_count == 0
    assert result.live_outbound_allowed is False
    assert result.tender_submission_allowed is False
    assert result.payment_sar is None
    assert result.device_ready is False
    assert result.no_ban is False
    assert result.authority_state == RESEARCH_ONLY
    assert "email_with_consent" not in result.channels_used


def test_team_queue_has_no_external_or_payment_authority() -> None:
    queue = LargeScaleSectorExecutor().team_authorization_queue()
    assert queue
    assert all(item["external_effect"] == "NONE" for item in queue)
    assert all(item["status"] in {"RESEARCH_ONLY", "DRAFT_ONLY"} for item in queue)
    joined = " ".join(item["task"].lower() for item in queue)
    assert "payment" not in joined
    assert "auto-ingest" not in joined
    assert "1000 per sector" not in joined


def test_sector_coverage_is_intelligence_not_relationship() -> None:
    engine = SaudiSectorTargetingEngine()
    targets = engine.target_all_saudi_sectors()
    assert len(targets) == len(tuple(Sector))
    assert all(target.evidence_state == RESEARCH_ONLY for target in targets)
    assert all(target.relationship_authority is False for target in targets)
    assert all(target.consent_authority is False for target in targets)
    assert all(target.outbound_authority is False for target in targets)
    assert all(target.real_effective is False for target in targets)
    receipt = engine.to_dict(targets)
    assert receipt["relationships_created"] == 0
    assert receipt["consent_created"] == 0
    assert receipt["outbound_authority"] is False


def test_active_commercial_modules_drop_legacy_bulk_and_fixed_authority_tokens() -> None:
    paths = [
        ROOT / "dealix/commercial/delix_service_preparation.py",
        ROOT / "dealix/commercial/large_scale_sector_execution.py",
        ROOT / "dealix/commercial/saudi_sector_targeting.py",
    ]
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in paths)
    forbidden = (
        "5 وكلاء + 8 موسعون",
        "payment_sar: float = 5.6",
        "scale to 1000 per sector",
        "etimad auto-ingest",
        "all companies in",
        "real_effective: bool = true",
    )
    for token in forbidden:
        assert token.lower() not in text
