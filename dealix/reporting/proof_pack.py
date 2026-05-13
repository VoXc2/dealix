"""Proof Pack — Stage-7 (Prove) before/after evidence captured per project.

حِزمة إثبات الأثر للمرحلة السابعة — قبل/بعد، ملموسة، قابلة للاستشهاد.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ProofMetric(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name_ar: str
    name_en: str
    before: float | int | str
    after: float | int | str
    unit: str = ""
    method_ar: str
    method_en: str


class ProofPack(BaseModel):
    model_config = ConfigDict(extra="forbid")
    pack_id: str = Field(default_factory=lambda: f"proof_{uuid4().hex[:12]}")
    project_id: str
    customer_codename: str
    vertical: str
    headline_ar: str
    headline_en: str
    metrics: list[ProofMetric]
    customer_quote_ar: str | None = None
    customer_quote_en: str | None = None
    artifacts_links: list[str] = Field(default_factory=list)
    captured_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def build_proof_pack(
    project_id: str,
    customer_codename: str,
    vertical: str,
    headline_ar: str,
    headline_en: str,
    metrics: list[ProofMetric],
    *,
    customer_quote_ar: str | None = None,
    customer_quote_en: str | None = None,
    artifacts_links: list[str] | None = None,
) -> ProofPack:
    return ProofPack(
        project_id=project_id,
        customer_codename=customer_codename,
        vertical=vertical,
        headline_ar=headline_ar,
        headline_en=headline_en,
        metrics=list(metrics),
        customer_quote_ar=customer_quote_ar,
        customer_quote_en=customer_quote_en,
        artifacts_links=list(artifacts_links or []),
    )
