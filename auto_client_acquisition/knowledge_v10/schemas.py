"""Pydantic v2 schemas for knowledge_v10 — RAG contract.

Inspired by Qdrant + Haystack patterns. Pure contract layer: no LLM,
no external HTTP, no scraping. The Qdrant adapter ships in §S6.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SourceType(StrEnum):
    CUSTOMER_PROVIDED_URL = "customer_provided_url"
    CUSTOMER_UPLOADED_FILE = "customer_uploaded_file"
    OFFICIAL_PUBLIC_SITE = "official_public_site"
    SEARCH_API_RESULT = "search_api_result"
    CRM_RECORD = "crm_record"
    INTERNAL_DOC = "internal_doc"
    MANUALLY_ENTERED_NOTE = "manually_entered_note"
    BLOCKED_SCRAPING_SOURCE = "blocked_scraping_source"
    BLOCKED_PERSONAL_DATA_SOURCE = "blocked_personal_data_source"


class DocumentManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    id: str = Field(..., min_length=1)
    customer_handle: str = ""
    source_type: SourceType
    title: str = ""
    language: Literal["ar", "en", "mixed"] = "ar"
    chunk_count: int = Field(default=0, ge=0)
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    evidence_id: str = ""


class RetrievalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    query: str = Field(..., min_length=3)
    customer_handle: str = ""
    language: Literal["ar", "en", "both"] = "both"
    top_k: int = Field(default=5, ge=1, le=50)
    allowed_sources: list[SourceType] = Field(default_factory=list)


class RetrievalResult(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    chunk_id: str
    document_id: str
    snippet_redacted: str = ""
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    source_type: SourceType


class AnswerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    query: str = Field(..., min_length=3)
    retrieved_chunks: list[RetrievalResult] = Field(default_factory=list)
    language: Literal["ar", "en", "both"] = "both"


class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    answer_ar: str = ""
    answer_en: str = ""
    citations: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    insufficient_evidence: bool = True


class RAGEvalResult(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    faithfulness_score: float = Field(default=0.0, ge=0.0, le=1.0)
    context_relevance: float = Field(default=0.0, ge=0.0, le=1.0)
    answer_relevance: float = Field(default=0.0, ge=0.0, le=1.0)
    hallucination_detected: bool = False
    notes: str = ""
