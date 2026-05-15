"""Knowledge chunks — Phase 1 RAG (Postgres backend for knowledge_v10).

Companion to `auto_client_acquisition/knowledge_v10/store.py`
(PgKnowledgeStore) and `db.models.KnowledgeChunkRecord`.

The embedding is a JSON float array so the table works on plain
PostgreSQL; a pgvector `vector` column + ANN index is a later ALTER
once the extension is provisioned.

Migration 011.
Down revision: 010 (referral_program).
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "011"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "010"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "knowledge_chunks",
        sa.Column("chunk_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.String(length=64), nullable=False),
        sa.Column("customer_handle", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("source_type", sa.String(length=64), nullable=False, server_default="internal_doc"),
        sa.Column("text", sa.Text(), nullable=False, server_default=""),
        sa.Column("embedding_json", sa.JSON(), nullable=False),
        sa.Column("language", sa.String(length=8), nullable=False, server_default="ar"),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("chunk_id", name="pk_knowledge_chunks"),
    )
    op.create_index("ix_knowledge_chunks_document_id", "knowledge_chunks", ["document_id"])
    op.create_index(
        "ix_knowledge_chunks_customer_handle", "knowledge_chunks", ["customer_handle"]
    )
    op.create_index("ix_knowledge_chunks_source_type", "knowledge_chunks", ["source_type"])
    op.create_index("ix_knowledge_chunks_created_at", "knowledge_chunks", ["created_at"])
    op.create_index(
        "ix_knowledge_chunks_tenant_doc",
        "knowledge_chunks",
        ["customer_handle", "document_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_knowledge_chunks_tenant_doc", table_name="knowledge_chunks")
    op.drop_index("ix_knowledge_chunks_created_at", table_name="knowledge_chunks")
    op.drop_index("ix_knowledge_chunks_source_type", table_name="knowledge_chunks")
    op.drop_index("ix_knowledge_chunks_customer_handle", table_name="knowledge_chunks")
    op.drop_index("ix_knowledge_chunks_document_id", table_name="knowledge_chunks")
    op.drop_table("knowledge_chunks")
