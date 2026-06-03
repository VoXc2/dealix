#!/usr/bin/env python3
"""Generate Business NOW markdown snapshot and refresh auto section in DEALIX_BUSINESS_NOW_AR.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from dealix.business_now.snapshot_builder import (  # noqa: E402
    build_business_now_snapshot,
    render_snapshot_markdown,
)

_DOC = _REPO / "docs" / "business" / "DEALIX_BUSINESS_NOW_AR.md"
_EVIDENCE = _REPO / "docs" / "business" / "evidence" / "business_now_latest.md"
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
    snapshot = build_business_now_snapshot(
        run_verify=True,
        run_enterprise_cp=True,
        persist_cache=True,
    )
    md = render_snapshot_markdown(snapshot)
    _EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    _EVIDENCE.write_text(md, encoding="utf-8")
    _patch_doc(md)
    print(f"DEALIX_BUSINESS_NOW: generated {snapshot['generated_at'][:10]}")
    print(f"Evidence: {_EVIDENCE}")
    plat = snapshot["pillars"]["platform"]
    print(f"Transformation: {plat['transformation_verdict']}")
    print(f"Enterprise CP: {plat.get('enterprise_control_plane_verdict')}")
    print(f"Commercial KPI pending: {snapshot['pillars']['commercial']['commercial_kpi_pending']}")
    for a in snapshot.get("today_actions") or [][:5]:
        action = a["action_ar"].encode("ascii", errors="replace").decode("ascii")
        print(f"  P{a['priority']}: {action}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
