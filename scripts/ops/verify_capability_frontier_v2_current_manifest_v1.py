#!/usr/bin/env python3
"""Fail closed when Capability Frontier V2 rediscovers current-main capability authority.

The original frontier guard compared only with capability_top50_v1.tsv. Current
main also owns config/oss/oss_capability_manifest_v2.json, so a candidate that
is already an admitted component or already catalogued must not silently return
as a fresh ADOPT/PILOT decision.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
FRONTIER = ROOT / "config/oss/capability_frontier_v2.tsv"
MANIFEST = ROOT / "config/oss/oss_capability_manifest_v2.json"
ALLOWED_RECONCILED_DECISIONS = {"ALREADY_BOUNDED", "REJECT_DUPLICATE_DEFAULT"}


def norm_id(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def repo_from_source(value: str) -> str:
    raw = value.strip()
    if not raw:
        return ""
    if raw.startswith("http://") or raw.startswith("https://"):
        parsed = urlparse(raw)
        if parsed.netloc.lower() != "github.com":
            return ""
        parts = [part for part in parsed.path.strip("/").split("/") if part]
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}".removesuffix(".git").lower()
        return ""
    parts = [part for part in raw.strip("/").split("/") if part]
    if len(parts) >= 2:
        return f"{parts[-2]}/{parts[-1]}".removesuffix(".git").lower()
    return ""


def load_frontier() -> list[dict[str, str]]:
    with FRONTIER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_manifest_authority() -> tuple[set[str], set[str]]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries: list[dict[str, object]] = []
    for key in ("components", "catalogue_only"):
        value = data.get(key, [])
        if isinstance(value, list):
            entries.extend(item for item in value if isinstance(item, dict))
    ids = {norm_id(str(item.get("id", ""))) for item in entries if str(item.get("id", "")).strip()}
    repos = {
        repo
        for item in entries
        if (repo := repo_from_source(str(item.get("source", ""))))
    }
    return ids, repos


def find_unreconciled_overlaps() -> list[dict[str, str]]:
    current_ids, current_repos = load_manifest_authority()
    overlaps: list[dict[str, str]] = []
    for row in load_frontier():
        candidate_id = norm_id(row.get("id", ""))
        candidate_repo = repo_from_source(row.get("repository", ""))
        matched_by: list[str] = []
        if candidate_id and candidate_id in current_ids:
            matched_by.append("id")
        if candidate_repo and candidate_repo in current_repos:
            matched_by.append("repository")
        if matched_by and row.get("decision") not in ALLOWED_RECONCILED_DECISIONS:
            overlaps.append(
                {
                    "rank": row.get("rank", ""),
                    "id": row.get("id", ""),
                    "repository": row.get("repository", ""),
                    "decision": row.get("decision", ""),
                    "matched_by": "+".join(matched_by),
                }
            )
    return overlaps


def main() -> int:
    overlaps = find_unreconciled_overlaps()
    if overlaps:
        print("CAPABILITY_FRONTIER_CURRENT_MANIFEST=HOLD_UNRECONCILED_OVERLAP")
        for item in overlaps:
            print(
                "OVERLAP "
                f"rank={item['rank']} id={item['id']} repo={item['repository']} "
                f"decision={item['decision']} matched_by={item['matched_by']}"
            )
        print(f"OVERLAP_COUNT={len(overlaps)}")
        print("NEXT=replace the candidate or reconcile it explicitly as ALREADY_BOUNDED/REJECT_DUPLICATE_DEFAULT")
        print("L5_EXECUTED=NONE")
        return 2
    print("CAPABILITY_FRONTIER_CURRENT_MANIFEST=PASS_NO_UNRECONCILED_OVERLAP")
    print("L5_EXECUTED=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
