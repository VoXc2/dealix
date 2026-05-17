"""Evidence Ledger Audit — sample the ledger weekly and check integrity.

The Proof Pack is the product, so the Evidence Ledger is not optional.
Each sampled value event is checked for: a valid tier, a source on
verified events, a confirmation on client-confirmed events, a sane
amount, and no raw PII leaking into notes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.value_os.value_ledger import VALID_TIERS, list_events

MIN_COMPLETENESS = 0.90


@dataclass(frozen=True, slots=True)
class EvidenceFinding:
    event_id: str
    issue: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class EvidenceAuditResult:
    sampled: int
    clean: int
    completeness: float
    passed: bool
    findings: tuple[EvidenceFinding, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "sampled": self.sampled,
            "clean": self.clean,
            "completeness": self.completeness,
            "passed": self.passed,
            "findings": [f.to_dict() for f in self.findings],
        }


def _event_findings(event: Any) -> list[str]:
    issues: list[str] = []
    if not str(getattr(event, "event_id", "")).strip():
        issues.append("missing_event_id")
    if not str(getattr(event, "kind", "")).strip():
        issues.append("missing_event_type")

    tier = str(getattr(event, "tier", "")).strip().lower()
    if tier not in VALID_TIERS:
        issues.append(f"invalid_tier:{tier}")
    if (
        tier in {"verified", "client_confirmed"}
        and not str(getattr(event, "source_ref", "")).strip()
    ):
        issues.append("missing_source")
    if tier == "client_confirmed" and not str(getattr(event, "confirmation_ref", "")).strip():
        issues.append("missing_confirmation_ref")

    amount = getattr(event, "amount", 0.0)
    try:
        if float(amount) < 0:
            issues.append("negative_amount")
    except (TypeError, ValueError):
        issues.append("non_numeric_amount")

    occurred_at = str(getattr(event, "occurred_at", "")).strip()
    if occurred_at:
        try:
            datetime.fromisoformat(occurred_at)
        except ValueError:
            issues.append("unparseable_timestamp")
    else:
        issues.append("missing_timestamp")

    notes = str(getattr(event, "notes", "") or "")
    if notes and redact_text(notes) != notes:
        issues.append("raw_pii_in_notes")

    return issues


def audit_evidence(
    *,
    sample_size: int = 20,
    customer_id: str | None = None,
) -> EvidenceAuditResult:
    """Audit a sample of the value ledger for evidence integrity.

    ``completeness`` is the share of sampled events with zero findings;
    ``passed`` is True when completeness meets :data:`MIN_COMPLETENESS`
    (an empty ledger passes vacuously — nothing is broken).
    """
    events = list_events(customer_id=customer_id, limit=max(1, sample_size))
    findings: list[EvidenceFinding] = []
    clean = 0
    for event in events:
        issues = _event_findings(event)
        if issues:
            event_id = str(getattr(event, "event_id", "")) or "<unknown>"
            findings.extend(EvidenceFinding(event_id, issue) for issue in issues)
        else:
            clean += 1
    sampled = len(events)
    completeness = round(clean / sampled, 3) if sampled else 1.0
    return EvidenceAuditResult(
        sampled=sampled,
        clean=clean,
        completeness=completeness,
        passed=completeness >= MIN_COMPLETENESS,
        findings=tuple(findings),
    )


__all__ = [
    "MIN_COMPLETENESS",
    "EvidenceAuditResult",
    "EvidenceFinding",
    "audit_evidence",
]
