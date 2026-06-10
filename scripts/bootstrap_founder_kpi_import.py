#!/usr/bin/env python3
"""Create kpi_founder_commercial_import.yaml from example when missing (zeros + pending CRM refs)."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "dealix/transformation/kpi_founder_commercial_import.example.yaml"
TARGET = ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"


def bootstrap(*, force: bool = False) -> dict[str, object]:
    if TARGET.is_file() and not force:
        return {"created": False, "path": str(TARGET), "reason": "exists"}
    if not EXAMPLE.is_file():
        return {"created": False, "path": str(TARGET), "reason": "example_missing"}
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(EXAMPLE, TARGET)
    text = TARGET.read_text(encoding="utf-8")
    text = text.replace(
        "# مثال — انسخ إلى kpi_founder_commercial_import.yaml وعبّئ من CRM حقيقي.\n",
        "# Founder commercial KPI import — عبّئ value_numeric و source_ref من CRM/مالية فعلي.\n",
        1,
    )
    TARGET.write_text(text, encoding="utf-8")
    return {"created": True, "path": str(TARGET), "reason": "copied_from_example"}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--force", action="store_true", help="Overwrite existing import file")
    args = p.parse_args()
    blob = bootstrap(force=args.force)
    action = "CREATED" if blob["created"] else "SKIP"
    print(f"KPI_IMPORT_BOOTSTRAP={action} path={blob['path']} reason={blob['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
