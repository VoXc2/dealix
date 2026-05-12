"""knowledge tables — T5b pgvector RAG

Revision ID: 006
Revises: 005
Create Date: 2026-05-21 00:00:00.000000

Changes:
  - Enable pgvector extension (idempotent CREATE EXTENSION).
  - Create knowledge_documents table.
  - Create knowledge_chunks table with a 1024-dim vector column +
    HNSW index for cosine similarity.

Backend portability:
  - pgvector is Postgres-only. On SQLite (used in some tests) the
    create-extension + vector column statements are no-ops so the
    migration still completes; the column lives as bytea-style and
    is never queried from non-Postgres backends.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _is_postgres() -> bool:
    return op.get_bind().dialect.name == "postgresql"


def upgrade() -> None:
    if _is_postgres():
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "knowledge_documents",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("source_kind", sa.String(32), nullable=False, server_default="upload"),
        sa.Column("source_uri", sa.String(2048), nullable=True),
        sa.Column("locale", sa.String(8), nullable=False, server_default="ar"),
        sa.Column("status", sa.String(32), nullable=False, server_default="processing"),
        sa.Column("chunk_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("metadata", sa.JSON, nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_knowledge_documents_tenant_id", "knowledge_documents", ["tenant_id"])
    op.create_index("ix_knowledge_documents_status", "knowledge_documents", ["status"])
    op.create_index("ix_kd_tenant_status", "knowledge_documents", ["tenant_id", "status"])

    op.create_table(
        "knowledge_chunks",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column(
            "document_id",
            sa.String(64),
            sa.ForeignKey("knowledge_documents.id"),
            nullable=False,
        ),
        sa.Column("order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("text", sa.Text, nullable=False, server_default=""),
        sa.Column("embedding_model", sa.String(64), nullable=False, server_default=""),
        sa.Column("metadata", sa.JSON, nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index("ix_knowledge_chunks_tenant_id", "knowledge_chunks", ["tenant_id"])
    op.create_index("ix_knowledge_chunks_document_id", "knowledge_chunks", ["document_id"])
    op.create_index("ix_kc_tenant_document", "knowledge_chunks", ["tenant_id", "document_id"])

    if _is_postgres():
        # Add the vector column + HNSW index only on Postgres. We pick
        # 1024 dims to fit Voyage v3 and Cohere multilingual v3; OpenAI
        # text-embedding-3-small (1536 dims) will fail to insert
        # against this column — callers using OpenAI must either
        # truncate to 1024 or run a separate 1536 column on a future
        # migration. We pin to 1024 deliberately for now to keep the
        # index small.
        op.execute("ALTER TABLE knowledge_chunks ADD COLUMN embedding vector(1024)")
        op.execute(
            "CREATE INDEX ix_kc_embedding_hnsw "
            "ON knowledge_chunks USING hnsw (embedding vector_cosine_ops)"
        )


def downgrade() -> None:
    if _is_postgres():
        op.execute("DROP INDEX IF EXISTS ix_kc_embedding_hnsw")
        op.execute("ALTER TABLE knowledge_chunks DROP COLUMN IF EXISTS embedding")
    op.drop_index("ix_kc_tenant_document", "knowledge_chunks")
    op.drop_index("ix_knowledge_chunks_document_id", "knowledge_chunks")
    op.drop_index("ix_knowledge_chunks_tenant_id", "knowledge_chunks")
    op.drop_table("knowledge_chunks")
    op.drop_index("ix_kd_tenant_status", "knowledge_documents")
    op.drop_index("ix_knowledge_documents_status", "knowledge_documents")
    op.drop_index("ix_knowledge_documents_tenant_id", "knowledge_documents")
    op.drop_table("knowledge_documents")
