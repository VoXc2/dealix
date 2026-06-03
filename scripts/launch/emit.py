# -*- coding: utf-8 -*-
"""File-writing helpers that also accumulate the launch file manifest."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


class Assets:
    """Writes generated assets and records them for the manifest."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.entries: list[dict] = []

    def _write(self, relpath: str, content: str, pack: str, kind: str) -> None:
        target = self.root / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        self.entries.append(
            {
                "path": relpath,
                "pack": pack,
                "type": kind,
                "min_bytes": min(64, len(content.encode("utf-8"))),
            }
        )

    # --- typed writers -----------------------------------------------------
    def doc(self, relpath: str, body: str, pack: str) -> None:
        self._write(relpath, body.rstrip() + "\n", pack, "doc")

    def report(self, relpath: str, body: str, pack: str) -> None:
        self._write(relpath, body.rstrip() + "\n", pack, "report")

    def schema(self, relpath: str, obj: dict, pack: str) -> None:
        self._write(relpath, json.dumps(obj, ensure_ascii=False, indent=2) + "\n", pack, "schema")

    def yaml(self, relpath: str, obj: Any, pack: str) -> None:
        text = yaml.safe_dump(obj, allow_unicode=True, sort_keys=False)
        self._write(relpath, text, pack, "data")

    def jsonl(self, relpath: str, rows: list[dict], pack: str) -> None:
        text = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
        self._write(relpath, text + "\n", pack, "data")

    def code(self, relpath: str, content: str, pack: str) -> None:
        self._write(relpath, content.rstrip() + "\n", pack, "route")

    # --- manifest ----------------------------------------------------------
    def manifest(self) -> dict:
        by_pack: dict[str, list[dict]] = {}
        for e in self.entries:
            by_pack.setdefault(e["pack"], []).append(
                {"path": e["path"], "type": e["type"], "min_bytes": e["min_bytes"]}
            )
        return {
            "generated_by": "scripts/launch/build.py",
            "total_files": len(self.entries),
            "packs": by_pack,
        }


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {it}" for it in items)
