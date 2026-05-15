"""Operational infrastructure readiness endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from dealix_infrastructure import EnterpriseReadinessHarness

router = APIRouter(prefix="/api/v1/infrastructure", tags=["Admin"])


@router.get("/status")
async def infrastructure_status() -> dict[str, object]:
    return {
        "mode": "operational_infrastructure",
        "workflow_spec": "workflows/sales/lead_qualification.workflow.yaml",
        "focus": [
            "workflow_integration",
            "governance",
            "observability",
            "operational_reliability",
        ],
    }


@router.post("/readiness-test")
async def enterprise_readiness_test() -> dict[str, object]:
    harness = EnterpriseReadinessHarness()
    return harness.run().to_dict()
