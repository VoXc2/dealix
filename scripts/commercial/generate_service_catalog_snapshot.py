#!/usr/bin/env python3
"""Generate the frontend service-catalog snapshot from governed public truth.

The internal Python registry intentionally retains historical/future planning
entries. Public frontend data must not re-export those internal fixed prices or
inactive packages. The governed public projection is produced by
``scripts/dealix_export_service_catalog_json.py`` and contains only the current
Free Mini Diagnostic -> qualified discovery -> customer-specific quote ->
30-Day Revenue Command Pilot path.

No external calls are made.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "apps" / "web" / "lib" / "service-catalog-snapshot.ts"
EXPORTER = ROOT / "scripts" / "dealix_export_service_catalog_json.py"


def _load_public_catalog() -> dict:
    spec = importlib.util.spec_from_file_location("dealix_public_catalog_exporter", EXPORTER)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load governed public catalog exporter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    payload = module.build_catalog_dict()
    if payload.get("public_commercial_truth") != "one_governed_path":
        raise RuntimeError("public commercial authority drift")
    return payload


def main() -> int:
    payload = _load_public_catalog()
    snapshot = {
        "generated_from": "scripts/dealix_export_service_catalog_json.py",
        "public_only": True,
        **payload,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "export const serviceCatalogSnapshot = "
        + json.dumps(snapshot, ensure_ascii=False, indent=2)
        + " as const;\n",
        encoding="utf-8",
    )
    print(f"SERVICE_CATALOG_SNAPSHOT={OUT.relative_to(ROOT)}")
    print(f"PUBLIC_OFFERINGS={len(payload['offerings'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
