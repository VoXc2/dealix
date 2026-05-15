"""QA gate — validates a delivery payload against the YAML matrix."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from auto_client_acquisition.self_growth_os.safe_publishing_gate import check_text
from auto_client_acquisition.self_growth_os.service_activation_matrix import (
    ALLOWED_STATUSES,
    load_matrix,
)


class QAVerdict(StrEnum):
    PASS = "pass"  # noqa: S105 - QA verdict enum value, not a secret
    NEEDS_REVIEW = "needs_review"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class QAGateResult:
    verdict: QAVerdict
    service_id: str
    missing_required_inputs: list[str]
    forbidden_action_attempts: list[str]
    forbidden_vocabulary_hits: list[str]
    deliverable_missing: bool
    notes: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict.value,
            "service_id": self.service_id,
            "missing_required_inputs": list(self.missing_required_inputs),
            "forbidden_action_attempts": list(self.forbidden_action_attempts),
            "forbidden_vocabulary_hits": list(self.forbidden_vocabulary_hits),
            "deliverable_missing": self.deliverable_missing,
            "notes": self.notes,
        }


def _service_record(service_id: str) -> dict[str, Any]:
    matrix = load_matrix()
    for svc in matrix.get("services", []) or []:
        if svc.get("service_id") == service_id:
            return svc
    raise KeyError(f"unknown service_id: {service_id}")


def check_delivery_payload(service_id: str, payload: dict[str, Any]) -> QAGateResult:
    """Validate a delivery payload against the service contract.

    Payload shape (typed by convention; not enforced):
      - ``provided_inputs``       list[str] — what the operator supplied
      - ``intended_actions``      list[str] — actions the operator plans to take
      - ``deliverable``           any       — the actual output/draft
      - ``draft_text``            str       — optional Arabic/English text to gate
    """
    svc = _service_record(service_id)
    required = list(svc.get("required_inputs") or [])
    blocked = list(svc.get("blocked_actions") or [])

    provided = set(payload.get("provided_inputs") or [])
    intended = set(payload.get("intended_actions") or [])
    draft_text = str(payload.get("draft_text") or "")
    deliverable_present = bool(payload.get("deliverable"))

    missing = [r for r in required if r not in provided]
    forbidden_attempts = [a for a in intended if a in blocked]

    # Run any draft text through the safe-publishing gate.
    forbidden_vocab: list[str] = []
    if draft_text:
        result = check_text(draft_text)
        forbidden_vocab = list(result.forbidden_tokens_found)

    deliverable_missing = not deliverable_present

    # Decision tree:
    if forbidden_attempts or forbidden_vocab:
        verdict = QAVerdict.BLOCKED
        notes = "blocked_action_attempt_or_forbidden_vocabulary"
    elif missing or deliverable_missing:
        verdict = QAVerdict.NEEDS_REVIEW
        notes = "incomplete_inputs_or_missing_deliverable"
    else:
        verdict = QAVerdict.PASS
        notes = "all_gates_passed_at_payload_level"

    return QAGateResult(
        verdict=verdict,
        service_id=service_id,
        missing_required_inputs=missing,
        forbidden_action_attempts=forbidden_attempts,
        forbidden_vocabulary_hits=forbidden_vocab,
        deliverable_missing=deliverable_missing,
        notes=notes,
    )


def is_status_known(status: str) -> bool:
    return status in ALLOWED_STATUSES
