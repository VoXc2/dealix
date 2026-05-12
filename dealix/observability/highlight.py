"""
Highlight.io — session replay + frontend error tracking.

Server-side: we attach the Highlight project ID + an opt-in cookie
check so PII-bearing flows never get replayed unless the user
consented (PDPL-compliant by default).

The browser-side script lives in the Next.js frontend and reads the
project ID from `NEXT_PUBLIC_HIGHLIGHT_PROJECT_ID`.
"""

from __future__ import annotations

import os


def is_configured() -> bool:
    return bool(os.getenv("HIGHLIGHT_PROJECT_ID", "").strip())


def consent_required_paths() -> set[str]:
    """Paths where session replay must be off unless analytics consent given."""
    return {
        "/api/v1/auth/login",
        "/api/v1/auth/sso/callback",
        "/api/v1/billing/checkout/stripe",
        "/api/v1/pdpl/dsr/portability",
    }
