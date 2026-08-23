"""Regression guards for the Dealix VPS automation runtime."""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _local_ai_gate_block(script: str) -> str:
    start = script.index('section "6. PRE-LOAD RESOURCE GUARD + CONSTRAINED LOCAL MODEL ACCEPTANCE"')
    end = script.index(
        '\nif [[ "$OLLAMA_MINIMAL_ACCEPT" == "PASS" && "$HERMES_ACCEPT" == "PASS" ]]; then',
        start,
    )
    gate = script[start:end].rstrip()
    assert gate.endswith("fi")
    return gate[: gate.rfind("\nfi")] + "\n"


def _run_local_ai_gate_harness(
    tmp_path: Path,
    *,
    available_mb: int,
    curl_rc: int,
    curl_response: str = "",
) -> tuple[subprocess.CompletedProcess[str], str]:
    script = read("scripts/ops/repair_dealix_vps_runtime_compat.sh")
    gate = _local_ai_gate_block(script)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    mock_log = tmp_path / "mock.log"

    curl = bin_dir / "curl"
    curl.write_text(
        "#!/usr/bin/env bash\n"
        "printf 'curl %s\\n' \"$*\" >>\"$MOCK_LOG\"\n"
        "printf '%s' \"$MOCK_CURL_RESPONSE\"\n"
        "exit \"$MOCK_CURL_RC\"\n",
        encoding="utf-8",
    )
    curl.chmod(0o755)

    sudo = bin_dir / "sudo"
    sudo.write_text(
        "#!/usr/bin/env bash\n"
        "printf 'sudo %s\\n' \"$*\" >>\"$MOCK_LOG\"\n"
        "exit 99\n",
        encoding="utf-8",
    )
    sudo.chmod(0o755)

    prelude = f'''\
set -Eeuo pipefail
RUN_USER="dealix"
ROOT="{tmp_path}"
HERMES_ACCEPT_TIMEOUT=45
HERMES_ACCEPT_MIN_AVAILABLE_MB=8192
OLLAMA_API="http://127.0.0.1:11434"
OLLAMA_MODEL="qwen3:4b-instruct-2507-q4_K_M"
PYTHON="$(command -v python3)"
HERMES="/mock/hermes"
PROMPT_DIR="{tmp_path / 'prompts'}"
STAMP="test"
HERMES_PROMPT=""
HERMES_ACCEPT="BLOCKED_BINARY_MISSING"
OLLAMA_MINIMAL_ACCEPT="NOT_RUN"
LOCAL_AI_READY="DEGRADED"
OLLAMA_UNLOAD_ARMED=0
HERMES_PATH="$PATH"
available_mb() {{ printf '%s\\n' "{available_mb}"; }}
section() {{ :; }}
'''
    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{bin_dir}:{env['PATH']}",
            "MOCK_LOG": str(mock_log),
            "MOCK_CURL_RC": str(curl_rc),
            "MOCK_CURL_RESPONSE": curl_response,
        }
    )
    result = subprocess.run(
        ["bash", "-c", prelude + gate],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    log = mock_log.read_text(encoding="utf-8") if mock_log.exists() else ""
    return result, log


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


def test_runtime_compat_low_memory_never_loads_ollama_or_invokes_hermes(tmp_path: Path) -> None:
    result, log = _run_local_ai_gate_harness(tmp_path, available_mb=4096, curl_rc=0)
    assert result.returncode == 0, result.stderr
    assert "OLLAMA_MINIMAL_ACCEPT=SKIPPED_RESOURCE_GUARD" in result.stdout
    assert "HERMES_ACCEPT=DEGRADED_RESOURCE_GUARD" in result.stdout
    assert "curl " not in log
    assert "sudo " not in log


def test_runtime_compat_failed_ollama_probe_never_invokes_hermes(tmp_path: Path) -> None:
    result, log = _run_local_ai_gate_harness(tmp_path, available_mb=12288, curl_rc=7)
    assert result.returncode == 0, result.stderr
    assert "OLLAMA_MINIMAL_ACCEPT=DEGRADED rc=7" in result.stdout
    assert "HERMES_ACCEPT=DEGRADED_LOCAL_MODEL" in result.stdout
    assert "curl " in log
    assert "sudo " not in log


def test_runtime_compat_cleanup_contains_real_ollama_unload_request() -> None:
    script = read("scripts/ops/repair_dealix_vps_runtime_compat.sh")
    start = script.index("cleanup_local_ai() {")
    end = script.index('\n}\n\nif [[ "$(id -u)"', start) + 2
    cleanup = script[start:end]
    assert 'if [[ "$OLLAMA_UNLOAD_ARMED" == "1" ]]' in cleanup
    assert '--data-binary "{\\"model\\":\\"${OLLAMA_MODEL}\\",\\"keep_alive\\":0}"' in cleanup
    assert '"$OLLAMA_API/api/generate"' in cleanup


def test_runtime_compat_repairs_root_executive_runner_without_root_hermes() -> None:
    script = read("scripts/ops/repair_dealix_vps_runtime_compat.sh")
    assert 'HERMES="/home/${RUN_USER}/.local/bin/hermes"' in script
    assert "exec sudo -u dealix -H env" in script
    assert '"$HERMES" chat --query-file "$PROMPT_FILE"' in script
    assert '"$HERMES" chat -Q --ignore-rules --toolsets clarify --max-turns 1' in script
    assert "hermes --ignore-rules --toolsets clarify -z" not in script
    assert "DEALIX_HERMES_MINIMAL_OK" in script
    assert "DEALIX_HERMES_8K_OK" not in script
    assert "HERMES_ACCEPT=FAIL_CLOSED" in script
    assert 'HERMES_ACCEPT_TIMEOUT="${HERMES_ACCEPT_TIMEOUT:-45}"' in script
    assert "timeout --signal=TERM --kill-after=10s" in script
    assert "DEGRADED_TIMEOUT" in script
    assert "DEGRADED_RESOURCE_GUARD" in script
    assert "DEGRADED_LOCAL_MODEL" in script
    assert "timeout 300" not in script


def test_runtime_compat_constrains_local_model_resource_probe() -> None:
    script = read("scripts/ops/repair_dealix_vps_runtime_compat.sh")
    assert 'HERMES_ACCEPT_MIN_AVAILABLE_MB="${HERMES_ACCEPT_MIN_AVAILABLE_MB:-8192}"' in script
    assert 'OLLAMA_MODEL="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"' in script
    assert '\\"num_ctx\\":2048' in script
    assert '\\"num_predict\\":16' in script
    assert '\\"keep_alive\\":0' in script
    assert "OLLAMA_MINIMAL_ACCEPT=PASS" in script
    assert 'HERMES_AVAILABLE_MB="$(available_mb)"' in script
    assert "OLLAMA_MINIMAL_ACCEPT=SKIPPED_RESOURCE_GUARD" in script
    assert 'HERMES_AVAILABLE_MB_POST_OLLAMA="$(available_mb)"' in script
    assert '--query-file "$HERMES_PROMPT"' in script
    assert 'if [[ "$OLLAMA_MINIMAL_ACCEPT" == "PASS" && "$HERMES_ACCEPT" == "PASS" ]]' in script
    assert 'echo "DEALIX_LOCAL_AI_READY=$LOCAL_AI_READY"' in script


def test_runtime_compat_query_file_is_dealix_readable_and_cleanup_is_always_armed() -> None:
    script = read("scripts/ops/repair_dealix_vps_runtime_compat.sh")
    assert 'PROMPT_DIR="/opt/dealix/executive-prompts"' in script
    assert 'install -d -m 0750 -o root -g "$RUN_USER" "$PROMPT_DIR"' in script
    assert 'HERMES_PROMPT="$PROMPT_DIR/hermes-accept-${STAMP}.txt"' in script
    assert 'install -m 0600 -o "$RUN_USER" -g "$RUN_USER" /dev/null "$HERMES_PROMPT"' in script
    assert 'chown "$RUN_USER:$RUN_USER" "$HERMES_PROMPT"' in script
    cleanup_pos = script.index("cleanup_local_ai()")
    trap_pos = script.index("trap cleanup_local_ai EXIT")
    first_model_pos = script.index('OLLAMA_OUT="$(curl -sS --max-time 45')
    assert cleanup_pos < trap_pos < first_model_pos
    assert 'if [[ "$OLLAMA_UNLOAD_ARMED" == "1" ]]' in script
    assert 'rm -f "$HERMES_PROMPT"' in script


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
