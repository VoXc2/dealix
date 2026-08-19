"""Tenant-isolation regression tests for revenue-memory conversation embeddings.

Conversation memory is tenant-owned end to end: the base ``ConversationRecord``
read, the ``ConversationEmbeddingRecord`` upsert, and semantic search must all
stay inside a non-empty tenant scope. ``tenant_id=None`` is rejected before
session creation, model access, or database access.

``index_account`` remains deliberately different because ``AccountRecord`` is a
platform-global entity in the current schema and ``account_embeddings.account_id``
is unique. The final contract test pins that intentional asymmetry.
"""

from __future__ import annotations

import inspect

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.models import Base, ConversationEmbeddingRecord

TENANT_A = "tenant_attacker"
TENANT_B = "tenant_victim"
CONVERSATION = "conv_shared_id"


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        # Only the table under test, matching the other *_tenant_isolation
        # suites. Creating the whole metadata can fail once another test has
        # imported a PostgreSQL-only column type that SQLite cannot render.
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[ConversationEmbeddingRecord.__table__],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as sess:
        yield sess
    await engine.dispose()


@pytest.fixture
def service(monkeypatch):
    """EmbeddingService with a deterministic, offline embedder."""
    from core.memory.embedding_service import EmbeddingService

    svc = EmbeddingService()

    async def _fake_embed(text: str):
        # Distinct, recognisable vectors per caller so an overwrite is visible.
        return [float(len(text))] * 4

    monkeypatch.setattr(svc, "embed", _fake_embed)
    return svc


async def _rows(session) -> list[ConversationEmbeddingRecord]:
    result = await session.execute(
        select(ConversationEmbeddingRecord).where(
            ConversationEmbeddingRecord.conversation_id == CONVERSATION
        )
    )
    return list(result.scalars().all())


@pytest.mark.asyncio
async def test_second_tenant_does_not_overwrite_the_first(service, session):
    """A second tenant must get its own embedding row, never rewrite the first."""
    await service.index_conversation(
        conversation_id=CONVERSATION, text="victim", tenant_id=TENANT_B, session=session
    )
    await session.commit()

    victim_before = (await _rows(session))[0]
    original_vector = list(victim_before.embedding_json)

    await service.index_conversation(
        conversation_id=CONVERSATION,
        text="attacker-supplied text that is a different length",
        tenant_id=TENANT_A,
        session=session,
    )
    await session.commit()

    rows = {row.tenant_id: row for row in await _rows(session)}

    assert TENANT_B in rows, "the victim's row disappeared"
    assert rows[TENANT_B].embedding_json == original_vector, (
        "another tenant's index call overwrote the victim's embedding"
    )
    assert TENANT_A in rows, "the second tenant got no row of its own"
    assert rows[TENANT_A].embedding_json != original_vector


@pytest.mark.asyncio
async def test_a_tenant_still_updates_its_own_row_in_place(service, session):
    """Scoping must not turn every re-index into a duplicate row."""
    await service.index_conversation(
        conversation_id=CONVERSATION, text="first", tenant_id=TENANT_B, session=session
    )
    await session.commit()
    await service.index_conversation(
        conversation_id=CONVERSATION,
        text="second pass, longer text",
        tenant_id=TENANT_B,
        session=session,
    )
    await session.commit()

    rows = await _rows(session)

    assert len(rows) == 1, f"re-indexing duplicated the row: {len(rows)} rows"
    assert rows[0].embedding_json == [float(len("second pass, longer text"))] * 4


@pytest.mark.asyncio
async def test_a_tenantless_caller_is_rejected_before_data_access(service, session):
    """Missing tenant context fails closed instead of matching NULL or every row."""
    await service.index_conversation(
        conversation_id=CONVERSATION, text="victim", tenant_id=TENANT_B, session=session
    )
    await session.commit()
    original = list((await _rows(session))[0].embedding_json)

    with pytest.raises(ValueError, match="tenant_id_required"):
        await service.index_conversation(
            conversation_id=CONVERSATION,
            text="anonymous caller with different length",
            tenant_id=None,
            session=session,
        )

    rows = await _rows(session)
    assert len(rows) == 1
    assert rows[0].tenant_id == TENANT_B
    assert rows[0].embedding_json == original


@pytest.mark.asyncio
async def test_different_conversations_stay_separate(service, session):
    await service.index_conversation(
        conversation_id="conv_one", text="one", tenant_id=TENANT_B, session=session
    )
    await service.index_conversation(
        conversation_id="conv_two", text="two", tenant_id=TENANT_B, session=session
    )
    await session.commit()

    result = await session.execute(select(ConversationEmbeddingRecord))
    assert len({row.conversation_id for row in result.scalars().all()}) == 2


def test_base_conversation_read_and_search_are_always_tenant_scoped():
    """Pin fail-closed tenant validation and both owned-memory read predicates."""
    from core.memory.embedding_service import EmbeddingService

    index_source = inspect.getsource(EmbeddingService.index_conversation)
    search_source = inspect.getsource(EmbeddingService.search_conversations)

    assert "tenant_id = self._required_tenant_id(tenant_id)" in index_source
    assert "tenant_id = self._required_tenant_id(tenant_id)" in search_source
    assert "ConversationRecord.id == conversation_id" in index_source
    assert "ConversationRecord.tenant_id == tenant_id" in index_source
    assert "ConversationEmbeddingRecord.tenant_id == tenant_id" in search_source
    assert "if tenant_id:" not in search_source, (
        "omitting tenant_id must never turn semantic search into a platform-wide read"
    )


def test_account_embeddings_are_intentionally_global_but_conversations_are_owned():
    """Pin the current schema boundary so the account/conversation asymmetry is explicit."""
    from db.models import AccountEmbeddingRecord, AccountRecord, ConversationRecord

    assert AccountEmbeddingRecord.__table__.columns["account_id"].unique is True
    assert "tenant_id" not in AccountRecord.__table__.columns
    assert "tenant_id" in ConversationRecord.__table__.columns
    assert ConversationEmbeddingRecord.__table__.columns["conversation_id"].unique is not True
