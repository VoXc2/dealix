"""Full Ops 2.0 — real learning loops.

Two loops turn live operational signal into actionable libraries:

  (a) ``reply_objection_loop`` — aggregates classified replies into a
      deduplicated objection library with counts.
  (b) ``ticket_kb_loop`` — aggregates recurring support-ticket
      categories into KB-gap article candidates.

Both are pure-function cores. They read from the existing classifier
output / ticket store and never auto-apply anything — the output is a
suggestion set for human review.
"""
from auto_client_acquisition.learning_loops.reply_objection_loop import (
    ObjectionLibraryEntry,
    build_objection_library,
    load_classified_replies,
)
from auto_client_acquisition.learning_loops.ticket_kb_loop import (
    KBArticleCandidate,
    build_kb_candidates,
    load_ticket_categories,
)

__all__ = [
    "KBArticleCandidate",
    "ObjectionLibraryEntry",
    "build_kb_candidates",
    "build_objection_library",
    "load_classified_replies",
    "load_ticket_categories",
]
