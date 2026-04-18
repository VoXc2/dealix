"""
Dealix — LinkedInAgent
=======================
Channel agent for LinkedIn via Unipile API.

Unipile provides a unified API for LinkedIn (and other platforms):
  Base URL: https://{DSN}.unipile.com:13465/api/v1

Key endpoints used:
  POST /messaging/chats             — start a new chat / send InMail
  POST /messaging/chats/{id}/messages — send message in existing thread
  GET  /messaging/chats             — list conversations
  POST /users/connect               — send connection request
  GET  /users/search                — search LinkedIn users

All methods are placeholders (raise NotImplementedError with TODO comments)
until Unipile credentials are configured. The architecture and method
signatures are production-ready.

Compliance note (LinkedIn ToS):
  - Use the official Unipile API only — never raw scraping.
  - Respect LinkedIn's rate limits (connection requests, InMails per day).
  - Only message users who have consented or are reachable via InMail.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from ..base import (
    AgentContext,
    BaseEngagementAgent,
    ChannelType,
    DeliveryReceipt,
    DeliveryStatus,
    EngagementSettings,
    IncomingMessage,
)
from ..memory import ConversationMemory
from ..llm import LLMGateway

logger = logging.getLogger("dealix.engagement.linkedin")

# Unipile API base — format: https://{DSN}.unipile.com:13465/api/v1
_UNIPILE_BASE = "https://{dsn}.unipile.com:13465/api/v1"


class LinkedInAgent(BaseEngagementAgent):
    """
    LinkedIn channel agent using the Unipile unified API.

    Methods raise NotImplementedError until Unipile credentials are set.
    Constructor signature is production-ready for dependency injection.
    """

    channel = ChannelType.LINKEDIN

    def __init__(
        self,
        settings: EngagementSettings,
        memory: ConversationMemory | None = None,
        llm: LLMGateway | None = None,
    ) -> None:
        super().__init__(settings=settings, memory=memory, llm=llm)
        self._base_url = _UNIPILE_BASE.format(dsn=settings.unipile_dsn)

    # ── Abstract interface implementation ────────────────────

    async def send(
        self, to: str, message: str, context: AgentContext
    ) -> DeliveryReceipt:
        """
        Send a LinkedIn message to a profile URN or existing chat ID.

        `to` can be:
          - LinkedIn profile URN: "urn:li:fs_salesProfile:ACoAA..."
          - Unipile chat ID: "chat_..."

        TODO: Implement via Unipile POST /messaging/chats/{id}/messages
        """
        raise NotImplementedError(
            "TODO: LinkedInAgent.send() — implement via Unipile API.\n"
            "Endpoint: POST {base}/messaging/chats/{chat_id}/messages\n"
            "Headers:  X-API-KEY: {unipile_api_key}\n"
            "Body:     {\"text\": message, \"chat_id\": to}"
        )

    async def receive(self, payload: dict[str, Any]) -> IncomingMessage:
        """
        Parse a Unipile LinkedIn inbound webhook payload.

        TODO: Implement webhook parsing when Unipile webhook is configured.
        Expected payload fields: from_urn, text, chat_id, message_id, timestamp
        """
        raise NotImplementedError(
            "TODO: LinkedInAgent.receive() — implement Unipile webhook parsing.\n"
            "Docs: https://developer.unipile.com/webhooks"
        )

    # ── Connection request ───────────────────────────────────

    async def send_connection_request(
        self,
        profile_urn: str,
        note: str | None = None,
    ) -> dict[str, Any]:
        """
        Send a LinkedIn connection request.

        Args:
            profile_urn: LinkedIn profile URN.
            note:        Optional note (max 300 chars per LinkedIn limit).

        Returns the Unipile API response.

        TODO: Implement via Unipile POST /users/connect
        """
        if len(note or "") > 300:
            note = (note or "")[:297] + "..."

        # TODO: implement
        # async with httpx.AsyncClient() as client:
        #     resp = await client.post(
        #         f"{self._base_url}/users/connect",
        #         headers={"X-API-KEY": self.settings.unipile_api_key},
        #         json={"account_id": ..., "provider_id": profile_urn, "message": note}
        #     )
        #     resp.raise_for_status()
        #     return resp.json()

        raise NotImplementedError(
            "TODO: LinkedInAgent.send_connection_request()\n"
            "Endpoint: POST {base}/users/connect\n"
            "Body: {\"account_id\": ..., \"provider_id\": profile_urn, \"message\": note}"
        )

    async def send_inmail(
        self,
        profile_urn: str,
        subject: str,
        body: str,
    ) -> dict[str, Any]:
        """
        Send a LinkedIn InMail to a 2nd/3rd-degree connection.

        TODO: Implement via Unipile POST /messaging/chats
        """
        # TODO: implement
        # async with httpx.AsyncClient() as client:
        #     resp = await client.post(
        #         f"{self._base_url}/messaging/chats",
        #         headers={"X-API-KEY": self.settings.unipile_api_key},
        #         json={
        #             "account_id": ...,
        #             "attendees_ids": [profile_urn],
        #             "text": body,
        #             "subject": subject,
        #         }
        #     )
        #     resp.raise_for_status()
        #     return resp.json()

        raise NotImplementedError(
            "TODO: LinkedInAgent.send_inmail()\n"
            "Endpoint: POST {base}/messaging/chats\n"
            "Body: {account_id, attendees_ids: [profile_urn], text, subject}"
        )

    async def search_profiles(
        self,
        keywords: str,
        company: str | None = None,
        title: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Search LinkedIn profiles via Unipile.

        TODO: Implement via Unipile GET /users/search
        """
        # TODO: implement
        # params = {"keywords": keywords, "limit": limit}
        # if company: params["company"] = company
        # if title: params["title"] = title
        # async with httpx.AsyncClient() as client:
        #     resp = await client.get(
        #         f"{self._base_url}/users/search",
        #         headers={"X-API-KEY": self.settings.unipile_api_key},
        #         params=params,
        #     )
        #     resp.raise_for_status()
        #     return resp.json().get("items", [])

        raise NotImplementedError(
            "TODO: LinkedInAgent.search_profiles()\n"
            "Endpoint: GET {base}/users/search\n"
            "Params: keywords, company, title, limit"
        )

    async def list_conversations(self, limit: int = 20) -> list[dict[str, Any]]:
        """
        List recent LinkedIn conversations via Unipile.

        TODO: Implement via Unipile GET /messaging/chats
        """
        raise NotImplementedError(
            "TODO: LinkedInAgent.list_conversations()\n"
            "Endpoint: GET {base}/messaging/chats"
        )

    # ── Reply generation (LLM-powered, override of base) ────

    async def reply(self, incoming: IncomingMessage) -> str:
        """Generate a LinkedIn-appropriate reply (may be English or Arabic)."""
        history = await self.memory.get_history(
            channel=self.channel.value,
            address=incoming.from_address,
            limit=6,  # shorter context for LinkedIn
        )
        # LinkedIn replies are often in English — use base system prompt
        system_prompt = self.llm.compose_prompt("system_base_ar", "linkedin_followup_ar")
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": incoming.body})
        return await self.llm.chat(messages=messages, max_tokens=300)
