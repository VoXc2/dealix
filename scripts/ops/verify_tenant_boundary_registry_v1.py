#!/usr/bin/env python3
"""Verify Dealix private-SaaS tenant-boundary inventory before RLS activation."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "config" / "saas" / "tenant_boundary_registry_v1.json"
DB_DIR = ROOT / "db"


def _literal_str(node: ast.AST | None) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _iter_assignments(class_node: ast.ClassDef) -> Iterable[tuple[str, ast.AST | None]]:
    for statement in class_node.body:
        if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            yield statement.target.id, statement.value
        elif isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Name):
                    yield target.id, statement.value


def discover_explicit_tenant_tables() -> frozenset[str]:
    tables: set[str] = set()
    for path in sorted(DB_DIR.glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            raise RuntimeError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            table_name: str | None = None
            has_tenant_id = False
            for name, value in _iter_assignments(node):
                if name == "__tablename__":
                    table_name = _literal_str(value)
                elif name == "tenant_id":
                    has_tenant_id = True
            if table_name and has_tenant_id:
                tables.add(table_name)
    return frozenset(tables)


def _literal_name_set(path: Path, name: str) -> frozenset[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for statement in tree.body:
        if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
            continue
        targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
        if not any(isinstance(target, ast.Name) and target.id == name for target in targets):
            continue
        value = statement.value
        if isinstance(value, ast.Dict):
            raw_items = value.keys
        elif isinstance(value, (ast.Set, ast.List, ast.Tuple)):
            raw_items = value.elts
        else:
            raise RuntimeError(f"{name} must remain a literal dict/list/set/tuple for static verification")
        values: list[str] = []
        for item in raw_items:
            text = _literal_str(item)
            if text is None:
                raise RuntimeError(f"{name} keys/items must be literal strings only")
            values.append(text)
        return frozenset(values)
    raise RuntimeError(f"{name} not found in {path.relative_to(ROOT)}")


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def evaluate() -> dict:
    registry = load_registry()
    tenant_tables = discover_explicit_tenant_tables()
    rls_file = DB_DIR / "rls_policies.py"
    policies = _literal_name_set(rls_file, "RLS_POLICIES")
    exemptions = _literal_name_set(rls_file, "RLS_EXEMPT_TABLES")
    pending = frozenset(registry["pending_tenant_rls_review"])
    mismatch = frozenset(registry["rls_model_mismatch_review"])

    uncovered = tenant_tables - policies - exemptions
    rls_without_explicit_tenant_model = policies - tenant_tables
    errors: list[str] = []

    if pending != uncovered:
        errors.append(
            "pending_tenant_rls_review drift: "
            f"registry_only={sorted(pending - uncovered)} discovered_only={sorted(uncovered - pending)}"
        )
    if mismatch != rls_without_explicit_tenant_model:
        errors.append(
            "rls_model_mismatch_review drift: "
            f"registry_only={sorted(mismatch - rls_without_explicit_tenant_model)} "
            f"discovered_only={sorted(rls_without_explicit_tenant_model - mismatch)}"
        )
    overlap = pending & mismatch
    if overlap:
        errors.append(f"registry categories overlap: {sorted(overlap)}")
    exempt_with_policy = exemptions & policies
    if exempt_with_policy:
        errors.append(f"RLS exemptions also have policies: {sorted(exempt_with_policy)}")

    activation_ready = not pending and not mismatch and not errors
    return {
        "schema_version": registry.get("schema_version"),
        "mode": registry.get("mode"),
        "explicit_tenant_tables": len(tenant_tables),
        "rls_policy_tables": len(policies),
        "rls_exempt_tables": len(exemptions),
        "covered_explicit_tenant_tables": len(tenant_tables & policies),
        "pending_tenant_rls_review": sorted(pending),
        "rls_model_mismatch_review": sorted(mismatch),
        "inventory_sync": not errors,
        "activation_ready": activation_ready,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--activation-ready",
        action="store_true",
        help="return non-zero until every pending/mismatch item is resolved",
    )
    args = parser.parse_args()
    result = evaluate()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"TENANT_BOUNDARY_INVENTORY_SYNC={'PASS' if result['inventory_sync'] else 'FAIL'}")
        print(f"EXPLICIT_TENANT_TABLES={result['explicit_tenant_tables']}")
        print(f"RLS_POLICY_TABLES={result['rls_policy_tables']}")
        print(f"RLS_EXEMPT_TABLES={result['rls_exempt_tables']}")
        print(f"COVERED_EXPLICIT_TENANT_TABLES={result['covered_explicit_tenant_tables']}")
        print(f"PENDING_TENANT_RLS_REVIEW={len(result['pending_tenant_rls_review'])}")
        print(f"RLS_MODEL_MISMATCH_REVIEW={len(result['rls_model_mismatch_review'])}")
        print(f"PRIVATE_SAAS_RLS_ACTIVATION_READY={'true' if result['activation_ready'] else 'false'}")
        for error in result["errors"]:
            print(f"ERROR={error}")
    if not result["inventory_sync"]:
        return 1
    if args.activation_ready and not result["activation_ready"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
