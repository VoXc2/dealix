#!/usr/bin/env python3
"""Apply founder commercial KPI entries from registry into kpi_baselines.yaml.

Merges optional dealix/transformation/kpi_founder_commercial_import.yaml (gitignored)
into the registry before apply. Rejects placeholder source_ref values.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
_REGISTRY = _REPO_ROOT / "dealix/transformation/kpi_founder_commercial_registry.yaml"
_IMPORT = _REPO_ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"
_BASELINES = _REPO_ROOT / "dealix/transformation/kpi_baselines.yaml"

_FORBIDDEN_REF = re.compile(
    r"REPLACE:|fake|invented|synthetic_default|example_only|placeholder",
    re.I,
)


def _patch_snapshot_line(text: str, key: str, value: float, source_ref: str) -> str:
    lines = text.splitlines(keepends=True)
    in_key = False
    out: list[str] = []
    val_re = re.compile(r"^(\s*)value_numeric:\s*.*\n?$")
    ref_re = re.compile(r"^(\s*)source_ref:\s*.*\n?$")
    for line in lines:
        if re.match(rf"^\s*{re.escape(key)}:\s*$", line.rstrip("\n")):
            in_key = True
            out.append(line)
            continue
        if in_key:
            m_val = val_re.match(line.rstrip("\n"))
            if m_val:
                indent = m_val.group(1)
                nl = "\n" if line.endswith("\n") else ""
                out.append(f"{indent}value_numeric: {value}{nl}")
                continue
            m_ref = ref_re.match(line.rstrip("\n"))
            if m_ref:
                indent = m_ref.group(1)
                nl = "\n" if line.endswith("\n") else ""
                safe_ref = source_ref.replace('"', "'")
                out.append(f'{indent}source_ref: "{safe_ref}"{nl}')
                in_key = False
                continue
            if line.strip() and not line.startswith(" "):
                in_key = False
        out.append(line)
    return "".join(out)


def _validate_ref(key: str, source_ref: str) -> str | None:
    ref = source_ref.strip()
    if not ref:
        return f"{key}: empty source_ref"
    if _FORBIDDEN_REF.search(ref):
        return f"{key}: forbidden placeholder in source_ref"
    return None


def _merge_import_into_registry() -> int:
    if not _IMPORT.exists():
        return 0
    imp = yaml.safe_load(_IMPORT.read_text(encoding="utf-8")) or {}
    entries = imp.get("entries") or {}
    if not entries:
        return 0
    reg = yaml.safe_load(_REGISTRY.read_text(encoding="utf-8")) or {}
    commercial = reg.setdefault("commercial_entries", {})
    merged = 0
    for key, row in entries.items():
        if key not in commercial:
            continue
        val = row.get("value_numeric")
        ref = (row.get("source_ref") or "").strip()
        err = _validate_ref(key, ref) if ref else None
        if err:
            print(err, file=sys.stderr)
            return 1
        if val is not None and ref:
            commercial[key]["value_numeric"] = val
            commercial[key]["source_ref"] = ref
            merged += 1
    if imp.get("updated_period_iso"):
        reg["updated_period_iso"] = imp["updated_period_iso"]
    _REGISTRY.write_text(
        yaml.safe_dump(reg, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Merged {merged} entries from kpi_founder_commercial_import.yaml into registry")
    return 0


def _load_registry() -> dict:
    data = yaml.safe_load(_REGISTRY.read_text(encoding="utf-8"))
    return data.get("commercial_entries") or {}


def _ensure_import_file() -> None:
    if _IMPORT.exists():
        return
    bootstrap = _REPO_ROOT / "scripts" / "bootstrap_founder_kpi_import.py"
    if not bootstrap.is_file():
        return
    import subprocess

    subprocess.run([sys.executable, str(bootstrap)], check=False, cwd=_REPO_ROOT)


def _status() -> int:
    _ensure_import_file()
    entries = _load_registry()
    pending = []
    ready = []
    for key, row in entries.items():
        val = row.get("value_numeric")
        ref = (row.get("source_ref") or "").strip()
        if val is None or ref == "":
            pending.append(key)
        else:
            ready.append(key)
    print(f"commercial_registry_pending={len(pending)} ready={len(ready)}")
    if not _IMPORT.exists():
        print("hint: py -3 scripts/bootstrap_founder_kpi_import.py")
    else:
        print("kpi_import: present (fill CRM values; pending refs OK until export)")
    for key in pending:
        print(f"  pending: {key}")
    for key in ready:
        print(f"  ready: {key}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true", help="Print pending vs ready keys")
    parser.add_argument("--merge-import-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.status:
        return _status()

    if _merge_import_into_registry() != 0:
        return 1
    if args.merge_import_only:
        return 0

    entries = _load_registry()
    text = _BASELINES.read_text(encoding="utf-8")
    applied: list[str] = []
    for key, row in entries.items():
        val = row.get("value_numeric")
        ref = (row.get("source_ref") or "").strip()
        if val is None or ref == "":
            continue
        err = _validate_ref(key, ref)
        if err:
            print(err, file=sys.stderr)
            return 1
        text = _patch_snapshot_line(text, key, float(val), ref)
        applied.append(key)

    if not applied:
        print("No commercial entries to apply (fill import or registry first).")
        return 0

    if args.dry_run:
        print(f"Would apply: {', '.join(applied)}")
        return 0

    _BASELINES.write_text(text, encoding="utf-8")
    print(f"Applied commercial KPIs: {', '.join(applied)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
