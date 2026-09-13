from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACCESS_GATE = ROOT / "landing" / "assets" / "js" / "access-gate.js"


def test_access_gate_contains_no_static_credentials_or_url_token_flow() -> None:
    text = ACCESS_GATE.read_text(encoding="utf-8")
    lowered = text.lower()

    forbidden = (
        "default_tokens",
        "dealix-founder-2026",
        "dealix-pilot-2026",
        "dealix_access_tokens",
        "?access=",
        "storage_key",
        "localstorage.getitem",
        "localstorage.setitem",
        "localstorage.removeitem",
        "tierfortoken",
        "readstored",
        "writestored",
    )
    for marker in forbidden:
        assert marker not in lowered


def test_access_gate_fails_closed_without_authenticated_app_context() -> None:
    text = ACCESS_GATE.read_text(encoding="utf-8")

    assert "DEALIX_ACCESS_CONTEXT" in text
    assert "raw.authorized !== true" in text
    assert "lockPage(required)" in text
    assert "No browser token, URL credential, or localStorage value can unlock this page" in text


def test_public_landing_bundle_has_no_legacy_founder_or_subscriber_codes() -> None:
    forbidden = ("dealix-founder-2026", "dealix-pilot-2026")
    public_suffixes = {".html", ".js", ".json", ".txt", ".css"}

    for path in (ROOT / "landing").rglob("*"):
        if not path.is_file() or path.suffix.lower() not in public_suffixes:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for marker in forbidden:
            assert marker not in text, f"legacy access code exposed in public bundle: {path}"
