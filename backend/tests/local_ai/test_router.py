"""Unit tests for the LocalModelRouter."""
from __future__ import annotations

import os
from unittest import mock

import pytest

from app.services.local_ai.client import OllamaChatResult
from app.services.local_ai.router import (
    LocalModelRouter,
    _pick_better_result,
)
from app.services.local_ai.catalog import TaskKind


# ── Task mapping ──────────────────────────────────────────────────

@pytest.mark.parametrize("task_string,expected", [
    ("fast_classify", TaskKind.ROUTER),
    ("arabic_summarization", TaskKind.MULTILINGUAL),
    ("coding", TaskKind.CODER),
    ("research", TaskKind.REASONER),
    ("unknown_task", TaskKind.GENERAL),
])
def test_resolve_task_maps_known_strings(task_string, expected):
    with mock.patch.dict(os.environ, {"LOCAL_LLM_FORCE_TIER": "balanced"}):
        r = LocalModelRouter()
    assert r.resolve_task(task_string) == expected


# ── Env overrides ─────────────────────────────────────────────────

def test_env_override_for_router_model_is_respected():
    with mock.patch.dict(os.environ, {
        "LOCAL_LLM_FORCE_TIER": "balanced",
        "LOCAL_LLM_ROUTER_MODEL": "my-tiny-model",
    }):
        r = LocalModelRouter()
    decision = r.decide(TaskKind.ROUTER)
    assert decision.available is True
    assert decision.model is not None
    assert decision.model.ollama_tag == "my-tiny-model"
    assert decision.reason == "env override"


def test_env_override_for_coder_model_is_respected():
    with mock.patch.dict(os.environ, {
        "LOCAL_LLM_FORCE_TIER": "balanced",
        "LOCAL_LLM_CODER_MODEL": "my-coder",
    }):
        r = LocalModelRouter()
    decision = r.decide(TaskKind.CODER)
    assert decision.model is not None
    assert decision.model.ollama_tag == "my-coder"


def test_decide_catalog_pick_on_balanced_tier():
    with mock.patch.dict(os.environ, {"LOCAL_LLM_FORCE_TIER": "balanced"}, clear=False):
        # Clear overrides
        for k in ("LOCAL_LLM_DEFAULT_MODEL", "LOCAL_LLM_ROUTER_MODEL",
                   "LOCAL_LLM_CODER_MODEL", "LOCAL_LLM_REASONER_MODEL"):
            os.environ.pop(k, None)
        r = LocalModelRouter()
        decision = r.decide(TaskKind.MULTILINGUAL)
    assert decision.available is True
    assert decision.model is not None
    assert decision.reason == "catalog pick"
    assert decision.model.family == "qwen2.5"


# ── Enablement gate ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_is_enabled_false_by_default():
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop("LOCAL_LLM_ENABLED", None)
        r = LocalModelRouter()
        assert r.is_enabled() is False


@pytest.mark.asyncio
async def test_is_enabled_true_when_env_set():
    with mock.patch.dict(os.environ, {"LOCAL_LLM_ENABLED": "1"}):
        r = LocalModelRouter()
        assert r.is_enabled() is True


@pytest.mark.asyncio
async def test_run_returns_disabled_error_when_flag_off():
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop("LOCAL_LLM_ENABLED", None)
        r = LocalModelRouter()
        result = await r.run(task="internal_drafting", prompt="hi")
    assert result.success is False
    assert "local_llm_enabled" in (result.error or "").lower()


# ── Race evaluator ────────────────────────────────────────────────

def _ok(model: str, content: str, latency_ms: int = 100) -> OllamaChatResult:
    return OllamaChatResult(model=model, content=content, latency_ms=latency_ms,
                            total_tokens=len(content), success=True)


def _fail(model: str, latency_ms: int = 100) -> OllamaChatResult:
    return OllamaChatResult(model=model, content="", latency_ms=latency_ms,
                            success=False, error="boom")


def test_pick_better_prefers_success_over_failure():
    a, b = _ok("a", "some answer"), _fail("b")
    assert _pick_better_result(a, b).model == "a"
    assert _pick_better_result(b, a).model == "a"


def test_pick_better_prefers_longer_meaningful_response():
    a = _ok("a", "too short")   # < 40 chars → heavily penalized
    b = _ok("b", "This is a properly detailed answer with enough content to be useful.")
    assert _pick_better_result(a, b).model == "b"


def test_pick_better_breaks_tie_on_both_failed_with_lower_latency():
    a = _fail("a", latency_ms=500)
    b = _fail("b", latency_ms=100)
    assert _pick_better_result(a, b).model == "b"
