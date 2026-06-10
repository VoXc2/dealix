#!/usr/bin/env python3
"""Validate PR body contains engineering cutover markers when cutover env vars mentioned."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_CUTOVER_ENV = re.compile(
    r"(PROOF_LEDGER_BACKEND|VALUE_LEDGER_BACKEND|DEALIX_OPERATIONAL_STREAM_BACKEND|OTEL_CONTRACT_TRACE_EXPORT)",
    re.I,
)
_EXTERNAL = re.compile(r"external_signal\s*:", re.I)
_CONTRACT = re.compile(r"contract_or_pilot_ref\s*:", re.I)
_SECURITY_EXCEPTION = re.compile(r"security_review_note|CI breakage|security patch", re.I)


def validate(body: str) -> list[str]:
    errors: list[str] = []
    if not _CUTOVER_ENV.search(body):
        return errors
    if _SECURITY_EXCEPTION.search(body):
        return errors
    if not _EXTERNAL.search(body):
        errors.append("Missing external_signal: marker (required when cutover env vars appear)")
    if not _CONTRACT.search(body):
        errors.append("Missing contract_or_pilot_ref: marker")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, help="PR body markdown file")
    parser.add_argument("--text", type=str, default="", help="Inline PR body")
    args = parser.parse_args()
    body = args.text
    if args.file:
        body = args.file.read_text(encoding="utf-8")
    errs = validate(body)
    if errs:
        for e in errs:
            print(e, file=sys.stderr)
        return 1
    print("CUTOVER_PR_BODY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
