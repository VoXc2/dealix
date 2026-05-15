"""Regex-based secret scanner. Mirrors gitleaks heuristics."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

SECRET_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("moyasar_live_secret", re.compile(r"sk_live_[A-Za-z0-9]{16,}")),
    ("github_pat", re.compile(r"ghp_[A-Za-z0-9]{36,}")),
    ("github_oauth", re.compile(r"gho_[A-Za-z0-9]{36,}")),
    ("github_app_token", re.compile(r"ghu_[A-Za-z0-9]{36,}")),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("anthropic_key", re.compile(r"sk-ant-[A-Za-z0-9_-]{30,}")),
    ("openai_key", re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{40,}")),
    ("groq_key", re.compile(r"gsk_[A-Za-z0-9]{40,}")),
    ("resend_key", re.compile(r"re_[A-Za-z0-9_-]{20,}")),
    ("google_api_key", re.compile(r"AIza[A-Za-z0-9_-]{30,}")),
    ("private_key_block", re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("password_assignment", re.compile(r"\b(?:password|passwd|pwd)\s*=\s*['\"]([^'\"]{8,})['\"]", re.IGNORECASE)),
]


@dataclass(frozen=True)
class SecretFinding:
    pattern_id: str
    excerpt_redacted: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "excerpt_redacted": self.excerpt_redacted,
        }


def scan_text_for_secrets(text: str) -> list[SecretFinding]:
    """Return findings as redacted excerpts (NEVER include raw secret in output)."""
    if not isinstance(text, str):
        return []
    out: list[SecretFinding] = []
    for pid, pat in SECRET_PATTERNS:
        for m in pat.finditer(text):
            # Redact the actual match — keep only first 4 + last 2 chars.
            raw = m.group(0)
            redacted_excerpt = (
                "[REDACTED]" if len(raw) <= 8 else raw[:4] + "***" + raw[-2:]
            )
            out.append(SecretFinding(pattern_id=pid, excerpt_redacted=redacted_excerpt))
    return out


def is_clean(text: str) -> bool:
    """Convenience boolean."""
    return not scan_text_for_secrets(text)
