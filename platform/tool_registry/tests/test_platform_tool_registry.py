"""Self-verification for the Tool Registry operating-model system.

Asserts the scaffold is intact and still maps to real modules. This is the
anti-drift guard: if an implementing module is renamed or deleted, this fails.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SYSTEM_DIR = REPO / "platform/tool_registry"
IMPLEMENTED_BY = ['auto_client_acquisition/agent_os/tool_permissions.py', 'auto_client_acquisition/tool_guardrail_gateway']
ARTIFACTS = ['architecture.md', 'readiness.md', 'observability.md', 'rollback.md', 'metrics.md', 'risk_model.md']


def test_artifacts_present():
    for name in ARTIFACTS:
        path = SYSTEM_DIR / name
        assert path.exists(), f"missing artifact: {path}"
        assert path.read_text(encoding="utf-8").strip(), f"empty artifact: {path}"


def test_implementing_modules_exist():
    missing = [m for m in IMPLEMENTED_BY if not (REPO / m).exists()]
    assert not missing, (
        f"Tool Registry architecture.md references modules that no longer exist: "
        f"{missing}. Update architecture.md or restore the modules."
    )
