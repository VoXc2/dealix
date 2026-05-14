"""Channel policy facade — canonical name for forbidden-channel-mode rules.

Wraps existing `channel_policy_gateway.policy.check_channel_policy` for
positive-cases. For hard refusals (cold WhatsApp, LinkedIn automation,
bulk outreach, scraping) returns a fast (True, reason) without going
through the gateway — these are non-negotiable.
"""
from __future__ import annotations

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
    """Returns (True, reason) if (channel, mode) is on the forbidden list.
    Returns (False, "") otherwise. Case-insensitive on both args."""
    key = (channel.strip().lower(), mode.strip().lower())
    if key in FORBIDDEN_CHANNEL_MODES:
        return True, FORBIDDEN_CHANNEL_MODES[key]
    # Generic scrape mode is always forbidden regardless of channel.
    if key[1] in {"scrape", "scraping", "harvest", "crawl_aggressive"}:
        return True, "scraping is forbidden (Dealix non-negotiable)"
    return False, ""


__all__ = ["FORBIDDEN_CHANNEL_MODES", "is_forbidden"]
