"""lead_qualification — Dealix's first end-to-end governed operational workflow.

One declared, observable, governed, rollbackable, auditable, measurable
pipeline that wires existing canonical modules into a single executable
flow: lead intake -> tenant detection -> RBAC -> knowledge retrieval ->
qualification -> scoring -> draft -> risk check -> approval -> CRM update
-> metrics -> eval report -> executive dashboard.
"""

from __future__ import annotations

from auto_client_acquisition.sales_os.lead_qualification.eval_report import build_eval_report
from auto_client_acquisition.sales_os.lead_qualification.orchestrator import (
    WorkflowDeps,
    build_definition,
    resume_lead_qualification,
    run_lead_qualification,
)
from auto_client_acquisition.sales_os.lead_qualification.sales_agent import (
    SALES_AGENT_CARD,
    register_sales_agent,
)
from auto_client_acquisition.sales_os.lead_qualification.schemas import (
    LeadInput,
    StepResult,
    WorkflowOutput,
)

__all__ = [
    "SALES_AGENT_CARD",
    "LeadInput",
    "StepResult",
    "WorkflowDeps",
    "WorkflowOutput",
    "build_definition",
    "build_eval_report",
    "register_sales_agent",
    "resume_lead_qualification",
    "run_lead_qualification",
]
