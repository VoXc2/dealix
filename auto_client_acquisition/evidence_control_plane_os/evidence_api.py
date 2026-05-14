"""Evidence API — route specification as data (no HTTP server required)."""

from __future__ import annotations

EVIDENCE_API_ROUTES: tuple[tuple[str, str], ...] = (
    ("POST", "/evidence/source"),
    ("POST", "/evidence/ai-run"),
    ("POST", "/evidence/policy-check"),
    ("POST", "/evidence/review"),
    ("POST", "/evidence/approval"),
    ("POST", "/evidence/output"),
    ("POST", "/evidence/proof"),
    ("POST", "/evidence/value"),
    ("GET", "/evidence/graph/{project_id}"),
    ("GET", "/evidence/gaps/{client_id}"),
)


def evidence_route_registered(method: str, path: str) -> bool:
    return (method.upper(), path) in {(m, p) for m, p in EVIDENCE_API_ROUTES}
