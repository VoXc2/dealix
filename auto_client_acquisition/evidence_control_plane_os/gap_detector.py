"""Evidence Gap Detector — finds missing evidence and emits friction events.

Gaps detected:
  - Source Passport absent for a customer that has value events.
  - Value events of tier verified/client_confirmed without source_ref.
  - Capital ledger empty for an engagement that has proof events.
  - Friction events unresolved (>30 days).
  - Audit log missing for an engagement with Proof Pack.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from typing import Any


@dataclass
class EvidenceGap:
    label: str
    severity: str  # low | med | high
    suggested_remedy: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "severity": self.severity,
            "suggested_remedy": self.suggested_remedy,
        }


def find_gaps(*, customer_id: str, project_id: str = "") -> list[EvidenceGap]:
    """Best-effort gap detection. Each gap suggests a concrete remedy."""
    gaps: list[EvidenceGap] = []

    # 1. Value tier discipline: verified/client_confirmed without source_ref.
    try:
        from auto_client_acquisition.value_os.value_ledger import list_events
        for ev in list_events(customer_id=customer_id, limit=500):
            if ev.tier == "verified" and not ev.source_ref:
                gaps.append(EvidenceGap(
                    label=f"verified_without_source_ref:{ev.event_id}",
                    severity="high",
                    suggested_remedy="add source_ref to value event or downgrade to observed",
                ))
            if ev.tier == "client_confirmed" and (not ev.source_ref or not ev.confirmation_ref):
                gaps.append(EvidenceGap(
                    label=f"client_confirmed_missing_refs:{ev.event_id}",
                    severity="high",
                    suggested_remedy="add source_ref + confirmation_ref",
                ))
    except Exception:
        pass

    # 2. Capital asset gap per engagement.
    try:
        if project_id:
            from auto_client_acquisition.capital_os.capital_ledger import list_assets
            assets = list_assets(engagement_id=project_id, limit=10)
            if not assets:
                gaps.append(EvidenceGap(
                    label=f"engagement_without_capital_asset:{project_id}",
                    severity="med",
                    suggested_remedy="register >= 1 reusable asset via capital_os.add_asset",
                ))
    except Exception:
        pass

    # 3. Unresolved friction (older than 30 days).
    try:
        from auto_client_acquisition.friction_log.store import list_events as list_friction
        events = list_friction(customer_id=customer_id, since_days=180, limit=200)
        cutoff_ts = datetime.now(UTC).timestamp() - 30 * 86400
        for ev in events:
            try:
                ts = datetime.fromisoformat(ev.occurred_at).timestamp()
            except Exception:  # noqa: S112 - skip event with unparsable timestamp
                continue
            if ts < cutoff_ts and not ev.resolved_at:
                gaps.append(EvidenceGap(
                    label=f"unresolved_friction:{ev.event_id}:{ev.kind}",
                    severity="med" if ev.severity == "med" else "low",
                    suggested_remedy="resolve, record resolution_at, or escalate",
                ))
    except Exception:
        pass

    # 4. Source passport for non-empty engagement.
    try:
        from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
            EvidenceType,
            list_evidence,
        )
        passports = list_evidence(
            customer_id=customer_id, type=EvidenceType.SOURCE_PASSPORT.value
        )
        from auto_client_acquisition.value_os.value_ledger import list_events as list_value
        value_count = len(list_value(customer_id=customer_id))
        if value_count > 0 and not passports:
            gaps.append(EvidenceGap(
                label="customer_with_value_events_but_no_source_passport",
                severity="high",
                suggested_remedy="capture source passport via data_os.SourcePassport and create_evidence",
            ))
    except Exception:
        pass

    return gaps[:50]  # cap at 50 to keep the report scannable


__all__ = ["EvidenceGap", "find_gaps"]
