"""Pydantic request schemas for the Ops Console domain.

نماذج طلبات غرفة التشغيل.

Responses are returned as plain dicts (built via `_common.governed`) so that
graceful-degradation payloads (`{"note": "...unavailable"}`) always serialize.
Only request bodies need strict validation.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProofPackPreviewRequest(BaseModel):
    """Input for POST /api/v1/ops/proof-pack/preview.

    The caller composes the diagnostic input — no scraping, no autonomous
    data collection. Mirrors `diagnostic_engine.schemas.DiagnosticRequest`.
    """

    model_config = ConfigDict(extra="forbid")

    company: str = Field(min_length=1, max_length=200)
    sector: str = "b2b_services"
    region: str = "ksa"
    pipeline_state: str = Field(default="", max_length=2000)
