"""Proof economy rules — proof as internal currency."""

from __future__ import annotations


def can_make_public_claim(*, has_substantiating_proof: bool) -> bool:
    return has_substantiating_proof


def can_publish_case_study(*, has_proof_pack: bool, client_authorized: bool) -> bool:
    return has_proof_pack and client_authorized


def can_push_retainer(*, proof_strength_score: float, minimum: float = 80.0) -> bool:
    return proof_strength_score >= minimum
