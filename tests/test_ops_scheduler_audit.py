"""Contracts for the deterministic scheduler audit (one job, one owner)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scheduler_audit = _load("audit_dealix_schedulers")

HERMES_TEXT = """
  34d8d39ce69f [active]
    Name:      Dealix Founder Intelligence
    Schedule:  0 8 * * *
    Repeat:    ∞
    Script:    dealix_founder_evidence_packet.sh
    Mode:      no-agent (script stdout delivered directly)

  57e1e378691c [active]
    Name:      Dealix Learning Distillation
    Schedule:  0 20 * * *
    Repeat:    ∞
    Script:    dealix_learning_evidence_packet.sh
"""


def test_parse_hermes_cron_extracts_owner_name_schedule_target() -> None:
    jobs = scheduler_audit.parse_hermes_cron(HERMES_TEXT)
    assert len(jobs) == 2
    assert jobs[0]["owner"] == "hermes"
    assert jobs[0]["name"] == "Dealix Founder Intelligence"
    assert jobs[0]["schedule"] == "0 8 * * *"
    assert jobs[0]["target"] == "dealix_founder_evidence_packet.sh"
    assert jobs[1]["target"] == "dealix_learning_evidence_packet.sh"


def test_parse_exec_start_prefers_argv_and_falls_back_to_path() -> None:
    argv_line = "ExecStart={ path=/usr/local/bin/run ; argv[]=/usr/local/bin/run --flag ; ignore_errors=no }"
    assert scheduler_audit.parse_exec_start(argv_line) == "/usr/local/bin/run --flag"
    path_line = "ExecStart={ path=/usr/local/bin/only ; ignore_errors=no }"
    assert scheduler_audit.parse_exec_start(path_line) == "/usr/local/bin/only"
    assert scheduler_audit.parse_exec_start("") == "UNKNOWN"


def test_duplicate_targets_are_detected() -> None:
    jobs = [
        {"owner": "systemd", "name": "a", "target": "/usr/local/sbin/dealix-watch"},
        {"owner": "systemd", "name": "b", "target": "/opt/bin/dealix-watch"},
        {"owner": "hermes", "name": "c", "target": "dealix-founder.sh"},
    ]
    duplicates = scheduler_audit.find_duplicate_targets(jobs)
    assert duplicates == [{"target": "dealix-watch", "owners": ["a", "b"]}]


def test_overlap_candidates_group_same_responsibility_keyword() -> None:
    jobs = [
        {"owner": "systemd", "name": "dealix-live-watch.service", "target": "/usr/local/bin/dealix-live-watch"},
        {"owner": "systemd", "name": "dealix-omega-watch.service", "target": "/usr/local/sbin/dealix-omega-watch"},
    ]
    overlaps = scheduler_audit.find_overlap_candidates(jobs)
    assert any(item["keyword"] == "watch" and len(item["jobs"]) == 2 for item in overlaps)


def test_build_audit_warns_only_on_duplicates() -> None:
    unique = scheduler_audit.build_audit([{"owner": "systemd", "name": "one", "target": "/bin/one"}])
    assert unique["verdict"] == "PASS"
    duplicate = scheduler_audit.build_audit(
        [
            {"owner": "systemd", "name": "one", "target": "/bin/same"},
            {"owner": "systemd", "name": "two", "target": "/other/same"},
        ]
    )
    assert duplicate["verdict"] == "WARN"
    assert duplicate["duplicate_targets"]
