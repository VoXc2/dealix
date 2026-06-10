#!/usr/bin/env python3
"""Queue weekly content drafts into Approval Center (local store or HTTP)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

WEEKLY_DIR = REPO_ROOT / "var/content_drafts"


def _latest_payload() -> dict:
    files = sorted(WEEKLY_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No JSON in {WEEKLY_DIR}")
    return json.loads(files[0].read_text(encoding="utf-8"))


def _create_via_store(draft: dict) -> dict:
    from auto_client_acquisition.approval_center.approval_store import get_default_approval_store
    from auto_client_acquisition.approval_center.schemas import ApprovalRequest

    body = (draft.get("body") or "")[:4000]
    req = ApprovalRequest(
        object_type="content_draft",
        object_id=str(draft.get("id") or "linkedin_draft"),
        action_type="linkedin_post_draft",
        action_mode="approval_required",
        channel="linkedin",
        summary_ar=(draft.get("title_ar") or "مسودة LinkedIn")[:200],
        summary_en=f"LinkedIn draft: {draft.get('slug', '')}",
        risk_level="low",
        proof_impact="authority_content",
    )
    stored = get_default_approval_store().create(req)
    return {"approval_id": stored.approval_id, "channel": "linkedin", "body_preview": body[:120]}


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--use-http", action="store_true", help="POST to API instead of local store")
    args = p.parse_args()

    payload = _latest_payload()
    drafts = list(payload.get("drafts") or [])
    if not drafts:
        print("No drafts in pack", file=sys.stderr)
        return 1

    created: list[dict] = []
    for draft in drafts:
        if args.dry_run:
            created.append(
                {
                    "dry_run": True,
                    "id": draft.get("id"),
                    "title_ar": draft.get("title_ar"),
                    "channel": "linkedin",
                }
            )
            continue
        if args.use_http:
            base = (os.environ.get("DEALIX_API_BASE") or os.environ.get("DEALIX_API_URL") or "").rstrip("/")
            key = os.environ.get("DEALIX_ADMIN_API_KEY") or os.environ.get("DEALIX_API_KEY") or ""
            if not base or not key:
                print("Set DEALIX_API_BASE + DEALIX_ADMIN_API_KEY for --use-http", file=sys.stderr)
                return 1
            import urllib.request

            body_json = json.dumps(
                {
                    "object_type": "content_draft",
                    "object_id": draft.get("id"),
                    "action_type": "linkedin_post_draft",
                    "action_mode": "approval_required",
                    "channel": "linkedin",
                    "summary_ar": draft.get("title_ar") or "",
                    "summary_en": f"slug={draft.get('slug')}",
                }
            ).encode("utf-8")
            req = urllib.request.Request(  # noqa: S310
                f"{base}/api/v1/approvals/create",
                data=body_json,
                headers={
                    "Content-Type": "application/json",
                    "X-Admin-API-Key": key,
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
                created.append(json.loads(resp.read().decode("utf-8")))
        else:
            created.append(_create_via_store(draft))

    print(json.dumps({"queued": len(created), "items": created}, ensure_ascii=False, indent=2))
    if args.dry_run:
        print("DRY-RUN — no approvals created")
    else:
        print("Review: /ar/ops/approvals")
    return 0


if __name__ == "__main__":
    sys.exit(main())
