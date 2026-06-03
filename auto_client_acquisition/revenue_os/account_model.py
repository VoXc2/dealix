"""Typed account row shape for Revenue Intelligence (import-safe, no I/O)."""

from __future__ import annotations

from typing import NotRequired, TypedDict


class AccountRow(TypedDict, total=False):
    """Minimum fields used by scoring + dedupe hints."""

    company_name: str
    sector: str
    city: str
    source: str
    domain: NotRequired[str]
    phone: NotRequired[str]
    email: NotRequired[str]


__all__ = ["AccountRow"]
