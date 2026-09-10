from pathlib import Path


def test_client_delivery_control_assets_exist():
    required = [
        Path("data/commercial/client_delivery_control_manifest.json"),
        Path("scripts/commercial/generate_client_delivery_control.py"),
        Path("apps/web/lib/client-delivery-control-snapshot.ts"),
        Path("apps/web/app/(saas)/app/client-delivery/page.tsx"),
    ]
    for path in required:
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8").strip(), f"empty {path}"


def test_client_delivery_control_has_delivery_method_and_proof():
    manifest = Path("data/commercial/client_delivery_control_manifest.json").read_text(encoding="utf-8")
    assert "workflow map" in manifest
    assert "stakeholder map" in manifest
    assert "Proof Pack" in manifest
    assert "acceptance criteria" in manifest
    assert "renewal" in manifest
