"""
WhatsApp safety: no secrets/API keys in message text, no API-key requests,
and post-consent-only sending (never cold).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .claims import find_prohibited_claims
from .constants import APPROVAL_REQUIRED_DEFAULT, SEND_ENABLED_DEFAULT

# Patterns that look like a leaked secret / credential / API key.
_SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),          # OpenAI-style
    re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{16,}\b"),   # Anthropic-style
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),             # AWS access key id
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),         # GitHub PAT
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), # Slack token
    re.compile(r"\beyJ[A-Za-z0-9_\-]{6,}\.[A-Za-z0-9_\-]{6,}\.[A-Za-z0-9_\-]{4,}"),  # JWT
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password|passwd|bearer)\b\s*[:=]\s*\S{8,}"),
    re.compile(r"\b[A-Fa-f0-9]{32,}\b"),             # long hex blob
]

# Phrases that *request* a credential from the other party.
_API_KEY_REQUEST_PATTERNS = [
    re.compile(r"(?i)(send|share|give|provide|paste|forward).{0,30}(api[\s_-]?key|secret|token|password|credential)"),
    re.compile(r"(?i)(what'?s|whats|need).{0,20}(api[\s_-]?key|secret|token|password)"),
    re.compile(r"(ارسل|أرسل|شارك|اعطني|أعطني|زودني).{0,30}(مفتاح|سر|توكن|كلمة المرور|باسورد|api)"),
    re.compile(r"(?i)\bapi[\s_-]?key\b.{0,20}(please|من فضلك|لو سمحت)"),
]


def contains_secret_or_api_key(text: Optional[str]) -> bool:
    """True if the text appears to contain a credential/secret/API key."""
    if not text:
        return False
    return any(p.search(text) for p in _SECRET_PATTERNS)


def requests_api_key(text: Optional[str]) -> bool:
    """True if the text asks the recipient to share a key/secret/credential."""
    if not text:
        return False
    return any(p.search(text) for p in _API_KEY_REQUEST_PATTERNS)


@dataclass
class WhatsAppAssessment:
    allowed: bool
    violations: List[str] = field(default_factory=list)
    approval_required: bool = APPROVAL_REQUIRED_DEFAULT
    send_enabled: bool = SEND_ENABLED_DEFAULT
    requires_human: bool = False

    def as_dict(self) -> Dict:
        return {
            "allowed": self.allowed,
            "violations": self.violations,
            "approval_required": self.approval_required,
            "send_enabled": self.send_enabled,
            "requires_human": self.requires_human,
        }


def assess_whatsapp_message(
    text: str,
    *,
    has_consent: bool = False,
    inbound: bool = False,
) -> WhatsAppAssessment:
    """Evaluate a WhatsApp message for safety.

    Rules:
      * Outbound WhatsApp is **post-consent only** (never cold automation).
      * Message text must never contain a secret / API key.
      * Message text must never *request* a secret / API key.
      * No guaranteed/exaggerated claims.
    For inbound messages, consent is not required to *receive*; but the same
    secret rules apply and a key request is escalated to a human.
    """
    violations: List[str] = []
    requires_human = False

    if contains_secret_or_api_key(text):
        violations.append("secret_in_text")
    if requests_api_key(text):
        violations.append("api_key_request")
        requires_human = True
    if find_prohibited_claims(text):
        violations.append("prohibited_claims")
    if not inbound and not has_consent:
        violations.append("cold_whatsapp_not_allowed")

    return WhatsAppAssessment(
        allowed=len(violations) == 0,
        violations=violations,
        requires_human=requires_human,
    )
