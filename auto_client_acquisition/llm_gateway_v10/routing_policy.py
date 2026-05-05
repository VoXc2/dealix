"""Deterministic intent → tier router + cost estimator.

Pure: no I/O, no LLM calls, no external HTTP. The router's only job
is to translate a free-form ``task_purpose`` into a tier choice +
bounded cost estimate + bilingual reason string.
"""
from __future__ import annotations

from auto_client_acquisition.llm_gateway_v10.cache_policy import cache_key
from auto_client_acquisition.llm_gateway_v10.model_catalog import lookup_model
from auto_client_acquisition.llm_gateway_v10.schemas import (
    CostEstimate,
    ModelTier,
    RoutingDecision,
    RoutingPolicy,
)
from auto_client_acquisition.llm_gateway_v10.token_estimator import estimate_tokens


# Order matters — first hit wins. Keeps the mapping purpose-bound.
_TIER_KEYWORDS: tuple[tuple[ModelTier, tuple[str, ...]], ...] = (
    (
        ModelTier.local_no_model,
        ("deterministic", "lookup"),
    ),
    (
        ModelTier.strong_for_strategy,
        ("strategy", "plan", "review", "audit"),
    ),
    (
        ModelTier.balanced_for_drafts,
        ("draft", "summary", "translation"),
    ),
    (
        ModelTier.cheap_for_classification,
        ("classification", "qualification", "scoring"),
    ),
)


_PER_ESTIMATE_USD_CEILING: float = 0.40


def _pick_tier(task_purpose: str) -> ModelTier:
    needle = (task_purpose or "").strip().lower()
    for tier, keywords in _TIER_KEYWORDS:
        for kw in keywords:
            if kw in needle:
                return tier
    # Unknown intents must not silently escalate — default cheapest.
    return ModelTier.cheap_for_classification


def estimate_cost(req: RoutingPolicy) -> CostEstimate:
    """Return a bounded :class:`CostEstimate` for ``req`` (no I/O)."""
    try:
        tier = _pick_tier(req.task_purpose)
        # Input tokens approximated from purpose + handle, bounded by max_tokens.
        seed_text = f"{req.task_purpose} {req.customer_handle}".strip()
        in_tok_raw = estimate_tokens(seed_text, multiplier=2.0)
        in_tok = max(64, min(in_tok_raw or 64, int(req.max_tokens)))
        # Output is heuristically smaller than input — bounded by max_tokens.
        out_tok = max(32, min(int(in_tok * 0.6), int(req.max_tokens)))

        catalog = lookup_model(tier, req.language)
        rate_in = float(catalog.get("input_cost_per_1k_usd", 0.0))
        rate_out = float(catalog.get("output_cost_per_1k_usd", 0.0))
        usd = (in_tok / 1000.0) * rate_in + (out_tok / 1000.0) * rate_out
        usd = round(min(usd, _PER_ESTIMATE_USD_CEILING), 6)

        return CostEstimate(
            tier=tier,
            estimated_input_tokens=int(in_tok),
            estimated_output_tokens=int(out_tok),
            estimated_usd=usd,
            cache_key=cache_key(req),
            stop_when_good_enough=True,
            human_review_when_budget_exceeded=True,
        )
    except Exception:  # noqa: BLE001 - never crash routing
        return CostEstimate(
            tier=ModelTier.local_no_model,
            estimated_input_tokens=0,
            estimated_output_tokens=0,
            estimated_usd=0.0,
            cache_key="",
            stop_when_good_enough=True,
            human_review_when_budget_exceeded=True,
        )


_REASON_AR: dict[ModelTier, str] = {
    ModelTier.cheap_for_classification: "تم اختيار الفئة الاقتصادية للتصنيف.",
    ModelTier.balanced_for_drafts: "تم اختيار الفئة المتوازنة لكتابة المسودات.",
    ModelTier.strong_for_strategy: "تم اختيار الفئة الأقوى للمهام الاستراتيجية.",
    ModelTier.local_no_model: "تم تنفيذ المهمة محلياً بدون نموذج.",
}
_REASON_EN: dict[ModelTier, str] = {
    ModelTier.cheap_for_classification: "Cheap tier selected for classification-style task.",
    ModelTier.balanced_for_drafts: "Balanced tier selected for drafting/summary task.",
    ModelTier.strong_for_strategy: "Strong tier selected for strategy/audit reasoning.",
    ModelTier.local_no_model: "Routed locally — deterministic lookup, no model call.",
}


def route(req: RoutingPolicy) -> RoutingDecision:
    """Return a :class:`RoutingDecision` for the given policy."""
    try:
        est = estimate_cost(req)
        # Action defaults to proceed; hard ceilings get pause_for_approval.
        action = "proceed"
        if est.estimated_usd >= _PER_ESTIMATE_USD_CEILING:
            action = "pause_for_approval"
        return RoutingDecision(
            tier=est.tier,
            cost_estimate=est,
            action=action,  # type: ignore[arg-type]
            reason_ar=_REASON_AR.get(est.tier, "تم اختيار الفئة الافتراضية."),
            reason_en=_REASON_EN.get(est.tier, "Default tier selected."),
        )
    except Exception:  # noqa: BLE001 - degrade to local
        est = CostEstimate(
            tier=ModelTier.local_no_model,
            estimated_input_tokens=0,
            estimated_output_tokens=0,
            estimated_usd=0.0,
        )
        return RoutingDecision(
            tier=ModelTier.local_no_model,
            cost_estimate=est,
            action="hard_stop",
            reason_ar="تعذر التوجيه — تم الإيقاف بأمان.",
            reason_en="Routing failed — safe hard stop.",
        )
