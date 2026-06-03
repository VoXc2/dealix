"""
EmbeddingService — OpenAI text-embedding-3-small for Revenue Memory.
خدمة التضمين المتجهي — نموذج OpenAI لذاكرة الإيرادات.

Uses OpenAI text-embedding-3-small (1536 dims).
Stores vectors in AccountEmbeddingRecord / ConversationEmbeddingRecord.
Cosine similarity is computed in pure Python (no pgvector required in dev).

Usage:
    svc = EmbeddingService(session=db_session)
    vector = await svc.embed("logistics SaaS Riyadh 50 employees")
    results = await svc.search_accounts(query="...", tenant_id="t1", top_k=5)
"""

from __future__ import annotations

import logging
import math
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.settings import get_settings
from core.utils import generate_id, utcnow

logger = logging.getLogger(__name__)

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMS = 1536


class EmbeddingService:
    """
    Generates, stores, and queries vector embeddings.
    يُنشئ التضمينات المتجهية ويخزّنها ويستعلم عنها.

    Accepts an optional AsyncSession. When omitted, index_* methods
    create their own session; search_* methods require an explicit session.
    """

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session
        self._model = DEFAULT_EMBEDDING_MODEL
        self._client: Any = None  # lazy — only built when OpenAI key available

    def _get_client(self) -> Any:
        """Lazily build AsyncOpenAI client."""
        if self._client is None:
            import openai as _openai
            settings = get_settings()
            if settings.openai_api_key is None:
                raise RuntimeError(
                    "OPENAI_API_KEY is not configured. "
                    "EmbeddingService requires OpenAI API access."
                )
            self._client = _openai.AsyncOpenAI(
                api_key=settings.openai_api_key.get_secret_value()
            )
        return self._client

    # ── Public API ────────────────────────────────────────────────

    async def embed(self, text: str) -> list[float]:
        """
        Call OpenAI Embeddings API and return the float vector.
        استدعاء API لتضمين النص وإعادة المتجه.

        Falls back to zero-vector on API failure so callers never crash.
        """
        text = text.strip().replace("\n", " ")
        if not text:
            return [0.0] * EMBEDDING_DIMS
        try:
            client = self._get_client()
            response = await client.embeddings.create(
                model=self._model,
                input=text,
                encoding_format="float",
            )
            return response.data[0].embedding
        except Exception as exc:
            logger.warning("embedding_api_error", extra={"error": str(exc)})
            return [0.0] * EMBEDDING_DIMS

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple texts in a single API call (up to 2048 inputs).
        تضمين عدة نصوص في استدعاء واحد.
        """
        cleaned = [t.strip().replace("\n", " ") for t in texts]
        if not any(cleaned):
            return [[0.0] * EMBEDDING_DIMS] * len(texts)
        try:
            client = self._get_client()
            response = await client.embeddings.create(
                model=self._model,
                input=cleaned,
                encoding_format="float",
            )
            # API returns embeddings in the same order as input
            return [item.embedding for item in response.data]
        except Exception as exc:
            logger.warning("embedding_batch_api_error", extra={"error": str(exc)})
            return [[0.0] * EMBEDDING_DIMS] * len(texts)

    async def index_account(
        self,
        account_id: str,
        text: str | None = None,
        tenant_id: str | None = None,
        session: AsyncSession | None = None,
    ) -> dict[str, Any]:
        """
        Embed an account and upsert into account_embeddings.
        تضمين حساب وتحديث سجل التضمين في قاعدة البيانات.

        If `text` is None, builds a summary from AccountRecord fields.
        """
        from db.models import AccountEmbeddingRecord, AccountRecord

        sess = session or self._session
        if sess is None:
            from db.session import get_session
            async with get_session() as auto_sess:
                return await self.index_account(
                    account_id=account_id,
                    text=text,
                    tenant_id=tenant_id,
                    session=auto_sess,
                )

        # Build text if not provided
        if text is None:
            result = await sess.execute(
                select(AccountRecord).where(AccountRecord.id == account_id)
            )
            account = result.scalar_one_or_none()
            if not account:
                return {"status": "not_found", "account_id": account_id}
            text = _account_to_text(account)

        vector = await self.embed(text)

        # Upsert embedding record
        existing = await sess.execute(
            select(AccountEmbeddingRecord).where(AccountEmbeddingRecord.account_id == account_id)
        )
        record = existing.scalar_one_or_none()
        if record:
            record.embedding_json = vector
            record.text_used = text
            record.updated_at = utcnow()
        else:
            record = AccountEmbeddingRecord(
                id=generate_id("embacc"),
                tenant_id=tenant_id,
                account_id=account_id,
                embedding_json=vector,
                model_name=self._model,
                text_used=text,
            )
            sess.add(record)

        logger.info("account_indexed", account_id=account_id, dims=len(vector))
        return {"status": "ok", "account_id": account_id, "dims": len(vector)}

    async def index_conversation(
        self,
        conversation_id: str,
        text: str | None = None,
        tenant_id: str | None = None,
        session: AsyncSession | None = None,
    ) -> dict[str, Any]:
        """
        Embed a conversation turn and upsert into conversation_embeddings.
        تضمين محادثة وتحديث سجل التضمين.
        """
        from db.models import ConversationEmbeddingRecord, ConversationRecord

        sess = session or self._session
        if sess is None:
            from db.session import get_session
            async with get_session() as auto_sess:
                return await self.index_conversation(
                    conversation_id=conversation_id,
                    text=text,
                    tenant_id=tenant_id,
                    session=auto_sess,
                )

        # Build text if not provided
        if text is None:
            result = await sess.execute(
                select(ConversationRecord).where(ConversationRecord.id == conversation_id)
            )
            conv = result.scalar_one_or_none()
            if not conv:
                return {"status": "not_found", "conversation_id": conversation_id}
            text = _conversation_to_text(conv)

        vector = await self.embed(text)

        # Upsert
        existing = await sess.execute(
            select(ConversationEmbeddingRecord).where(
                ConversationEmbeddingRecord.conversation_id == conversation_id
            )
        )
        record = existing.scalar_one_or_none()
        if record:
            record.embedding_json = vector
        else:
            record = ConversationEmbeddingRecord(
                id=generate_id("embconv"),
                tenant_id=tenant_id,
                conversation_id=conversation_id,
                embedding_json=vector,
                model_name=self._model,
            )
            sess.add(record)

        logger.info("conversation_indexed", conversation_id=conversation_id, dims=len(vector))
        return {"status": "ok", "conversation_id": conversation_id, "dims": len(vector)}

    async def search_accounts(
        self,
        query: str,
        tenant_id: str | None = None,
        top_k: int = 10,
        session: AsyncSession | None = None,
    ) -> list[dict[str, Any]]:
        """
        Semantic search over account embeddings using cosine similarity.
        بحث دلالي في تضمينات الحسابات.
        """
        from db.models import AccountEmbeddingRecord

        sess = session or self._session
        if sess is None:
            from db.session import get_session
            async with get_session() as auto_sess:
                return await self.search_accounts(
                    query=query,
                    tenant_id=tenant_id,
                    top_k=top_k,
                    session=auto_sess,
                )

        query_vec = await self.embed(query)

        stmt = select(AccountEmbeddingRecord)
        if tenant_id:
            stmt = stmt.where(AccountEmbeddingRecord.tenant_id == tenant_id)
        result = await sess.execute(stmt)
        records = result.scalars().all()

        scored: list[tuple[float, AccountEmbeddingRecord]] = []
        for rec in records:
            emb = rec.embedding_json
            if emb and len(emb) == EMBEDDING_DIMS:
                sim = cosine_similarity(query_vec, emb)
                scored.append((sim, rec))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "account_id": rec.account_id,
                "similarity": round(sim, 4),
                "text_used": rec.text_used,
            }
            for sim, rec in scored[:top_k]
        ]

    async def search_conversations(
        self,
        query: str,
        tenant_id: str | None = None,
        top_k: int = 10,
        session: AsyncSession | None = None,
    ) -> list[dict[str, Any]]:
        """
        Semantic search over conversation embeddings.
        بحث دلالي في تضمينات المحادثات.
        """
        from db.models import ConversationEmbeddingRecord

        sess = session or self._session
        if sess is None:
            from db.session import get_session
            async with get_session() as auto_sess:
                return await self.search_conversations(
                    query=query,
                    tenant_id=tenant_id,
                    top_k=top_k,
                    session=auto_sess,
                )

        query_vec = await self.embed(query)

        stmt = select(ConversationEmbeddingRecord)
        if tenant_id:
            stmt = stmt.where(ConversationEmbeddingRecord.tenant_id == tenant_id)
        result = await sess.execute(stmt)
        records = result.scalars().all()

        scored: list[tuple[float, ConversationEmbeddingRecord]] = []
        for rec in records:
            emb = rec.embedding_json
            if emb and len(emb) == EMBEDDING_DIMS:
                sim = cosine_similarity(query_vec, emb)
                scored.append((sim, rec))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "conversation_id": rec.conversation_id,
                "similarity": round(sim, 4),
            }
            for sim, rec in scored[:top_k]
        ]


# ── Text builders ──────────────────────────────────────────────────

def _account_to_text(account: Any) -> str:
    """Build a rich text string from AccountRecord for embedding."""
    parts = [
        account.company_name or "",
        f"sector:{account.sector}" if account.sector else "",
        f"city:{account.city}" if account.city else "",
        f"country:{account.country}" if account.country else "",
        f"domain:{account.domain}" if account.domain else "",
        f"status:{account.status}" if account.status else "",
    ]
    return " | ".join(p for p in parts if p)


def _conversation_to_text(conv: Any) -> str:
    """Build text from ConversationRecord for embedding."""
    parts = [
        f"channel:{conv.channel}" if conv.channel else "",
        conv.inbound_message or "",
        conv.outbound_response or "",
        f"classification:{conv.classification}" if conv.classification else "",
        f"sentiment:{conv.sentiment}" if conv.sentiment else "",
    ]
    return " ".join(p for p in parts if p)


# ── Math ───────────────────────────────────────────────────────────

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two float vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
