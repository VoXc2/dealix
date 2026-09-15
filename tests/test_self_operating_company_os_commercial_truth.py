from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "commercial" / "run_self_operating_company_os.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("dealix_self_operating_company_os", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_runner_does_not_reintroduce_retired_fixed_price_authority() -> None:
    text = RUNNER.read_text(encoding="utf-8")
    for forbidden in (
        "499 SAR",
        "499-1,500 SAR",
        "4,999 SAR",
        "8,000-20,000 SAR",
        "10,000-50,000 SAR",
        "Revenue Proof Sprint",
        "Revenue Leak Diagnostic",
    ):
        assert forbidden not in text
    assert "Free Mini Diagnostic" in text
    assert "30-Day Revenue Command Pilot" in text


def test_runner_has_no_synthetic_default_target_fallback(tmp_path) -> None:
    module = load_runner()
    module.DATA_ROOT = tmp_path
    assert module.load_targets() == []
    assert module.build_target_cards(50) == []


def test_research_contact_cannot_enter_external_approval_queue(tmp_path) -> None:
    module = load_runner()
    module.DATA_ROOT = tmp_path
    target = {
        "company_name": "Evidence Research Co",
        "segment": "Saudi B2B",
        "source": "official-source",
        "evidence_refs": ["https://example.test/evidence"],
        "relationship_state": "RESEARCH",
        "consent_state": "NONE",
        "suppression_state": "CLEAR",
        "commercial_stage": "RESEARCH",
    }
    (tmp_path / "targets.json").write_text(json.dumps([target]), encoding="utf-8")
    cards = module.build_target_cards(50)
    assert len(cards) == 1
    assert cards[0].approval_status == "internal_only_not_dispatch_eligible"
    assert module.build_approval_queue(cards) == []


def test_real_interaction_can_prepare_draft_but_not_send(tmp_path) -> None:
    module = load_runner()
    module.DATA_ROOT = tmp_path
    target = {
        "company_name": "Warm Co",
        "segment": "Saudi B2B",
        "source": "first-party-interaction",
        "evidence_refs": ["interaction:123"],
        "relationship_state": "REAL_INTERACTION",
        "consent_state": "NONE",
        "suppression_state": "CLEAR",
        "commercial_stage": "REAL_INTERACTION",
        "pain_hypothesis": "Follow-up ownership is unclear.",
    }
    (tmp_path / "targets.json").write_text(json.dumps([target]), encoding="utf-8")
    cards = module.build_target_cards(50)
    queue = module.build_approval_queue(cards)
    assert len(queue) == 1
    assert queue[0]["status"] == "pending_action_bound_approval"
    assert "no_auto_send" in queue[0]["risk_flags"]


def test_executive_focus_is_state_driven_not_retired_ticket_authority(tmp_path) -> None:
    text = RUNNER.read_text(encoding="utf-8")
    for retired in ("#1494", "#1476", "#1121"):
        assert retired not in text
    for required in (
        "Production Trust: current exact-head acceptance + current-main Web/API release parity.",
        "Revenue/Customer: real interaction -> qualified problem -> Diagnostic -> customer-specific quote -> verified payment.",
        "Company/Scale: Deep-WIP <= 3",
        "Delivery/Proof: predefine acceptance and a customer-validated Proof Pack for paid work.",
        "Learning: convert root causes into bounded regression and evidence rules.",
    ):
        assert required in text

    module = load_runner()
    module.OUT_ROOT = tmp_path
    (tmp_path / "daily").mkdir(parents=True, exist_ok=True)
    report = module.write_daily_report([], [], [], [])
    rendered = report.read_text(encoding="utf-8")
    assert "SAFE_INTERNAL_AUTONOMY" in rendered
    assert "Production Trust: current exact-head acceptance" in rendered
    for retired in ("#1494", "#1476", "#1121"):
        assert retired not in rendered


def test_inbound_paid_collaboration_uses_review_lane_not_generic_diagnostic(tmp_path) -> None:
    module = load_runner()
    module.DATA_ROOT = tmp_path
    target = {
        "company_name": "iMini",
        "target_type": "inbound_paid_collaboration_pilot",
        "segment": "AI creator / marketing collaboration",
        "source": "gmail://thread/example",
        "evidence_refs": ["gmail:thread:example", "gmail:draft:current"],
        "relationship_state": "REAL_INTERACTION",
        "consent_state": "NONE",
        "suppression_state": "CLEAR",
        "commercial_stage": "SCRIPT_READY_FOR_REVIEW",
        "pain_hypothesis": "Scope, attribution, payment and performance-term clarity.",
        "recommended_offer": "Bounded paid collaboration pilot",
        "current_draft_ref": "gmail:draft:current",
        "pilot_fixed_fee_usd": 80,
        "payment_method": "PayPal",
    }
    (tmp_path / "targets.json").write_text(json.dumps([target]), encoding="utf-8")
    cards = module.build_target_cards(50)
    queue = module.build_approval_queue(cards)
    assert len(queue) == 1
    item = queue[0]
    assert item["target_type"] == "INBOUND_PAID_COLLABORATION_PILOT"
    assert item["action_type"] == "inbound_paid_collaboration_review"
    assert "Free Mini Diagnostic" not in item["draft_text"]
    assert "USD 80" in item["draft_text"]
    assert "PayPal" in item["draft_text"]
    assert "gmail:draft:current" in item["draft_text"]
    assert "founder-income collaboration" in item["draft_text"]
    assert item["status"] == "pending_action_bound_approval"
