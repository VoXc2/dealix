"""
Compliance — Saudi-first safety primitives.

Modules:
    forbidden_claims: scan and assert text doesn't contain banned marketing
        claims (e.g., "نضمن", "guaranteed", "cold whatsapp"). Used at draft
        generation time + by the existing landing audit.
"""

from auto_client_acquisition.compliance.forbidden_claims import (
    ForbiddenClaimError,
    ForbiddenMatch,
    assert_safe,
    scan,
)

__all__ = ["ForbiddenClaimError", "ForbiddenMatch", "assert_safe", "scan"]
