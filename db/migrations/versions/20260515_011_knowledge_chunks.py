"""Knowledge OS — documents, chunks, events.

Companion to ``auto_client_acquisition/knowledge_os/`` (Wave 16). The
runtime spine uses the JSONL knowledge ledger; these tables are the
DB-backed upgrade path for the in-memory index + ledger.

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
        "knowledge_documents",
        sa.Column("document_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=True),
        sa.Column("customer_handle", sa.String(length=128), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False, server_default=""),
        sa.Column("language", sa.String(length=8), nullable=False, server_default="ar"),
        sa.Column("chunk_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("evidence_id", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("document_id", name="pk_knowledge_documents"),
    )
    op.create_index(
        "ix_knowledge_documents_customer",
        "knowledge_documents",
        ["customer_handle", "created_at"],
    )

    op.create_table(
        "knowledge_chunks",
        sa.Column("chunk_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.String(length=64), nullable=False),
        sa.Column("customer_handle", sa.String(length=128), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("snippet_redacted", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["knowledge_documents.document_id"],
            name="fk_knowledge_chunks_document",
        ),
        sa.PrimaryKeyConstraint("chunk_id", name="pk_knowledge_chunks"),
    )
    op.create_index(
        "ix_knowledge_chunks_customer", "knowledge_chunks", ["customer_handle"]
    )
    op.create_index(
        "ix_knowledge_chunks_document", "knowledge_chunks", ["document_id"]
    )

    op.create_table(
        "knowledge_events",
        sa.Column("knowledge_event_id", sa.String(length=64), nullable=False),
        sa.Column("customer_handle", sa.String(length=128), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("document_id", sa.String(length=64), nullable=True),
        sa.Column("query", sa.String(length=512), nullable=False, server_default=""),
        sa.Column("chunk_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("citation_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "insufficient_evidence",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("knowledge_event_id", name="pk_knowledge_events"),
    )
    op.create_index(
        "ix_knowledge_events_customer",
        "knowledge_events",
        ["customer_handle", "occurred_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_knowledge_events_customer", table_name="knowledge_events")
    op.drop_table("knowledge_events")

    op.drop_index("ix_knowledge_chunks_document", table_name="knowledge_chunks")
    op.drop_index("ix_knowledge_chunks_customer", table_name="knowledge_chunks")
    op.drop_table("knowledge_chunks")

    op.drop_index("ix_knowledge_documents_customer", table_name="knowledge_documents")
    op.drop_table("knowledge_documents")
