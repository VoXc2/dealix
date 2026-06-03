#!/usr/bin/env python3
"""Write Motion A/B/C/D pipeline briefs under data/founder_briefs/."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.motion_pipelines import (  # noqa: E402
    build_all_motions_summary,
    build_motion_pipeline_plan,
    render_motion_markdown,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

BRIEFS = ROOT / "data/founder_briefs"


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top-n", type=int, default=5)
    p.add_argument("--motion", choices=["A", "B", "C", "D"], default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    top_n = max(1, min(args.top_n, 15))
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    BRIEFS.mkdir(parents=True, exist_ok=True)

    if args.motion:
        plan = build_motion_pipeline_plan(motion=args.motion, top_n=top_n)
        md = render_motion_markdown(plan)
        out = BRIEFS / f"motion_{args.motion.lower()}_{day}.md"
        out.write_text(md, encoding="utf-8")
        print(md)
        print(f"\nMOTION_{args.motion}_PIPELINE: OK → {out.relative_to(ROOT)}")
        return 0

    summary = build_all_motions_summary(top_n=top_n)
    json_path = BRIEFS / f"motions_all_{day}.json"
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    md_lines = [f"# Motions A–D · {day}", ""]
    for m in ("A", "B", "C", "D"):
        plan = summary["motions"][m]
        out = BRIEFS / f"motion_{m.lower()}_{day}.md"
        out.write_text(render_motion_markdown(plan), encoding="utf-8")
        md_lines.append(f"## Motion {m} — {'نشط' if plan.get('motion_active') else 'مؤجّل'}")
        md_lines.append(f"- pool: {plan.get('pool_size', 0)} · targets: {len(plan.get('targets') or [])}")
        md_lines.append(f"- file: `{out.relative_to(ROOT)}`")
        md_lines.append("")
    md_path = BRIEFS / f"motions_all_{day}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(md_path.read_text(encoding="utf-8"))
    print(f"\nMOTIONS_ALL_PIPELINE: OK → {json_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
