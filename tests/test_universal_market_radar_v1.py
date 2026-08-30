from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from dealix.commercial.portfolio_router import DemandSignal, EntryPackage, PortfolioPackageRouter

ROOT = Path(__file__).resolve().parents[1]

AUTHORITY = {
    "relationship": False,
    "consent": False,
    "offer": False,
    "price": False,
    "quote": False,
    "contract": False,
    "external_send": False,
    "payment": False,
    "customer_proof": False,
    "execution": False,
    "production": False,
}


def run(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(ROOT) + (os.pathsep + existing if existing else "")
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_universal_market_radar_verifier_passes() -> None:
    result = run("scripts/verify_universal_market_radar.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DEALIX_UNIVERSAL_MARKET_RADAR_VERDICT=PASS" in result.stdout
    assert "SIGNAL_SELF_PROMOTION=BLOCKED" in result.stdout
    assert "EXTERNAL_SEND_SPEND_PAYMENT_PRODUCTION_AUTHORITY=NO" in result.stdout


def test_strategic_ai_demand_families_route_to_bounded_company_brain() -> None:
    router = PortfolioPackageRouter()
    cases = [
        ("decision-intelligence", ["decision_intelligence"], "We need decision intelligence."),
        ("tender-intelligence", ["tender_intelligence"], "We need tender intelligence."),
        ("customer-operations", ["customer_operations"], "We need customer operations intelligence."),
        ("knowledge-management", ["knowledge_management"], "We need governed knowledge management."),
        ("document-intelligence", ["document_intelligence"], "We need document intelligence."),
        ("arabic-decision", [], "نحتاج ذكاء القرارات داخل الشركة."),
    ]

    for case_id, capabilities, statement in cases:
        decision = router.route(
            DemandSignal(
                signal_id=f"strategic-{case_id}",
                company_name="Strategic Demand Co",
                source_ref=f"inbound://source/{case_id}",
                observed_at="2026-08-29T10:00:00+00:00",
                evidence_refs=[f"evidence://inbound/{case_id}"],
                real_interaction_state="EXPLICIT_INBOUND",
                explicit_inbound_ref=f"inbound://message/{case_id}",
                consent_state="CONSENTED",
                problem_statement=statement,
                requested_capabilities=capabilities,
                urgency="HIGH",
                economic_relevance="HIGH",
                risk_class="STANDARD",
            )
        )
        assert decision.recommended_package == EntryPackage.COMPANY_BRAIN, case_id
        assert decision.authority_class == "PACKAGE_HYPOTHESIS_ONLY", case_id
        assert decision.next_action == "RUN_COMPANY_BRAIN_SPRINT_ASSESSMENT", case_id
        assert not any(decision.authority.values()), case_id


def _rankable_signal(source_id: str = "COMPANY_OWNED_WEB") -> dict:
    return {
        "signal_id": f"signal-{source_id.lower()}-1",
        "source_id": source_id,
        "source_ref": "https://example.com/official-company-update",
        "observed_at": "2026-08-30T10:00:00+00:00",
        "ingested_at": "2026-08-30T10:01:00+00:00",
        "provenance_ref": "https://example.com/official-company-update#snapshot-2026-08-30",
        "fresh_until": "2026-09-02T10:00:00+00:00",
        "signal_family": "COMPANY_CHANGE",
        "market": "SA",
        "sector_family": "ICT",
        "business_archetype": "RECURRING_SAAS_OR_SERVICES",
        "company_or_subject": "Synthetic unit-test public company change",
        "evidence_refs": ["test-evidence://company-owned-web/update-1"],
        "facts": ["synthetic unit-test source observation only"],
        "inferences": ["account research hypothesis"],
        "unknowns": ["buyer identity", "relationship", "purchase intent"],
        "risk_class": "LOW",
        "allowed_use": "ACCOUNT_RESEARCH",
        "next_evidence": ["reverify official source", "map business implication"],
        "authority": AUTHORITY,
        "priority_factors": {
            "economic_pain": 4,
            "measurable_outcome": 4,
            "buyer_access": 3,
            "data_availability": 4,
            "repeatability": 5,
            "readiness": 5,
            "distribution_density": 4,
            "regulatory_friction": 2,
            "integration_complexity": 2,
            "founder_minutes": 2,
        },
    }


def test_read_only_runner_ranks_research_without_authority(tmp_path: Path) -> None:
    signals = {"signals": [_rankable_signal()]}
    input_path = tmp_path / "signals.json"
    output_path = tmp_path / "brief.json"
    input_path.write_text(json.dumps(signals), encoding="utf-8")

    result = run(
        "scripts/commercial/run_universal_market_radar_v1.py",
        "--signals",
        str(input_path),
        "--out",
        str(output_path),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DEALIX_UNIVERSAL_MARKET_RADAR_RUNNER=PASS" in result.stdout

    brief = json.loads(output_path.read_text(encoding="utf-8"))
    assert brief["schema"] == "dealix.universal-market-radar-brief.v1"
    assert brief["admitted_signal_count"] == 1
    assert brief["invalid_signal_count"] == 0
    assert "AHREFS" in brief["blocked_source_ids"]
    assert brief["blocked_source_semantics"] == "BLOCKED_CAPABILITY_IS_UNKNOWN_NOT_ZERO_DEMAND"
    row = brief["ranked_research_signals"][0]
    assert isinstance(row["priority_score"], (int, float))
    assert row["priority_score_semantics"] == "INTERNAL_RESEARCH_PRIORITY_ONLY_NOT_PURCHASE_PROBABILITY"
    assert not any(row["authority"].values())
    assert not any(brief["authority"].values())
    assert brief["external_send_or_spend"] is False
    assert brief["new_scheduler"] is False


def test_runner_rejects_currently_blocked_ahrefs_source(tmp_path: Path) -> None:
    signal = _rankable_signal("AHREFS")
    signal.update(
        {
            "source_ref": "ahrefs://keywords/ai-automation-sa",
            "provenance_ref": "ahrefs://query/2026-08-30/ai-automation-sa",
            "signal_family": "SEARCH_DEMAND",
            "allowed_use": "SEO_AEO_AND_CONTENT_HYPOTHESIS",
        }
    )
    input_path = tmp_path / "signals.json"
    output_path = tmp_path / "brief.json"
    input_path.write_text(json.dumps({"signals": [signal]}), encoding="utf-8")

    result = run(
        "scripts/commercial/run_universal_market_radar_v1.py",
        "--signals",
        str(input_path),
        "--out",
        str(output_path),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    brief = json.loads(output_path.read_text(encoding="utf-8"))
    assert brief["admitted_signal_count"] == 0
    assert brief["invalid_signal_count"] == 1
    row = brief["invalid_signals"][0]
    assert row["status"] == "INVALID_NOT_ADMITTED_TO_RADAR"
    assert any("AHREFS:BLOCKED_CAPABILITY:INSUFFICIENT_PLAN" in error for error in row["errors"])
    assert brief["blocked_source_semantics"] == "BLOCKED_CAPABILITY_IS_UNKNOWN_NOT_ZERO_DEMAND"


def test_runner_rejects_unknown_source_and_missing_receipt_fields(tmp_path: Path) -> None:
    input_path = tmp_path / "signals.json"
    output_path = tmp_path / "brief.json"
    input_path.write_text(
        json.dumps(
            {
                "signals": [
                    {
                        "signal_id": "bad-1",
                        "source_id": "UNADMITTED_SCRAPER",
                        "source_ref": "scraper://1",
                        "authority": AUTHORITY,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = run(
        "scripts/commercial/run_universal_market_radar_v1.py",
        "--signals",
        str(input_path),
        "--out",
        str(output_path),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    brief = json.loads(output_path.read_text(encoding="utf-8"))
    assert brief["admitted_signal_count"] == 0
    assert brief["invalid_signal_count"] == 1
    assert brief["invalid_signals"][0]["status"] == "INVALID_NOT_ADMITTED_TO_RADAR"
    assert any("source_id is not admitted" in error for error in brief["invalid_signals"][0]["errors"])
