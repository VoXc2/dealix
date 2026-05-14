"""Unit tests for ``governance_os.runtime_decision.decide``.

Locks the contract that the data_os router and the delivery sprint rely on:

- hard-blocked actions (scrape_*, bulk_cold_outreach, …) return BLOCK
- forbidden channel/mode pairs return BLOCK with the channel reason
- ``generate_draft`` without a passport → BLOCK
- ``generate_draft`` with a valid passport whose ``allowed_use`` covers the
  intended use → ALLOW (or DRAFT_ONLY when the channel implies a draft path)
- claim-unsafe text triggers REDACT
"""

from __future__ import annotations

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.runtime_decision import decide
from auto_client_acquisition.sovereignty_os.source_passport_standard import SourcePassport


def _good_passport(**overrides) -> SourcePassport:
    defaults = dict(
        source_id="src_unit",
        source_type="client_upload",
        owner="client",
        allowed_use=frozenset({"internal_analysis", "draft_only", "scoring"}),
        contains_pii=False,
        sensitivity="low",
        retention_policy="project_duration",
        ai_access_allowed=True,
        external_use_allowed=False,
    )
    defaults.update(overrides)
    return SourcePassport(**defaults)


def test_hard_blocked_action_returns_block() -> None:
    res = decide(action="scrape_linkedin")
    assert res.decision == GovernanceDecision.BLOCK
    assert any("hard-blocked" in r for r in res.reasons)


def test_cold_whatsapp_without_consent_blocks() -> None:
    res = decide(
        action="send_message",
        context={"channel": "whatsapp", "is_cold": True},
    )
    assert res.decision == GovernanceDecision.BLOCK


def test_generate_draft_without_passport_blocks() -> None:
    res = decide(action="generate_draft", context={"text": "hello"})
    assert res.decision == GovernanceDecision.BLOCK
    assert any("no_source_passport" in r for r in res.reasons)


def test_generate_draft_with_valid_passport_allows() -> None:
    res = decide(
        action="generate_draft",
        context={
            "source_passport": _good_passport(),
            "intended_use": "draft_only",
            "text": "نلخص الفرص بناءً على البيانات المرفوعة",
            "channel": "email",
        },
    )
    # Channel + "draft" in the action name triggers DRAFT_ONLY default
    assert res.decision in {
        GovernanceDecision.ALLOW,
        GovernanceDecision.ALLOW_WITH_REVIEW,
        GovernanceDecision.DRAFT_ONLY,
    }


def test_invalid_passport_blocks() -> None:
    bad = _good_passport(ai_access_allowed=False)
    res = decide(
        action="generate_draft",
        context={"source_passport": bad, "intended_use": "draft_only"},
    )
    assert res.decision == GovernanceDecision.BLOCK
    assert any("invalid_source_passport" in r for r in res.reasons)


def test_unsafe_claim_text_routes_to_redact() -> None:
    res = decide(
        action="generate_draft",
        context={
            "source_passport": _good_passport(),
            "intended_use": "draft_only",
            "text": "we promise guaranteed results to every client",
        },
    )
    # When the text is unsafe, the decision tightens at least to REDACT.
    assert res.decision in {
        GovernanceDecision.REDACT,
        GovernanceDecision.REQUIRE_APPROVAL,
        GovernanceDecision.BLOCK,
    }
    assert any("unsafe_claim:" in r for r in res.reasons)


def test_validate_rejects_whitespace_source_id() -> None:
    from auto_client_acquisition.data_os.source_passport import validate

    res = validate(_good_passport(source_id="   "))
    assert not res.is_valid
    assert "source_id" in res.missing


def test_validate_rejects_none_source_id() -> None:
    from auto_client_acquisition.data_os.source_passport import (
        SourcePassport,
        validate,
    )

    # ``source_id=None`` would have been coerced to the literal string
    # ``'None'`` by ``str(passport.source_id).strip()`` and silently pass
    # before the None-guard was added.
    passport = SourcePassport(
        source_id=None,  # type: ignore[arg-type]
        source_type="client_upload",
        owner="client",
        allowed_use=frozenset({"draft_only"}),
        contains_pii=False,
        sensitivity="low",
        retention_policy="project_duration",
        ai_access_allowed=True,
        external_use_allowed=False,
    )
    res = validate(passport)
    assert not res.is_valid
    assert "source_id" in res.missing


def test_step5_governance_review_accepts_dict_passport() -> None:
    """The API boundary hands the sprint orchestrator a JSON dict for the
    passport; step5 must convert it before handing it to ``decide()`` to
    avoid the AttributeError that otherwise blocked every draft review."""
    from auto_client_acquisition.delivery_factory.delivery_sprint import (
        step5_governance_review,
    )

    passport_dict = {
        "source_id": "src_dict_test",
        "source_type": "client_upload",
        "owner": "client",
        "allowed_use": frozenset({"draft_only", "scoring"}),
        "contains_pii": False,
        "sensitivity": "low",
        "retention_policy": "project_duration",
        "ai_access_allowed": True,
        "external_use_allowed": False,
    }
    out = step5_governance_review(
        customer_id="cust1",
        engagement_id="eng1",
        drafts=[{"account": "A1", "outline_ar": "ملخص", "outline_en": "summary"}],
        source_passport=passport_dict,
    )
    assert out["reviews"], "expected at least one review row"
    # The crucial assertion: no ``no_source_passport`` reason — the dict
    # was converted to a SourcePassport before reaching ``decide()``.
    review = out["reviews"][0]
    assert not any("no_source_passport" in r for r in review["reasons"]), (
        f"step5 still blocking on missing passport: {review!r}"
    )
