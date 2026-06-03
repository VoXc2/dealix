"""PDPL-oriented lawful basis labels (documentation + intake helpers)."""

from __future__ import annotations

from enum import StrEnum


class LawfulBasis(StrEnum):
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGITIMATE_INTEREST = "legitimate_interest"
    PUBLIC_SOURCE = "public_source"
    OTHER = "other"


def describe_basis(basis: LawfulBasis) -> str:
    return {
        LawfulBasis.CONSENT: "Data subject consent documented.",
        LawfulBasis.CONTRACT: "Processing necessary to perform a contract.",
        LawfulBasis.LEGITIMATE_INTEREST: "Legitimate interest — document balancing test.",
        LawfulBasis.PUBLIC_SOURCE: "Derived from lawful publicly available sources only.",
        LawfulBasis.OTHER: "Other — requires legal review note.",
    }[basis]
