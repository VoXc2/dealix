"""
ChannelOrchestrator — picks the safest, highest-leverage channel for
contacting a prospect, given:
    - prospect record (consent_status, allowed_channels, blocked_channels)
    - customer Brain (approved_channels, blocked_channels)
    - active live-action gates (settings)
    - inbound 24h window state (last_customer_inbound_at)

Returns a ranked list of allowed channels with reasoning. Pure logic — no
I/O. Used by:
    - Sprint Day 2 (Opportunity Pack) to recommend a channel per opp
    - Sprint Day 3 (Message Pack) to validate the chosen channel
    - GET /api/v1/intelligence/channel-recommend (operator surface)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass(frozen=True)
class ChannelRecommendation:
    channel: str          # "linkedin_manual" | "email_draft" | "whatsapp_inbound_reply" | ...
    allowed: bool
    score: float          # 0..1 — higher = better
    reason_ar: str
    safe_template: str | None = None  # the template id the founder should use


_CHANNEL_LIBRARY: list[dict[str, Any]] = [
    # Allowed-by-default channels
    {
        "id": "linkedin_manual",
        "default_score": 0.85,
        "needs_consent": False,
        "needs_24h_window": False,
        "saudi_b2b_strength_ar": "قناة LinkedIn warm 1st-degree (أعلى reply rate في MENA)",
    },
    {
        "id": "email_draft",
        "default_score": 0.55,
        "needs_consent": True,  # PDPL
        "needs_24h_window": False,
        "saudi_b2b_strength_ar": "Email آمن بشرط opt-in/تفاعل سابق",
    },
    {
        "id": "referral_intro",
        "default_score": 0.95,
        "needs_consent": False,
        "needs_24h_window": False,
        "saudi_b2b_strength_ar": "أعلى تحويل (warm intro من شخص يعرفه العميل)",
    },
    {
        "id": "wa_inbound_reply",
        "default_score": 0.90,
        "needs_consent": True,
        "needs_24h_window": True,
        "saudi_b2b_strength_ar": "WhatsApp رد ضمن نافذة 24 ساعة بعد رسالة العميل",
    },
    {
        "id": "wa_template_outbound",
        "default_score": 0.40,
        "needs_consent": True,
        "needs_24h_window": False,
        "saudi_b2b_strength_ar": "Meta-approved template — يحتاج opt-in موثَّق + WHATSAPP_ALLOW_CUSTOMER_SEND",
    },
    # Blocked-by-default channels — labels carry blocked_ marker on every line
    {"id": "cold_whatsapp", "blocked_label": True,  # blocked_label
        "default_score": 0.0, "needs_consent": True, "needs_24h_window": False,
        "saudi_b2b_strength_ar": "BLOCKED — يخالف PDPL + WhatsApp ToS (غرامة حتى 5M SAR)",
        "always_blocked": True,
    },
    {"id": "linkedin_auto_dm", "blocked_label": True,  # blocked_label
        "default_score": 0.0, "needs_consent": False, "needs_24h_window": False,
        "saudi_b2b_strength_ar": "BLOCKED — يخالف LinkedIn ToS، يُغلق الحساب",
        "always_blocked": True,
    },
    {
        "id": "purchased_list_blast",
        "default_score": 0.0,
        "needs_consent": True,
        "needs_24h_window": False,
        "saudi_b2b_strength_ar": "BLOCKED — قائمة بدون consent = غرامة PDPL مباشرة",
        "always_blocked": True,
    },
]


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _is_in_wa_window(last_inbound_at: datetime | str | None) -> bool:
    if not last_inbound_at:
        return False
    if isinstance(last_inbound_at, str):
        try:
            d = datetime.fromisoformat(last_inbound_at.replace("Z", "+00:00"))
            last_inbound_at = d.astimezone(timezone.utc).replace(tzinfo=None) if d.tzinfo else d
        except (ValueError, TypeError):
            return False
    return (_now() - last_inbound_at) < timedelta(hours=24)


def recommend(
    prospect: dict[str, Any] | None = None,
    brain: dict[str, Any] | None = None,
    gates: dict[str, bool] | None = None,
) -> list[ChannelRecommendation]:
    """Return ranked list of channel recommendations.

    Args:
      prospect: dict-like with keys consent_status, allowed_channels,
                blocked_channels, last_customer_inbound_at
      brain: dict-like with approved_channels + blocked_channels
      gates: dict of live-action gates (settings flags)

    Output is sorted: allowed first by score, then blocked with reasoning.
    """
    p = prospect or {}
    b = brain or {}
    g = gates or {}

    p_allowed = set(p.get("allowed_channels") or [])
    p_blocked = set(p.get("blocked_channels") or [])
    b_approved = set(b.get("approved_channels") or [])
    b_blocked = set(b.get("blocked_channels") or [])

    consent_recorded = (p.get("consent_status") == "opt_in_recorded")
    in_wa_window = _is_in_wa_window(p.get("last_customer_inbound_at"))

    out: list[ChannelRecommendation] = []
    for ch in _CHANNEL_LIBRARY:
        cid = ch["id"]
        score = float(ch["default_score"])
        reasons: list[str] = []
        allowed = True

        # Hard policy: cold/auto/scrape are immutable blocks
        if ch.get("always_blocked"):
            out.append(ChannelRecommendation(
                channel=cid,
                allowed=False,
                score=0.0,
                reason_ar=ch["saudi_b2b_strength_ar"],
            ))
            continue

        # Customer Brain blocks override prospect allowlist
        if cid in b_blocked or cid in p_blocked:
            allowed = False
            reasons.append("blocked-by-policy")

        # Channel needs consent → check
        if ch["needs_consent"] and not consent_recorded:
            if cid not in ("linkedin_manual",):  # warm-LinkedIn is consent-implicit when 1st-degree
                allowed = False
                reasons.append("no-consent-recorded")

        # WhatsApp 24h window check
        if ch["needs_24h_window"] and not in_wa_window:
            allowed = False
            reasons.append("outside-24h-service-window")

        # Live-action gates
        if cid == "wa_template_outbound":
            if not g.get("whatsapp_allow_customer_send", False):
                allowed = False
                reasons.append("gate-WHATSAPP_ALLOW_CUSTOMER_SEND-false")
        if cid == "wa_inbound_reply":
            if not g.get("whatsapp_allow_customer_send", False):
                # Reply is allowed conceptually, but the actual send still
                # requires the gate. We mark allowed but with reduced score.
                score *= 0.7
                reasons.append("gate-customer_send-false-(can-prepare-only)")

        # Prospect explicit allowlist boost
        if cid in p_allowed:
            score = min(1.0, score + 0.05)
            reasons.append("prospect-allowlisted")
        # Brain allowlist boost
        if cid in b_approved:
            score = min(1.0, score + 0.05)
            reasons.append("brain-approved")

        out.append(ChannelRecommendation(
            channel=cid,
            allowed=allowed,
            score=round(score, 3),
            reason_ar=ch["saudi_b2b_strength_ar"]
                + (f" — {'، '.join(reasons)}" if reasons else ""),
        ))

    # Sort: allowed first, then by score desc
    out.sort(key=lambda r: (-int(r.allowed), -r.score))
    return out


def best_allowed(
    prospect: dict[str, Any] | None = None,
    brain: dict[str, Any] | None = None,
    gates: dict[str, bool] | None = None,
) -> ChannelRecommendation | None:
    """Return the single best allowed channel, or None if all blocked."""
    recs = recommend(prospect, brain, gates)
    for r in recs:
        if r.allowed:
            return r
    return None
