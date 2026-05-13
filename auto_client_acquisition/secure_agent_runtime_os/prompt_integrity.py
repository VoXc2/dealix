"""Prompt Integrity — trusted instruction vs untrusted data envelopes."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PromptTrust(str, Enum):
    TRUSTED_INSTRUCTION = "trusted_instruction"
    UNTRUSTED_DATA = "untrusted_data"


@dataclass(frozen=True)
class PromptEnvelope:
    type: PromptTrust
    source: str
    content: str

    def can_override_policy(self) -> bool:
        """Doctrine: untrusted data may inform outputs but never overrides policy."""

        return False  # always — even trusted instructions go through the policy engine
