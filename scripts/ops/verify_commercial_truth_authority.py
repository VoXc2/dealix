#!/usr/bin/env python3
"""Inventory and verify Dealix commercial truth authority without network access."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from dealix.commercial.commercial_truth_authority import (
    CURRENT_AUTHORITY,
    UNCLASSIFIED_CONTEXT,
    classify_source,
    load_registry,
)

ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ".html", ".ts", ".tsx"}
SCAN_ROOTS = ("docs", "business", "config/company", "landing", "apps/web")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def build_inventory(root: Path = ROOT) -> dict:
    registry = load_registry()
    records: list[dict] = []
    marker_hits: list[dict] = []
    markers = [str(item) for item in registry.get("legacy_content_markers", [])]

    for relative_root in SCAN_ROOTS:
        base = root / relative_root
        if not base.exists():
            continue
        for path in sorted(p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES):
            relative = path.relative_to(root).as_posix()
            text = _read(path)
            classification = classify_source(relative, text=text)
            records.append({"path": relative, "classification": classification})
            hits = [marker for marker in markers if marker.casefold() in text.casefold()]
            if hits:
                marker_hits.append({"path": relative, "classification": classification, "markers": hits})

    counts = Counter(item["classification"] for item in records)
    current_paths = [str(item.get("path")) for item in registry.get("current_authority", [])]
    missing_current = [path for path in current_paths if not (root / path).is_file()]
    unsafe_marker_hits = [
        item
        for item in marker_hits
        if item["classification"] in {CURRENT_AUTHORITY, UNCLASSIFIED_CONTEXT}
    ]

    return {
        "schema": "dealix.commercial_truth_authority_inventory.v1",
        "registry_schema": registry.get("schema"),
        "scan_roots": list(SCAN_ROOTS),
        "files_scanned": len(records),
        "classification_counts": dict(sorted(counts.items())),
        "legacy_marker_files": marker_hits,
        "legacy_marker_file_count": len(marker_hits),
        "current_authority_paths": current_paths,
        "missing_current_authority_paths": missing_current,
        "unsafe_current_marker_hits": unsafe_marker_hits,
        "default_retrieval_mode": registry.get("default_retrieval_mode"),
        "verdict": "PASS" if not missing_current and not unsafe_marker_hits else "FAIL",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify Dealix commercial truth authority registry")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    receipt = build_inventory()
    if args.json:
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
    else:
        print(f"COMMERCIAL_TRUTH_AUTHORITY={receipt['verdict']}")
        print(f"FILES_SCANNED={receipt['files_scanned']}")
        print(f"LEGACY_MARKER_FILES={receipt['legacy_marker_file_count']}")
        print(f"CLASSIFICATIONS={json.dumps(receipt['classification_counts'], sort_keys=True)}")
        print(f"DEFAULT_RETRIEVAL_MODE={receipt['default_retrieval_mode']}")
        if receipt["missing_current_authority_paths"]:
            print("MISSING_CURRENT_AUTHORITY=" + ",".join(receipt["missing_current_authority_paths"]))
        if receipt["unsafe_current_marker_hits"]:
            print("UNSAFE_MARKER_HITS=" + json.dumps(receipt["unsafe_current_marker_hits"], ensure_ascii=False))
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
