"""GCC Governed AI Ops Pulse — quarterly aggregated authority report.

Aggregates governance risk-score signals into a quarterly "GCC
Governed AI Ops Pulse": count of risk scores, most-frequent risks,
most-requested workflows, evidence gaps and best practices.

DOCTRINE — the report is aggregate/anonymized ONLY. Any per-client
identifier in an input record is dropped during aggregation; the
output never exposes an individual client's data without consent.

Pure-function core. NO LLM. NO external send.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

# Minimum occurrences before a workflow / risk is reported — protects
# against a single client being identifiable from a rare data point
# (k-anonymity floor).
DEFAULT_MIN_GROUP_SIZE = 3


@dataclass
class GovernedAIOpsPulse:
    """The quarterly GCC Governed AI Ops Pulse report."""

    quarter: str
    risk_scores_count: int
    distinct_clients: int
    most_frequent_risks: list[dict[str, Any]] = field(default_factory=list)
    most_requested_workflows: list[dict[str, Any]] = field(default_factory=list)
    evidence_gaps: list[dict[str, Any]] = field(default_factory=list)
    best_practices: list[str] = field(default_factory=list)
    anonymized: bool = True
    consent_note_en: str = (
        "Aggregate, anonymized report. No individual client is named or "
        "identifiable. Groups below the k-anonymity floor are withheld."
    )
    consent_note_ar: str = (
        "تقرير مُجمَّع ومجهول الهوية. لا يُذكر أي عميل بعينه ولا يمكن "
        "تمييزه. تُحجب المجموعات الأصغر من حد إخفاء الهوية."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report": "gcc_governed_ai_ops_pulse",
            "quarter": self.quarter,
            "risk_scores_count": self.risk_scores_count,
            "distinct_clients": self.distinct_clients,
            "most_frequent_risks": self.most_frequent_risks,
            "most_requested_workflows": self.most_requested_workflows,
            "evidence_gaps": self.evidence_gaps,
            "best_practices": self.best_practices,
            "anonymized": self.anonymized,
            "consent_note_en": self.consent_note_en,
            "consent_note_ar": self.consent_note_ar,
        }


def _field(record: Any, key: str, default: Any = None) -> Any:
    if isinstance(record, dict):
        return record.get(key, default)
    return getattr(record, key, default)


def _top_counts(
    counter: dict[str, int],
    *,
    min_group_size: int,
    label_key: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Return the top-N counted items above the k-anonymity floor."""
    rows = [
        {label_key: name, "count": count}
        for name, count in counter.items()
        if count >= min_group_size
    ]
    rows.sort(key=lambda r: (-int(r["count"]), str(r[label_key])))
    return rows[:limit]


def build_gcc_pulse(
    risk_records: Iterable[Any],
    *,
    quarter: str,
    min_group_size: int = DEFAULT_MIN_GROUP_SIZE,
) -> GovernedAIOpsPulse:
    """Build the GCC Governed AI Ops Pulse from governance risk records.

    Each ``risk_record`` may be a dict or object with optional fields:
      - ``risk_category`` — the classified risk
      - ``workflow`` — the AI workflow requested
      - ``has_evidence`` — whether the workflow has a source/proof
      - ``client_id`` — used only for the distinct-client count; never
        emitted in the report

    DOCTRINE — ``client_id`` is consumed for the anonymized count only.
    Risks and workflows seen fewer than ``min_group_size`` times are
    withheld so no single client is identifiable.
    """
    records = list(risk_records)
    risk_counter: dict[str, int] = {}
    workflow_counter: dict[str, int] = {}
    evidence_gap_counter: dict[str, int] = {}
    clients: set[str] = set()

    for rec in records:
        risk = str(_field(rec, "risk_category", "") or "").strip()
        if risk:
            risk_counter[risk] = risk_counter.get(risk, 0) + 1

        workflow = str(_field(rec, "workflow", "") or "").strip()
        if workflow:
            workflow_counter[workflow] = workflow_counter.get(workflow, 0) + 1

        has_evidence = _field(rec, "has_evidence", True)
        if workflow and not has_evidence:
            evidence_gap_counter[workflow] = evidence_gap_counter.get(workflow, 0) + 1

        client = str(_field(rec, "client_id", "") or "").strip()
        if client:
            clients.add(client)

    best_practices = [
        "Every AI workflow must cite a source before it runs — no sourceless decisioning.",
        "External actions stay human-approved; no autonomous outbound send.",
        "Risk-classify each workflow before deployment and record the decision.",
        "Close evidence gaps with a documented proof artifact each quarter.",
    ]

    return GovernedAIOpsPulse(
        quarter=quarter,
        risk_scores_count=len(records),
        distinct_clients=len(clients),
        most_frequent_risks=_top_counts(
            risk_counter, min_group_size=min_group_size, label_key="risk_category"
        ),
        most_requested_workflows=_top_counts(
            workflow_counter, min_group_size=min_group_size, label_key="workflow"
        ),
        evidence_gaps=_top_counts(
            evidence_gap_counter, min_group_size=min_group_size, label_key="workflow"
        ),
        best_practices=best_practices,
    )


__all__ = ["DEFAULT_MIN_GROUP_SIZE", "GovernedAIOpsPulse", "build_gcc_pulse"]
