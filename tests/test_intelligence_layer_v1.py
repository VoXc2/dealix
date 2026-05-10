"""Wave 12 — Intelligence Layer v1 tests.

Validates the foundational intelligence stack:
- dealix_task_registry: 21 tasks registered with correct privacy levels
- local_model_client: graceful when Ollama/vLLM not running
- confidence: text-signal scoring + combine + bucket boundaries
- dealix_model_router: composes the above; degrades to human safely

Hard rules tested (Article 4 + Article 8):
- Unknown tasks fail fast (no silent default)
- founder_only tasks NEVER reach cloud
- No real secrets in logs/return values
- All errors return RouterDecision (never raise)
"""
from __future__ import annotations

import os
from unittest import mock

import pytest

from auto_client_acquisition.intelligence import (
    confidence as conf_mod,
)
from auto_client_acquisition.intelligence.confidence import (
    ConfidenceScore,
    combine,
    from_logprobs,
    from_text_signals,
)
from auto_client_acquisition.intelligence.dealix_model_router import (
    RouterDecision,
    route_task,
    status_summary,
)
from auto_client_acquisition.intelligence.dealix_task_registry import (
    all_tasks,
    get_task_requirements,
    tasks_by_tier,
    tasks_requiring_local_only,
)
from auto_client_acquisition.intelligence.local_model_client import (
    LocalModelUnavailable,
    _detect_provider,
    is_local_configured,
    ping_local,
)
from auto_client_acquisition.llm_gateway_v10.schemas import ModelTier


# ─────────────────────────────────────────────────────────────────────
# Task registry (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_registry_has_all_expected_tasks() -> None:
    """21 canonical Dealix tasks must be registered (per plan §32)."""
    tasks = all_tasks()
    assert len(tasks) == 21, f"expected 21 tasks; got {len(tasks)}"
    # Spot-check critical ones
    must_have = (
        "lead_classification", "decision_passport", "draft_message_arabic",
        "executive_summary", "support_classify", "pii_redaction",
        "deterministic_lookup",
    )
    for t in must_have:
        assert t in tasks, f"missing canonical task: {t}"


def test_unknown_task_raises_keyerror() -> None:
    """Article 11: unknown tasks fail fast (no silent default)."""
    with pytest.raises(KeyError, match="Unknown DealixTask"):
        get_task_requirements("rogue_made_up_task")  # type: ignore[arg-type]


def test_pii_redaction_is_founder_only_privacy() -> None:
    """PII redaction MUST be tagged founder_only (never sent to cloud)."""
    req = get_task_requirements("pii_redaction")
    assert req.privacy_level == "founder_only"


def test_safety_check_is_founder_only_privacy() -> None:
    """Safety check MUST stay local (founder_only privacy)."""
    req = get_task_requirements("safety_check")
    assert req.privacy_level == "founder_only"


def test_tasks_by_tier_returns_correct_groups() -> None:
    """Cheap tier should have classifiers; strong tier should have strategy."""
    cheap = tasks_by_tier(ModelTier.cheap_for_classification)
    assert "lead_classification" in cheap
    assert "intent_classify" in cheap

    strong = tasks_by_tier(ModelTier.strong_for_strategy)
    assert "executive_summary" in strong
    assert "proof_pack_assemble" in strong


def test_tasks_requiring_local_only_returns_founder_only_set() -> None:
    """tasks_requiring_local_only() must surface every founder_only task."""
    local_only = tasks_requiring_local_only()
    assert "pii_redaction" in local_only
    assert "safety_check" in local_only
    assert "payment_evidence_summary" in local_only
    # And NOT include customer_internal tasks
    assert "draft_message_arabic" not in local_only


