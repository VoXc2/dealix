"""Tests for the Dealix intelligence model router (cloud path wired).

The cloud LLM router (``core.llm.router.ModelRouter``) is monkeypatched to a
fake — zero network calls. One optional test (``@pytest.mark.llm``) exercises
a real provider and is skipped unless ``RUN_LLM_TESTS=1`` + a real API key.
"""

from __future__ import annotations

import os

import pytest

from auto_client_acquisition.intelligence import dealix_model_router as router_mod
from auto_client_acquisition.intelligence.dealix_model_router import route_task


class _FakeLLMResponse:
    def __init__(self, content: str) -> None:
        self.content = content
        self.provider = "anthropic"
        self.model = "claude-fake"
        self.input_tokens = 120
        self.output_tokens = 60


def _make_fake_router(*, content: str | None = None, raises: bool = False):
    """Build a fake ModelRouter class for monkeypatching core.llm.router."""

    class _FakeRouter:
        instantiated = 0

        def __init__(self, *a, **kw) -> None:
            type(self).instantiated += 1

        async def run(self, task, messages, *, max_tokens=900, temperature=0.3):
            if raises:
                raise RuntimeError("all providers failed")
            return _FakeLLMResponse(content or "")

    return _FakeRouter


def test_unknown_task_degrades_to_human():
    decision = route_task("not_a_real_task", prompt="hello")  # type: ignore[arg-type]
    assert decision.status == "degraded_to_human"
    assert decision.needs_human


def test_deterministic_lookup_is_rules_only():
    decision = route_task("deterministic_lookup", prompt="")
    assert decision.status == "ok_local"
    assert decision.backend_used == "rules"
    assert decision.estimated_cost_usd == 0.0


def test_founder_only_task_never_reaches_cloud(monkeypatch):
    fake = _make_fake_router(content="should not be used")
    monkeypatch.setattr("core.llm.router.ModelRouter", fake)
    # pii_redaction is privacy_level="founder_only" → cloud is forbidden.
    decision = route_task("pii_redaction", prompt="redact this", json_mode=True)
    assert decision.status == "blocked_by_privacy"
    assert fake.instantiated == 0  # the cloud router was never constructed


def test_cost_cap_blocks_expensive_call(monkeypatch):
    fake = _make_fake_router(content="x")
    monkeypatch.setattr("core.llm.router.ModelRouter", fake)
    # Force the pre-call estimate above any cap.
    monkeypatch.setattr(router_mod, "estimate_call_cost_usd", lambda tier, prompt: 999.0)
    decision = route_task("draft_message_english", prompt="write an outreach note")
    assert decision.status == "blocked_by_cost"
    assert fake.instantiated == 0  # blocked before constructing the router
    assert any("cost_cap" in r for r in decision.fallback_reasons)


def test_cloud_success_returns_ok_cloud(monkeypatch):
    fake = _make_fake_router(
        content="مرحباً، هذه مسودة رسالة احترافية متكاملة للعميل بدون أي ادعاءات."
    )
    monkeypatch.setattr("core.llm.router.ModelRouter", fake)
    decision = route_task("draft_message_english", prompt="draft an outreach email")
    assert decision.status == "ok_cloud"
    assert decision.text.startswith("مرحبا") or decision.text
    assert decision.backend_used == "cloud:anthropic"
    assert decision.model_used == "claude-fake"
    assert decision.confidence.score is not None
    assert decision.estimated_cost_usd > 0.0
    assert fake.instantiated == 1


def test_cloud_failure_degrades_to_human(monkeypatch):
    fake = _make_fake_router(raises=True)
    monkeypatch.setattr("core.llm.router.ModelRouter", fake)
    decision = route_task("draft_message_english", prompt="draft an outreach email")
    assert decision.status == "degraded_to_human"
    assert decision.needs_human
    assert any("cloud_call_failed" in r for r in decision.fallback_reasons)
    # The exception TYPE only — never the message — to avoid leaking secrets.
    assert all("all providers failed" not in r for r in decision.fallback_reasons)


@pytest.mark.llm
def test_cloud_real_call_optional():
    """Optional: hits a real provider. Skipped unless explicitly enabled."""
    if os.environ.get("RUN_LLM_TESTS") != "1":
        pytest.skip("RUN_LLM_TESTS!=1 — real-LLM test disabled")
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key or key.startswith("test-"):
        pytest.skip("no real ANTHROPIC_API_KEY")
    decision = route_task("draft_message_english", prompt="Write one short, friendly sentence.")
    assert decision.status in ("ok_cloud", "ok_local", "degraded_to_human")
