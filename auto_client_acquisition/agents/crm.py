"""
CRM Agent — mirrors verified Dealix commercial state into HubSpot.
وكيل CRM — يعكس الحالة التجارية المتحققة من Dealix إلى HubSpot.

Dealix Company OS / Revenue Mesh is the commercial truth owner. HubSpot is a
CRM mirror only. This adapter must never turn research, fit scores, drafts,
invoices, or synthetic/test records into relationship, opportunity, payment,
or revenue truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from auto_client_acquisition.agents.icp_matcher import FitScore
from auto_client_acquisition.agents.intake import Lead, LeadStatus
from auto_client_acquisition.revenue_os.crm_mirror_policy import (
    HubSpotMirrorDecision,
    evaluate_hubspot_mirror,
)
from core.agents.base import BaseAgent
from core.config.settings import get_settings
from core.errors import IntegrationError


@dataclass
class CRMSyncResult:
    synced: bool
    contact_id: str | None = None
    deal_id: str | None = None
    provider: str = "hubspot"
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "synced": self.synced,
            "contact_id": self.contact_id,
            "deal_id": self.deal_id,
            "provider": self.provider,
            "reason": self.reason,
        }


# Internal status → HubSpot stage. A WON stage is allowed only when the mirror
# policy has verified payment evidence for the same account case.
STATUS_TO_STAGE: dict[LeadStatus, str] = {
    LeadStatus.NEW: "appointmentscheduled",
    LeadStatus.QUALIFIED: "qualifiedtobuy",
    LeadStatus.DISCOVERY: "presentationscheduled",
    LeadStatus.PROPOSAL: "decisionmakerboughtin",
    LeadStatus.NEGOTIATION: "contractsent",
    LeadStatus.WON: "closedwon",
    LeadStatus.LOST: "closedlost",
    LeadStatus.DISQUALIFIED: "closedlost",
}


class CRMAgent(BaseAgent):
    """Mirror evidence-backed Dealix contacts/deals into HubSpot."""

    name = "crm"
    HUBSPOT_BASE_URL = "https://api.hubapi.com"

    def __init__(self) -> None:
        super().__init__()
        self.settings = get_settings()

    @property
    def _configured(self) -> bool:
        return self.settings.hubspot_access_token is not None

    def _headers(self) -> dict[str, str]:
        if not self.settings.hubspot_access_token:
            raise IntegrationError("HUBSPOT_ACCESS_TOKEN not configured")
        token = self.settings.hubspot_access_token.get_secret_value()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    async def run(
        self,
        *,
        lead: Lead,
        fit_score: FitScore | None = None,
        create_deal: bool = False,
        **_: Any,
    ) -> CRMSyncResult:
        """Mirror a verified contact and, when allowed, a qualified deal.

        ``create_deal`` defaults to False. Even when callers request a deal,
        the deterministic mirror policy must separately permit it.
        """

        decision = evaluate_hubspot_mirror(lead)
        if not decision.allow_contact:
            reason = "HubSpot mirror blocked: " + ",".join(decision.reasons)
            self.log.info("crm_mirror_blocked", lead_id=lead.id, reason=reason)
            return CRMSyncResult(synced=False, reason=reason)

        if not self._configured:
            self.log.warning("crm_not_configured")
            return CRMSyncResult(synced=False, reason="HubSpot not configured — skipped")

        try:
            contact_id = await self._upsert_contact(lead, fit_score)
            deal_id: str | None = None
            if create_deal and lead.company_name:
                if decision.allow_deal:
                    deal_id = await self._create_deal(lead, contact_id, fit_score, decision)
                else:
                    self.log.info(
                        "crm_deal_mirror_blocked",
                        lead_id=lead.id,
                        reasons=decision.reasons,
                    )

            self.log.info("crm_sync_ok", lead_id=lead.id, contact_id=contact_id, deal_id=deal_id)
            return CRMSyncResult(synced=True, contact_id=contact_id, deal_id=deal_id)
        except Exception as e:
            self.log.exception("crm_sync_failed", error=str(e))
            return CRMSyncResult(synced=False, reason=str(e))

    def _contact_properties(self, lead: Lead, fit: FitScore | None) -> dict[str, Any]:
        """Build contact properties without manufacturing identifiers."""

        properties: dict[str, Any] = {
            "firstname": (lead.contact_name or "").split(" ")[0] if lead.contact_name else "",
            "lastname": " ".join((lead.contact_name or "").split(" ")[1:]),
            "company": lead.company_name,
        }
        if lead.contact_email:
            properties["email"] = lead.contact_email
        if lead.contact_phone:
            properties["phone"] = lead.contact_phone
        if lead.sector:
            properties["industry"] = lead.sector
        if fit:
            # Fit is context only. It does not promote lifecycle stage or truth.
            properties["hs_analytics_source_data_1"] = f"fit_tier_{fit.tier}"
        return properties

    async def _search_contact(self, client: httpx.AsyncClient, property_name: str, value: str) -> str | None:
        response = await client.post(
            f"{self.HUBSPOT_BASE_URL}/crm/v3/objects/contacts/search",
            json={
                "filterGroups": [
                    {
                        "filters": [
                            {
                                "propertyName": property_name,
                                "operator": "EQ",
                                "value": value,
                            }
                        ]
                    }
                ],
                "limit": 1,
            },
            headers=self._headers(),
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        return str(results[0]["id"]) if results else None

    # ── Contact mirror ──────────────────────────────────────────
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def _upsert_contact(self, lead: Lead, fit: FitScore | None) -> str:
        """Create/update a verified contact by real email or phone."""

        properties = self._contact_properties(lead, fit)
        email = lead.contact_email or ""
        phone = lead.contact_phone or ""

        async with httpx.AsyncClient(timeout=30) as client:
            existing_id: str | None = None
            if email:
                existing_id = await self._search_contact(client, "email", email)
            if not existing_id and phone:
                existing_id = await self._search_contact(client, "phone", phone)

            payload = {"properties": properties}
            if existing_id:
                response = await client.patch(
                    f"{self.HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{existing_id}",
                    json=payload,
                    headers=self._headers(),
                )
                response.raise_for_status()
                return existing_id

            response = await client.post(
                f"{self.HUBSPOT_BASE_URL}/crm/v3/objects/contacts",
                json=payload,
                headers=self._headers(),
            )
            response.raise_for_status()
            return str(response.json()["id"])

    # ── Deal mirror ─────────────────────────────────────────────
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def _create_deal(
        self,
        lead: Lead,
        contact_id: str,
        fit: FitScore | None,
        decision: HubSpotMirrorDecision,
    ) -> str:
        """Create a mirrored deal only after the truth policy allows it."""

        if not decision.allow_deal:
            raise IntegrationError("HubSpot deal mirror blocked by commercial truth policy")
        if lead.status == LeadStatus.WON and not decision.payment_verified:
            raise IntegrationError("closedwon requires verified payment evidence")

        stage = STATUS_TO_STAGE.get(lead.status, "qualifiedtobuy")
        deal_name = f"{lead.company_name} — {lead.sector or 'Qualified Opportunity'}"
        properties: dict[str, Any] = {
            "dealname": deal_name,
            "dealstage": stage,
            "pipeline": "default",
        }

        # A verified customer-specific quote may be mirrored as expected deal
        # value. Never copy lead.budget into CRM amount and never treat CRM
        # amount as verified revenue.
        if decision.approved_quote_amount_sar is not None:
            properties["amount"] = str(decision.approved_quote_amount_sar)

        if fit:
            properties["description"] = (
                f"Dealix mirror only. Fit tier {fit.tier} (score {fit.overall_score:.2f}). "
                "Commercial truth remains in Dealix Company OS."
            )

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.HUBSPOT_BASE_URL}/crm/v3/objects/deals",
                json={"properties": properties},
                headers=self._headers(),
            )
            response.raise_for_status()
            deal_id = str(response.json()["id"])

            association = await client.put(
                f"{self.HUBSPOT_BASE_URL}/crm/v4/objects/deals/{deal_id}/associations/"
                f"default/contacts/{contact_id}",
                headers=self._headers(),
            )
            association.raise_for_status()
            return deal_id
