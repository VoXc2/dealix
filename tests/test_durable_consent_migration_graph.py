from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = ROOT / "db" / "migrations" / "versions"
APPROVAL_REVISION = "20260905_022_approval_center_snapshots"
CONSENT_REVISION = "20260908_023_consent_events"


def _literal_assignment(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            return ast.literal_eval(node.value)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"{name} missing from {path}")


def _revision_graph() -> dict[str, tuple[str, ...]]:
    graph: dict[str, tuple[str, ...]] = {}
    for path in sorted(VERSIONS.glob("*.py")):
        if path.name.startswith("__"):
            continue
        try:
            revision = _literal_assignment(path, "revision")
            down = _literal_assignment(path, "down_revision")
        except (AssertionError, ValueError):
            continue
        if down is None:
            parents: tuple[str, ...] = ()
        elif isinstance(down, str):
            parents = (down,)
        else:
            parents = tuple(down)
        assert isinstance(revision, str) and revision
        assert revision not in graph, f"duplicate revision {revision}"
        graph[revision] = parents
    return graph


def test_durable_consent_migration_extends_current_single_head():
    graph = _revision_graph()
    assert graph[CONSENT_REVISION] == (APPROVAL_REVISION,)

    referenced = {parent for parents in graph.values() for parent in parents}
    heads = set(graph) - referenced
    assert heads == {CONSENT_REVISION}
