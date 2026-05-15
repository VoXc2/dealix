"""Governance facade — risk routing + doctrine non-negotiables.

``approval_for_action`` maps an action to a (risk, route) pair.
``enforce_doctrine_non_negotiables`` raises ``ValueError`` if any of the
non-negotiable lines is crossed; routers map that to HTTP 403.
"""

from __future__ import annotations

from auto_client_acquisition.governance_os.approval_matrix import Risk, approval_for_action
from auto_client_acquisition.safe_send_gateway.doctrine import (
    doctrine_violations_for_revenue_intelligence,
    enforce_doctrine_non_negotiables,
)

__all__ = [
    "Risk",
    "approval_for_action",
    "doctrine_violations_for_revenue_intelligence",
    "enforce_doctrine_non_negotiables",
]
