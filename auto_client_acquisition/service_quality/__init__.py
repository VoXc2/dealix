"""Service Quality v5 — QA gate + SLA tracker over the YAML matrix.

Each service in ``docs/registry/SERVICE_READINESS_MATRIX.yaml`` is
loaded once; the QA gate validates a delivery payload against the
service's documented requirements (required_inputs, blocked_actions,
deliverables) without ever taking an external action itself.

Also exposes the per-service SLA from the YAML so the founder can
warn customers honestly when delivery is at risk.
"""
from auto_client_acquisition.service_quality.qa_gate import (
    QAGateResult,
    QAVerdict,
    check_delivery_payload,
)
from auto_client_acquisition.service_quality.sla_tracker import (
    SLA,
    get_sla,
    list_slas,
)

__all__ = [
    "SLA",
    "QAGateResult",
    "QAVerdict",
    "check_delivery_payload",
    "get_sla",
    "list_slas",
]
