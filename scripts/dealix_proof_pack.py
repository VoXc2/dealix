#!/usr/bin/env python3
"""Assemble a bilingual Proof Pack from local JSONL ProofEvent files.

Day 7 of a Pilot: the founder has 5-10 ProofEvents in
``docs/proof-events/<date>.jsonl``. This script reads them, runs
each through the Self-Growth OS publishing gate, and emits a
single bilingual markdown document ready for review and (after
manual approval) sharing.

Usage:
    # Read every JSONL in docs/proof-events/ for one customer:
    python scripts/dealix_proof_pack.py --customer-handle "ACME-Saudi-Pilot"

    # Read a single file:
    python scripts/dealix_proof_pack.py --customer-handle "ACME" \\
        --events docs/proof-events/2026-05-04.jsonl

    # Write the markdown to disk instead of stdout:
    python scripts/dealix_proof_pack.py --customer-handle "ACME" \\
        --out docs/proof-events/ACME-pack.md

NEVER auto-publishes. Always exits with `approval_status=approval_required`.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.self_growth_os.proof_snippet_engine import (  # noqa: E402
    render_pack,
)


DEFAULT_EVENTS_DIR = REPO_ROOT / "docs" / "proof-events"


def _iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue  # skip malformed lines, never fail the pack


def _load_events(
    *,
    explicit_files: list[Path] | None,
    customer_handle: str,
    events_dir: Path,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    paths: list[Path]
    if explicit_files:
        paths = explicit_files
    else:
        if not events_dir.exists():
            return out
        paths = sorted(events_dir.glob("*.jsonl"))

    for p in paths:
        if not p.exists():
            continue
        for evt in _iter_jsonl(p):
            if not isinstance(evt, dict):
                continue
            if customer_handle and evt.get("customer_handle") != customer_handle:
                continue
            out.append(evt)
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Assemble a Proof Pack from JSONL events.")
    p.add_argument("--customer-handle", required=True,
                   help="customer handle to filter events on")
    p.add_argument("--events", type=Path, action="append", default=None,
                   help="explicit JSONL file(s) to read; repeat or use default dir")
    p.add_argument("--events-dir", type=Path, default=DEFAULT_EVENTS_DIR,
                   help="directory of JSONL files (default: docs/proof-events/)")
    p.add_argument("--period-label", default="",
                   help="optional human-readable period label")
    p.add_argument("--out", type=Path, default=None,
                   help="write markdown to this path instead of stdout")
    p.add_argument("--lang", choices=["ar", "en", "both"], default="both",
                   help="which language(s) to emit (default: both)")
    args = p.parse_args(argv)

    events = _load_events(
        explicit_files=args.events,
        customer_handle=args.customer_handle,
        events_dir=args.events_dir,
    )
    if not events:
        print(
            f"[proof-pack] no events found for {args.customer_handle!r} "
            f"in {args.events_dir} or {args.events}",
            file=sys.stderr,
        )
        return 1

    pack = render_pack(
        events=events,
        customer_handle=args.customer_handle,
        period_label=args.period_label,
    )

    if pack.get("decision") == "blocked":
        # Don't emit the markdown. Surface why it was blocked.
        print(
            f"[proof-pack] BLOCKED — pack contains forbidden vocabulary "
            f"or empty events. Notes: {pack.get('notes')}",
            file=sys.stderr,
        )
        return 2

    parts: list[str] = []
    parts.append(f"<!-- Dealix Proof Pack — {args.customer_handle} -->")
    parts.append(f"<!-- approval_status: {pack['approval_status']} -->")
    parts.append(f"<!-- audience: {pack['audience']} -->")
    parts.append("")
    if args.lang in ("ar", "both"):
        parts.append(pack.get("markdown_ar", ""))
    if args.lang == "both":
        parts.append("")
        parts.append("---")
        parts.append("")
    if args.lang in ("en", "both"):
        parts.append(pack.get("markdown_en", ""))
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("> ⚠️ **Founder approval required before sharing externally.**")
    parts.append(f"> approval_status: {pack['approval_status']} · audience: {pack['audience']}")

    text = "\n".join(parts)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"[proof-pack] wrote {len(events)} events → {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
