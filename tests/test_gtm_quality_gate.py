"""The combined GTM quality gate: only fully-clean drafts become send-ready,
and even then approval stays required and sending stays disabled."""

from core.safety.draft import evaluate_draft
from tests._fixtures import good_cold_email, generic_bad_draft


def test_clean_personalized_draft_is_send_ready():
    result = evaluate_draft(good_cold_email(), channel="email")
    assert result.send_ready is True, result.violations
    # Defaults must remain conservative even when send_ready.
    assert result.approval_required is True
    assert result.send_enabled is False


def test_generic_draft_is_not_send_ready():
    result = evaluate_draft(generic_bad_draft(), channel="email")
    assert result.send_ready is False
    assert result.violations  # at least one reason


def test_dry_run_and_approval_defaults_are_safe():
    result = evaluate_draft(good_cold_email(), channel="email")
    d = result.as_dict()
    assert d["send_enabled"] is False
    assert d["approval_required"] is True
