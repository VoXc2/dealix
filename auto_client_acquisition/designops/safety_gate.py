"""Safety gate — regex-only artifact safety check.

Pure function. Runs ALL checks and aggregates blocked_reasons.
No LLM, no I/O. The output is the contract: callers MUST
respect `safe_to_publish` / `safe_to_send` before any side effect.
"""
from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text

# ── Forbidden tokens (case-insensitive in positive context) ────────
_FORBIDDEN_TOKENS: tuple[str, ...] = (
    "نضمن",
    "guaranteed",
    "blast",
    "scrape",
    "cold whatsapp",
    "live send",
    "revenue guaranteed",
    "ranking guaranteed",
)

# Live-send markers — literal API-call shaped strings.
_LIVE_SEND_MARKERS: tuple[str, ...] = (
    "send_email_live",
    "send_whatsapp_live",
    "charge_payment_live",
)

# Unsupported ROI claim. Matches "10x revenue", "5x growth", etc.
_ROI_CLAIM_RE = re.compile(
    r"\b\d+\s*x\s+(revenue|growth|leads|sales|pipeline)\b",
    re.IGNORECASE,
)

# Fake-customer-name patterns — too specific to be a generic placeholder.
# We allow `*-EXAMPLE`, `Acme`, `Pilot-N`, but block real-sounding entity names
# adjacent to a verb of attribution.
_FAKE_CUSTOMER_RE = re.compile(
    r"\b("
    r"big\s+saudi\s+bank"
    r"|aramco\s+(said|reported|told)"
    r"|sabic\s+(said|reported|told)"
    r"|stc\s+(said|reported|told)"
    r"|saudi\s+aramco"
    r")\b",
    re.IGNORECASE,
)


class SafetyGateResult(BaseModel):
    """Result of running the safety gate against one artifact."""

    model_config = ConfigDict(extra="forbid")

    passed: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    forbidden_tokens_found: list[str] = Field(default_factory=list)
    risk_level: Literal["low", "medium", "high", "blocked"] = "low"
    safe_to_publish: bool = False
    safe_to_send: bool = False


def _coerce_text(manifest_or_text: dict | str) -> str:
    if isinstance(manifest_or_text, str):
        return manifest_or_text
    if isinstance(manifest_or_text, dict):
        # Concatenate every string value recursively for scanning.
        parts: list[str] = []

        def _walk(v: object) -> None:
            if isinstance(v, str):
                parts.append(v)
            elif isinstance(v, dict):
                for vv in v.values():
                    _walk(vv)
            elif isinstance(v, (list, tuple)):
                for vv in v:
                    _walk(vv)

        _walk(manifest_or_text)
        return "\n".join(parts)
    return ""


def _check_forbidden_tokens(text: str) -> list[str]:
    lo = text.lower()
    found: list[str] = []
    for tok in _FORBIDDEN_TOKENS:
        if tok.lower() in lo:
            found.append(tok)
    return found


def _check_pii(text: str) -> bool:
    """Return True if redaction changed text — meaning raw PII present."""
    return redact_text(text) != text


def _check_fake_customer(text: str) -> bool:
    return bool(_FAKE_CUSTOMER_RE.search(text))


def _check_roi_claim(text: str) -> bool:
    return bool(_ROI_CLAIM_RE.search(text))


def _check_live_send(text: str) -> list[str]:
    return [m for m in _LIVE_SEND_MARKERS if m in text]


def check_artifact(
    manifest_or_text: dict | str,
    language: str = "bilingual",
) -> SafetyGateResult:
    """Run every gate. Aggregate. Never raise — always return a result."""
    text = _coerce_text(manifest_or_text)
    blocked_reasons: list[str] = []
    forbidden_tokens: list[str] = []

    tokens = _check_forbidden_tokens(text)
    if tokens:
        forbidden_tokens.extend(tokens)
        blocked_reasons.append(f"forbidden_tokens:{','.join(tokens)}")

    if _check_pii(text):
        blocked_reasons.append("raw_pii_detected")

    if _check_fake_customer(text):
        blocked_reasons.append("fake_customer_name_pattern")

    if _check_roi_claim(text):
        blocked_reasons.append("unsupported_roi_claim")

    live_markers = _check_live_send(text)
    if live_markers:
        blocked_reasons.append(f"live_send_marker:{','.join(live_markers)}")
        forbidden_tokens.extend(live_markers)

    if blocked_reasons:
        risk_level: Literal["low", "medium", "high", "blocked"] = "blocked"
        passed = False
    else:
        risk_level = "low"
        passed = True

    # safe_to_send is ALWAYS False by default — manual review required.
    return SafetyGateResult(
        passed=passed,
        blocked_reasons=blocked_reasons,
        forbidden_tokens_found=forbidden_tokens,
        risk_level=risk_level,
        safe_to_publish=passed,
        safe_to_send=False,
    )
