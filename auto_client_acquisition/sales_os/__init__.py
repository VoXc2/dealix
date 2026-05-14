"""Canonical Sales OS — qualification + bad-revenue filter + proposal
generation.

Phase 1 of the 90-day commercial activation: qualification scorer that
runs on every diagnostic intake and returns Accept / Diagnostic-only /
Reframe / Reject / Refer-out.
"""
from auto_client_acquisition.sales_os.qualification import (
    Decision,
    QualificationResult,
    qualify,
)

__all__ = ["Decision", "QualificationResult", "qualify"]
