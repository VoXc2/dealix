"""Social drafts must not resurrect retired Dealix prices/offers/funnels or authority."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
import yaml

from dealix.commercial_ops.social_queue import (
    CURRENT_LAUNCH_AUTHORITY,
    format_linkedin_draft,
    get_post_for_date,
    is_current_launch_safe_post,
    mark_post_status,
)

ROOT = Path(__file__).resolve().parents[1]


def _safe_post(*, week: int = 1, day: int = 0) -> dict[str, object]:
    return {
        "week": week,
        "day": day,
        "surface": "founder_linkedin",
        "pillar": "proof",
        "title_ar": "من التشخيص إلى تنفيذ قابل للإثبات",
        "body_ar": (
            "Execution Diagnostic → qualified discovery → customer-specific quote → "
            "governed outcome sprint → source-backed Proof."
        ),
        "cta_ar": "ابدأ Execution Diagnostic؛ لا Checkout أو إرسال تلقائي.",
        "status": "draft",
        "launch_authority": CURRENT_LAUNCH_AUTHORITY,
        "external_publish_allowed": False,
    }


def test_retired_fixed_price_post_is_not_launch_safe() -> None:
    post = _safe_post()
    post["body_ar"] = "ابدأ بـ 499 ر.س — pilot وليس عقد سنوي."
    assert is_current_launch_safe_post(post) is False


def test_today_picker_skips_retired_matching_slot_and_uses_safe_draft() -> None:
    unsafe = _safe_post(week=1, day=0)
    unsafe["body_ar"] = "4,999–15,000 ر.س — مدخل محادثة."
    safe = _safe_post(week=1, day=0)
    safe["title_ar"] = "Current authority"
    queue = {
        "anchor_date": "2026-09-13",
        "cycle_weeks": 1,
        "posts": [unsafe, safe],
    }

    selected = get_post_for_date(date(2026, 9, 13), queue=queue)

    assert selected is not None
    assert selected["title_ar"] == "Current authority"
    assert "customer-specific quote" in selected["body_ar"]


def test_today_picker_rejects_legacy_launch_authority_even_if_copy_is_safe() -> None:
    legacy = _safe_post()
    legacy["launch_authority"] = "revenue_command_pilot_30d"
    assert get_post_for_date(queue={"cycle_weeks": 1, "posts": [legacy]}) is None


def test_today_picker_does_not_reuse_already_published_post() -> None:
    published = _safe_post()
    published["status"] = "published"
    assert get_post_for_date(queue={"cycle_weeks": 1, "posts": [published]}) is None


def test_today_picker_fails_closed_when_every_post_is_retired() -> None:
    unsafe = _safe_post()
    unsafe["aeo_slug"] = "first-paid-diagnostic"
    assert get_post_for_date(queue={"cycle_weeks": 1, "posts": [unsafe]}) is None


def test_formatter_refuses_legacy_authority() -> None:
    legacy = _safe_post()
    legacy["launch_authority"] = "revenue_command_pilot_30d"
    with pytest.raises(ValueError, match="legacy launch authority"):
        format_linkedin_draft(legacy)


def test_formatter_refuses_retired_offer() -> None:
    unsafe = _safe_post()
    unsafe["body_ar"] = "Growth 2999 بعد Proof فقط."
    with pytest.raises(ValueError, match="retired commercial authority"):
        format_linkedin_draft(unsafe)


def test_approval_status_refuses_retired_offer(tmp_path: Path) -> None:
    unsafe = _safe_post()
    unsafe["cta_ar"] = "/ar/risk-score"
    queue_path = tmp_path / "social_content_queue.yaml"
    queue_path.write_text(
        yaml.safe_dump({"posts": [unsafe]}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="no safe unpublished"):
        mark_post_status(week=1, day=0, status="approved", path=queue_path)


def test_approval_targets_safe_replacement_after_published_history(tmp_path: Path) -> None:
    historical = _safe_post()
    historical["body_ar"] = "4,999–15,000 ر.س — historical published copy."
    historical["status"] = "published"
    current = _safe_post()
    queue_path = tmp_path / "social_content_queue.yaml"
    queue_path.write_text(
        yaml.safe_dump(
            {"posts": [historical, current]},
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    result = mark_post_status(week=1, day=0, status="approved", path=queue_path)
    saved = yaml.safe_load(queue_path.read_text(encoding="utf-8"))

    assert result["updated"] is True
    assert saved["posts"][0]["status"] == "published"
    assert saved["posts"][1]["status"] == "approved"


def test_expander_contains_only_current_authority_offer_language() -> None:
    text = (ROOT / "scripts/expand_social_queue_12w.py").read_text(encoding="utf-8")

    assert "corporate_brand_gtm_v1" in text
    assert "customer-specific quote" in text
    assert "Execution Diagnostic" in text
    assert "Dealix OS" in text
    assert "external_publish_allowed" in text
    for token in ("4,999", "15,000", "2,999", "Sprint 499", "Data Pack 1500", "Risk Score"):
        assert token not in text
