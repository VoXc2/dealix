"""Reporting OS — proof pack builder tests.

اختبارات بنّاء حِزَم الإثبات (Proof Pack) في Reporting OS.

Guards `dealix/reporting/proof_pack.py`: build_proof_pack composes a valid
ProofPack from sample metrics, required fields are present, and the
Pydantic v2 to_dict() serializer returns a clean JSON-ready payload.
"""
from __future__ import annotations

import pytest

pytest.importorskip("pydantic", reason="pydantic required for reporting modules")


def _sample_metrics():
    from dealix.reporting.proof_pack import ProofMetric

    return [
        ProofMetric(
            name_ar="نسبة التحويل",
            name_en="Conversion rate",
            before=2.1,
            after=4.8,
            unit="%",
            method_ar="قياس مقارن قبل/بعد على عينة 8 أسابيع.",
            method_en="Before/after measurement across an 8-week window.",
        ),
        ProofMetric(
            name_ar="عدد الفرص المؤهلة",
            name_en="Qualified opportunities",
            before=14,
            after=37,
            unit="count",
            method_ar="عدّ من CRM للقطاع المستهدف.",
            method_en="CRM count for the targeted vertical.",
        ),
    ]


def test_build_proof_pack_returns_valid_proof_pack():
    from dealix.reporting.proof_pack import ProofPack, build_proof_pack

    pack = build_proof_pack(
        project_id="prj_alpha",
        customer_codename="bank_aleph",
        vertical="bfsi",
        headline_ar="ارتفاع التحويل بنسبة 128٪",
        headline_en="Conversion lifted by 128%",
        metrics=_sample_metrics(),
        customer_quote_en="The team delivered exactly what we needed.",
        artifacts_links=["s3://proofs/alpha/before.pdf"],
    )
    assert isinstance(pack, ProofPack)
    assert pack.project_id == "prj_alpha"
    assert pack.customer_codename == "bank_aleph"
    assert pack.vertical == "bfsi"
    assert pack.headline_en.endswith("128%")
    assert len(pack.metrics) == 2
    assert pack.artifacts_links == ["s3://proofs/alpha/before.pdf"]


def test_proof_pack_required_fields_present():
    from dealix.reporting.proof_pack import build_proof_pack

    pack = build_proof_pack(
        project_id="prj_beta",
        customer_codename="retailer_beth",
        vertical="retail_ecomm",
        headline_ar="...",
        headline_en="...",
        metrics=_sample_metrics(),
    )
    # auto-generated identifiers and timestamps
    assert pack.pack_id.startswith("proof_")
    assert pack.captured_at  # ISO-8601 string
    # defaults
    assert pack.artifacts_links == []
    assert pack.customer_quote_ar is None
    assert pack.customer_quote_en is None


def test_to_dict_serializes_to_json_ready_payload():
    from dealix.reporting.proof_pack import build_proof_pack

    pack = build_proof_pack(
        project_id="prj_gamma",
        customer_codename="logistics_gimel",
        vertical="logistics",
        headline_ar="تسليم أسرع بنسبة 30٪",
        headline_en="30% faster fulfilment",
        metrics=_sample_metrics(),
    )
    payload = pack.to_dict()
    assert payload["project_id"] == "prj_gamma"
    assert payload["vertical"] == "logistics"
    assert isinstance(payload["metrics"], list) and len(payload["metrics"]) == 2
    assert payload["metrics"][0]["name_en"] == "Conversion rate"
    assert payload["pack_id"].startswith("proof_")
    assert isinstance(payload["captured_at"], str)


def test_extra_field_on_metric_is_rejected():
    """Negative path — Pydantic v2 ConfigDict(extra='forbid') must reject extras."""
    from pydantic import ValidationError

    from dealix.reporting.proof_pack import ProofMetric

    with pytest.raises(ValidationError):
        ProofMetric(
            name_ar="x",
            name_en="x",
            before=0,
            after=1,
            method_ar="m",
            method_en="m",
            not_a_real_field="boom",  # type: ignore[call-arg]
        )
