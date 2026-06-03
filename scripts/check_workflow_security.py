#!/usr/bin/env python3
"""
Workflow security guard.

Fails CI if any GitHub Actions workflow:
  * uses the dangerous ``pull_request_target`` trigger, or
  * combines a writable ``permissions:`` block with ``secrets.`` usage, or
  * references ``${{ secrets.* }}`` while triggered by untrusted events
    (pull_request / issue_comment / issues), or
  * grants repo-wide ``permissions: write-all``.

This enforces the least-privilege policy in
``docs/security/GITHUB_ACTIONS_SECURITY_POLICY.md`` and threat T10.

Usage:  python3 scripts/check_workflow_security.py
Exit:   0 if clean, 1 if a violation is found.
"""

from __future__ import annotations

import glob
import os
import re
import sys

WF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".github", "workflows")

UNTRUSTED_TRIGGERS = ["pull_request_target", "issue_comment", "issues", "pull_request"]
WRITE_PERM = re.compile(r":\s*write\b")
SECRET_REF = re.compile(r"\$\{\{\s*secrets\.", re.IGNORECASE)


def check_file(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    name = os.path.basename(path)
    problems: list[str] = []

    if "pull_request_target" in text:
        problems.append(f"{name}: uses pull_request_target (forbidden)")

    if re.search(r"permissions:\s*write-all", text):
        problems.append(f"{name}: permissions: write-all (forbidden)")

    has_secrets = bool(SECRET_REF.search(text))
    if has_secrets:
        # Secrets must not appear on untrusted triggers.
        on_block = text.split("jobs:", 1)[0]
        for trig in UNTRUSTED_TRIGGERS:
            if re.search(rf"^\s*{trig}\s*:", on_block, re.MULTILINE) or re.search(rf"\b{trig}\b", on_block):
                problems.append(f"{name}: references secrets on untrusted trigger '{trig}'")
                break
        if WRITE_PERM.search(text):
            problems.append(f"{name}: combines write permissions with secrets")

    return problems


def main() -> int:
    files = sorted(glob.glob(os.path.join(WF_DIR, "*.yml")) + glob.glob(os.path.join(WF_DIR, "*.yaml")))
    if not files:
        print("No workflows found (nothing to check).")
        return 0
    all_problems: list[str] = []
    for path in files:
        all_problems.extend(check_file(path))
    if all_problems:
        print("WORKFLOW SECURITY VIOLATIONS:")
        for p in all_problems:
            print("  - " + p)
        return 1
    print(f"OK: {len(files)} workflow(s) pass least-privilege checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
