"""Unit tests for dealix/gcc/currency.py."""

from __future__ import annotations

from decimal import Decimal

import pytest

from dealix.gcc.currency import (
    GCC_CURRENCIES,
    format_amount,
    from_minor,
    is_weekend,
    to_minor,
)


def test_all_six_currencies_present() -> None:
    assert set(GCC_CURRENCIES) == {"SAR", "AED", "QAR", "KWD", "BHD", "OMR"}


@pytest.mark.parametrize(
    "amount,ccy,expected_minor",
    [
        (12.50, "SAR", 1250),
        (12.50, "AED", 1250),
        (1.500, "KWD", 1500),
        (1.500, "BHD", 1500),
        (0.001, "OMR", 1),
    ],
)
def test_to_minor_handles_2_and_3_decimal_currencies(
    amount: float, ccy: str, expected_minor: int
) -> None:
    assert to_minor(amount, ccy) == expected_minor


def test_from_minor_is_inverse_of_to_minor() -> None:
    for ccy in GCC_CURRENCIES:
        original = Decimal("12.500") if GCC_CURRENCIES[ccy].decimals == 3 else Decimal("12.50")
        assert from_minor(to_minor(original, ccy), ccy) == original


def test_format_amount_ar_uses_local_symbol() -> None:
    out_ar = format_amount(1250, "SAR", locale="ar")
    out_en = format_amount(1250, "SAR", locale="en")
    assert "ر.س" in out_ar
    assert "SAR" in out_en


def test_to_minor_rejects_unknown_currency() -> None:
    with pytest.raises(ValueError, match="unknown_gcc_currency"):
        to_minor(1.0, "XYZ")


def test_is_weekend_sa_friday() -> None:
    # 0=Mon ... 4=Fri, 5=Sat
    assert is_weekend("SA", 4) is True
    assert is_weekend("SA", 5) is True
    assert is_weekend("SA", 6) is False  # Sunday is work day in KSA
    assert is_weekend("SA", 0) is False  # Monday


def test_is_weekend_ae_saturday_sunday() -> None:
    assert is_weekend("AE", 5) is True
    assert is_weekend("AE", 6) is True
    assert is_weekend("AE", 4) is False


def test_is_weekend_unknown_country_returns_false() -> None:
    assert is_weekend("XX", 0) is False
