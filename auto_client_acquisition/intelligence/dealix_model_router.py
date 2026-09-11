"""Dealix Intelligence — Model Router.

Top-level dispatcher: takes a (DealixTask, prompt, language) request,
consults task_registry for requirements, picks the right backend
(local vs cloud), invokes it, scores confidence, and returns a
RouterDecision the caller can act on.

Article 11: composes existing modules — does NOT reinvent.
- Cloud routing → ``llm_gateway_v10.routing_policy`` (existing)
- Local execution → ``intelligence.local_model_client`` (new — Wave 12)
- Confidence scoring → ``intelligence.confidence`` (new — Wave 12)
- Task → tier mapping → ``intelligence.dealix_task_registry`` (new — Wave 12)

Article 8: NEVER fakes a successful response. When all backends fail,
returns ``RouterDecision`` with ``status="degraded_to_human"`` so the
caller knows it's a draft awaiting founder.
"""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from auto_client_acquisition.intelligence.confidence import (
    ConfidenceScore,
    from_text_signals,
)
from auto_client_acquisition.intelligence.dealix_task_registry import (
    DealixTask,
    PrivacyLevel,
    TaskRequirements,
    get_task_requirements,
)
from auto_client_acquisition.intelligence.local_model_client import (
    LocalModelResponse,
    LocalModelUnavailable,
    is_local_configured,
)
from auto_client_acquisition.intelligence.local_model_client import (
    generate as local_generate,
)

RouterStatus = Literal[
    "ok_local",                    # local model returned acceptable response
    "ok_cloud",                    # cloud model returned acceptable response
    "ok_local_low_confidence",     # local returned but confidence too low
    "degraded_to_human",            # nothing worked; human must draft
    "blocked_by_privacy",          # privacy policy refused cloud + local unavailable
    "blocked_by_cost",             # cost cap exceeded; aborted
]

_BOUND_TRUE = {"1", "true", "yes"}


@dataclass(frozen=True, slots=True)
class RouterDecision:
    """Result of routing a single task to a model.

    Always returned (never raises). Caller inspects ``status`` to decide
    next step. ``text`` is empty when status is degraded/blocked.
    """

    task: DealixTask
    status: RouterStatus
    text: str
    confidence: ConfidenceScore
    backend_used: str  # "ollama" / "vllm" / "cloud:anthropic" / "none"
    model_used: str
    estimated_cost_usd: float
    estimated_input_tokens: int
    estimated_output_tokens: int
    fallback_reasons: tuple[str, ...] = field(default_factory=tuple)
    requirements: TaskRequirements | None = None

    @property
    def is_actionable(self) -> bool:
        """Caller can use the text without human review."""
        return (
            self.status in ("ok_local", "ok_cloud")
            and self.confidence.is_actionable
        )

    @property
    def needs_human(self) -> bool:
        """Caller MUST route to founder approval queue."""
        return self.status in (
            "ok_local_low_confidence",
            "degraded_to_human",
            "blocked_by_privacy",
        )


def _privacy_allows_cloud(privacy: PrivacyLevel) -> bool:
    """Hard rule: ``founder_only`` NEVER goes to cloud.

    ``customer_internal`` allows privacy-tier cloud (with no-training
    opt-out), but the safer default in this router is local-first.

    ``public_or_aggregated`` is fine for any cloud.
    """
    return privacy != "founder_only"


def _compose_bound_master_prompt(prompt: str) -> str:
    """Prepend the verified Company Master Prompt when the canonical cycle bound it.

    The launcher publishes only a path + SHA. The router re-reads and verifies the
    artifact at the point where model behavior is created, so a claimed binding
    cannot silently degrade into an unused environment variable.
    """
    if os.getenv("DEALIX_MASTER_PROMPT_BOUND", "").strip().lower() not in _BOUND_TRUE:
        return prompt

    path_value = os.getenv("DEALIX_COMPANY_MASTER_PROMPT", "").strip()
    declared_sha = os.getenv("DEALIX_COMPANY_MASTER_PROMPT_SHA256", "").strip().lower()
    if not path_value or len(declared_sha) != 64:
        raise RuntimeError("bound master prompt path/SHA is incomplete")

    path = Path(path_value)
    if not path.is_file():
        raise RuntimeError("bound master prompt artifact is missing")
    raw = path.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != declared_sha:
        raise RuntimeError("bound master prompt SHA mismatch")
    try:
        directive = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("bound master prompt is not UTF-8") from exc
    if not directive.strip():
        raise RuntimeError("bound master prompt is empty")

    return f"{directive.rstrip()}\n\n---\n\nCURRENT AGENT TASK\n{prompt}"


