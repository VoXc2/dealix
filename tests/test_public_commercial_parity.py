from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/ops/verify_public_commercial_parity.py"


def _module():
    spec = importlib.util.spec_from_file_location("public_commercial_parity", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_repository_public_commercial_surfaces_are_canonical() -> None:
    module = _module()
    results = module.verify_repo()
    assert results
    assert all(row.ok for row in results), results


def test_legacy_ai_team_copy_is_rejected() -> None:
    module = _module()
    result = module.evaluate_surface(
        "/ai-team.html",
        "فريق AI تشغيلي داخل نظام شركة واحد لا توجد باقات ثابتة عامة 499 SAR 7-Day Pilot 5 وكلاء AI",
    )
    assert result.ok is False
    assert "499 sar" in result.legacy_markers
    assert "7-day pilot" in result.legacy_markers
    assert "5 وكلاء ai" in result.legacy_markers


def test_customer_portal_must_be_retired_noindex_surface() -> None:
    module = _module()
    good = module.evaluate_surface(
        "/customer-portal.html",
        '<meta name="robots" content="noindex,nofollow"><!-- DEALIX_RETIRED_PUBLIC_SURFACE -->',
    )
    assert good.ok is True

    bad = module.evaluate_surface(
        "/customer-portal.html",
        "جاهز تربط بياناتك؟ احجز Sprint مباشرة",
    )
    assert bad.ok is False
    assert "احجز sprint مباشرة" in bad.legacy_markers
