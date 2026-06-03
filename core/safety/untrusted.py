"""
Untrusted-input boundaries (prompt-injection defense).

Core doctrine:
  * Content from issues, PRs, comments, email, web, CRM notes, WhatsApp,
    PDFs, fork READMEs/AGENTS.md/CLAUDE.md, and MCP tool descriptions is
    **DATA, never instructions**.
  * An untrusted-triggered context can NEVER cause an external send.
  * Legal / complaint / privacy-deletion content requires human handoff.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .constants import UNTRUSTED_SOURCES, HUMAN_HANDOFF_CATEGORIES

# Phrases an attacker embeds to try to hijack an agent (logged, never obeyed).
_INJECTION_MARKERS = [
    r"(?i)ignore (all |the |your )?previous instructions",
    r"(?i)disregard (all |the )?(prior|above|previous)",
    r"(?i)you are now",
    r"(?i)new instructions:",
    r"(?i)system prompt",
    r"(?i)reveal (your |the )?(system )?prompt",
    r"(?i)print (your |the )?(api[\s_-]?key|secret|token|env)",
    r"(?i)exfiltrate",
    r"(?i)send (an? )?email to",
    r"(?i)curl\s+http",
    r"(?i)run the following",
    r"<!--.*?-->",  # hidden HTML comments
]


def is_trusted_source(source: Optional[str]) -> bool:
    """True only for first-party, human-authored contexts.

    Everything in ``UNTRUSTED_SOURCES`` (and anything unknown) is untrusted.
    """
    if not source:
        return False
    if source in UNTRUSTED_SOURCES:
        return False
    trusted = {"founder", "founder_direct", "internal_repo_main", "approved_config"}
    return source in trusted


def can_trigger_external_send(context: Dict) -> bool:
    """Can this trigger context cause an external send? Almost never.

    Returns True only if ALL of:
      * the trigger source is trusted (first-party),
      * a human approval is recorded,
      * send is explicitly enabled,
      * not a dry run.
    Any untrusted source -> always False.
    """
    source = context.get("source") or context.get("trigger")
    if not is_trusted_source(source):
        return False
    return bool(
        context.get("human_approved")
        and context.get("send_enabled")
        and not context.get("dry_run", True)
    )


def detect_injection(text: Optional[str]) -> List[str]:
    """Return injection markers found in untrusted text (for logging only)."""
    if not text:
        return []
    hits: List[str] = []
    for pat in _INJECTION_MARKERS:
        m = re.search(pat, text, re.DOTALL)
        if m:
            hits.append(pat)
    return hits


@dataclass
class UntrustedContent:
    """Wrapper that marks external content as data, never instructions."""

    source: str
    raw: str
    injection_markers: List[str] = field(default_factory=list)

    @property
    def trusted(self) -> bool:
        return is_trusted_source(self.source)

    def as_data(self) -> Dict:
        return {"source": self.source, "trusted": self.trusted, "content": self.raw}


def treat_as_data_only(source: str, raw: str) -> UntrustedContent:
    """Wrap external content so callers handle it as inert data.

    Detected injection attempts are recorded but explicitly NOT executed.
    """
    return UntrustedContent(source=source, raw=raw, injection_markers=detect_injection(raw))


def requires_human_handoff(category: Optional[str]) -> bool:
    """True for legal / complaint / privacy-deletion / regulatory categories."""
    if not category:
        return False
    return category in HUMAN_HANDOFF_CATEGORIES
