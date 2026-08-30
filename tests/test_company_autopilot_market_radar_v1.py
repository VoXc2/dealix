from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTOPILOT = ROOT / "scripts" / "ops" / "dealix_company_autopilot.sh"


def test_autopilot_market_radar_mode_is_syntax_valid_and_fail_closed() -> None:
    result = subprocess.run(
        ["bash", "-n", str(AUTOPILOT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr

    script = AUTOPILOT.read_text(encoding="utf-8")
    assert "market-radar) market_radar ;;" in script
    assert "market_radar_run" in script
    assert "DEALIX_MARKET_RADAR_SIGNALS_FILE" in script
    assert "MARKET_RADAR_STATE=WAITING_FOR_CANONICAL_SIGNAL_INPUT" in script
    assert 'market-radar) FLEET_EVENT="heartbeat"' in script
    assert "systemctl enable" not in script
    assert "crontab -e" not in script


def test_autopilot_market_radar_produces_read_only_brief_from_handoff(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    input_path = inbox / "market-radar-signals.json"
    input_path.write_text(
        json.dumps(
            {
                "signals": [
                    {
                        "signal_id": "autopilot-test-signal",
                        "source_id": "AHREFS",
                        "source_ref": "ahrefs://test/query",
                        "observed_at": "2026-08-30T10:00:00+00:00",
                        "ingested_at": "2026-08-30T10:01:00+00:00",
                        "provenance_ref": "ahrefs://test/provenance",
                        "fresh_until": "2030-01-01T00:00:00+00:00",
                        "signal_family": "SEARCH_DEMAND",
                        "market": "SA",
                        "sector_family": "ICT",
                        "business_archetype": "RECURRING_SAAS_OR_SERVICES",
                        "company_or_subject": "Synthetic test signal",
                        "evidence_refs": ["test-evidence://signal"],
                        "facts": ["synthetic test observation"],
                        "inferences": ["research-only hypothesis"],
                        "unknowns": ["buyer", "relationship", "purchase intent"],
                        "risk_class": "LOW",
                        "allowed_use": "SEO_AEO_AND_CONTENT_HYPOTHESIS",
                        "next_evidence": ["validate buyer question"],
                        "authority": {
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
                        },
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
                ]
            }
        ),
        encoding="utf-8",
    )

    autopilot_root = tmp_path / "autopilot"
    env = dict(os.environ)
    env.update(
        {
            "DEALIX_REPO_ROOT": str(ROOT),
            "DEALIX_AUTOPILOT_ROOT": str(autopilot_root),
            "DEALIX_MARKET_RADAR_INBOX_DIR": str(inbox),
            "DEALIX_MARKET_RADAR_SIGNALS_FILE": str(input_path),
        }
    )
    result = subprocess.run(
        ["bash", str(AUTOPILOT), "market-radar"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DEALIX_UNIVERSAL_MARKET_RADAR_RUNNER=PASS" in result.stdout
    assert "MARKET_RADAR_INPUT=SOURCE_BOUND_HANDOFF" in result.stdout

    reports = sorted((autopilot_root / "reports").glob("universal-market-radar-*.json"))
    assert len(reports) == 1
    brief = json.loads(reports[0].read_text(encoding="utf-8"))
    assert brief["admitted_signal_count"] == 1
    assert brief["invalid_signal_count"] == 0
    assert brief["new_scheduler"] is False
    assert brief["new_permanent_agent"] is False
    assert brief["external_send_or_spend"] is False
    assert not any(brief["authority"].values())