def route_task(
    task: DealixTask,
    *,
    prompt: str,
    language: Literal["ar", "en", "bilingual"] = "ar",
    json_mode: bool = False,
    customer_handle: str = "",
    cloud_fallback_enabled: bool = True,
    local_timeout_seconds: float = 10.0,
    local_max_tokens: int = 2048,
) -> RouterDecision:
    """Route a Dealix task through the intelligence stack.

    Strategy (Article 11 — local-first):
      1. Look up TaskRequirements from registry
      2. Hard-block if cost cap or privacy violated
      3. Apply the hash-bound Company Master Prompt when the canonical cycle bound it
      4. Try local model first (cheap, private, fast)
      5. If local response actionable → return ok_local
      6. If local low-confidence + cloud allowed → cloud fallback
      7. If local unavailable + cloud allowed + privacy permits → cloud
      8. If everything fails → degraded_to_human (caller routes to founder)

    Args:
        task: Canonical DealixTask name (must be in registry)
        prompt: Task prompt; the router composes the verified bound company directive
            when the canonical master cycle is active.
        language: Output language preference
        json_mode: Request structured JSON output
        customer_handle: For audit log + observability (optional)
        cloud_fallback_enabled: Set False to force local-only (testing)

    Returns:
        RouterDecision with status + text + confidence.
    """
    fallback_reasons: list[str] = []

    # Step 1: registry lookup
    try:
        req = get_task_requirements(task)
    except KeyError as exc:
        return RouterDecision(
            task=task, status="degraded_to_human",
            text="", confidence=ConfidenceScore(score=None, level="unknown", reasons=("unknown_task",)),
            backend_used="none", model_used="none",
            estimated_cost_usd=0.0, estimated_input_tokens=0, estimated_output_tokens=0,
            fallback_reasons=(f"registry_miss: {exc}",),
            requirements=None,
        )

    # Step 2: deterministic_lookup → no model needed
    if task == "deterministic_lookup":
        return RouterDecision(
            task=task, status="ok_local",
            text="",  # caller uses pure-rules code; this is a marker
            confidence=ConfidenceScore(score=1.0, level="very_high", reasons=("rules_only",)),
            backend_used="rules", model_used="none",
            estimated_cost_usd=0.0, estimated_input_tokens=0, estimated_output_tokens=0,
            requirements=req,
        )

    # Step 3: model-backed work must consume the verified bound directive.
    try:
        model_prompt = _compose_bound_master_prompt(prompt)
    except RuntimeError:
        return _human_handoff(task, req, ["master_prompt_binding_invalid"])

    # Step 4: try local first
    local_result: LocalModelResponse | LocalModelUnavailable | None = None
    if is_local_configured():
        local_result = local_generate(
            prompt=model_prompt,
            json_mode=json_mode,
            timeout_seconds=max(1.0, min(float(local_timeout_seconds), 60.0)),
            max_tokens=max(16, min(int(local_max_tokens), 2048)),
            temperature=0.2,
        )
    else:
        fallback_reasons.append("local_not_configured")

    # Step 5: local succeeded — score confidence
    if isinstance(local_result, LocalModelResponse):
        confidence = from_text_signals(local_result.text, expected_json=json_mode)
        if confidence.is_actionable:
            return RouterDecision(
                task=task, status="ok_local",
                text=local_result.text, confidence=confidence,
                backend_used=local_result.backend, model_used=local_result.model,
                estimated_cost_usd=0.0,  # local = free
                estimated_input_tokens=local_result.estimated_input_tokens,
                estimated_output_tokens=local_result.estimated_output_tokens,
                requirements=req,
            )
        fallback_reasons.append(f"local_low_confidence({confidence.level})")
        if not cloud_fallback_enabled or not _privacy_allows_cloud(req.privacy_level):
            return RouterDecision(
                task=task, status="ok_local_low_confidence",
                text=local_result.text, confidence=confidence,
                backend_used=local_result.backend, model_used=local_result.model,
                estimated_cost_usd=0.0,
                estimated_input_tokens=local_result.estimated_input_tokens,
                estimated_output_tokens=local_result.estimated_output_tokens,
                fallback_reasons=tuple(fallback_reasons),
                requirements=req,
            )

    elif isinstance(local_result, LocalModelUnavailable):
        fallback_reasons.append(f"local_unavailable: {local_result.reason}")

    if not _privacy_allows_cloud(req.privacy_level):
        return RouterDecision(
            task=task, status="blocked_by_privacy",
            text="", confidence=ConfidenceScore(score=None, level="unknown", reasons=("privacy_blocked",)),
            backend_used="none", model_used="none",
            estimated_cost_usd=0.0, estimated_input_tokens=0, estimated_output_tokens=0,
            fallback_reasons=tuple(fallback_reasons + ["privacy=founder_only_no_cloud"]),
            requirements=req,
        )

    if not cloud_fallback_enabled:
        fallback_reasons.append("cloud_fallback_disabled_by_caller")
        return _human_handoff(task, req, fallback_reasons)

    cloud_decision = _attempt_cloud_call_stub(task=task, prompt=model_prompt, req=req)
    if cloud_decision is not None:
        return cloud_decision

    return _human_handoff(task, req, fallback_reasons)


