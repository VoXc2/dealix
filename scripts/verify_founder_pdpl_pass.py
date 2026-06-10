#!/usr/bin/env python3
"""Verify founder PDPL pass checklist — doc refs + privacy route in frontend."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PDPL_YAML = ROOT / "docs/commercial/operations/founder_pdpl_compliance_pass.yaml"
PRIVACY_PAGE = ROOT / "frontend/src/app/[locale]/privacy/page.tsx"
PRIVACY_DOC = ROOT / "docs/knowledge-base/privacy_pdpl_ar_en.md"


def _load_items() -> list[dict[str, Any]]:
    if not PDPL_YAML.is_file():
        return []
    data = yaml.safe_load(PDPL_YAML.read_text(encoding="utf-8"))
    items = (data or {}).get("items") or []
    return [i for i in items if isinstance(i, dict)]


def verify(*, require_privacy_route: bool = True) -> dict[str, Any]:
    items = _load_items()
    missing_docs: list[str] = []
    for item in items:
        ref = (item.get("ref") or "").strip()
        if not ref:
            continue
        path = ROOT / ref.replace("/", "\\") if "\\" in ref else ROOT / ref
        if not path.is_file():
            missing_docs.append(ref)

    privacy_route_ok = PRIVACY_PAGE.is_file()
    privacy_doc_ok = PRIVACY_DOC.is_file()

    verified: list[dict[str, Any]] = []
    for item in items:
        item_id = item.get("id", "")
        ref = (item.get("ref") or "").strip()
        ref_ok = bool(ref) and (ROOT / ref).is_file()
        if item_id == "privacy_policy_public":
            ref_ok = ref_ok and privacy_route_ok
        verified.append(
            {
                "id": item_id,
                "ref_ok": ref_ok,
                "done": bool(item.get("done")),
                "label_ar": item.get("label_ar"),
            }
        )

    done_count = sum(1 for v in verified if v["done"] and v["ref_ok"])
    all_refs_ok = not missing_docs and privacy_doc_ok and (not require_privacy_route or privacy_route_ok)
    verdict = "PASS" if done_count == len(verified) and all_refs_ok else "OPEN"

    return {
        "verdict": verdict,
        "items_total": len(verified),
        "items_done_verified": done_count,
        "missing_docs": missing_docs,
        "privacy_route_ok": privacy_route_ok,
        "privacy_doc_ok": privacy_doc_ok,
        "items": verified,
        "yaml_path": str(PDPL_YAML.relative_to(ROOT)).replace("\\", "/"),
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--skip-privacy-route", action="store_true")
    args = p.parse_args()

    blob = verify(require_privacy_route=not args.skip_privacy_route)
    print("== Founder PDPL Pass Verify ==")
    print(f"  verdict: {blob['verdict']}")
    print(f"  items: {blob['items_done_verified']}/{blob['items_total']} done+ref_ok")
    print(f"  privacy_route: {blob['privacy_route_ok']}")
    if blob["missing_docs"]:
        print(f"  missing_docs: {blob['missing_docs']}")
    print(f"FOUNDER_PDPL_PASS_VERDICT={blob['verdict']}")
    return 0 if blob["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
