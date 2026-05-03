"""
Delivery — Phase 2: 7-Day Growth Proof Sprint engine.

Pure deterministic generators. No LLM calls; no I/O. The router calls
these with the customer's Company Brain + intake answers, gets the
day's output dict, persists it to SprintRecord.day_outputs_json, and
emits the matching Proof Event.
"""

from auto_client_acquisition.delivery.sprint_templates import (
    generate_close_out,
    generate_diagnostic,
    generate_meeting_prep,
    generate_message_pack,
    generate_opportunity_pack,
    generate_pipeline_review,
    generate_proof_draft,
)

__all__ = [
    "generate_close_out",
    "generate_diagnostic",
    "generate_meeting_prep",
    "generate_message_pack",
    "generate_opportunity_pack",
    "generate_pipeline_review",
    "generate_proof_draft",
]
