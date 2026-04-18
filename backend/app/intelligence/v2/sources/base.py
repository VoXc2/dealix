"""
Base Source Adapter — Dealix Lead Intelligence Engine V2
========================================================
Abstract base class for all source adapters.
Provides rate limiting, retry logic, and mock fallback support.
"""

from __future__ import annotations

import asyncio
import functools
import logging
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import AsyncGenerator, Callable, List, Optional

import httpx

from app.intelligence.v2.models import DiscoveryQuery, ProvenanceRecord, RawLead, SearchPlan

logger = logging.getLogger(__name__)

# ─────────────────────────── Rate Limit Decorator ────────────────────────────


def rate_limited(calls_per_second: float = 1.0, calls_per_minute: Optional[float] = None):
    """
    Decorator: enforce rate limits on async methods.
    Uses token bucket approach.
    """
    min_interval = 1.0 / calls_per_second if calls_per_second else 0
    minute_interval = 60.0 / calls_per_minute if calls_per_minute else 0

    def decorator(func: Callable):
        last_call_time = [0.0]
        minute_window = [0.0, 0]  # [window_start, call_count]
        lock = asyncio.Lock()

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with lock:
                now = time.monotonic()

                # Per-second rate limit
                if min_interval > 0:
                    elapsed = now - last_call_time[0]
                    if elapsed < min_interval:
                        await asyncio.sleep(min_interval - elapsed)
                        now = time.monotonic()

                # Per-minute rate limit
                if minute_interval > 0:
                    if now - minute_window[0] >= 60:
                        minute_window[0] = now
                        minute_window[1] = 0
                    if minute_window[1] >= calls_per_minute:
                        sleep_time = 60 - (now - minute_window[0])
                        if sleep_time > 0:
                            await asyncio.sleep(sleep_time)
                        minute_window[0] = time.monotonic()
                        minute_window[1] = 0
                    minute_window[1] += 1

                last_call_time[0] = time.monotonic()

            return await func(*args, **kwargs)

        return wrapper

    return decorator


# ─────────────────────────── Retry Decorator ─────────────────────────────────


