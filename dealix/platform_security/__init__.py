"""Dealix platform-security readiness package (Omega V3).

Source-level readiness gates only. No services, no auth-plane changes.
"""

from dealix.platform_security.readiness import evaluate, receipt_is_closed

__all__ = ["evaluate", "receipt_is_closed"]
