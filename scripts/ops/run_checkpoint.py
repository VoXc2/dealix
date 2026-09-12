#!/usr/bin/env python3
"""GitHub run checkpoint — durable RUN_ID receipt + manifest for a master run.

Writes docs/company-os/runs/<RUN_ID>/{RECEIPT.md,MANIFEST.json} and refreshes
docs/company-os/LATEST_AUTONOMOUS_RECEIPT.md. Never writes secrets: everything
comes from explicit arguments plus live git identity.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "docs" / "company-os"

SECRET_RE = re.compile(r"sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----")


def _run(cmd: list[str], timeout: int = 20) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False).stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""


def git_identity(repo_root: Path = REPO_ROOT) -> dict[str, str]:
    return {
        "end_head": _run(["git", "-C", str(repo_root), "rev-parse", "HEAD"]).strip() or "UNKNOWN",
        "branch": _run(["git", "-C", str(repo_root), "branch", "--show-current"]).strip() or "UNKNOWN",
        "origin_main": _run(["git", "-C", str(repo_root), "rev-parse", "origin/main"]).strip() or "UNKNOWN",
    }


def build_manifest(
    run_id: str,
    objective: str,
    base: str,
    pr: str,
    tests: str,
    go_usage: str,
    l5_required: list[str],
    next_action: str,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    identity = git_identity(repo_root)
    return {
        "schema": "dealix_run_checkpoint_v1",
        "run_id": run_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "objective": objective or "UNKNOWN",
        "start_head": base or "UNKNOWN",
        "end_head": identity["end_head"],
        "branch": identity["branch"],
        "origin_main": identity["origin_main"],
        "pr": pr or "NONE",
        "tests": tests or "UNKNOWN",
        "go_usage_if_observable": go_usage or "UNKNOWN",
        "l5_required": l5_required,
        "next_action": next_action or "UNKNOWN",
        "truth_class": "RECEIPT",
        "secrets_included": False,
    }


def render_receipt(manifest: dict[str, Any]) -> str:
    lines = [
        f"# DEALIX RUN CHECKPOINT — {manifest['run_id']}",
        "",
        f"- Objective: {manifest['objective']}",
        f"- Branch: `{manifest['branch']}`",
        f"- Start head: `{manifest['start_head']}`",
        f"- End head: `{manifest['end_head']}`",
        f"- Origin main: `{manifest['origin_main']}`",
        f"- PR: {manifest['pr']}",
        f"- Tests: {manifest['tests']}",
        f"- Go usage (observable only): {manifest['go_usage_if_observable']}",
        f"- Secrets included: {manifest['secrets_included']}",
        "",
        "## L5 required",
        "",
    ]
    lines.extend([f"- {item}" for item in manifest["l5_required"]] or ["- NONE"])
    lines.extend(["", "## Next action", "", manifest["next_action"], ""])
    return "\n".join(lines)


def write_checkpoint(manifest: dict[str, Any], docs_root: Path = DOCS_ROOT) -> dict[str, str]:
    rendered = render_receipt(manifest)
    payload = json.dumps(manifest, indent=2, ensure_ascii=False)
    if SECRET_RE.search(rendered) or SECRET_RE.search(payload):
        raise ValueError("checkpoint refused: secret-like content detected")
    run_dir = docs_root / "runs" / manifest["run_id"]
    run_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = run_dir / "RECEIPT.md"
    manifest_path = run_dir / "MANIFEST.json"
    receipt_path.write_text(rendered, encoding="utf-8")
    manifest_path.write_text(payload, encoding="utf-8")
    latest_path = docs_root / "LATEST_AUTONOMOUS_RECEIPT.md"
    latest_path.write_text(rendered, encoding="utf-8")
    return {"receipt": str(receipt_path), "manifest": str(manifest_path), "latest": str(latest_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a durable Dealix run checkpoint (docs/company-os/runs)")
    parser.add_argument("--run-id", default=datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ"))
    parser.add_argument("--objective", default="")
    parser.add_argument("--base", default="")
    parser.add_argument("--pr", default="")
    parser.add_argument("--tests", default="")
    parser.add_argument("--go-usage", default="")
    parser.add_argument("--l5", action="append", default=[])
    parser.add_argument("--next", default="")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    manifest = build_manifest(
        args.run_id, args.objective, args.base, args.pr, args.tests, args.go_usage, args.l5, args.next
    )
    if args.json:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    else:
        print(render_receipt(manifest))
    if args.write:
        paths = write_checkpoint(manifest)
        print(f"WROTE {paths['manifest']}")
        print(f"WROTE {paths['receipt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
