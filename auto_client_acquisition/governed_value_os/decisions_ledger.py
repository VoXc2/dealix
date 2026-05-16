"""Governed Value Decisions ledger — Dealix's North Star metric.

North Star: **Governed Value Decisions Created** (doctrine §2).

A *governed value decision* is a revenue or operational decision that has:

    - a clear source        (``source_ref``)
    - a clear approval      (``approval_ref``)
    - an evidence trail     (``evidence_refs`` — at least one)
    - a measurable value    (``decision_kind`` + ``value_estimate_sar``)

:func:`record_decision` refuses to record anything missing source, approval, or
evidence — the refusal *is* the metric definition. JSONL-backed, mirroring the
``capital_os.capital_ledger`` pattern; path via ``DEALIX_GOVERNED_DECISIONS_PATH``.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_DEFAULT_PATH = "var/governed-decisions.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_GOVERNED_DECISIONS_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


@dataclass(frozen=True, slots=True)
class GovernedValueDecision:
    """One governed value decision — the North Star unit."""

    decision_id: str
    summary: str
    decision_kind: str
    source_ref: str
    approval_ref: str
    evidence_refs: tuple[str, ...]
    value_estimate_sar: float = 0.0
    is_estimate: bool = True
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["evidence_refs"] = list(self.evidence_refs)
        return d


def record_decision(
    *,
    summary: str,
    decision_kind: str,
    source_ref: str,
    approval_ref: str,
    evidence_refs: tuple[str, ...] | list[str],
    value_estimate_sar: float = 0.0,
) -> GovernedValueDecision:
    """Append a governed value decision to the ledger.

    Raises ``ValueError`` unless source, approval and at least one evidence
    reference are all present — a decision without those three is not governed.
    """
    if not summary.strip():
        raise ValueError("summary is required")
    if not decision_kind.strip():
        raise ValueError("decision_kind is required")
    if not source_ref.strip():
        raise ValueError("source_ref is required — no decision without a source")
    if not approval_ref.strip():
        raise ValueError("approval_ref is required — no decision without an approval")
    clean_evidence = tuple(e for e in evidence_refs if e and e.strip())
    if not clean_evidence:
        raise ValueError("evidence_refs is required — no decision without an evidence trail")
    if value_estimate_sar < 0:
        raise ValueError("value_estimate_sar must be >= 0")

    decision = GovernedValueDecision(
        decision_id=f"gvd_{uuid.uuid4().hex[:12]}",
        summary=summary.strip(),
        decision_kind=decision_kind.strip(),
        source_ref=source_ref.strip(),
        approval_ref=approval_ref.strip(),
        evidence_refs=clean_evidence,
        value_estimate_sar=float(value_estimate_sar),
        is_estimate=True,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(decision.to_dict(), ensure_ascii=False) + "\n")
    return decision


def list_decisions(*, limit: int = 200) -> list[GovernedValueDecision]:
    """Return recorded decisions, newest last, capped at ``limit``."""
    path = _path()
    if not path.exists():
        return []
    out: list[GovernedValueDecision] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    data["evidence_refs"] = tuple(data.get("evidence_refs", ()))
                    out.append(GovernedValueDecision(**data))
                except Exception:  # noqa: BLE001
                    continue
    return out[-limit:]


def count_decisions() -> int:
    """North Star value: total governed value decisions created."""
    return len(list_decisions(limit=10_000_000))
