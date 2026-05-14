"""Doctrine: retainer eligibility requires a proof pack with score >= 80."""
from __future__ import annotations

import pytest

from auto_client_acquisition.adoption_os.retainer_readiness import (
    evaluate as evaluate_retainer_readiness,
)


def test_retainer_readiness_blocks_without_proof() -> None:
    """proof_score=0 means there is effectively no proof pack: not eligible."""
    out = evaluate_retainer_readiness(
        customer_id="acme",
        adoption_score=85.0,
        proof_score=0.0,
        workflow_owner_present=True,
        governance_risk_controlled=True,
    )
    assert out.eligible is False
    assert any("proof" in g.lower() for g in out.gaps)


def test_retainer_readiness_blocks_below_threshold() -> None:
    """proof_score=70 is below the 80 threshold: not eligible."""
    out = evaluate_retainer_readiness(
        customer_id="acme",
        adoption_score=85.0,
        proof_score=70.0,
        workflow_owner_present=True,
        governance_risk_controlled=True,
    )
    assert out.eligible is False
    assert any("proof" in g.lower() for g in out.gaps)


def test_retainer_readiness_eligible_at_80() -> None:
    """proof_score=80 is exactly on the threshold and should be eligible."""
    out = evaluate_retainer_readiness(
        customer_id="acme",
        adoption_score=70.0,
        proof_score=80.0,
        workflow_owner_present=True,
        governance_risk_controlled=True,
    )
    assert out.eligible is True
    assert out.gaps == []
