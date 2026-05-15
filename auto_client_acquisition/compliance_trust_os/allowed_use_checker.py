"""Allowed-use checks against Source Passport declarations."""

from __future__ import annotations


def allowed_use_permits_ai(*, allowed_use: tuple[str, ...]) -> bool:
    """No allowed_use entries → treat as no declared permission for AI consumption."""
    return bool(allowed_use)


def allowed_use_internal_analysis_only(*, allowed_use: tuple[str, ...]) -> bool:
    return allowed_use == ("internal_analysis",)
