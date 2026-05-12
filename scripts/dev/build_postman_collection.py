"""
Convert the live FastAPI OpenAPI spec into a Postman v2.1 collection.
Run during CI on tag push so each release ships a Postman + Bruno
collection alongside the SDK release.

Usage:
    python scripts/dev/build_postman_collection.py > dealix-api.postman_collection.json
"""

from __future__ import annotations

import json
import sys


def _request_from_op(method: str, path: str, op: dict) -> dict:
    name = op.get("summary") or op.get("operationId") or f"{method.upper()} {path}"
    description = op.get("description", "")
    item = {
        "name": name,
        "request": {
            "method": method.upper(),
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": {
                "raw": "{{base_url}}" + path,
                "host": ["{{base_url}}"],
                "path": [p for p in path.strip("/").split("/") if p],
            },
            "description": description,
        },
    }
    body = op.get("requestBody")
    if body:
        item["request"]["body"] = {
            "mode": "raw",
            "raw": "{}",
            "options": {"raw": {"language": "json"}},
        }
    return item


def main() -> int:
    try:
        # Import the live FastAPI app to get a definitive openapi spec.
        from api.main import app

        spec = app.openapi()
    except Exception:
        print(json.dumps({"error": "could_not_import_app"}), file=sys.stderr)
        return 2

    paths = spec.get("paths", {}) or {}
    items: list[dict] = []
    folders: dict[str, list[dict]] = {}
    for path, methods in paths.items():
        for method, op in methods.items():
            if method.lower() not in {"get", "post", "put", "delete", "patch"}:
                continue
            tags = op.get("tags", ["misc"]) or ["misc"]
            tag = str(tags[0])
            folders.setdefault(tag, []).append(_request_from_op(method, path, op))

    for tag, ops in sorted(folders.items()):
        items.append({"name": tag, "item": ops})

    collection = {
        "info": {
            "name": "Dealix API",
            "_postman_id": "dealix-api-v3.3.0",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            "description": "Generated from the live OpenAPI document.",
        },
        "variable": [{"key": "base_url", "value": "https://api.dealix.me"}],
        "item": items,
    }
    print(json.dumps(collection, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
