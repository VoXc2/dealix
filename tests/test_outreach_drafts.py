"""Tests for governed outreach draft snippets."""

from __future__ import annotations

from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts, build_outreach_draft_ar


def test_build_outreach_draft_contains_company_and_cta() -> None:
    row = {
        "company": "وكالة اختبار",
        "pain_hypothesis": "لا owner للمتابعة",
        "motion": "A",
        "channel": "linkedin_manual",
    }
    text = build_outreach_draft_ar(row, icp={"core_message_ar": "Dealix يثبت ما بعد الـ lead."}, objection_snippet="")
    assert "وكالة اختبار" in text
    assert "Risk Score" in text
    assert "مسودة" in text


def test_attach_outreach_drafts_mutates_payload() -> None:
    payload = {
        "targets": {
            "items": [{"company": "Co", "pain_hypothesis": "pain", "motion": "A"}],
        },
        "follow_ups_due": [],
    }
    out = attach_outreach_drafts(payload)
    item = out["targets"]["items"][0]
    assert item.get("outreach_draft_ar")
    assert out.get("outreach_policy_ar")
