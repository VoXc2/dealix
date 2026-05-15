"""
Operational Memory — NOT a chat-memory clone.

This stores what an *operations* runtime needs to reason about an entity:
its workflow history, the decisions taken, the approvals, and the execution
traces. Retrieval is permission-aware — a caller only ever sees runs for the
tenant it is scoped to.

Phase 0–1: in-process store. Phase 2: Postgres (append-only `workflow_runs`
table) + pgvector for semantic retrieval over rationales.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dealix.execution.workflow import WorkflowContext


class PermissionError_(Exception):
    """Raised on a cross-tenant retrieval attempt."""


class OperationalMemory:
    """Tenant-isolated store of workflow run history."""

    def __init__(self) -> None:
        # run_id -> snapshot
        self._runs: dict[str, dict[str, Any]] = {}
        # tenant_id -> entity_id -> [run_id, ...] (insertion order = chronological)
        self._index: dict[str, dict[str, list[str]]] = {}

    def record(self, ctx: WorkflowContext) -> None:
        """Persist (or update) a run snapshot. Append-only semantics:
        a run_id's snapshot is overwritten as the run progresses, never deleted."""
        snapshot = ctx.to_dict()
        self._runs[ctx.run_id] = snapshot
        tenant = self._index.setdefault(ctx.tenant_id, {})
        entity_runs = tenant.setdefault(ctx.entity_id, [])
        if ctx.run_id not in entity_runs:
            entity_runs.append(ctx.run_id)

    def get_run(self, run_id: str, *, tenant_id: str) -> dict[str, Any] | None:
        """Fetch one run. Cross-tenant access raises rather than leaking."""
        snap = self._runs.get(run_id)
        if snap is None:
            return None
        if snap["tenant_id"] != tenant_id:
            raise PermissionError_(
                f"run {run_id} belongs to another tenant — retrieval denied"
            )
        return snap

    def history_for_entity(
        self, entity_id: str, *, tenant_id: str, limit: int = 20
    ) -> list[dict[str, Any]]:
        """Permission-aware retrieval: prior runs for one business entity."""
        run_ids = self._index.get(tenant_id, {}).get(entity_id, [])
        runs = [self._runs[r] for r in run_ids if r in self._runs]
        return runs[-limit:]

    def all_runs(self, *, tenant_id: str | None = None) -> list[dict[str, Any]]:
        runs = list(self._runs.values())
        if tenant_id is not None:
            runs = [r for r in runs if r["tenant_id"] == tenant_id]
        return runs

    def summary(self, *, tenant_id: str | None = None) -> dict[str, Any]:
        runs = self.all_runs(tenant_id=tenant_id)
        by_status: dict[str, int] = {}
        for r in runs:
            by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        return {"total_runs": len(runs), "by_status": by_status}


# Process-wide singleton (swap for a Postgres-backed impl in Phase 2).
_MEMORY = OperationalMemory()


def get_memory() -> OperationalMemory:
    return _MEMORY


__all__ = ["OperationalMemory", "PermissionError_", "get_memory"]
