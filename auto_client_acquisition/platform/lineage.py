"""Memory lineage graph helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LineageEdge:
    parent_id: str
    child_id: str
    relation: str


def build_lineage_index(edges: tuple[LineageEdge, ...]) -> dict[str, tuple[str, ...]]:
    index: dict[str, list[str]] = {}
    for edge in edges:
        index.setdefault(edge.child_id, []).append(edge.parent_id)
    return {child: tuple(parents) for child, parents in index.items()}


def trace_lineage_to_roots(memory_id: str, lineage_index: dict[str, tuple[str, ...]]) -> tuple[str, ...]:
    visited: list[str] = []
    stack = [memory_id]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.append(node)
        for parent in lineage_index.get(node, ()):  # top-down chain
            stack.append(parent)
    return tuple(visited)


__all__ = ['LineageEdge', 'build_lineage_index', 'trace_lineage_to_roots']
