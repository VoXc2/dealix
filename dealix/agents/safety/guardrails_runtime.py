"""
Lightweight runtime that applies `dealix/agents/safety/guardrails.yaml`
to agent input + output streams. Designed to be small enough to read
in one screen — NeMo Guardrails is the optional drop-in upgrade when
the team is ready for the heavier machinery.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Awaitable

import yaml

from core.logging import get_logger

log = get_logger(__name__)

_RAILS_PATH = Path(__file__).parent / "guardrails.yaml"


@dataclass
class RailDecision:
    rail_id: str
    action: str  # block | redact | truncate | warn | refuse | pass
    payload: str | dict[str, Any] | None = None
    reason: str = ""


def _load_rails() -> dict[str, Any]:
    if not _RAILS_PATH.is_file():
        return {}
    return yaml.safe_load(_RAILS_PATH.read_text(encoding="utf-8")) or {}


async def run_input_rails(text: str, *, max_chars_override: int | None = None) -> tuple[str, list[RailDecision]]:
    rails = _load_rails()
    decisions: list[RailDecision] = []
    out = text or ""
    for rule in rails.get("input_rails") or []:
        rid = rule.get("id", "")
        if rid == "max_input_chars":
            cap = int(max_chars_override or rule.get("max_chars", 12000))
            if len(out) > cap:
                out = out[:cap]
                decisions.append(RailDecision(rail_id=rid, action="truncate", reason="cap"))
        elif rid == "prompt_injection_check":
            from dealix.agents.safety.prompt_injection import defend

            result = await defend(out)
            if not result.safe and result.score >= float(rule.get("threshold", 0.7)):
                decisions.append(
                    RailDecision(
                        rail_id=rid,
                        action="block",
                        payload={"score": result.score, "provider": result.provider},
                        reason=result.reason,
                    )
                )
                return "", decisions
        elif rid == "pii_block_on_input":
            from core.llm.guardrails import redact_pii

            r = redact_pii(out)
            if not r.ok:
                out = r.redacted_text
                decisions.append(
                    RailDecision(
                        rail_id=rid,
                        action="redact",
                        payload={"violations": r.violations},
                    )
                )
    return out, decisions


async def run_output_rails(text: str, *, allowed_emails: list[str] | None = None) -> tuple[str, list[RailDecision]]:
    rails = _load_rails()
    decisions: list[RailDecision] = []
    out = text or ""
    for rule in rails.get("output_rails") or []:
        rid = rule.get("id", "")
        if rid == "pii_redact_on_output":
            from core.llm.guardrails import redact_pii

            r = redact_pii(out, allowed_emails=allowed_emails or [])
            out = r.redacted_text
            if not r.ok:
                decisions.append(
                    RailDecision(
                        rail_id=rid, action="redact", payload={"violations": r.violations}
                    )
                )
        elif rid == "jailbreak_followup":
            for pat in rule.get("patterns", []) or []:
                if re.search(pat, out):
                    decisions.append(
                        RailDecision(rail_id=rid, action="block", reason="jailbreak_echo")
                    )
                    return "", decisions
        elif rid == "ar_tone_check":
            for needle in rule.get("forbid_substrings", []) or []:
                if needle in out:
                    decisions.append(
                        RailDecision(rail_id=rid, action="warn", reason=f"forbidden:{needle}")
                    )
    return out, decisions
