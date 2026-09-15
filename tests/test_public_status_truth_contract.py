from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "apps/web/app/status/page.tsx"
NEXT_CONFIG = ROOT / "apps/web/next.config.js"


def test_public_status_never_invents_live_green_state() -> None:
    text = STATUS.read_text(encoding="utf-8")
    forbidden = (
        "All systems are operational",
        "جميع الأنظمة تعمل",
        "آخر تحقق: الآن",
        "●  يعمل",
        "لا توجد حوادث مسجلة",
    )
    assert not [token for token in forbidden if token in text]
    assert "Verification required" in text
    assert "HTTP 200 ≠ release identity" in text
    assert "Production Green requires" in text


def test_public_status_exposes_receipts_not_internal_operator_surfaces() -> None:
    text = STATUS.read_text(encoding="utf-8")
    assert '`${siteUrl}/healthz`' in text
    assert '`${apiUrl}/version`' in text
    assert 'href="/safety"' in text
    assert 'href="/book"' in text
    assert 'href="/cases"' in text
    assert 'href="/control-plane"' not in text
    assert 'href="/agents"' not in text


def test_legacy_status_and_case_urls_preserve_safe_public_equity() -> None:
    config = NEXT_CONFIG.read_text(encoding="utf-8")
    assert '{ source: "/system-status.html", destination: "/status", permanent: true }' in config
    assert '{ source: "/case-study.html", destination: "/cases", permanent: true }' in config
