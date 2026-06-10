from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class VectorPoint(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vector: list[float]
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SearchResult(BaseModel):
    id: str
    score: float
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    distance: float | None = None


class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    MARKDOWN = "md"
    TEXT = "txt"


class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    doc_type: DocumentType | None = None
    source: str | None = None
    chunk_index: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentEmbedding(BaseModel):
    document_id: str
    chunk_index: int
    embedding: list[float]
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestResult(BaseModel):
    collection: str
    source: str
    chunks_count: int
    document_ids: list[str]
    success: bool = True
    error: str | None = None


class EmbeddingConfig(BaseModel):
    model: str = "text-embedding-3-small"
    dimensions: int = 1536
    batch_size: int = 20
    max_retries: int = 3
    retry_delay: float = 1.0


class CollectionConfig(BaseModel):
    name: str
    dimensions: int = 1536
    distance: str = "Cosine"
    on_disk: bool = False


class MultiModalDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str | None = None
    image_path: str | None = None
    embedding: list[float] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    modality: str = "text"
