"""Case Study Engine — turns approved + consented proof events into
publishable case studies.

Hard rules (Article 8):
- proof events with evidence_level=observed cannot be published
- consent_for_publication MUST be True (signed via consent_signature)
- approval_status MUST be approved
- pii_redacted MUST be True
- forbidden-token scrub on every narrative before return

Persistence: JSONL library at data/case_studies/library.jsonl.
"""
from auto_client_acquisition.case_study_engine.builder import (
    approve_candidate,
    build_candidate,
    list_library,
    request_quote,
    select_publishable,
)

__all__ = [
    "approve_candidate",
    "build_candidate",
    "list_library",
    "request_quote",
    "select_publishable",
]
