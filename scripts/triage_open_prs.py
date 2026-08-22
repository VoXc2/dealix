#!/usr/bin/env python3
"""Triage open pull requests into actionable buckets and portfolio signals.

Reads the open PR list via the ``gh`` CLI, sorts each PR into exactly one bucket
per ``docs/agents/PR_TRIAGE_POLICY.md``, and writes a read-only triage report.
Humans decide what to merge, rebase, supersede, or close; this tool never
mutates GitHub state.

Outputs:
  - reports/pr_triage/OPEN_PR_TRIAGE.md
  - reports/pr_triage/open_pr_triage.json
  - stdout line: ``DEALIX_PR_TRIAGE=PASS|SKIPPED``

Always exits 0 -- triage is informational and must never break a build.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "pr_triage"

BUCKET_ORDER = ("draft", "security", "dependencies", "agent", "docs", "needs_review")
PER_BUCKET_LIMIT = 50
STALE_AFTER_DAYS = 30
_CONVENTIONAL_PREFIX = re.compile(
    r"^(?:draft[\s:\-]+|(?:feat|fix|docs|test|chore|refactor|perf|ci|build|security)"
    r"(?:\([^)]*\))?[!\s:\-]+)",
    re.IGNORECASE,
)


def _labels(pr: dict) -> str:
    return " ".join(label.get("name", "").lower() for label in pr.get("labels", []))


def classify(pr: dict) -> str:
    title = (pr.get("title") or "").lower()
    labels = _labels(pr)
    author = (pr.get("author") or {}).get("login", "").lower()

    if pr.get("isDraft"):
        return "draft"
    if any(word in title or word in labels for word in ("security", "auth", "secret", "vuln")):
        return "security"
    if "dependabot" in author or "deps" in labels or any(
        word in title for word in ("bump ", "dependabot", "dependency", "upgrade ")
    ):
        return "dependencies"
    if any(word in title for word in ("claude", "codex", "agent")):
        return "agent"
    if "docs" in labels or title.startswith("docs") or "documentation" in title:
        return "docs"
    return "needs_review"


def normalize_title(title: str) -> str:
    """Normalize title for evidence-only duplicate-intent review."""
    value = (title or "").strip().lower()
    previous = None
    while value and value != previous:
        previous = value
        value = _CONVENTIONAL_PREFIX.sub("", value, count=1).strip()
    value = re.sub(r"#\d+", " ", value)
    value = re.sub(r"[^\w]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def age_days(pr: dict, *, now: datetime | None = None) -> int | None:
    updated = _parse_timestamp(pr.get("updatedAt"))
    if updated is None:
        return None
    current = (now or datetime.now(UTC)).astimezone(UTC)
    return max(0, (current - updated).days)


def duplicate_title_groups(prs: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for pr in prs:
        key = normalize_title(pr.get("title", ""))
        if key:
            groups.setdefault(key, []).append(pr)
    return {
        key: sorted(items, key=lambda item: item.get("number", 0))
        for key, items in sorted(groups.items())
        if len(items) > 1
    }


def risk_flags(
    pr: dict,
    *,
    duplicate_keys: set[str],
    now: datetime | None = None,
) -> list[str]:
    flags: list[str] = []
    age = age_days(pr, now=now)
    if age is not None and age >= STALE_AFTER_DAYS:
        flags.append(f"stale_{age}d")
    if (pr.get("mergeStateStatus") or "").upper() == "DIRTY":
        flags.append("merge_conflict")
    key = normalize_title(pr.get("title", ""))
    if key in duplicate_keys:
        flags.append("duplicate_title")
    base = pr.get("baseRefName")
    if base and base != "main":
        flags.append(f"stacked_on:{base}")
    return flags


def fetch_prs() -> list[dict] | None:
    if shutil.which("gh") is None:
        return None
    try:
        raw = subprocess.check_output(
            [
                "gh",
                "pr",
                "list",
                "--state",
                "open",
                "--limit",
                "500",
                "--json",
                (
                    "number,title,author,createdAt,updatedAt,labels,isDraft,"
                    "baseRefName,headRefName,mergeStateStatus,url"
                ),
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return json.loads(raw)
    except Exception:
        return None


def build_buckets(prs: list[dict]) -> dict[str, list[dict]]:
    buckets: dict[str, list[dict]] = {name: [] for name in BUCKET_ORDER}
    for pr in prs:
        buckets[classify(pr)].append(pr)
    for items in buckets.values():
        items.sort(key=lambda pr: pr.get("updatedAt", ""))
    return buckets


def build_summary(
    prs: list[dict],
    buckets: dict[str, list[dict]],
    *,
    now: datetime | None = None,
) -> dict:
    current = (now or datetime.now(UTC)).astimezone(UTC)
    duplicates = duplicate_title_groups(prs)
    duplicate_keys = set(duplicates)
    items = []
    for pr in sorted(prs, key=lambda item: item.get("number", 0)):
        items.append(
            {
                "number": pr.get("number"),
                "title": pr.get("title", ""),
                "bucket": classify(pr),
                "updated_at": pr.get("updatedAt"),
                "age_days": age_days(pr, now=current),
                "base": pr.get("baseRefName"),
                "head": pr.get("headRefName"),
                "merge_state": pr.get("mergeStateStatus"),
                "flags": risk_flags(pr, duplicate_keys=duplicate_keys, now=current),
                "url": pr.get("url"),
            }
        )
    return {
        "status": "PASS",
        "generated_at_utc": current.isoformat(),
        "total_open": len(prs),
        "stale_total": sum(
            any(flag.startswith("stale_") for flag in item["flags"]) for item in items
        ),
        "conflicted_total": sum("merge_conflict" in item["flags"] for item in items),
        "duplicate_title_groups": [
            {
                "normalized_title": key,
                "pr_numbers": [item.get("number") for item in group],
            }
            for key, group in duplicates.items()
        ],
        "buckets": {name: len(bucket_items) for name, bucket_items in buckets.items()},
        "items": items,
    }


def render_markdown(
    buckets: dict[str, list[dict]],
    total: int,
    *,
    all_prs: list[dict] | None = None,
    now: datetime | None = None,
) -> str:
    current = (now or datetime.now(UTC)).astimezone(UTC)
    prs = all_prs if all_prs is not None else [pr for items in buckets.values() for pr in items]
    duplicates = duplicate_title_groups(prs)
    duplicate_keys = set(duplicates)
    stale_total = sum((age_days(pr, now=current) or 0) >= STALE_AFTER_DAYS for pr in prs)
    conflicted_total = sum(
        (pr.get("mergeStateStatus") or "").upper() == "DIRTY" for pr in prs
    )

    lines = [
        "# Open PR Triage",
        "",
        f"- Generated: `{current.isoformat()}`",
        f"- Open PRs: {total}",
        f"- Stale ({STALE_AFTER_DAYS}+ days): {stale_total}",
        f"- Merge conflicts: {conflicted_total}",
        f"- Duplicate-title groups: {len(duplicates)}",
        "",
        "See policy: `docs/agents/PR_TRIAGE_POLICY.md`. Agents never merge or close PRs from triage output.",
        "Flags are review evidence only; they do not make a disposition.",
        "",
    ]
    for name in BUCKET_ORDER:
        items = buckets[name]
        lines.append(f"## {name} ({len(items)})")
        if not items:
            lines.append("- none")
        for pr in items[:PER_BUCKET_LIMIT]:
            num = pr.get("number")
            title = pr.get("title", "")
            updated = pr.get("updatedAt", "")
            age = age_days(pr, now=current)
            flags = risk_flags(pr, duplicate_keys=duplicate_keys, now=current)
            suffix_parts = [f"updated {updated}"]
            if age is not None:
                suffix_parts.append(f"age {age}d")
            if flags:
                suffix_parts.append("flags: " + ", ".join(flags))
            lines.append(f"- #{num} {title} -- {'; '.join(suffix_parts)}")
        if len(items) > PER_BUCKET_LIMIT:
            lines.append(f"- ... and {len(items) - PER_BUCKET_LIMIT} more")
        lines.append("")

    lines.append("## Duplicate-title review groups")
    if not duplicates:
        lines.append("- none")
    else:
        for key, group in duplicates.items():
            numbers = ", ".join(f"#{item.get('number')}" for item in group)
            lines.append(f"- `{key}`: {numbers}")
    lines.append("")
    return "\n".join(lines)


def write_skipped_report(reason: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "OPEN_PR_TRIAGE.md").write_text(
        "# Open PR Triage\n\n"
        f"Status: **SKIPPED** -- {reason}\n\n"
        "Populate by either:\n"
        "- running where the `gh` CLI is installed and authenticated "
        "(`GITHUB_TOKEN` set), or\n"
        "- from an agent session with GitHub tools, using the live PR list "
        "and applying `docs/agents/PR_TRIAGE_POLICY.md`.\n",
        encoding="utf-8",
    )
    (OUT_DIR / "open_pr_triage.json").write_text(
        json.dumps({"status": "SKIPPED", "reason": reason}, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    prs = fetch_prs()
    if prs is None:
        write_skipped_report("gh CLI unavailable or PR list could not be read")
        print("DEALIX_PR_TRIAGE=SKIPPED")
        return 0

    now = datetime.now(UTC)
    buckets = build_buckets(prs)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "OPEN_PR_TRIAGE.md").write_text(
        render_markdown(buckets, len(prs), all_prs=prs, now=now), encoding="utf-8"
    )
    summary = build_summary(prs, buckets, now=now)
    (OUT_DIR / "open_pr_triage.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("DEALIX_PR_TRIAGE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
