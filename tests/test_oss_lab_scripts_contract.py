"""Static safety contract for isolated OSS lab scripts.

These tests intentionally inspect shell source rather than starting services or
installing packages. They guard the exact failure modes seen during the first
VPS bootstrap and preserve the no-production/no-public-service contract.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "scripts/ops/bootstrap_oss_labs_v1.sh"
SMOKE = ROOT / "scripts/ops/run_oss_smoke_v1.sh"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_venv_setup_output_is_not_captured_as_directory_path():
    source = _source(BOOTSTRAP)
    assert 'dir="$(ensure_venv "$name")"' not in source
    assert 'ensure_venv "$name"' in source
    assert 'local dir="$LAB_ROOT/$name"' in source


def test_sudo_argument_boundary_is_explicit():
    for path in (BOOTSTRAP, SMOKE):
        source = _source(path)
        assert 'sudo -u "$DEALIX_USER" -H --' in source


def test_promptfoo_uses_isolated_supported_node_runtime():
    source = _source(BOOTSTRAP)
    assert 'NODE_VERSION="${DEALIX_OSS_NODE_VERSION:-v24.20.0}"' in source
    assert 'version_ge "$node_version" "v22.22.0"' in source
    assert 'SHASUMS256.txt' in source
    assert 'sha256sum -c expected.sha256' in source
    smoke = _source(SMOKE)
    assert 'PATH="$NODE_ROOT/bin:' in smoke


def test_bootstrap_never_starts_containers_or_services():
    source = _source(BOOTSTRAP)
    forbidden = (
        "docker run",
        "docker compose up",
        "systemctl start",
        "systemctl enable",
        "ufw allow",
    )
    for token in forbidden:
        assert token not in source
    assert 'SERVICES_STARTED=false' in source
    assert 'PORTS_EXPOSED=false' in source


def test_smoke_never_executes_active_security_scan():
    source = _source(SMOKE)
    assert 'ACTIVE_SCAN_EXECUTED=false' in source
    assert 'docker run' not in source
    assert 'zap-baseline.py' not in source
    assert 'zap-full-scan.py' not in source


def test_python_smoke_uses_component_virtualenvs():
    source = _source(SMOKE)
    assert 'local py="$LAB_ROOT/$name/venv/bin/python"' in source
    assert 'check_py_import presidio' in source
    assert 'check_py_import docling' in source
    assert 'check_py_import faster-whisper' in source
    assert 'check_py_import camel-tools' in source
    assert 'check_py_import livekit-agents' in source
    assert 'check_py_import pipecat' in source
