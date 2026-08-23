"""Regression guards for keeping mutable VPS operating state out of Git main."""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest


def test_runtime_root_redirects_mutable_commercial_paths(monkeypatch, tmp_path: Path) -> None:
    import dealix.commercial_ops.paths as paths

    monkeypatch.setenv("DEALIX_RUNTIME_STATE_ROOT", str(tmp_path))
    paths = importlib.reload(paths)
    try:
        assert paths.EVIDENCE_TRACKER_CSV == tmp_path / "commercial/evidence_events_tracker.csv"
        assert paths.SOCIAL_QUEUE_YAML == tmp_path / "commercial/social_content_queue.yaml"
        assert paths.WAR_ROOM_TODAY_JSON == tmp_path / "commercial/war_room_today.json"
        assert (
            paths.SOFT_LAUNCH_TRACKER_YAML
            == tmp_path / "commercial/soft_launch_meetings_tracker.yaml"
        )
        assert paths.FOUNDER_BRIEFS_DIR == tmp_path / "commercial/founder_briefs"
        assert paths.FOUNDER_DEBRIEFS_DIR == tmp_path / "commercial/founder_debriefs"
        assert paths.FOUNDER_WEEKLY_DECISION_DIR == tmp_path / "commercial/founder_weekly"
        assert (
            paths.DEALIX_DOGFOODING_WAR_ROOM_JSON
            == tmp_path / "commercial/dealix_dogfooding_war_room.json"
        )
        assert (
            paths.FOUNDER_AGENT_QUEUE_TODAY_JSON
            == tmp_path / "commercial/founder_agent_queue_today.json"
        )
        assert paths.display_path(paths.EVIDENCE_TRACKER_CSV) == str(
            tmp_path / "commercial/evidence_events_tracker.csv"
        ).replace("\\", "/")
    finally:
        monkeypatch.delenv("DEALIX_RUNTIME_STATE_ROOT", raising=False)
        importlib.reload(paths)


