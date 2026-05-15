"""Tool registry for the agent runtime.

Tools are the *only* way the loop can affect the world. Every tool
declares whether it ``requires_approval``. A tool that sends a message,
spends money, or otherwise acts externally MUST set ``requires_approval``
or ``mutating`` — the loop refuses to auto-run an unguarded mutating tool
(``no_live_send`` / ``no_live_charge`` / ``no_cold_whatsapp``).

The default registry contains read-only Knowledge OS tools only.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.knowledge_os.index import KnowledgeIndex, get_default_index
from auto_client_acquisition.knowledge_os.retriever import retrieve
from auto_client_acquisition.knowledge_os.schemas import RetrievalRequest
from auto_client_acquisition.knowledge_os.synthesizer import answer_query

__all__ = ["Tool", "ToolRegistry", "ToolResult", "default_tool_registry"]


@dataclass(frozen=True, slots=True)
class ToolResult:
    """What a tool hands back to the loop."""

    observation: str
    insufficient_evidence: bool = False
    data: dict[str, Any] = field(default_factory=dict)


# A handler maps validated args → ToolResult. It must never raise for
# ordinary "no result" cases — only for genuine faults.
ToolHandler = Callable[[dict[str, Any]], ToolResult]


@dataclass(frozen=True, slots=True)
class Tool:
    """A single capability the loop may invoke."""

    name: str
    description: str
    handler: ToolHandler
    requires_approval: bool = False
    mutating: bool = False  # True ⇒ acts on the outside world


class ToolRegistry:
    """Name → Tool. The loop can only call tools registered here."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    def unguarded_mutating_tools(self) -> tuple[str, ...]:
        """Mutating tools that are NOT approval-gated — must always be empty
        for the safe runtime."""
        return tuple(
            sorted(
                t.name
                for t in self._tools.values()
                if t.mutating and not t.requires_approval
            )
        )


# ── Default Knowledge OS tools (read-only, safe to auto-run) ──────────
def _make_retrieve_tool(index: KnowledgeIndex) -> Tool:
    def _handler(args: dict[str, Any]) -> ToolResult:
        customer_id = str(args.get("customer_id", "")).strip()
        query = str(args.get("query", "")).strip()
        top_k = int(args.get("top_k", 5))
        if not customer_id or len(query) < 3:
            return ToolResult(observation="INVALID_ARGS", insufficient_evidence=True)
        results = retrieve(
            RetrievalRequest(query=query, customer_handle=customer_id, top_k=top_k),
            index=index,
        )
        if not results:
            return ToolResult(observation="NO_MATCHING_CHUNKS", insufficient_evidence=True)
        lines = [f"[{r.chunk_id}] {r.snippet_redacted}" for r in results]
        return ToolResult(
            observation="\n".join(lines),
            data={"chunk_ids": [r.chunk_id for r in results]},
        )

    return Tool(
        name="knowledge.retrieve",
        description="Retrieve permission-scoped knowledge chunks for a query.",
        handler=_handler,
    )


def _make_answer_tool(index: KnowledgeIndex) -> Tool:
    def _handler(args: dict[str, Any]) -> ToolResult:
        customer_id = str(args.get("customer_id", "")).strip()
        query = str(args.get("query", "")).strip()
        if not customer_id or len(query) < 3:
            return ToolResult(observation="INVALID_ARGS", insufficient_evidence=True)
        answer = answer_query(
            RetrievalRequest(query=query, customer_handle=customer_id, language="both"),
            index=index,
        )
        if answer.insufficient_evidence:
            return ToolResult(observation="INSUFFICIENT_EVIDENCE", insufficient_evidence=True)
        text = answer.answer_ar or answer.answer_en
        return ToolResult(
            observation=text,
            data={"citations": answer.citations, "confidence": answer.confidence},
        )

    return Tool(
        name="knowledge.answer",
        description="Produce a grounded, cited answer from indexed knowledge.",
        handler=_handler,
    )


def default_tool_registry(index: KnowledgeIndex | None = None) -> ToolRegistry:
    """Registry with the read-only Knowledge OS tools."""
    idx = index or get_default_index()
    registry = ToolRegistry()
    registry.register(_make_retrieve_tool(idx))
    registry.register(_make_answer_tool(idx))
    return registry
