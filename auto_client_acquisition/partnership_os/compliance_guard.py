"""Partner content + recruitment compliance guard.

Two doctrine surfaces:

  1. ``scan_partner_content`` — flags guaranteed-outcome claims in any
     partner-authored copy, reusing the platform's guaranteed-claim
     regex from ``governance_os.runtime_decision`` (NO_GUARANTEED_CLAIMS).
  2. ``scan_recruitment_request`` — refuses any partner recruitment
     plan that proposes cold WhatsApp blasts, LinkedIn automation, or
     scraping (non-negotiables #1-3).

Pure functions. No I/O. Every violation carries a stable ``code`` so
the router and tests can assert on it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.governance_os.runtime_decision import (
    _contains_guaranteed_claim,
)

# ── Forbidden recruitment channels (non-negotiables #1-3) ────────────
_COLD_WHATSAPP = re.compile(
    r"\bcold[\s\-_]?whats?app\b"
    r"|whats?app[\s\-_]+(?:blast|spam|bulk|mass)"
    r"|(?:blast|bulk|mass)[\s\-_]+whats?app"
    r"|واتساب\s*(?:بارد|جماعي|عشوائي)"
    r"|رسائل\s*جماعية\s*(?:على|عبر)?\s*واتساب",
    re.IGNORECASE,
)
_LINKEDIN_AUTOMATION = re.compile(
    r"linkedin[\s\-_]+(?:automation|bot|auto[\s\-_]?connect|auto[\s\-_]?message|scraper)"
    r"|automate[\s\-_]+linkedin"
    r"|أتمتة\s*لينكد",
    re.IGNORECASE,
)
_SCRAPING = re.compile(
    r"\bscrap(?:e|ing|er)\b"
    r"|\bweb[\s\-_]?scrap"
    r"|\bemail[\s\-_]?harvest"
    r"|\bdata[\s\-_]?harvest"
    r"|كشط\s*(?:البيانات|المواقع)"
    r"|سحب\s*بيانات",
    re.IGNORECASE,
)


@dataclass(slots=True)
class ComplianceViolation:
    """A single doctrine violation found in partner content/plans."""

    code: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "severity": self.severity, "message": self.message}


@dataclass(slots=True)
class ComplianceScan:
    """Result of a compliance scan."""

    ok: bool
    violations: list[ComplianceViolation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "violations": [v.to_dict() for v in self.violations],
        }


def scan_partner_content(text: str) -> list[ComplianceViolation]:
    """Scan partner-authored marketing copy for doctrine violations.

    Flags guaranteed-outcome claims (NO_GUARANTEED_CLAIMS) and any of
    the three forbidden recruitment channels appearing in the copy.
    """
    violations: list[ComplianceViolation] = []
    body = text or ""

    if _contains_guaranteed_claim(body):
        violations.append(
            ComplianceViolation(
                code="forbidden_claim",
                severity="high",
                message="content makes a guaranteed-outcome / ROI claim "
                "(NO_GUARANTEED_CLAIMS)",
            )
        )
    violations.extend(_scan_forbidden_channels(body))
    return violations


def scan_recruitment_request(text: str) -> ComplianceScan:
    """Scan a partner's proposed recruitment / go-to-market plan.

    Refuses (``ok=False``) any plan mentioning cold WhatsApp blasts,
    LinkedIn automation, or scraping — non-negotiables #1-3. A
    guaranteed-claim in the pitch is also a refusal.
    """
    body = text or ""
    violations: list[ComplianceViolation] = list(_scan_forbidden_channels(body))
    if _contains_guaranteed_claim(body):
        violations.append(
            ComplianceViolation(
                code="forbidden_claim",
                severity="high",
                message="recruitment plan makes a guaranteed-outcome claim "
                "(NO_GUARANTEED_CLAIMS)",
            )
        )
    return ComplianceScan(ok=not violations, violations=violations)


def _scan_forbidden_channels(text: str) -> list[ComplianceViolation]:
    violations: list[ComplianceViolation] = []
    if _COLD_WHATSAPP.search(text):
        violations.append(
            ComplianceViolation(
                code="cold_whatsapp",
                severity="high",
                message="cold / bulk WhatsApp outreach is forbidden "
                "(NO_COLD_WHATSAPP)",
            )
        )
    if _LINKEDIN_AUTOMATION.search(text):
        violations.append(
            ComplianceViolation(
                code="linkedin_automation",
                severity="high",
                message="LinkedIn automation is forbidden "
                "(NO_LINKEDIN_AUTOMATION)",
            )
        )
    if _SCRAPING.search(text):
        violations.append(
            ComplianceViolation(
                code="scraping",
                severity="high",
                message="scraping / data harvesting is forbidden "
                "(NO_SCRAPING_ENGINE)",
            )
        )
    return violations


__all__ = [
    "ComplianceScan",
    "ComplianceViolation",
    "scan_partner_content",
    "scan_recruitment_request",
]
