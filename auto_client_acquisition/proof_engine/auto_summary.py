"""Wave 12.5 §33.2.5 — Proof Event Auto-Summary (deterministic v1).

Bilingual executive summary auto-generation from proof events.
v1 uses templates per ``event_type`` — no LLM (deterministic, testable,
zero-cost). v2 (post-Article-13) can swap to Intelligence Layer router
if customer demands richer narrative.

Hard rule (Article 8): summaries reference ONLY recorded events.
NEVER fabricates metrics, customer quotes, or outcomes that aren't
explicitly in the source proof event.

Hard rule (proof_engine/evidence.py): summaries refuse to mention
public quotes / case-study language unless evidence_level >= L4.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.proof_engine.evidence import EvidenceLevel


@dataclass(frozen=True, slots=True)
class ProofSummary:
    """Bilingual auto-generated summary of a proof event."""

    event_id: str
    headline_ar: str
    headline_en: str
    detail_ar: str
    detail_en: str
    metric_text_ar: str
    metric_text_en: str
    is_public_publishable: bool
    publish_block_reason: str  # empty when publishable
    evidence_level: int
    sources_used: tuple[str, ...] = field(default_factory=tuple)


# ─────────────────────────────────────────────────────────────────────
# Template registry — one bilingual template per known event_type.
# Add new templates only when a new event_type is introduced.
# ─────────────────────────────────────────────────────────────────────
_TEMPLATES: dict[str, dict[str, str]] = {
    # Generic / fallback templates
    "deliverable_completed": {
        "headline_ar": "تم تسليم {what}",
        "headline_en": "Delivered {what}",
        "detail_ar": "تم تسليم {what} للعميل {customer} في {when}.",
        "detail_en": "Delivered {what} to {customer} on {when}.",
    },
    "demo_booked": {
        "headline_ar": "حجز عرض توضيحي",
        "headline_en": "Demo booked",
        "detail_ar": "تم حجز عرض توضيحي مع {customer} في {when}.",
        "detail_en": "Demo booked with {customer} on {when}.",
    },
    "diagnostic_delivered": {
        "headline_ar": "تشخيص مُسلَّم",
        "headline_en": "Diagnostic delivered",
        "detail_ar": "تم تسليم التشخيص لـ {customer} متضمناً {detail}.",
        "detail_en": "Delivered diagnostic to {customer} including {detail}.",
    },
    "payment_confirmed": {
        "headline_ar": "تأكيد دفع",
        "headline_en": "Payment confirmed",
        "detail_ar": "تأكَّد الدفع من {customer} بمبلغ {amount} ر.س في {when}.",
        "detail_en": "Payment confirmed from {customer} for SAR {amount} on {when}.",
    },
    "proof_pack_assembled": {
        "headline_ar": "تجميع Proof Pack",
        "headline_en": "Proof Pack assembled",
        "detail_ar": "تم تجميع Proof Pack لـ {customer} يحوي {event_count} حدث.",
        "detail_en": "Assembled Proof Pack for {customer} containing {event_count} events.",
    },
    "expansion_offered": {
        "headline_ar": "اقتراح توسعة",
        "headline_en": "Expansion offered",
        "detail_ar": "اقتُرح على {customer} باقة {offer} بناءً على نتائج {basis}.",
        "detail_en": "Offered {customer} the {offer} package based on {basis} results.",
    },
}


def _safe_format(template: str, **kwargs: Any) -> str:
    """Format template with safe defaults — missing keys → ``[—]``.

    Article 8: NEVER raises on missing keys (would mask the issue).
    Instead, surfaces the gap visibly so reader knows the source data
    was incomplete.
    """
    class _Defaulter(dict):
        def __missing__(self, key: str) -> str:
            return "[—]"
    return template.format_map(_Defaulter(**{k: str(v) for k, v in kwargs.items()}))


def _metric_text(metric: dict[str, Any] | None) -> tuple[str, str]:
    """Render the metric block in both languages.

    Article 8: when metric.before is None, says "baseline pending"
    instead of inventing a number.
    """
    if not metric:
        return ("(لا توجد قيم مُسجَّلة)", "(no recorded values)")
    name = metric.get("name", "metric")
    unit = metric.get("unit", "")
    before = metric.get("before")
    after = metric.get("after")
    if before is None and after is None:
        return (f"{name}: (لا قيم)", f"{name}: (no values)")
    if before is None:
        return (
            f"{name}: قبل غير مُسجَّل، بعد {after} {unit}",
            f"{name}: baseline pending, after {after} {unit}",
        )
    if after is None:
        return (
            f"{name}: قبل {before} {unit}، بعد قيد الجمع",
            f"{name}: before {before} {unit}, after pending collection",
        )
    return (
        f"{name}: من {before} إلى {after} {unit}",
        f"{name}: from {before} to {after} {unit}",
    )


def build_summary(
    *,
    event_id: str,
    event_type: str,
    customer_handle: str,
    evidence_level: int,
    consent_status: str = "internal_only",
    approval_status: str = "pending",
    metric: dict[str, Any] | None = None,
    detail_ar: str = "",
    detail_en: str = "",
    when: str = "[—]",
    extra: dict[str, Any] | None = None,
) -> ProofSummary:
    """Build a bilingual auto-summary from a proof event.

    Args:
        event_id: Unique proof event identifier.
        event_type: One of the known template keys (else falls back to
            generic ``deliverable_completed`` template).
        customer_handle: Tenant scope (rendered as {customer}).
        evidence_level: L0-L5 IntEnum value.
        consent_status: ``internal_only | granted | revoked``.
        approval_status: ``pending | approved | rejected``.
        metric: Optional dict with name/unit/before/after.
        detail_ar / detail_en: Optional explicit detail strings.
        when: ISO date or "today" — rendered into templates.
        extra: Optional dict of extra format kwargs (amount, offer, etc.).

    Returns:
        ProofSummary with publish-eligibility precomputed.
    """
    extra = extra or {}
    template = _TEMPLATES.get(event_type, _TEMPLATES["deliverable_completed"])

    # Compose template kwargs
    kwargs = {
        "customer": customer_handle,
        "when": when,
        "detail": detail_ar or "[—]",
        "what": event_type.replace("_", " "),
        **extra,
    }
    headline_ar = _safe_format(template["headline_ar"], **kwargs)
    headline_en = _safe_format(template["headline_en"], **kwargs)

    # Detail: prefer explicit caller-provided over template default
    d_ar = detail_ar or _safe_format(template["detail_ar"], **kwargs)
    if detail_en:
        d_en = detail_en
    else:
        d_en = _safe_format(template["detail_en"], **{**kwargs, "detail": detail_en or "[—]"})

    metric_ar, metric_en = _metric_text(metric)

    # Publish gate (Article 8 + proof_engine.evidence rules)
    is_pub, block_reason = _check_publish_eligibility(
        evidence_level=evidence_level,
        consent_status=consent_status,
        approval_status=approval_status,
    )

    sources = tuple(filter(None, [
        f"event_id={event_id}",
        f"event_type={event_type}",
        f"evidence_level=L{evidence_level}",
        f"consent={consent_status}",
        f"approval={approval_status}",
    ]))

    return ProofSummary(
        event_id=event_id,
        headline_ar=headline_ar,
        headline_en=headline_en,
        detail_ar=d_ar,
        detail_en=d_en,
        metric_text_ar=metric_ar,
        metric_text_en=metric_en,
        is_public_publishable=is_pub,
        publish_block_reason=block_reason,
        evidence_level=evidence_level,
        sources_used=sources,
    )


def _check_publish_eligibility(
    *, evidence_level: int, consent_status: str, approval_status: str,
) -> tuple[bool, str]:
    """Hard rule: public proof requires evidence_level >= L4 AND
    consent_status == granted AND approval_status == approved.

    Returns (is_publishable, block_reason). When publishable,
    block_reason is empty.
    """
    if evidence_level < EvidenceLevel.L4_PUBLIC_APPROVED:
        return (False, f"evidence_level=L{evidence_level} < L4_PUBLIC_APPROVED")
    if consent_status != "granted":
        return (False, f"consent_status={consent_status!r} != 'granted'")
    if approval_status != "approved":
        return (False, f"approval_status={approval_status!r} != 'approved'")
    return (True, "")


def known_event_types() -> tuple[str, ...]:
    """All event types that have explicit templates."""
    return tuple(_TEMPLATES.keys())
