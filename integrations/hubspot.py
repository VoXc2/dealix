"""
HubSpot thin client wrapper — re-exports the CRMAgent in a convenience facade.
واجهة مبسطة لـ HubSpot.

Dealix Company OS / Revenue Mesh owns commercial truth. HubSpot is a CRM
mirror only; deal creation therefore defaults to False and remains subject to
the CRMAgent fail-closed truth policy even when explicitly requested.
"""

from __future__ import annotations

from auto_client_acquisition.agents.crm import CRMAgent, CRMSyncResult
from auto_client_acquisition.agents.intake import Lead

__all__ = ["CRMSyncResult", "HubSpotClient"]


class HubSpotClient:
    """Convenience wrapper over the truth-gated CRMAgent."""

    def __init__(self) -> None:
        self._agent = CRMAgent()

    async def sync_lead(self, lead: Lead, create_deal: bool = False) -> CRMSyncResult:
        return await self._agent.run(lead=lead, create_deal=create_deal)

    @property
    def configured(self) -> bool:
        return self._agent._configured
