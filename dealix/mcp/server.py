"""
Anthropic Model-Context-Protocol (MCP) server exposing Dealix as a
toolchain a customer's Claude / Cursor / ChatGPT agent can call.

Tools exposed:
    leads.list              — paginated list scoped to caller's tenant.
    leads.read              — single lead.
    deals.read              — single deal.
    audit.export            — same as the REST CSV endpoint.
    onboarding.start        — kicks off the public onboarding flow.

Transport: stdio (default) + SSE (when MCP_SSE_PORT set).

Auth: caller MUST provide a Dealix API key via the `DEALIX_API_KEY`
env var the host MCP client passes in.

To run locally:
    python -m dealix.mcp.server

To register in Claude Desktop config:
    {
      "mcpServers": {
        "dealix": {
          "command": "python",
          "args": ["-m", "dealix.mcp.server"],
          "env": { "DEALIX_API_KEY": "dlx_live_..." }
        }
      }
    }
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


def _http_kwargs() -> dict[str, str]:
    api_key = os.getenv("DEALIX_API_KEY", "").strip()
    return {"X-API-Key": api_key} if api_key else {}


def _base_url() -> str:
    return os.getenv("DEALIX_API_BASE", "https://api.dealix.me").rstrip("/")


async def _list_leads(limit: int = 25) -> dict[str, Any]:
    import httpx

    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(
            f"{_base_url()}/api/v1/leads",
            headers=_http_kwargs(),
            params={"limit": min(max(limit, 1), 200)},
        )
        r.raise_for_status()
        return r.json()


async def _read_lead(lead_id: str) -> dict[str, Any]:
    import httpx

    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(
            f"{_base_url()}/api/v1/leads/{lead_id}", headers=_http_kwargs()
        )
        r.raise_for_status()
        return r.json()


async def _audit_export(since: str | None = None, limit: int = 500) -> dict[str, Any]:
    import httpx

    params: dict[str, Any] = {"limit": limit}
    if since:
        params["since"] = since
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get(
            f"{_base_url()}/api/v1/audit-logs", headers=_http_kwargs(), params=params
        )
        r.raise_for_status()
        return r.json()


async def _start_onboarding(company: str, email: str, name: str = "Owner") -> dict[str, Any]:
    import httpx

    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.post(
            f"{_base_url()}/api/v1/onboarding/start",
            json={"company": company, "email": email, "name": name, "locale": "ar"},
        )
        r.raise_for_status()
        return r.json()


def main() -> None:
    """Entry point — runs the MCP server over stdio."""
    try:
        from mcp.server.fastmcp import FastMCP  # type: ignore
    except ImportError:
        log.error(
            "mcp_sdk_not_installed",
            install="pip install mcp",
        )
        raise SystemExit(2)

    server = FastMCP("dealix", version="3.3.0")

    @server.tool(description="List recent leads scoped to the caller's tenant.")
    async def leads_list(limit: int = 25) -> dict[str, Any]:
        return await _list_leads(limit)

    @server.tool(description="Read a single lead by id.")
    async def leads_read(lead_id: str) -> dict[str, Any]:
        return await _read_lead(lead_id)

    @server.tool(description="Export the tenant's audit log (paginated).")
    async def audit_export(since: str | None = None, limit: int = 500) -> dict[str, Any]:
        return await _audit_export(since, limit)

    @server.tool(description="Begin onboarding a new tenant.")
    async def onboarding_start(
        company: str, email: str, name: str = "Owner"
    ) -> dict[str, Any]:
        return await _start_onboarding(company, email, name)

    sse_port = os.getenv("MCP_SSE_PORT", "").strip()
    if sse_port:
        asyncio.run(server.run_sse_async(int(sse_port)))
    else:
        server.run()


if __name__ == "__main__":
    main()
