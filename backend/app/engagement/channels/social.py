"""
Dealix — SocialListener
========================
Monitors X (Twitter) and Instagram for brand mentions, keywords,
and direct messages. Uses official APIs and Apify actors as alternatives.

X (Twitter) API v2 reference:
  https://developer.twitter.com/en/docs/twitter-api
  Filtered stream: GET https://api.twitter.com/2/tweets/search/stream
  Recent search:   GET https://api.twitter.com/2/tweets/search/recent

Instagram Graph API reference:
  https://developers.facebook.com/docs/instagram-api
  Mentions: GET /me/mentioned_media

Apify (alternative for X + IG):
  X Scraper:          apify/twitter-scraper
  Instagram Scraper:  apify/instagram-scraper
  Actor runs: POST https://api.apify.com/v2/acts/{actor_id}/runs

Status: STUB — implement when social listening is prioritised.

TODO items:
  - [ ] X API v2 Filtered Stream for real-time mentions
  - [ ] Instagram Mentions webhook (requires Business account)
  - [ ] DM monitoring and auto-reply
  - [ ] Sentiment analysis on mentions
  - [ ] Alert routing (notify human for negative mentions)
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from ..base import ChannelType, EngagementSettings

logger = logging.getLogger("dealix.engagement.social")

_X_RECENT_SEARCH = "https://api.twitter.com/2/tweets/search/recent"
_X_STREAM_RULES = "https://api.twitter.com/2/tweets/search/stream/rules"
_X_STREAM = "https://api.twitter.com/2/tweets/search/stream"
_APIFY_ACTOR_BASE = "https://api.apify.com/v2/acts"


class SocialListener:
    """
    Monitors X (Twitter) and Instagram for brand mentions and signals.

    Not a full BaseEngagementAgent subclass (social listening is passive;
    send/receive semantics differ from direct messaging channels).

    Constructor accepts settings for dependency injection.
    """

    def __init__(self, settings: EngagementSettings) -> None:
        self.settings = settings
        self._x_bearer: str = getattr(settings, "x_bearer_token", "")
        self._ig_token: str = getattr(settings, "instagram_access_token", "")
        self._apify_token: str = getattr(settings, "apify_api_key", "")

    # ── X (Twitter) ──────────────────────────────────────────

    async def search_x_mentions(
        self,
        query: str = "Dealix OR @Dealix",
        max_results: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Search recent X posts mentioning Dealix (or any custom query).

        Uses X API v2 Recent Search (last 7 days for Essential/Basic access).

        TODO: implement
        """
        if not self._x_bearer:
            raise NotImplementedError(
                "TODO: SocialListener.search_x_mentions()\n"
                "Requires X_BEARER_TOKEN in environment.\n"
                "Endpoint: GET https://api.twitter.com/2/tweets/search/recent"
            )

        # TODO: implement
        # params = {
        #     "query": query,
        #     "max_results": max_results,
        #     "tweet.fields": "created_at,author_id,text,public_metrics",
        # }
        # headers = {"Authorization": f"Bearer {self._x_bearer}"}
        # async with httpx.AsyncClient() as client:
        #     resp = await client.get(_X_RECENT_SEARCH, params=params, headers=headers)
        #     resp.raise_for_status()
        #     return resp.json().get("data", [])

        raise NotImplementedError(
            "TODO: SocialListener.search_x_mentions() — X API v2 not yet configured."
        )

    async def add_x_stream_rule(self, value: str, tag: str = "dealix") -> dict[str, Any]:
        """
        Add a filtered stream rule for real-time X mention monitoring.

        TODO: implement
        """
        raise NotImplementedError(
            "TODO: SocialListener.add_x_stream_rule()\n"
            "Endpoint: POST https://api.twitter.com/2/tweets/search/stream/rules"
        )

    async def start_x_stream(self) -> None:
        """
        Start listening to the X filtered stream (real-time mentions).

        TODO: implement as a long-running async task / Celery worker.
        """
        raise NotImplementedError(
            "TODO: SocialListener.start_x_stream()\n"
            "Run as background ARQ task: async for tweet in stream_x(): ..."
        )

    # ── Instagram ────────────────────────────────────────────

    async def get_ig_mentions(self, since_id: str | None = None) -> list[dict[str, Any]]:
        """
        Get Instagram posts that mention the Dealix account.
        Requires Instagram Business account + approved permissions.

        TODO: implement
        """
        raise NotImplementedError(
            "TODO: SocialListener.get_ig_mentions()\n"
            "Endpoint: GET /me/mentioned_media (Instagram Graph API)\n"
            "Requires: instagram_graph_access_token, ig_user_id"
        )

    async def get_ig_dm_conversations(self) -> list[dict[str, Any]]:
        """
        Get Instagram DM conversations via Instagram Messaging API.

        TODO: implement
        """
        raise NotImplementedError(
            "TODO: SocialListener.get_ig_dm_conversations()\n"
            "Endpoint: GET /me/conversations?platform=instagram (Graph API)\n"
            "Docs: https://developers.facebook.com/docs/messenger-platform/instagram"
        )

    # ── Apify alternative ────────────────────────────────────

    async def run_x_scraper_apify(
        self,
        search_query: str,
        max_items: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Run the Apify X (Twitter) Scraper actor as an alternative to the X API.
        Useful when X API access tier is restrictive.

        Apify actor: apify/twitter-scraper

        TODO: implement
        """
        if not self._apify_token:
            raise NotImplementedError(
                "TODO: SocialListener.run_x_scraper_apify()\n"
                "Requires APIFY_API_KEY in environment.\n"
                "Actor: POST https://api.apify.com/v2/acts/apify~twitter-scraper/runs"
            )

        # TODO: implement
        # async with httpx.AsyncClient() as client:
        #     resp = await client.post(
        #         f"{_APIFY_ACTOR_BASE}/apify~twitter-scraper/runs",
        #         headers={"Authorization": f"Bearer {self._apify_token}"},
        #         json={
        #             "searchTerms": [search_query],
        #             "maxItems": max_items,
        #             "lang": "ar",
        #         }
        #     )
        #     resp.raise_for_status()
        #     run = resp.json().get("data", {})
        #     # Poll for results using run["id"]
        #     ...

        raise NotImplementedError(
            "TODO: SocialListener.run_x_scraper_apify() — Apify not yet configured."
        )

    async def run_ig_scraper_apify(
        self,
        hashtags: list[str],
        max_items: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Run the Apify Instagram Scraper actor.

        Apify actor: apify/instagram-scraper

        TODO: implement
        """
        raise NotImplementedError(
            "TODO: SocialListener.run_ig_scraper_apify()\n"
            "Actor: POST https://api.apify.com/v2/acts/apify~instagram-scraper/runs\n"
            "Body: {\"hashtags\": hashtags, \"maxPosts\": max_items}"
        )
