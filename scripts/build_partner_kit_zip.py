#!/usr/bin/env python3
"""Build a byte-stable partner-kit zip.

Output: landing/assets/downloads/dealix-partner-kit-v1.zip

Byte-stable so CI can `git diff --exit-code` on it:
  - sorted filename order,
  - fixed ZipInfo dates (no current time),
  - external attrs zeroed,
  - DEFLATE level 6 (default), no compression-time randomness.

Usage:
    python scripts/build_partner_kit_zip.py
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "partner-kit"
OUTPUT_DIR = REPO_ROOT / "landing" / "assets" / "downloads"
OUTPUT_PATH = OUTPUT_DIR / "dealix-partner-kit-v1.zip"

# Fixed date for ZipInfo so the same content produces the same bytes.
STABLE_DATE = (2026, 5, 14, 0, 0, 0)


def build(output_path: Path = OUTPUT_PATH) -> Path:
    if not SOURCE_DIR.exists():
        print(f"missing source dir: {SOURCE_DIR}", file=sys.stderr)
        sys.exit(2)

    files = sorted(p for p in SOURCE_DIR.rglob("*") if p.is_file())
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for p in files:
            arcname = p.relative_to(SOURCE_DIR.parent).as_posix()  # "partner-kit/..."
            data = p.read_bytes()
            info = zipfile.ZipInfo(filename=arcname, date_time=STABLE_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            # Zero out external attrs so we don't leak filesystem state.
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)
    return output_path


def main(argv: list[str] | None = None) -> int:
    out = build()
    print(f"wrote {out.relative_to(REPO_ROOT)} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
