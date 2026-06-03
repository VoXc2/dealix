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


__all__ = [
    "CHANNEL_POLICY_AR",
    "draft_text_has_forbidden_channel_language",
    "forbidden_channel_markers",
]
