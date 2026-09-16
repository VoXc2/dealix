import json
from pathlib import Path


def test_commercial_launch_control_assets_exist():
    required = [
        Path("data/commercial/commercial_launch_control_manifest.json"),
        Path("scripts/commercial/generate_commercial_launch_control.py"),
        Path("apps/web/lib/commercial-launch-control-snapshot.ts"),
        Path("apps/web/app/(saas)/app/commercial-launch/page.tsx"),
    ]
    for path in required:
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8").strip(), f"empty {path}"


def test_commercial_launch_control_keeps_guardrails():
    manifest = Path("data/commercial/commercial_launch_control_manifest.json").read_text(encoding="utf-8")
    assert "no fake ROI" in manifest
    assert "no fake testimonials" in manifest
    assert "source_url required" in manifest
    assert "proof pack required" in manifest


def test_commercial_launch_control_has_no_fixed_public_price_or_duration_authority():
    manifest = json.loads(Path("data/commercial/commercial_launch_control_manifest.json").read_text(encoding="utf-8"))
    authority = manifest["public_commercial_authority"]
    assert authority["all_diagnostics_free"] is True
    assert authority["public_fixed_price"] is False
    assert authority["public_fixed_duration"] is False
    assert authority["quote_authority"] == "customer_specific_after_qualified_discovery"
    rendered = json.dumps(manifest["commercial_sprint_packages"])
    for forbidden in ("price_range_sar", "duration_days", '"duration"', "5000-12000", "15000-35000", "7-Day", "14-Day"):
        assert forbidden not in rendered

    page = Path("apps/web/app/(saas)/app/commercial-launch/page.tsx").read_text(encoding="utf-8")
    assert "pkg.commercial_terms" in page
    assert "pkg.price_range_sar" not in page
    assert "pkg.duration" not in page


def test_commercial_launch_generator_fails_closed_on_fixed_term_fields():
    source = Path("scripts/commercial/generate_commercial_launch_control.py").read_text(encoding="utf-8")
    assert "def governed_public_packages" in source
    assert '{"price_range_sar", "price_sar", "duration", "duration_days"}' in source
    assert "fixed public commercial authority is forbidden" in source
