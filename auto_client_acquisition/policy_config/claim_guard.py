"""Free-text claim scanner (reads claim_policy.yaml).

Flags marketing/customer-facing copy that makes claims requiring a cited source
or governance approval — non-negotiable 4 ("no fake / un-sourced claims"). It
does not block on its own; routers map findings to a 403 or an approval task.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.policy_config.loader import load_policy


@dataclass(frozen=True)
class ClaimFinding:
    keyword: str
    severity: str  # "blocked_without_source" | "requires_approval"


def _keywords(key: str) -> tuple[str, ...]:
    raw = load_policy("claim_policy").get(key) or ()
    return tuple(str(k).lower() for k in raw)


def scan_claim(text: str, *, has_source: bool = False) -> tuple[ClaimFinding, ...]:
    """Return findings for ``text``.

    A ``blocked_without_source`` keyword is reported unless ``has_source`` is
    True. ``requires_approval`` keywords are always reported (publishing the
    topic needs sign-off regardless of sourcing).
    """
    haystack = (text or "").lower()
    findings: list[ClaimFinding] = []
    if not has_source:
        for kw in _keywords("blocked_without_source"):
            if kw in haystack:
                findings.append(ClaimFinding(kw, "blocked_without_source"))
    for kw in _keywords("requires_approval"):
        if kw in haystack:
            findings.append(ClaimFinding(kw, "requires_approval"))
    return tuple(findings)


def claim_is_publishable(text: str, *, has_source: bool = False) -> bool:
    """True only if no ``blocked_without_source`` finding applies."""
    return not any(
        f.severity == "blocked_without_source"
        for f in scan_claim(text, has_source=has_source)
    )


__all__ = ["ClaimFinding", "claim_is_publishable", "scan_claim"]