def test_runtime_overrides_fail_closed_if_they_resolve_into_git(monkeypatch) -> None:
    import dealix.commercial_ops.paths as paths

    monkeypatch.setenv("DEALIX_RUNTIME_STATE_ROOT", str(paths.REPO_ROOT / "data/runtime-state"))
    with pytest.raises(RuntimeError, match="outside canonical repository"):
        importlib.reload(paths)
    monkeypatch.delenv("DEALIX_RUNTIME_STATE_ROOT", raising=False)
    importlib.reload(paths)

    monkeypatch.setenv(
        "DEALIX_EVIDENCE_TRACKER_CSV",
        str(paths.REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"),
    )
    with pytest.raises(RuntimeError, match="outside canonical repository"):
        importlib.reload(paths)
    monkeypatch.delenv("DEALIX_EVIDENCE_TRACKER_CSV", raising=False)
    importlib.reload(paths)


def test_runtime_root_rejects_symlink_back_into_git(monkeypatch, tmp_path: Path) -> None:
    import dealix.commercial_ops.paths as paths

    link = tmp_path / "repo-link"
    try:
        link.symlink_to(paths.REPO_ROOT, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable on this platform")

    monkeypatch.setenv("DEALIX_RUNTIME_STATE_ROOT", str(link / "runtime"))
    with pytest.raises(RuntimeError, match="outside canonical repository"):
        importlib.reload(paths)
    monkeypatch.delenv("DEALIX_RUNTIME_STATE_ROOT", raising=False)
    importlib.reload(paths)


def test_default_paths_remain_backward_compatible(monkeypatch) -> None:
    monkeypatch.delenv("DEALIX_RUNTIME_STATE_ROOT", raising=False)
    monkeypatch.delenv("DEALIX_EVIDENCE_TRACKER_CSV", raising=False)
    import dealix.commercial_ops.paths as paths

    paths = importlib.reload(paths)
    assert paths.EVIDENCE_TRACKER_CSV == paths.CANONICAL_EVIDENCE_TRACKER_CSV
    assert paths.SOCIAL_QUEUE_YAML == paths.CANONICAL_SOCIAL_QUEUE_YAML
    assert paths.WAR_ROOM_TODAY_JSON == paths.CANONICAL_WAR_ROOM_TODAY_JSON
    assert paths.SOFT_LAUNCH_TRACKER_YAML == paths.CANONICAL_SOFT_LAUNCH_TRACKER_YAML


def test_first_paid_reader_uses_same_runtime_evidence_authority() -> None:
    root = Path(__file__).resolve().parents[1]
    text = (root / "dealix/commercial_ops/first_paid_tracker.py").read_text(encoding="utf-8")
    assert "EVIDENCE = EVIDENCE_TRACKER_CSV" in text
    assert "SOFT_LAUNCH_TRACKER = SOFT_LAUNCH_TRACKER_YAML" in text
    assert 'REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"' not in text


def test_runtime_facing_renderers_do_not_assume_outputs_live_under_repo() -> None:
    root = Path(__file__).resolve().parents[1]
    files = (
        "dealix/commercial_ops/full_ops_autopilot.py",
        "dealix/commercial_ops/digest.py",
        "dealix/commercial_ops/founder_debrief.py",
        "dealix/commercial_ops/founder_comprehensive_plan.py",
        "dealix/commercial_ops/founder_agent_tasks.py",
        "dealix/commercial_ops/value_plan.py",
        "dealix/commercial_ops/value_map_status.py",
        "dealix/commercial_ops/autonomous_ops.py",
        "dealix/commercial_ops/unified_founder_day.py",
        "dealix/commercial_ops/founder_strongest_ops.py",
        "dealix/commercial_ops/complete_autonomous_day.py",
        "dealix/commercial_ops/founder_master_strategic_os.py",
    )
    for rel in files:
        text = (root / rel).read_text(encoding="utf-8")
        assert "relative_to(REPO_ROOT)" not in text, rel


def test_vps_installer_is_atomic_conflict_aware_and_has_no_l5_actions() -> None:
    root = Path(__file__).resolve().parents[1]
    installer = (root / "scripts/ops/install_dealix_runtime_state_isolation.sh").read_text(
        encoding="utf-8"
    )
    assert "DEALIX_RUNTIME_STATE_ROOT" in installer
    assert "DEALIX_MONEY_REPORT_ROOT" in installer
    assert "DEALIX_REVENUE_CYCLE_OUT" in installer
    assert "runtime-state.env" in installer
    assert "20-runtime-state.conf" in installer
    assert "PRESERVED_EXISTING" in installer
    assert "BindPaths=" in installer
    assert "COMPAT_BIND_UNTIL_PATCH_MERGED" in installer
    assert "RUNTIME_PATH_REDIRECTION=PASS" in installer
    assert "systemd-analyze verify" in installer
    assert "tracked_reports_tree_shadowed=false" in installer
    assert 'append_bind "$STATE_ROOT/reports" "$REPO_ROOT/reports"' not in installer
    assert "$STATE_ROOT/reports/founder_money_command" in installer
    assert "$STATE_ROOT/reports/canonical_revenue_cycle" in installer

    # An override must never silently route mutable state back into Git.
    assert 'REPO_ROOT_REAL="$(readlink -f "$REPO_ROOT")"' in installer
    assert 'STATE_ROOT_REAL="$(readlink -m "$STATE_ROOT")"' in installer
    assert 'CONTROL_ROOT_REAL="$(readlink -m "$CONTROL_ROOT")"' in installer
    assert "runtime-state root must not be filesystem root" in installer
    assert "runtime-state root must remain outside canonical repository" in installer
    assert "control root must remain outside canonical repository" in installer
    guard_pos = installer.index('case "$STATE_ROOT_REAL" in')
    mutation_pos = installer.index('install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER"')
    assert guard_pos < mutation_pos

    # Existing live processes/timers must not be declared migrated after only a
    # daemon-reload; the recovery transaction quiesces them first.
    assert "RUNTIME_NAMESPACE_ADOPTION=PREFLIGHT_QUIESCED" in installer
    assert "runtime namespace adoption pending" in installer
    active_guard_pos = installer.index("ACTIVE_COMPANY_SERVICES=")
    mutation_pos = installer.index('install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER"')
    assert active_guard_pos < mutation_pos

    # A dirty canonical copy that disagrees with existing runtime state must not
    # silently lose either side. Atomic config rollback must restore prior files.
    assert "dirty canonical/runtime conflict requires recovery reconciliation" in installer
    assert "runtime_state_config_rollback=START" in installer
    assert "runtime_state_config_rollback=COMPLETE" in installer
    assert "CONFIG_ARMED=1" in installer
    assert 'install -D -m 0640 -o root -g "$RUN_USER" "$ENV_STAGE" "$ENV_FILE"' in installer
    assert 'install -D -m 0644 -o root -g root "$DROPIN_STAGE" "$DROPIN"' in installer
    rollback_pos = installer.index("rollback_config()")
    install_pos = installer.index('install -D -m 0640 -o root -g "$RUN_USER" "$ENV_STAGE" "$ENV_FILE"')
    success_pos = installer.index("SUCCESS=1")
    assert rollback_pos < install_pos < success_pos

    for forbidden in (
        "gh pr merge",
        "railway up",
        "railway deploy",
        "vercel --prod",
        "WHATSAPP_ALLOW_LIVE_SEND=true",
        "AUTO_SEND_ENABLED=true",
        "MOYASAR_LIVE_MODE=1",
    ):
        assert forbidden not in installer


def test_direct_vps_control_loads_validated_runtime_state_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    control = (root / "scripts/ops/dealix_vps_control.sh").read_text(encoding="utf-8")

    assert 'RUNTIME_ENV="/opt/dealix/control/runtime-state.env"' in control
    assert "load_runtime_state_env()" in control
    assert '[[ -f "$RUNTIME_ENV" && ! -L "$RUNTIME_ENV" ]]' in control
    assert 'stat -c \'%u\' "$RUNTIME_ENV"' in control
    assert "must be owned by root" in control
    assert "must not be group/world writable" in control
    assert "DEALIX_RUNTIME_STATE_ROOT|DEALIX_MONEY_REPORT_ROOT|DEALIX_REVENUE_CYCLE_OUT" in control
    assert "unexpected runtime-state env key" in control
    assert "runtime-state path resolves inside canonical repo" in control
    assert '. "$RUNTIME_ENV"' not in control

    load_pos = control.index("load_runtime_state_env\n")
    case_pos = control.index('case "$COMMAND" in')
    daily_pos = control.index("  daily)")
    arena_pos = control.index("  sales-arena)")
    assert load_pos < case_pos < daily_pos < arena_pos


def test_activation_propagates_runtime_contract_and_preserves_hermes() -> None:
    root = Path(__file__).resolve().parents[1]
    activation = (root / "scripts/ops/activate_dealix_from_main.sh").read_text(encoding="utf-8")

    assert 'RUNTIME_ENV="/opt/dealix/control/runtime-state.env"' in activation
    assert "load_runtime_state_contract()" in activation
    assert '. "$RUNTIME_ENV"' not in activation
    assert "ACTIVATION_RUNTIME_STATE=FAIL_CLOSED" in activation
    assert "revenue_cycle=SKIP_FAIL_CLOSED_NO_RUNTIME_STATE" in activation
    assert "founder_money=SKIP_FAIL_CLOSED_NO_RUNTIME_STATE" in activation
    assert 'DEALIX_RUNTIME_STATE_ROOT="$RUNTIME_STATE_ROOT"' in activation
    assert 'DEALIX_MONEY_REPORT_ROOT="$MONEY_REPORT_ROOT"' in activation
    assert 'DEALIX_REVENUE_CYCLE_OUT="$REVENUE_CYCLE_OUT"' in activation
    assert "systemctl disable --now hermes-dealix.service" not in activation
    assert "restore_hermes_posture()" in activation
    assert "HERMES_QUIESCED=1" in activation
    assert "HERMES_ENTRY_ACTIVE" in activation
    assert "HERMES_FINAL_ACTIVE" in activation
    cleanup_pos = activation.index("trap cleanup EXIT")
    stop_pos = activation.index("systemctl stop hermes-dealix.service")
    assert cleanup_pos < stop_pos


def test_full_recovery_is_single_flight_conflict_aware_and_preserves_hermes_architecture() -> None:
    root = Path(__file__).resolve().parents[1]
    recovery = (root / "scripts/ops/dealix_full_vps_recovery.sh").read_text(encoding="utf-8")

    # A global lock must be held before any timer/state/repository mutation.
    assert 'LOCK="/run/lock/dealix-full-vps-recovery.lock"' in recovery
    assert "DEALIX_FULL_RECOVERY=BLOCKED_ALREADY_RUNNING" in recovery
    lock_pos = recovery.index("flock -n 9")
    proof_mutation_pos = recovery.index('mkdir -p "$PROOF"')
    quiesce_pos = recovery.index('section "1. QUIESCE REPO WRITERS"')
    assert lock_pos < proof_mutation_pos < quiesce_pos

    # Existing runtime state is authoritative when canonical input is clean;
    # conflicting dirty canonical state fails closed before the stash.
    assert "decision=PRESERVED_EXISTING" in recovery
    assert "decision=SEEDED_FROM_CURRENT_SOURCE" in recovery
    assert "decision=CONFLICT_DIRTY_CANONICAL" in recovery
    assert "dirty canonical/runtime state conflict requires explicit reconciliation" in recovery
    assert "source_sha=" in recovery and "target_sha=" in recovery

    # Recovery must not make an architecture decision by disabling a healthy
    # Hermes gateway. It records entry/final posture instead.
    assert "systemctl disable --now hermes-dealix.service" not in recovery
    assert "HERMES_MODE=ONE_SHOT_ONLY" not in recovery
    assert "HERMES_MODE=PRESERVE_EXISTING_GATEWAY_POSTURE" in recovery
    assert "HERMES_GATEWAY_ENTRY" in recovery
    assert "HERMES_GATEWAY_FINAL" in recovery

    # Exact-head staged verification includes the consumers that used to assume
    # runtime artifacts were repo-relative and the direct activation path.
    for rel in (
        "dealix/commercial_ops/first_paid_tracker.py",
        "dealix/commercial_ops/founder_comprehensive_plan.py",
        "dealix/commercial_ops/value_plan.py",
        "dealix/commercial_ops/autonomous_ops.py",
        "scripts/ops/activate_dealix_from_main.sh",
        "scripts/ops/dealix_vps_control.sh",
    ):
        assert rel in recovery

    # Post-repair proof uses the same private bundled Node runtime contract as
    # #1150 rather than falling back to the login-shell PATH.
    assert "OPENCLAW_NODE_DIR=" in recovery
    assert 'find /home/dealix/.openclaw/tools' in recovery
    assert 'PATH="$OPENCLAW_PATH" "$OPENCLAW" gateway status --require-rpc' in recovery

    for forbidden in (
        "gh pr merge",
        "railway up",
        "railway deploy",
        "vercel --prod",
        "AUTO_SEND_ENABLED=true",
        "WHATSAPP_ALLOW_LIVE_SEND=true",
        "MOYASAR_LIVE_MODE=1",
    ):
        assert forbidden not in recovery


def test_soft_launch_tracker_uses_governed_runtime_path() -> None:
    root = Path(__file__).resolve().parents[1]
    script = (root / "scripts/prepare_soft_launch_meetings.py").read_text(encoding="utf-8")
    assert "SOFT_LAUNCH_TRACKER_YAML" in script
    assert "TRACKER = SOFT_LAUNCH_TRACKER_YAML" in script
    assert "WAR_ROOM_TODAY_JSON" in script
    assert 'os.environ.get("DEALIX_SOFT_LAUNCH_TRACKER")' not in script
