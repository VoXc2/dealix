"""Regression guards for the Dealix VPS automation runtime."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_bootstrap_is_repo_local_hash_gated_and_covers_runtime_dependencies() -> None:
    script = read("scripts/ops/ensure_founder_automation_python.sh")
    assert 'VENV="${DEALIX_AUTOMATION_VENV:-$ROOT/.venv}"' in script
    assert 'REQ="$ROOT/requirements-dev.txt"' in script
    assert 'REQ_BASE="$ROOT/requirements.txt"' in script
    assert 'sha256sum "$REQ" "$REQ_BASE" | sha256sum' in script
    assert 'mkdir -p "$VENV"' in script
    assert "flock -w 300" in script
    lock_pos = script.index("flock -w 300")
    create_pos = script.index('"$PYTHON_BOOTSTRAP" -m venv "$VENV"')
    assert lock_pos < create_pos
    assert "--no-input --no-cache-dir -r" in script
    assert "import fastapi" in script
    assert "import pydantic" in script
    assert "import pytest" in script
    assert "DEALIX_AUTOMATION_PYTHON=PASS" in script
    assert "DEALIX_AUTOMATION_PYTHON=FAIL_CLOSED" in script
    assert "sudo " not in script
    assert "apt-get" not in script


def test_money_command_binds_legacy_python_to_verified_venv() -> None:
    script = read("scripts/ops/dealix_founder_money_command.sh")
    assert "ensure_founder_automation_python.sh" in script
    assert 'PY="${DEALIX_AUTOMATION_PYTHON:-$REPO_ROOT/.venv/bin/python}"' in script
    assert 'python() { "$PY" "$@"; }' in script
    assert "command -v python" not in script


def test_revenue_cycle_uses_verified_venv_for_pydantic_paths() -> None:
    script = read("scripts/ops/dealix_canonical_revenue_cycle.sh")
    assert "ensure_founder_automation_python.sh" in script
    assert 'PY="${DEALIX_AUTOMATION_PYTHON:-$ROOT/.venv/bin/python}"' in script
    assert '"$PY" scripts/commercial/run_company_loop_simulation.py' in script
    assert "python3 scripts/commercial" not in script


def test_founder_weekly_verification_never_falls_back_to_system_python() -> None:
    verifier = read("scripts/verify_founder_operating_system.sh")
    weekly = read("scripts/founder_weekly_loop.sh")
    assert "ensure_founder_automation_python.sh" in verifier
    assert "import pydantic, pytest" in verifier
    assert "command -v python3" not in verifier
    verify_pos = weekly.index("verify_founder_operating_system.sh")
    python_pos = weekly.index('PY="${DEALIX_AUTOMATION_PYTHON:-$ROOT/.venv/bin/python}"')
    assert verify_pos < python_pos
    assert "command -v python3" not in weekly


def test_vps_control_is_noninteractive_and_uses_verified_python() -> None:
    script = read("scripts/ops/dealix_vps_control.sh")
    assert "ensure_founder_automation_python.sh" in script
    assert "gh auth setup-git" in script
    assert "GIT_TERMINAL_PROMPT=0 git fetch origin main --quiet" in script
    assert '"$PY" scripts/verify_full_autonomous_ops_stack.py' in script
    assert '"$PY" scripts/run_dealix_complete_autonomous_day.py' in script
    assert '"$PY" scripts/ops/dealix_daily_self_runner.py' in script
    assert '"$PY" scripts/commercial/run_sales_arena.py' in script


def test_runtime_compat_pins_company_services_to_repo_venv() -> None:
    script = read("scripts/ops/repair_dealix_vps_runtime_compat.sh")
    assert 'DROPIN_DIR="/etc/systemd/system/dealix-company@.service.d"' in script
    assert 'Environment="VIRTUAL_ENV=${VENV}"' in script
    assert "SYSTEMD_CANONICAL_PYTHON=PASS" in script
    assert "SERVICE_STYLE_PYTHON_IMPORTS=PASS" in script
    assert "HEARTBEAT_ACCEPT=PASS" in script
    assert "reset-failed" not in script
    assert "python3 -c 'import fastapi, pydantic, pytest" in script
    assert "python3 - <<" not in script


def test_runtime_compat_repairs_root_executive_runner_without_root_hermes() -> None:
    script = read("scripts/ops/repair_dealix_vps_runtime_compat.sh")
    assert 'HERMES="/home/${RUN_USER}/.local/bin/hermes"' in script
    assert "exec sudo -u dealix -H env" in script
    assert '"$HERMES" chat --query-file "$PROMPT_FILE"' in script
    assert '"$HERMES" chat -Q --ignore-rules --toolsets clarify --max-turns 1' in script
    assert "hermes --ignore-rules --toolsets clarify -z" not in script
    assert "DEALIX_HERMES_8K_OK" in script
    assert "HERMES_ACCEPT=FAIL_CLOSED" in script
    assert 'HERMES_ACCEPT_TIMEOUT="${HERMES_ACCEPT_TIMEOUT:-45}"' in script
    assert "timeout --signal=TERM --kill-after=10s" in script
    assert "DEGRADED_TIMEOUT" in script
    assert "timeout 300" not in script


def test_runtime_compat_does_not_add_forbidden_external_mutations() -> None:
    script = read("scripts/ops/repair_dealix_vps_runtime_compat.sh")
    forbidden = (
        "gh pr merge",
        "railway up",
        "railway deploy",
        "vercel --prod",
        "AUTO_SEND_ENABLED=true",
        "WHATSAPP_ALLOW_LIVE_SEND=true",
        "MOYASAR_LIVE_MODE=1",
    )
    for marker in forbidden:
        assert marker not in script
