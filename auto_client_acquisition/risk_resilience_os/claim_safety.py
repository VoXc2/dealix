"""Claim risk — evidence classes and client-facing gates."""

from __future__ import annotations

CLAIM_CLASSES: tuple[str, ...] = ("estimated", "observed", "verified")


def claim_class_valid(claim_class: str) -> bool:
    return claim_class in CLAIM_CLASSES


def claim_may_appear_in_case_study(claim_class: str, *, client_permission: bool) -> bool:
    return claim_class == "verified" and client_permission
