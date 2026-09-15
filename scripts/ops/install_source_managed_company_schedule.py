#!/usr/bin/env python3
"""Install source-managed Dealix internal scheduler runtime files.

Dry-run is the default. This never edits systemd units and never grants external
action authority; it only converges the already-existing internal dispatcher files.
"""
from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "scripts/ops/runtime_templates/autonomous_company"
DEFAULT_RUNTIME = Path("/opt/dealix/control/autonomous-company/bin")
FILES = ("dealix-company-cycle", "dealix-company-dispatch.core-v6", "dealix-server-sentinel")


def stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def install_one(src: Path, dst: Path) -> Path:
    backup = dst.with_name(f"{dst.name}.bak-{stamp()}-source-managed")
    if dst.exists():
        shutil.copy2(dst, backup)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{dst.name}.", dir=dst.parent)
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        shutil.copy2(src, tmp)
        tmp.chmod(0o755)
        os.replace(tmp, dst)
    finally:
        if tmp.exists():
            tmp.unlink()
    return backup


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", type=Path, default=DEFAULT_RUNTIME)
    parser.add_argument("--apply-internal", action="store_true")
    args = parser.parse_args()

    for name in FILES:
        src = TEMPLATES / name
        if not src.is_file():
            print(f"INSTALL=HOLD missing_template={src}")
            return 2

    print(f"RUNTIME_ROOT={args.runtime_root}")
    print("SYSTEMD_MUTATION=NO")
    print("EXTERNAL_ACTION_AUTHORITY=NO")
    if not args.apply_internal:
        print("SOURCE_MANAGED_SCHEDULE_INSTALL=DRY_RUN_PASS")
        return 0

    if os.getenv("DEALIX_INTERNAL_SCHEDULER_APPLY", "") != "YES":
        print("INSTALL=HOLD DEALIX_INTERNAL_SCHEDULER_APPLY=YES required")
        return 78
    args.runtime_root.mkdir(parents=True, exist_ok=True)
    backups: list[Path] = []
    for name in FILES:
        backups.append(install_one(TEMPLATES / name, args.runtime_root / name))
    print("SOURCE_MANAGED_SCHEDULE_INSTALL=PASS")
    for backup in backups:
        if backup.exists():
            print(f"BACKUP={backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
