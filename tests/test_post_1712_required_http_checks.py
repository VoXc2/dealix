from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

SCRIPT = Path("scripts/commercial/verify_post_1712_commercial_launch.py")

def load_gate():
    spec = spec_from_file_location("post_1712_gate_required", SCRIPT)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_retired_404_is_not_a_required_http_failure() -> None:
    gate = load_gate()
    checks = [
        {"url": "https://dealix.me/", "ok": True, "status": 200},
        {"url": "https://dealix.me/trust.html", "ok": False, "status": 404, "surface": "/trust.html"},
    ]
    assert gate.required_http_failures(checks) == []


def test_core_http_failure_remains_blocking() -> None:
    gate = load_gate()
    checks = [{"url": "https://dealix.me/book", "ok": False, "status": 500}]
    assert gate.required_http_failures(checks) == checks
