"""Reviewer agent — deterministic.

Inspired by AutoGen's reviewer pattern. Pure local: scans every prior
output for forbidden tokens. If any are found → ``blocked``. If
outputs are coherent (>=1 entry, no errors) → ``approved``. Otherwise
→ ``needs_revision``.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_workforce_v10.schemas import ReviewerOutput

# Hard-coded forbidden tokens. Marketing claims, scraping markers, PII
# leak indicators. Lowercased before scan.
_FORBIDDEN_TOKENS: tuple[str, ...] = (
    "guaranteed roi",
    "guaranteed revenue",
    "100% success",
    "scrape linkedin",
    "linkedin scraping",
    "buy this list",
    "personal phone",
    "personal email",
)


def _stringify(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(_stringify(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(_stringify(v) for v in value)
    return str(value or "")


def run_reviewer(prior_outputs: list[dict]) -> ReviewerOutput:
    """Scan ``prior_outputs`` for forbidden tokens and overall coherence."""
    if not prior_outputs:
        return ReviewerOutput(
            verdict="needs_revision",
            reasons_ar=["لا توجد مخرجات للمراجعة."],
            reasons_en=["no outputs to review"],
        )

    blocked: list[str] = []
    error_count = 0
    for entry in prior_outputs:
        if not isinstance(entry, dict):
            continue
        if entry.get("error"):
            error_count += 1
        flat = _stringify(entry).lower()
        for token in _FORBIDDEN_TOKENS:
            if token in flat and token not in blocked:
                blocked.append(token)

    if blocked:
        return ReviewerOutput(
            verdict="blocked",
            reasons_ar=["تم اكتشاف لغة محظورة."],
            reasons_en=[f"forbidden token detected: {b}" for b in blocked],
            blocked_tokens=blocked,
        )

    if error_count and error_count >= len(prior_outputs):
        return ReviewerOutput(
            verdict="needs_revision",
            reasons_ar=["جميع الوكلاء فشلوا — يلزم إعادة التشغيل."],
            reasons_en=["all agents errored — needs revision"],
        )

    if error_count:
        return ReviewerOutput(
            verdict="needs_revision",
            reasons_ar=[f"عدد {error_count} وكيل فشل."],
            reasons_en=[f"{error_count} agent(s) errored"],
        )

    return ReviewerOutput(
        verdict="approved",
        reasons_ar=["المخرجات مكتملة ولا تحتوي على لغة محظورة."],
        reasons_en=["outputs complete and free of forbidden tokens"],
    )
