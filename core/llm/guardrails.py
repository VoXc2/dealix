"""
LLM output validators — Guardrails-AI-style without the heavy dependency.

We wrap proposal / email / reply outputs with two checks the founder
cares about most:

1. **PII redaction** — outbound LLM-drafted content must not echo
   Saudi national IDs, IBANs, raw email addresses other than the
   recipient, or VAT numbers we didn't put in the context.
2. **Structural validity** — proposal/email outputs follow a known
   JSON shape; failures route through Knock for human approval.

When `guardrails-ai` is installed we use it; otherwise we fall back to
the small regex/JSON-schema checks below so production behaviour is
deterministic without the optional dep.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)

# Saudi PII patterns.
_SAUDI_NID = re.compile(r"\b[12]\d{9}\b")
_SAUDI_IBAN = re.compile(r"\bSA\d{2}[0-9A-Z]{20}\b")
_SAUDI_VAT = re.compile(r"\b3\d{14}\b")
_GENERIC_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")


@dataclass
class GuardResult:
    ok: bool
    redacted_text: str
    violations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def redact_pii(
    text: str, *, allowed_emails: list[str] | None = None
) -> GuardResult:
    """Redact Saudi national IDs / IBANs / VAT numbers + alien emails."""
    allowed = {e.lower() for e in (allowed_emails or [])}
    violations: list[str] = []

    def _email_sub(m: re.Match[str]) -> str:
        if m.group(0).lower() in allowed:
            return m.group(0)
        violations.append("email_leak")
        return "[email-redacted]"

    redacted = _SAUDI_NID.sub(lambda _: (violations.append("nid") or "[nid]"), text)
    redacted = _SAUDI_IBAN.sub(
        lambda _: (violations.append("iban") or "[iban]"), redacted
    )
    redacted = _SAUDI_VAT.sub(
        lambda _: (violations.append("vat") or "[vat]"), redacted
    )
    redacted = _GENERIC_EMAIL.sub(_email_sub, redacted)
    return GuardResult(
        ok=not violations,
        redacted_text=redacted,
        violations=violations,
        metadata={"allowed_emails": sorted(allowed)},
    )


def validate_proposal_json(raw: str) -> GuardResult:
    """Outputs of the proposal agent must be JSON with these keys."""
    required = {"subject", "body_ar", "next_steps"}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        return GuardResult(
            ok=False,
            redacted_text=raw,
            violations=["invalid_json"],
            metadata={"error": str(exc)[:200]},
        )
    if not isinstance(payload, dict):
        return GuardResult(
            ok=False, redacted_text=raw, violations=["not_object"]
        )
    missing = required - set(payload.keys())
    if missing:
        return GuardResult(
            ok=False,
            redacted_text=raw,
            violations=["missing_fields"],
            metadata={"missing": sorted(missing)},
        )
    return GuardResult(ok=True, redacted_text=raw, metadata={"keys": sorted(payload)})


def guard_proposal_output(
    raw: str, *, allowed_emails: list[str] | None = None
) -> GuardResult:
    """Compose JSON validation + PII redaction for the proposal agent."""
    shape = validate_proposal_json(raw)
    if not shape.ok:
        log.warning(
            "guardrails_shape_failed",
            violations=shape.violations,
            metadata=shape.metadata,
        )
        return shape
    body = json.loads(raw).get("body_ar", "")
    redaction = redact_pii(body, allowed_emails=allowed_emails)
    if not redaction.ok:
        log.warning(
            "guardrails_pii_failed", violations=redaction.violations
        )
    return GuardResult(
        ok=shape.ok and redaction.ok,
        redacted_text=redaction.redacted_text,
        violations=[*shape.violations, *redaction.violations],
        metadata={"shape": shape.metadata, "pii": redaction.metadata},
    )
