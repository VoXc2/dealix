"""Channel posture helpers (documentation + deterministic string checks)."""

from __future__ import annotations

from auto_client_acquisition.governance_os.forbidden_actions import (
    FORBIDDEN_CHANNEL_MARKERS,
    is_channel_forbidden,
)

CHANNEL_POLICY_AR = (
    "لا إرسال واتساب بارد، ولا أتمتة لينكدإن، ولا قنوات ممنوعة في المسودات."
)


def forbidden_channel_markers() -> tuple[str, ...]:
    return FORBIDDEN_CHANNEL_MARKERS


def draft_text_has_forbidden_channel_language(text: str) -> bool:
    return is_channel_forbidden(text)


# Hard-forbidden (channel, mode) combinations — non-negotiable refusals.
FORBIDDEN_CHANNEL_MODES: dict[tuple[str, str], str] = {
    ("whatsapp", "cold"): "cold WhatsApp automation is forbidden (PDPL + Dealix non-negotiable)",
    ("whatsapp", "automate"): "WhatsApp blast automation is forbidden",
    ("whatsapp", "bulk"): "WhatsApp bulk outreach is forbidden",
    ("linkedin", "automate"): "LinkedIn automation is forbidden (TOS + Dealix non-negotiable)",
    ("linkedin", "scrape"): "LinkedIn scraping is forbidden",
    ("linkedin", "bulk"): "LinkedIn bulk send is forbidden",
    ("email", "scrape"): "email scraping is forbidden",
    ("email", "bulk_cold"): "bulk cold email is forbidden",
    ("web", "scrape"): "web scraping is forbidden (Dealix non-negotiable)",
    ("any", "scrape"): "scraping is forbidden",
}


def is_forbidden(*, channel: str, mode: str) -> tuple[bool, str]:
    """Returns (True, reason) if (channel, mode) is hard-forbidden, else
    (False, ""). Case-insensitive on both args."""
    key = (channel.strip().lower(), mode.strip().lower())
    if key in FORBIDDEN_CHANNEL_MODES:
        return True, FORBIDDEN_CHANNEL_MODES[key]
    if key[1] in {"scrape", "scraping", "harvest", "crawl_aggressive"}:
        return True, "scraping is forbidden (Dealix non-negotiable)"
    return False, ""


__all__ = [
    "CHANNEL_POLICY_AR",
    "FORBIDDEN_CHANNEL_MODES",
    "draft_text_has_forbidden_channel_language",
    "forbidden_channel_markers",
    "is_forbidden",
]
