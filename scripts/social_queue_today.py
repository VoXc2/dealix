#!/usr/bin/env python3
"""Print today's social post draft + SOAEN checklist (no auto-publish)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.social_queue import (  # noqa: E402
    format_linkedin_draft,
    get_post_for_date,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--format", choices=("md", "json"), default="md")
    args = p.parse_args()

    post = get_post_for_date()
    if not post:
        print("NO_POST: social_content_queue.yaml empty or missing", file=sys.stderr)
        return 1

    if args.format == "json":
        post["linkedin_draft"] = format_linkedin_draft(post)
        print(json.dumps(post, ensure_ascii=False, indent=2))
        return 0

    print(f"# منشور اليوم · {post.get('calendar_date')}\n")
    print(f"**{post.get('title_ar', '')}** · `{post.get('pillar')}` · status={post.get('status')}\n")
    print(format_linkedin_draft(post))
    print("\n## SOAEN\n")
    for chk in post.get("soaen_checklist_ar") or []:
        print(f"- [ ] {chk}")
    print(f"\nCTA: {post.get('cta_ar') or post.get('cta')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
