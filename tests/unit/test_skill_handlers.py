"""Pure unit tests for dealix/agents/skills/handlers.py (no router)."""

from __future__ import annotations

import asyncio

import pytest

from dealix.agents.skills.handlers import get_handler, registered_ids


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro) if asyncio.get_event_loop().is_running() else asyncio.run(coro)


def test_four_handlers_registered() -> None:
    assert set(registered_ids()) >= {
        "sales_qualifier",
        "lead_scorer",
        "content_generator_ar",
        "ar_en_translator",
    }


def test_sales_qualifier_zero_when_nothing_filled() -> None:
    handler = get_handler("sales_qualifier")
    assert handler is not None
    result = asyncio.run(handler({}))
    assert result["score"] == 0.0
    assert result["recommended_action"] == "disqualify"


def test_sales_qualifier_full_bant_plus_pdpl() -> None:
    handler = get_handler("sales_qualifier")
    assert handler is not None
    result = asyncio.run(handler({
        "lead_snapshot": {"budget": "y", "authority": "y", "need": "y", "timeline": "y"},
        "compliance_signals": {"has_pdpl_consent": True, "dnc_listed": False},
        "locale": "en",
    }))
    assert result["score"] == 1.0
    assert result["gates"]["pdpl"] is True


def test_sales_qualifier_dnc_listed_caps_score() -> None:
    handler = get_handler("sales_qualifier")
    result = asyncio.run(handler({
        "lead_snapshot": {"budget": "y", "authority": "y", "need": "y", "timeline": "y"},
        "compliance_signals": {"has_pdpl_consent": True, "dnc_listed": True},
    }))
    assert result["score"] <= 0.30
    assert result["gates"]["pdpl"] is False


def test_lead_scorer_weights_sum_returned() -> None:
    handler = get_handler("lead_scorer")
    result = asyncio.run(handler({
        "lead": {"industry": "real-estate", "company_size": "enterprise", "role": "CTO",
                 "signals": {"urgency": 0.9, "intent": 0.85}},
    }))
    w = result["weights_applied"]
    assert pytest.approx(w["fit"] + w["urgency"] + w["intent"] + w["sector"], rel=1e-6) == 1.0
    assert 0 < result["score"] <= 1.0


def test_lead_scorer_unknown_industry_gets_low_sector_boost() -> None:
    handler = get_handler("lead_scorer")
    result = asyncio.run(handler({
        "lead": {"industry": "rumple-stiltskin", "company_size": "small", "role": "intern",
                 "signals": {"urgency": 0.1, "intent": 0.1}},
    }))
    assert result["components"]["sector"] == 0.6


def test_content_generator_ar_short_has_no_zatca_paragraph() -> None:
    handler = get_handler("content_generator_ar")
    result = asyncio.run(handler({"length": "short"}))
    assert "ZATCA" not in result["copy"]
    assert result["length"] == "short"


def test_content_generator_ar_long_mentions_pdpl_and_zatca() -> None:
    handler = get_handler("content_generator_ar")
    result = asyncio.run(handler({"length": "long"}))
    assert "PDPL" in result["copy"]
    assert "ZATCA" in result["copy"]


def test_ar_en_translator_arabic_to_english() -> None:
    handler = get_handler("ar_en_translator")
    result = asyncio.run(handler({"text": "احتاج عرض سعر", "from": "ar", "to": "en"}))
    assert "quotation" in result["translated"]
    assert result["glossary_hits"] == ["عرض سعر"]


def test_ar_en_translator_english_to_arabic() -> None:
    handler = get_handler("ar_en_translator")
    result = asyncio.run(handler({"text": "send me an invoice", "from": "en", "to": "ar"}))
    assert "فاتورة" in result["translated"]


def test_ar_en_translator_auto_detects_arabic() -> None:
    handler = get_handler("ar_en_translator")
    result = asyncio.run(handler({"text": "مرحباً", "from": "auto", "to": "en"}))
    assert result["from"] == "ar"


def test_ar_en_translator_same_lang_is_identity() -> None:
    handler = get_handler("ar_en_translator")
    result = asyncio.run(handler({"text": "hello", "from": "en", "to": "en"}))
    assert result["translated"] == "hello"
    assert result["glossary_hits"] == []