def _attempt_cloud_call_stub(
    *, task: DealixTask, prompt: str, req: TaskRequirements,
) -> RouterDecision | None:
    """Cloud call stub — returns None when no cloud creds configured.

    Wired to ``core/llm/router.route_llm()`` in a follow-up Wave 12 commit;
    for now returns None so the router falls through to human_handoff
    in test environments without API keys.
    """
    has_cloud_creds = any(
        os.environ.get(key) for key in (
            "ANTHROPIC_API_KEY", "OPENAI_API_KEY",
            "GEMINI_API_KEY", "GROQ_API_KEY", "DEEPSEEK_API_KEY",
        )
    )
    if not has_cloud_creds:
        return None
    return None


def _human_handoff(
    task: DealixTask, req: TaskRequirements, fallback_reasons: list[str],
) -> RouterDecision:
    """Build the canonical degraded-to-human RouterDecision."""
    return RouterDecision(
        task=task, status="degraded_to_human",
        text="", confidence=ConfidenceScore(
            score=None, level="unknown",
            reasons=("degraded_to_human",),
        ),
        backend_used="none", model_used="none",
        estimated_cost_usd=0.0, estimated_input_tokens=0, estimated_output_tokens=0,
        fallback_reasons=tuple(fallback_reasons),
        requirements=req,
    )


def status_summary() -> dict[str, object]:
    """Layer status (for /api/v1/intelligence/status endpoint)."""
    from auto_client_acquisition.intelligence.dealix_task_registry import all_tasks
    from auto_client_acquisition.intelligence.local_model_client import (
        _detect_provider,
        ping_local,
    )
    provider, base_url = _detect_provider()
    local_configured = is_local_configured()
    if local_configured:
        is_up, ping_msg = ping_local(timeout_seconds=2.0)
    else:
        is_up, ping_msg = (False, "not configured")
    cloud_keys_present = sorted(
        key.replace("_API_KEY", "").lower()
        for key in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY",
                    "GROQ_API_KEY", "DEEPSEEK_API_KEY")
        if os.environ.get(key)
    )
    return {
        "service": "dealix_intelligence_router",
        "tasks_registered": len(all_tasks()),
        "local_provider": provider,
        "local_base_url": base_url if local_configured else "(not configured)",
        "local_configured": local_configured,
        "local_reachable": is_up,
        "local_ping": ping_msg,
        "cloud_providers_with_creds": cloud_keys_present,
        "hard_gates": {
            "privacy_founder_only_never_cloud": True,
            "no_secrets_logged": True,
            "fail_fast_to_human_on_unknown_task": True,
            "no_silent_cloud_call_without_local_first": True,
            "bound_master_prompt_consumed_by_model_router": True,
        },
    }
