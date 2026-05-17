"""Customer-facing chat — strictly source-grounded.

The chat responder answers ONLY from approved Knowledge Base articles.
Any question the KB cannot answer is escalated into a support ticket —
the widget never improvises an answer.
"""

from __future__ import annotations

from auto_client_acquisition.chat.responder import respond

__all__ = ["respond"]
