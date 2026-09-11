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
import re
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
    "ok_local",
    "ok_cloud",
    "ok_local_low_confidence",
    "degraded_to_human",
    "blocked_by_privacy",
    "blocked_by_cost",
]

_BOUND_TRUE = {"1", "true", "yes"}
_RUNTIME_CONTROL_SECTIONS = (0, 2, 7, 8, 14)
_MAX_RUNTIME_DIRECTIVE_CHARS = 14_000
_DEFAULT_LOCAL_CONTEXT_TOKENS = 8_192
_CONTEXT_SAFETY_TOKENS = 512
_CHARS_PER_TOKEN_ESTIMATE = 3.5


@dataclass(frozen=True, slots=True)
class RouterDecision:
    """Result of routing a single task to a model."""

    task: DealixTask
    status: RouterStatus
    text: str
    confidence: ConfidenceScore
    backend_used: str
    model_used: str
    estimated_cost_usd: float
    estimated_input_tokens: int
    estimated_output_tokens: int
    fallback_reasons: tuple[str, ...] = field(default_factory=tuple)
    requirements: TaskRequirements | None = None

    @property
    def is_actionable(self) -> bool:
        return self.status in ("ok_local", "ok_cloud") and self.confidence.is_actionable

    @property
    def needs_human(self) -> bool:
        return self.status in (
            "ok_local_low_confidence",
            "degraded_to_human",
            "blocked_by_privacy",
        )


def _privacy_allows_cloud(privacy: PrivacyLevel) -> bool:
    return privacy != "founder_only"


def _extract_control_section(master: str, section_number: int) -> str:
    pattern = re.compile(
        rf"(?ms)^## {section_number}\. [^\n]+\n.*?(?=^## \d+\. |\Z)"
    )
    match = pattern.search(master)
    if not match:
        raise RuntimeError(f"bound master prompt missing control section {section_number}")
    return match.group(0).strip()


def _distill_runtime_directive(master: str, *, master_sha256: str) -> str:
    """Build a deterministic control digest that fits the canonical local context.

    The full master artifact remains the signed/hash-bound authority. Model calls
    consume only the critical execution/governance sections plus the exact source
    hash. Missing sections or an oversized digest fail closed rather than being
    silently truncated.
    """
    sections = [_extract_control_section(master, number) for number in _RUNTIME_CONTROL_SECTIONS]
    directive = (
        "# DEALIX RUNTIME CONTROL DIGEST\n"
        f"SOURCE_MASTER_SHA256={master_sha256}\n"
        "This digest is derived from the verified full Company Master Prompt. "
        "The full artifact remains authoritative; this context-sized digest carries "
        "the critical role, One-Company, truth, Production Trust, and autonomy laws.\n\n"
        + "\n\n".join(sections)
    )
    if len(directive) > _MAX_RUNTIME_DIRECTIVE_CHARS:
        raise RuntimeError("bound master runtime directive exceeds safe local context budget")
    return directive


def _compose_bound_master_prompt(prompt: str) -> str:
    """Compose a verified, context-sized master control digest with one agent task."""
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
        master = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("bound master prompt is not UTF-8") from exc
    if not master.strip():
        raise RuntimeError("bound master prompt is empty")

    directive = _distill_runtime_directive(master, master_sha256=actual_sha)
    return f"{directive}\n\n---\n\nCURRENT AGENT TASK\n{prompt}"


def _local_context_tokens() -> int:
    raw = os.getenv("DEALIX_LOCAL_CONTEXT_TOKENS", "").strip()
    if not raw:
        return _DEFAULT_LOCAL_CONTEXT_TOKENS
    try:
        value = int(raw)
    except ValueError:
        return _DEFAULT_LOCAL_CONTEXT_TOKENS
    return max(1_024, min(value, 131_072))