def with_retry(max_attempts: int = 3, base_delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator: retry async methods on transient errors with exponential backoff.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except (httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException) as e:
                    last_exc = e
                    if attempt < max_attempts - 1:
                        delay = base_delay * (backoff ** attempt)
                        logger.warning(
                            f"[{func.__qualname__}] attempt {attempt+1} failed: {e}. "
                            f"Retrying in {delay:.1f}s"
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"[{func.__qualname__}] all {max_attempts} attempts failed: {e}")
                except Exception as e:
                    # Non-transient error — don't retry
                    logger.error(f"[{func.__qualname__}] non-retryable error: {e}")
                    raise
            raise last_exc

        return wrapper

    return decorator


# ─────────────────────────── Base Source ─────────────────────────────────────


class BaseSource(ABC):
    """
    Abstract base for all Lead Intelligence V2 source adapters.

    Subclasses must implement:
        - SOURCE_NAME: str class attribute
        - discover(query, plan) -> List[RawLead]

    Optional:
        - REQUIRES_KEY: bool — if True, returns mock when key missing
        - RATE_LIMIT_CPS: float — calls per second
        - RATE_LIMIT_CPM: float — calls per minute

    Example::

        class MySource(BaseSource):
            SOURCE_NAME = "my_source"
            REQUIRES_KEY = True

            async def discover(self, query, plan):
                if not self.api_key:
                    return self._mock_leads(query, plan, count=3)
                # ... real implementation
    """

    SOURCE_NAME: str = "base"
    REQUIRES_KEY: bool = False
    RATE_LIMIT_CPS: float = 2.0    # calls per second
    RATE_LIMIT_CPM: Optional[float] = None  # calls per minute

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._last_request: float = 0.0

    @property
    def api_key(self) -> Optional[str]:
        """Override in subclasses to return the relevant env var."""
        return None

    @property
    def is_available(self) -> bool:
        """True if source can return real data (has API key if required)."""
        if self.REQUIRES_KEY:
            return bool(self.api_key)
        return True

    async def get_client(self) -> httpx.AsyncClient:
        """Get or create a shared async HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0, connect=10.0),
                headers={
                    "User-Agent": (
                        "Dealix-LeadEngine/2.0 (Gulf B2B Intelligence; "
                        "contact: ops@dealix.sa)"
                    ),
                    "Accept-Language": "ar,en;q=0.9",
                },
                follow_redirects=True,
            )
        return self._client

    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    @abstractmethod
    async def discover(
        self,
        query: DiscoveryQuery,
        plan: SearchPlan,
    ) -> List[RawLead]:
        """
        Execute a search plan and return raw leads.

        Args:
            query: The top-level DiscoveryQuery with ICP + settings
            plan: The specific SearchPlan for this source (query string, filters)

        Returns:
            List of RawLead objects. Must include ProvenanceRecord on each.
            If REQUIRES_KEY and key not present, return mock data with is_mock=True.
        """
        ...

    def _make_provenance(
        self,
        plan: SearchPlan,
        url: Optional[str] = None,
        is_mock: bool = False,
    ) -> ProvenanceRecord:
        """Create a ProvenanceRecord for this source."""
        return ProvenanceRecord(
            source_name=self.SOURCE_NAME,
            query_used=plan.query_string,
            fetched_at=datetime.utcnow(),
            url=url,
            is_mock=is_mock,
        )

    def _mock_leads(
        self,
        query: DiscoveryQuery,
        plan: SearchPlan,
        count: int = 3,
    ) -> List[RawLead]:
        """
        Return mock leads when API key is missing.
        Generates plausible mock data based on the query context.
        """
        provenance = self._make_provenance(plan, is_mock=True)
        leads = []
        industry = (query.icp.industries[0] if query.icp.industries else "business")
        city = (query.icp.geo.cities[0] if query.icp.geo.cities else "Riyadh")

        mock_templates = [
            {
                "company_name": f"Al Noor {industry.title()} Co",
                "company_name_ar": f"شركة النور للـ{industry}",
                "domain": f"alnoor-{industry.lower().replace(' ', '')}.com.sa",
                "phone": "+966501234567",
                "email": f"info@alnoor-{industry.lower().replace(' ', '')}.com.sa",
                "city": city,
                "country": "SA",
                "industry": industry,
                "description": f"Mock {industry} company in {city} (SA)",
                "is_hiring": True,
                "hiring_roles": ["Sales Manager", "Marketing Coordinator"],
            },
            {
                "company_name": f"Gulf {industry.title()} Group",
                "company_name_ar": f"مجموعة الخليج للـ{industry}",
                "domain": f"gulf-{industry.lower().replace(' ', '')}.sa",
                "phone": "+966512345678",
                "email": f"contact@gulf-{industry.lower().replace(' ', '')}.sa",
                "city": city,
                "country": "SA",
                "industry": industry,
                "description": f"Mock Gulf {industry} group in {city}",
                "is_hiring": False,
                "hiring_roles": [],
            },
            {
                "company_name": f"Riyadh {industry.title()} Solutions",
                "company_name_ar": f"حلول الرياض للـ{industry}",
                "domain": f"riyadh-{industry.lower().replace(' ', '')}-solutions.com",
                "phone": "+966523456789",
                "email": f"hello@riyadh-{industry.lower().replace(' ', '')}-solutions.com",
                "city": city,
                "country": "SA",
                "industry": industry,
                "description": f"Mock {industry} solutions provider",
                "is_hiring": True,
                "hiring_roles": ["Digital Marketing Manager"],
            },
        ]

        for i, template in enumerate(mock_templates[:count]):
            lead = RawLead(provenance=provenance, **template)
            leads.append(lead)

        logger.info(
            f"[{self.SOURCE_NAME}] Returning {len(leads)} MOCK leads "
            f"(no API key). Set {self.SOURCE_NAME.upper().replace('-', '_')}_KEY "
            f"to get real data."
        )
        return leads

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