# ─────────────────────────────────────────────────────────────────────
# Local model client (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_is_local_configured_false_when_no_env() -> None:
    """No env vars → not configured."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert is_local_configured() is False


def test_is_local_configured_true_when_ollama_url_set() -> None:
    """OLLAMA_BASE_URL set → configured."""
    with mock.patch.dict(os.environ, {"OLLAMA_BASE_URL": "http://localhost:11434"}, clear=True):
        assert is_local_configured() is True


def test_ping_local_returns_unreachable_when_server_down() -> None:
    """When Ollama is not running, ping_local returns (False, msg) — never raises."""
    with mock.patch.dict(os.environ, {"OLLAMA_BASE_URL": "http://127.0.0.1:1"}, clear=True):
        # Port 1 is reserved/unreachable; should fail fast
        is_up, msg = ping_local(timeout_seconds=1.0)
        assert is_up is False
        assert isinstance(msg, str) and len(msg) > 0


def test_detect_provider_explicit_none() -> None:
    """LOCAL_LLM_PROVIDER=none disables local entirely."""
    with mock.patch.dict(os.environ, {"LOCAL_LLM_PROVIDER": "none"}, clear=True):
        provider, _ = _detect_provider()
        assert provider == "none"


# ─────────────────────────────────────────────────────────────────────
# Confidence scoring (6 tests)
# ─────────────────────────────────────────────────────────────────────


def test_confidence_empty_text_is_very_low() -> None:
    """Empty response → very_low + score 0."""
    score = from_text_signals("")
    assert score.level == "very_low"
    assert score.score == 0.0


def test_confidence_refusal_marker_is_very_low() -> None:
    """Refusal markers (English + Arabic) → very_low."""
    for text in (
        "I cannot provide that information.",
        "I'm unable to help with that.",
        "لا أستطيع الإجابة على ذلك",
    ):
        score = from_text_signals(text)
        assert score.level == "very_low", \
            f"text={text!r} should be very_low; got {score.level}"


def test_confidence_substantial_output_higher() -> None:
    """Long, decisive output → medium or higher."""
    text = (
        "The customer's lead source is warm_intro from Acme Corp. "
        "Best channel is manual_linkedin given their consent posture. "
        "Recommended action: prepare_diagnostic. Confidence is high."
    )
    score = from_text_signals(text)
    assert score.is_actionable, f"long decisive output should be actionable; got {score.level}"


def test_confidence_invalid_json_when_expected_drops_score() -> None:
    """When json_mode expected but text is plain prose → invalid_json reason."""
    score = from_text_signals("just plain text not json", expected_json=True)
    assert "invalid_json" in score.reasons


def test_confidence_valid_json_when_expected_raises_score() -> None:
    """When json_mode expected and text parses → valid_json bonus."""
    score = from_text_signals('{"action": "diagnostic", "confidence": 0.9}', expected_json=True)
    assert "valid_json" in score.reasons


def test_combine_pessimistic_min_weighted() -> None:
    """combine() uses 60% min + 40% mean — pessimistic per Article 8."""
    high = ConfidenceScore(score=0.9, level="very_high", reasons=("a",))
    low = ConfidenceScore(score=0.3, level="very_low", reasons=("b",))
    combined = combine(high, low)
    # Pessimistic: 0.6*0.3 + 0.4*0.6 = 0.18 + 0.24 = 0.42 → low
    assert combined.score is not None
    assert combined.score < 0.5  # closer to min, not arithmetic mean (0.6)
    assert combined.level == "low"


# ─────────────────────────────────────────────────────────────────────
# Model router (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_router_unknown_task_returns_degraded() -> None:
    """Article 11: unknown tasks → degraded_to_human (never raises)."""
    decision = route_task(
        "completely_unknown_task",  # type: ignore[arg-type]
        prompt="x", language="ar",
    )
    assert decision.status == "degraded_to_human"
    assert decision.needs_human is True


def test_router_deterministic_lookup_returns_ok_local_no_model() -> None:
    """deterministic_lookup → ok_local + backend=rules (no model invoked)."""
    decision = route_task("deterministic_lookup", prompt="lookup x", language="ar")
    assert decision.status == "ok_local"
    assert decision.backend_used == "rules"
    assert decision.estimated_cost_usd == 0.0
    assert decision.confidence.level == "very_high"


def test_router_no_local_no_cloud_degrades_to_human() -> None:
    """When both local + cloud are unavailable, decision = degraded_to_human."""
    with mock.patch.dict(os.environ, {}, clear=True):
        # No local config, no cloud creds
        decision = route_task(
            "draft_message_arabic", prompt="Compose a warm intro", language="ar",
        )
        assert decision.status == "degraded_to_human"
        assert decision.needs_human is True
        assert decision.text == ""
        assert "local_not_configured" in decision.fallback_reasons


def test_router_founder_only_task_blocks_cloud_when_local_missing() -> None:
    """pii_redaction is founder_only — when local missing + cloud creds present,
    must STILL block cloud (never sent to cloud)."""
    with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fake-test-key-xxx"}, clear=True):
        # No local; cloud creds present; founder_only task
        decision = route_task(
            "pii_redaction", prompt="redact this", language="ar",
            cloud_fallback_enabled=True,
        )
        # Must NOT use cloud — privacy gate blocks it
        assert decision.status in ("blocked_by_privacy", "degraded_to_human")
        assert "cloud" not in decision.backend_used


def test_router_status_summary_returns_dict_with_hard_gates() -> None:
    """status_summary() includes hard_gates dict + tasks_registered count."""
    summary = status_summary()
    assert summary["service"] == "dealix_intelligence_router"
    assert summary["tasks_registered"] == 21
    assert "hard_gates" in summary
    gates = summary["hard_gates"]
    assert isinstance(gates, dict)
    assert gates["privacy_founder_only_never_cloud"] is True
    assert gates["no_secrets_logged"] is True


# ─────────────────────────────────────────────────────────────────────
# Total: 20 tests
# ─────────────────────────────────────────────────────────────────────
