from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTOPILOT = ROOT / "scripts" / "ops" / "dealix_company_autopilot.sh"
LEGACY = ROOT / "scripts" / "ops" / "dealix_company_autopilot_legacy.sh"
INSTALLER = ROOT / "scripts" / "ops" / "install_dealix_company_autopilot.sh"
DISPATCHER = ROOT / "scripts" / "ops" / "dealix_vps_control.sh"
BRIDGE = ROOT / "scripts" / "ops" / "dealix_vps_issue_bridge.py"


def text(path: Path) -> str:
    assert path.is_file(), f"missing {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def operational_text() -> str:
    """The release-truth wrapper delegates non-production modes to legacy."""
    return text(AUTOPILOT) + "\n" + text(LEGACY)


def test_autopilot_has_hard_external_safety_flags() -> None:
    body = operational_text()
    required = (
        "DEALIX_EXTERNAL_OUTREACH_ENABLED=false",
        "EXTERNAL_OUTREACH_ENABLED=false",
        "AUTO_SEND_ENABLED=false",
        "AGENT_APPROVAL_MODE=required",
        "WHATSAPP_ALLOW_LIVE_SEND=false",
        "MOYASAR_LIVE_MODE=0",
    )
    for token in required:
        assert token in body


def test_autopilot_does_not_contain_l5_execution_primitives() -> None:
    body = operational_text()
    forbidden = (
        "gh pr merge",
        "git push --force",
        "railway up",
        "railway redeploy",
        "railway variables set",
        "vercel --prod",
        "docker system prune -a",
        "moyasar_live_cutover",
    )
    for token in forbidden:
        assert token not in body, f"unsafe primitive present: {token}"


def test_autopilot_runtime_checks_are_strict_and_redacted() -> None:
    body = operational_text()
    assert "is_http_ok" in body
    assert "^[23][0-9][0-9]$" in body
    assert "=~ ^2|3" not in body
    assert "[EMAIL_REDACTED]" in body
    assert "[PHONE_REDACTED]" in body
    assert "printf '%b\\n'" in body


def test_autopilot_reuses_existing_github_schedules_instead_of_duplicate_morning_run() -> None:
    body = operational_text()
    installer = text(INSTALLER)
    assert "workflow_success_today daily-revenue-machine.yml" in body
    assert "workflow_success_today governed-full-ops-daily.yml" in body
    assert "SKIP: Daily Revenue Machine already succeeded today" in body
    assert "SKIP: Governed Full Ops already succeeded today" in body
    assert "morning-fallback" in installer
    assert "08:45:00 Asia/Riyadh" in installer


def test_installer_has_continuous_and_business_cadence() -> None:
    body = text(INSTALLER)
    for expected in (
        "write_interval_timer heartbeat 2min 5min 15s",
        "write_interval_timer production 3min 15min 30s",
        "06:30:00 Asia/Riyadh",
        "08:45:00 Asia/Riyadh",
        "12:30:00 Asia/Riyadh",
        "19:00:00 Asia/Riyadh",
        "21:15:00 Asia/Riyadh",
        "23:30:00 Asia/Riyadh",
        "Sat *-*-* 21:00:00 Asia/Riyadh",
    ):
        assert expected in body


def test_installer_bootstraps_runtime_dependencies_and_releases_64k_benchmark() -> None:
    body = text(INSTALLER)
    for expected in ("missing_pkgs+=(curl)", "missing_pkgs+=(jq)", "missing_pkgs+=(util-linux)"):
        assert expected in body
    assert "--no-install-recommends" in body
    assert "ollama stop dealix-qwen3-4b-64k" in body
    assert "bash -n \"$TMP_AUTOPILOT\"" in body
    assert "bash -n \"$TMP_BRIDGE_INSTALLER\"" in body


def test_installer_makes_local_ai_8k_hardening_reinstall_safe() -> None:
    body = text(INSTALLER)
    assert 'SAFE_LOCAL_MODEL="qwen3:4b-instruct-2507-q4_K_M"' in body
    assert 'OLLAMA_SAFE_DROPIN="${OLLAMA_DROPIN_DIR}/90-dealix-safe-ai.conf"' in body
    assert 'Environment="OLLAMA_HOST=127.0.0.1:11434"' in body
    assert 'Environment="OLLAMA_KEEP_ALIVE=2m"' in body
    assert 'Environment="OLLAMA_MAX_LOADED_MODELS=1"' in body
    assert 'Environment="OLLAMA_NUM_PARALLEL=1"' in body
    assert 'Environment="OLLAMA_CONTEXT_LENGTH=8192"' in body
    assert "MemoryMax=8G" in body
    assert 'DEALIX_LOCAL_MODEL=${SAFE_LOCAL_MODEL}' in body
    assert 'OPENAI_MODEL=${SAFE_LOCAL_MODEL}' in body
    assert 'LOCAL_MODEL_FALLBACK="dealix-qwen3-4b-64k"' in body
    assert 'BLOCKED: unsafe 64K fallback remains' in body
    assert 'BLOCKED: effective Ollama context is not pinned to 8192' in body
    assert 'BLOCKED: Ollama is not pinned to loopback' in body


def test_local_ai_is_local_only_and_releases_model() -> None:
    body = operational_text()
    assert "http://127.0.0.1:11434/api/chat" in body
    assert '"num_ctx": 8192' in body
    assert '"keep_alive": "10m"' in body
    assert 'ollama stop "$model"' in body
    assert "Do not invent customers, revenue, payments, results, or proof" in body
    assert "sed 's/:latest$//'" in body


def test_bridge_exposes_only_named_autopilot_modes() -> None:
    bridge = text(BRIDGE)
    dispatcher = text(DISPATCHER)
    for command in (
        "autopilot-status",
        "autopilot-heartbeat",
        "autopilot-production",
        "autopilot-repo-watch",
        "autopilot-preflight",
        "autopilot-morning-fallback",
        "autopilot-midday",
        "autopilot-evening",
        "autopilot-nightly",
        "autopilot-weekly",
        "autopilot-local-ai",
    ):
        assert f'"{command}"' in bridge
        assert command in dispatcher
    assert "eval " not in dispatcher
    assert "bash -c \"$" not in dispatcher
