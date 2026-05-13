"""Data OS — PII detection tests (email, Saudi mobile, IBAN, card, mask).

اختبارات كاشف البيانات الشخصية في Data OS.

These tests guard `auto_client_acquisition/customer_data_plane/pii_detection.py`:
detection of common PII kinds, masking format, and the clean-record happy path.
"""
from __future__ import annotations

import pytest

pytest.importorskip("pydantic", reason="pydantic required for Data OS modules")


def test_email_is_detected():
    from auto_client_acquisition.customer_data_plane.pii_detection import scan_record

    res = scan_record({"contact": "ali@example.sa"})
    assert res.has_pii is True
    kinds = {h.kind for h in res.hits}
    assert "email" in kinds


def test_saudi_mobile_is_detected():
    from auto_client_acquisition.customer_data_plane.pii_detection import scan_record

    res = scan_record({"phone": "+966551234567"})
    assert res.has_pii is True
    kinds = {h.kind for h in res.hits}
    assert "phone_sa" in kinds


def test_iban_is_detected():
    from auto_client_acquisition.customer_data_plane.pii_detection import scan_record

    res = scan_record({"bank": "SA0380000000608010167519"})
    assert res.has_pii is True
    kinds = {h.kind for h in res.hits}
    assert "iban" in kinds


def test_card_number_is_detected():
    from auto_client_acquisition.customer_data_plane.pii_detection import scan_record

    res = scan_record({"payment": "4111 1111 1111 1111"})
    assert res.has_pii is True
    kinds = {h.kind for h in res.hits}
    assert "card" in kinds


def test_mask_keeps_first_two_and_last_two_chars():
    from auto_client_acquisition.customer_data_plane.pii_detection import mask

    masked = mask("ali@example.sa")
    assert masked.startswith("al")
    assert masked.endswith("sa")
    assert "*" in masked
    assert len(masked) == len("ali@example.sa")


def test_mask_short_value_is_fully_masked():
    from auto_client_acquisition.customer_data_plane.pii_detection import mask

    assert mask("abcd") == "****"
    assert mask("") == ""


def test_clean_record_produces_empty_hit_list():
    """Negative path — a record with no PII must yield has_pii=False."""
    from auto_client_acquisition.customer_data_plane.pii_detection import scan_record

    res = scan_record({"company_name": "Acme Trading Co", "vertical": "retail"})
    assert res.has_pii is False
    assert res.hits == []


def test_scan_serializes_via_to_dict():
    from auto_client_acquisition.customer_data_plane.pii_detection import scan_record

    res = scan_record({"contact": "ali@example.sa"})
    payload = res.to_dict()
    assert payload["has_pii"] is True
    assert isinstance(payload["hits"], list)
    assert payload["hits"][0]["field"] == "contact"
