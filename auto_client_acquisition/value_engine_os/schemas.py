"""Value Engine schemas for workflow-level ROI tracking."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class WorkflowValueMetric:
    metric_id: str
    tenant_id: str
    run_id: str
    metric_name: str
    metric_type: str  # estimated | measured
    value: float
    currency: str = "SAR"
    source_ref: str = ""
    notes: str = ""
    captured_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
