from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

SCRIPT = Path("scripts/commercial/verify_post_1712_commercial_launch.py")


def load_gate():
    spec = spec_from_file_location("post_1712_gate", SCRIPT)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_retired_surface_rejects_stale_claims_and_unconverged_page() -> None:
    gate = load_gate()
    errors: list[str] = []
    gate.validate_retired_surface(
        {"ok": True, "final_url": "https://dealix.me/trust.html", "body_sample": "PDPL Compliant · Saudi data residency · ZATCA Phase 2 Ready"},
        "/trust.html",
        "/trust-center.html",
        errors,
    )
    assert any("PDPL Compliant" in item for item in errors)
    assert any("not converged" in item for item in errors)


def test_retired_surface_accepts_redirect_or_repo_marker() -> None:
    gate = load_gate()
    redirected: list[str] = []
    gate.validate_retired_surface(
        {"ok": True, "final_url": "https://dealix.me/trust-center.html", "body_sample": "Current trust center"},
        "/trust.html",
        "/trust-center.html",
        redirected,
    )
    assert redirected == []

    marker: list[str] = []
    gate.validate_retired_surface(
        {"ok": True, "final_url": "https://dealix.me/trust.html", "body_sample": "DEALIX_RETIRED_PUBLIC_SURFACE"},
        "/trust.html",
        "/trust-center.html",
        marker,
    )
    assert marker == []
