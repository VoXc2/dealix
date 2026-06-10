"""Vertical Playbooks v5 — 5 sector-specific catalogs.

Each playbook is a STATIC, hand-curated record of:
  - ICP for the sector
  - common pains
  - the best Dealix offer to lead with
  - the first 3 Diagnostic questions
  - safe channels (and forbidden ones)
  - message patterns
  - the proof metric that matters most
  - blocked actions specific to the sector

Verticals: agency · b2b_services · saas · training_consulting · local_services.

Pure data — no LLM call, no DB. The router just exposes the catalog.
"""
from auto_client_acquisition.vertical_playbooks.catalog import (
    PLAYBOOKS,
    Vertical,
    get_playbook,
    list_playbooks,
    recommend_for,
    summary,
)

__all__ = [
    "PLAYBOOKS",
    "Vertical",
    "get_playbook",
    "list_playbooks",
    "recommend_for",
    "summary",
]
