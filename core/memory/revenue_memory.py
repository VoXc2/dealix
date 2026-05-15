"""
RevenueMemory — high-level semantic search interface for agents.
ذاكرة الإيرادات — واجهة البحث الدلالي للوكلاء.

Wraps EmbeddingService to provide a simple self.memory.search(query)
interface that BaseAgent can call directly.

Usage in an agent:
    class MyAgent(BaseAgent):
        async def run(self, query: str, tenant_id: str) -> dict:
            similar = await self.memory.search(query, tenant_id=tenant_id)
            # similar = [{"account_id": ..., "similarity": 0.92, ...}, ...]
"""

from __future__ import annotations

import logging
from typing import Any

from core.memory.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class RevenueMemory:
    """
    Agent-facing semantic memory backed by EmbeddingService.
    ذاكرة الوكيل الدلالية المدعومة بخدمة التضمين.

    This is a thin facade: it owns no DB session.
    Each call opens its own session via get_session() from db.session.
    Agents call self.memory.search(query) in their run() methods.
    """

    def __init__(self) -> None:
        self._svc = EmbeddingService()  # session-less, creates sessions per call

    # ── Primary interface ─────────────────────────────────────────

    async def search(
        self,
        query: str,
        *,
        entity_type: str = "account",
        tenant_id: str | None = None,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Semantic search over Revenue Memory.
        بحث دلالي في ذاكرة الإيرادات.

        Args:
            query:       Natural language query, e.g.
                         "logistics company Riyadh 100+ employees interested in AI"
            entity_type: "account" | "conversation"
            tenant_id:   Scope search to a single tenant.
            top_k:       Maximum results to return.

        Returns:
            List of dicts with entity_id + similarity score (0-1).
        """
        if entity_type == "account":
            return await self._svc.search_accounts(
                query=query, tenant_id=tenant_id, top_k=top_k
            )
        if entity_type == "conversation":
            return await self._svc.search_conversations(
                query=query, tenant_id=tenant_id, top_k=top_k
            )
        logger.warning("revenue_memory_unknown_entity_type", entity_type=entity_type)
        return []

    async def index_account(
        self,
        account_id: str,
        text: str | None = None,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Index (or re-index) an account into Revenue Memory.
        فهرسة حساب في ذاكرة الإيرادات.
        """
        return await self._svc.index_account(
            account_id=account_id,
            text=text,
            tenant_id=tenant_id,
        )

    async def index_conversation(
        self,
        conversation_id: str,
        text: str | None = None,
        tenant_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Index (or re-index) a conversation into Revenue Memory.
        فهرسة محادثة في ذاكرة الإيرادات.
        """
        return await self._svc.index_conversation(
            conversation_id=conversation_id,
            text=text,
            tenant_id=tenant_id,
        )

    async def auto_index_account(
        self,
        account_id: str,
        tenant_id: str | None = None,
    ) -> None:
        """
        Auto-index account when a new AccountRecord is created.
        الفهرسة التلقائية عند إنشاء حساب جديد.

        Silently skips on any error to avoid blocking the main flow.
        """
        try:
            await self.index_account(account_id=account_id, tenant_id=tenant_id)
        except Exception as exc:
            logger.warning(
                "auto_index_account_failed",
                account_id=account_id,
                error=str(exc),
            )

    async def auto_index_conversation(
        self,
        conversation_id: str,
        tenant_id: str | None = None,
    ) -> None:
        """
        Auto-index conversation turn when a new ConversationRecord is created.
        الفهرسة التلقائية عند إنشاء محادثة جديدة.
        """
        try:
            await self.index_conversation(
                conversation_id=conversation_id,
                tenant_id=tenant_id,
            )
        except Exception as exc:
            logger.warning(
                "auto_index_conversation_failed",
                conversation_id=conversation_id,
                error=str(exc),
            )
