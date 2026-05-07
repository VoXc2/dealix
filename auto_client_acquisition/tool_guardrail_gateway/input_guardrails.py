"""Input guardrails — prompt injection + PII overexposure check."""
from __future__ import annotations

import re
from typing import Any

# Common prompt-injection patterns (OWASP LLM01, LLM06 mappings)
_PROMPT_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(previous|prior|all)\s+instructions", re.IGNORECASE),
    re.compile(r"system\s*:\s*you\s+are\s+now", re.IGNORECASE),
    re.compile(r"<\|.*\|>"),  # special tokens (e.g., ChatML)
    re.compile(r"\[INST\]|\[/INST\]"),  # Mistral-style
    re.compile(r"disregard\s+(your|all)\s+(rules|instructions)", re.IGNORECASE),
    re.compile(r"(jailbreak|DAN|Do\s+Anything\s+Now)", re.IGNORECASE),
    re.compile(r"reveal\s+your\s+(prompt|system|instructions)", re.IGNORECASE),
    re.compile(r"تجاهل\s+(جميع|كل|التعليمات)"),
]

# Excessive PII exposure heuristic — too many emails or phones in one input
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"\+?\d[\d\s().-]{6,}\d")


def check_input(
    *,
    text: str,
    max_pii_email_count: int = 3,
    max_pii_phone_count: int = 3,
) -> dict[str, Any]:
    """Input guardrail check. Returns {passed, reasons, severity}."""
    reasons: list[str] = []

    # Prompt injection
    for pat in _PROMPT_INJECTION_PATTERNS:
        if pat.search(text):
            reasons.append(f"prompt_injection_pattern:{pat.pattern[:30]}")

    # PII overexposure
    email_count = len(_EMAIL_RE.findall(text))
    phone_count = len(_PHONE_RE.findall(text))
    if email_count > max_pii_email_count:
        reasons.append(f"pii_overexposure_emails:{email_count}")
    if phone_count > max_pii_phone_count:
        reasons.append(f"pii_overexposure_phones:{phone_count}")

    severity = "critical" if reasons and any("injection" in r for r in reasons) else (
        "high" if reasons else "info"
    )

    return {
        "passed": len(reasons) == 0,
        "reasons": reasons,
        "severity": severity,
        "input_length": len(text),
        "email_count": email_count,
        "phone_count": phone_count,
    }
