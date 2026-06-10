"""Standardization path steps (method → category language)."""

from __future__ import annotations

from enum import IntEnum


class StandardizationStep(IntEnum):
    INTERNAL_METHOD = 1
    CLIENT_FACING_METHOD = 2
    PUBLIC_STANDARD = 3
    ACADEMY = 4
    PARTNER_CERTIFICATION = 5
    BENCHMARK_REPORTS = 6
    CATEGORY_LANGUAGE = 7


def max_standardization_step_reached(
    *,
    internal_method_live: bool = False,
    client_facing_method_live: bool = False,
    public_standard_published: bool = False,
    academy_live: bool = False,
    partner_cert_live: bool = False,
    benchmark_reports_live: bool = False,
    category_language_signal: bool = False,
) -> StandardizationStep:
    """Return the highest consecutive step satisfied (sequential gate)."""
    if not internal_method_live:
        return StandardizationStep.INTERNAL_METHOD
    if not client_facing_method_live:
        return StandardizationStep.CLIENT_FACING_METHOD
    if not public_standard_published:
        return StandardizationStep.PUBLIC_STANDARD
    if not academy_live:
        return StandardizationStep.ACADEMY
    if not partner_cert_live:
        return StandardizationStep.PARTNER_CERTIFICATION
    if not benchmark_reports_live:
        return StandardizationStep.BENCHMARK_REPORTS
    if not category_language_signal:
        return StandardizationStep.BENCHMARK_REPORTS
    return StandardizationStep.CATEGORY_LANGUAGE
