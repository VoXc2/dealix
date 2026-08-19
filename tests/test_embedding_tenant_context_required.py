"""Fail-closed tenant-context contracts for conversation embeddings."""

from __future__ import annotations

import pytest

from core.memory.embedding_service import EmbeddingService


@pytest.mark.asyncio
@pytest.mark.parametrize("tenant_id", [None, "", "   "])
async def test_index_conversation_rejects_missing_tenant_before_data_access(
    tenant_id: str | None,
) -> None:
    service = EmbeddingService()

    with pytest.raises(ValueError, match="^tenant_id_required$"):
        await service.index_conversation(
            conversation_id="conv_missing_tenant",
            text="must not embed",
            tenant_id=tenant_id,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("tenant_id", [None, "", "   "])
async def test_search_conversations_rejects_missing_tenant_before_data_access(
    tenant_id: str | None,
) -> None:
    service = EmbeddingService()

    with pytest.raises(ValueError, match="^tenant_id_required$"):
        await service.search_conversations(
            query="must not search",
            tenant_id=tenant_id,
        )


def test_required_tenant_id_normalizes_whitespace() -> None:
    assert EmbeddingService._required_tenant_id("  tenant-alpha  ") == "tenant-alpha"
