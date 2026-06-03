#!/usr/bin/env python3
"""Generate commercial strategy evidence and patch DEALIX_COMMERCIAL_STRATEGY_AR.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from dealix.business_now.commercial_strategy import (  # noqa: E402
    build_commercial_strategy_snapshot,
    render_commercial_strategy_markdown,
)

_DOC = _REPO / "docs" / "business" / "DEALIX_COMMERCIAL_STRATEGY_AR.md"
_EVIDENCE = _REPO / "docs" / "business" / "evidence" / "commercial_strategy_latest.md"
_START = "<!-- AUTO_GENERATED_START -->"
_END = "<!-- AUTO_GENERATED_END -->"


def _patch_doc(body_md: str) -> None:
    text = _DOC.read_text(encoding="utf-8")
    block = f"{_START}\n{body_md}\n{_END}"
    if _START in text and _END in text:
        text = re.sub(
            re.escape(_START) + r".*?" + re.escape(_END),
            block,
            text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    _DOC.write_text(text, encoding="utf-8")


def main() -> int:
    snapshot = build_commercial_strategy_snapshot()
    md = render_commercial_strategy_markdown(snapshot)
    _EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    _EVIDENCE.write_text(md, encoding="utf-8")
    _patch_doc(md)
    focus = snapshot.get("focus") or {}
    print(f"DEALIX_COMMERCIAL_STRATEGY: generated {snapshot['generated_at'][:10]}")
    print(f"Focus stage: {focus.get('stage')}")
    print(f"Evidence: {_EVIDENCE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
