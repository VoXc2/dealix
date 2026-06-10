"""Read-only MCP-style tool registry for external agents."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.revenue_os.action_catalog import list_action_catalog
from dealix.commercial_ops.aeo_meta import build_aeo_snapshot
from dealix.commercial_ops.gtm_public_surfaces import build_gtm_public_surfaces_snapshot

router = APIRouter(prefix="/api/v1/mcp", tags=["mcp"])

_TOOLS: list[dict[str, str]] = [
    {"name": "dealix_meta", "method": "GET", "path": "/api/v1/meta"},
    {"name": "revenue_os_catalog", "method": "GET", "path": "/api/v1/revenue-os/catalog"},
    {"name": "decision_passport_golden_chain", "method": "GET", "path": "/api/v1/decision-passport/golden-chain"},
    {"name": "healthz", "method": "GET", "path": "/healthz"},
]


@router.get("/tools")
async def list_mcp_tools() -> dict[str, Any]:
    return {
        "protocol": "dealix-mcp-v1",
        "read_only": True,
        "external_send": False,
        "tools": _TOOLS,
        "action_catalog": list_action_catalog(),
    }


@router.post("/invoke/{tool_name}")
async def invoke_mcp_tool(tool_name: str) -> dict[str, Any]:
    if tool_name == "dealix_meta":
        return {"surfaces": build_gtm_public_surfaces_snapshot(), "aeo": build_aeo_snapshot()}
    if tool_name == "revenue_os_catalog":
        from api.routers.revenue_os_catalog import revenue_os_catalog

        return await revenue_os_catalog()
    if tool_name == "decision_passport_golden_chain":
        from api.routers.decision_passport import golden_chain

        return await golden_chain()
    if tool_name == "healthz":
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail=f"unknown tool: {tool_name}")