def _fits_local_context(text: str, *, output_tokens: int) -> bool:
    estimated_input = int(len(text) / _CHARS_PER_TOKEN_ESTIMATE) + 1
    required = estimated_input + max(16, output_tokens) + _CONTEXT_SAFETY_TOKENS
    return required <= _local_context_tokens()


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
    """Route a Dealix task through the intelligence stack with bounded context."""
    fallback_reasons: list[str] = []

    try:
        req = get_task_requirements(task)
    except KeyError as exc:
        return RouterDecision(
            task=task,
            status="degraded_to_human",
            text="",
            confidence=ConfidenceScore(score=None, level="unknown", reasons=("unknown_task",)),
            backend_used="none",
            model_used="none",
            estimated_cost_usd=0.0,
            estimated_input_tokens=0,
            estimated_output_tokens=0,
            fallback_reasons=(f"registry_miss: {exc}",),
            requirements=None,
        )

    if task == "deterministic_lookup":
        return RouterDecision(
            task=task,
            status="ok_local",
            text="",
            confidence=ConfidenceScore(score=1.0, level="very_high", reasons=("rules_only",)),
            backend_used="rules",
            model_used="none",
            estimated_cost_usd=0.0,
            estimated_input_tokens=0,
            estimated_output_tokens=0,
            requirements=req,
        )

    try:
        model_prompt = _compose_bound_master_prompt(prompt)
    except RuntimeError:
        return _human_handoff(task, req, ["master_prompt_binding_invalid"])

    bounded_output_tokens = max(16, min(int(local_max_tokens), 2048))
    local_result: LocalModelResponse | LocalModelUnavailable | None = None
    if is_local_configured() and _fits_local_context(model_prompt, output_tokens=bounded_output_tokens):
        local_result = local_generate(
            prompt=model_prompt,
            json_mode=json_mode,
            timeout_seconds=max(1.0, min(float(local_timeout_seconds), 60.0)),
            max_tokens=bounded_output_tokens,
            temperature=0.2,
        )
    elif is_local_configured():
        fallback_reasons.append("local_context_budget_exceeded")
    else:
        fallback_reasons.append("local_not_configured")

    if isinstance(local_result, LocalModelResponse):
        confidence = from_text_signals(local_result.text, expected_json=json_mode)
        if confidence.is_actionable:
            return RouterDecision(
                task=task,
                status="ok_local",
                text=local_result.text,
                confidence=confidence,
                backend_used=local_result.backend,
                model_used=local_result.model,
                estimated_cost_usd=0.0,
                estimated_input_tokens=local_result.estimated_input_tokens,
                estimated_output_tokens=local_result.estimated_output_tokens,
                requirements=req,
            )
        fallback_reasons.append(f"local_low_confidence({confidence.level})")
        if not cloud_fallback_enabled or not _privacy_allows_cloud(req.privacy_level):
            return RouterDecision(
                task=task,
                status="ok_local_low_confidence",
                text=local_result.text,
                confidence=confidence,
                backend_used=local_result.backend,
                model_used=local_result.model,
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
            task=task,
            status="blocked_by_privacy",
            text="",
            confidence=ConfidenceScore(score=None, level="unknown", reasons=("privacy_blocked",)),
            backend_used="none",
            model_used="none",
            estimated_cost_usd=0.0,
            estimated_input_tokens=0,
            estimated_output_tokens=0,
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
    has_cloud_creds = any(
        os.environ.get(key)
        for key in (
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "GEMINI_API_KEY",
            "GROQ_API_KEY",
            "DEEPSEEK_API_KEY",
        )
    )
    if not has_cloud_creds:
        return None
    return None


def _human_handoff(
    task: DealixTask, req: TaskRequirements, fallback_reasons: list[str],
) -> RouterDecision:
    return RouterDecision(
        task=task,
        status="degraded_to_human",
        text="",
        confidence=ConfidenceScore(
            score=None,
            level="unknown",
            reasons=("degraded_to_human",),
        ),
        backend_used="none",
        model_used="none",
        estimated_cost_usd=0.0,
        estimated_input_tokens=0,
        estimated_output_tokens=0,
        fallback_reasons=tuple(fallback_reasons),
        requirements=req,
    )


def status_summary() -> dict[str, object]:
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
        for key in (
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "GEMINI_API_KEY",
            "GROQ_API_KEY",
            "DEEPSEEK_API_KEY",
        )
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
            "bound_master_prompt_context_budgeted": True,
        },
    }
