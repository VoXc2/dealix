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


def test_resolve_hermes_owner_honors_env_override(monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_HERMES_USER", "dealix")
    assert scheduler_audit.resolve_hermes_owner() == "dealix"


def test_resolve_hermes_owner_is_none_for_non_root_without_override(monkeypatch) -> None:
    monkeypatch.delenv("DEALIX_HERMES_USER", raising=False)
    monkeypatch.setattr(scheduler_audit.os, "geteuid", lambda: 1000)
    assert scheduler_audit.resolve_hermes_owner() is None


def test_build_hermes_command_switches_to_canonical_owner(monkeypatch) -> None:
    monkeypatch.setattr(scheduler_audit, "resolve_hermes_owner", lambda: "dealix")
    monkeypatch.setattr(scheduler_audit.getpass, "getuser", lambda: "root")
    monkeypatch.setattr(scheduler_audit.shutil, "which", lambda name: "/usr/bin/sudo" if name == "sudo" else None)
    cmd = scheduler_audit.build_hermes_command("/home/dealix/.local/bin/hermes")
    assert cmd[:5] == ["sudo", "-n", "-u", "dealix", "-H"]
    assert cmd[-2:] == ["cron", "list"]


def test_build_hermes_command_stays_direct_for_owner(monkeypatch) -> None:
    monkeypatch.setattr(scheduler_audit, "resolve_hermes_owner", lambda: None)
    cmd = scheduler_audit.build_hermes_command("/home/dealix/.local/bin/hermes")
    assert cmd == ["/home/dealix/.local/bin/hermes", "cron", "list"]


def test_resolve_hermes_bin_falls_back_to_canonical_install(monkeypatch) -> None:
    monkeypatch.setattr(scheduler_audit.shutil, "which", lambda name: None)
    monkeypatch.setattr(scheduler_audit.os, "access", lambda path, mode: True)
    monkeypatch.setattr(scheduler_audit.Path, "is_file", lambda self: True)
    assert scheduler_audit.resolve_hermes_bin() == "/home/dealix/.local/bin/hermes"


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
