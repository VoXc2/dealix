"""
Base Agent — shared foundation for all agents.
الفئة الأساسية لكل الوكلاء.

v2 upgrades:
  - Tool-use / function-calling loop (run_with_tools)
  - Tool registry: register_tool / register_tools
  - Structured output enforcement (force_json=True)
  - Episodic conversation memory (self.history)
  - Cost budget enforcement per tenant with alerts
  - self.memory → RevenueMemory semantic search
"""

from __future__ import annotations

import json
import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Any

from core.config.models import Task
from core.errors import AgentError
from core.llm import get_router
from core.llm.base import Message
from core.logging import get_logger
from core.utils import generate_id, utcnow

if TYPE_CHECKING:
    from core.agents.tools import Tool

logger = get_logger(__name__)

# Cost hints (USD per 1k tokens) — conservative Anthropic estimate
_COST_INPUT_PER_1K: float = 0.003
_COST_OUTPUT_PER_1K: float = 0.015

# Default per-run budget ceiling (USD) — 0 means unlimited
DEFAULT_COST_BUDGET_USD: float = 0.0


class BaseAgent(ABC):
    """
    Base class for all agents.
    Provides:
      - Unique id + logging
      - LLM router access (self.router)
      - Revenue Memory (self.memory)
      - Tool registry + tool-calling loop (self.run_with_tools)
      - Episodic conversation memory (self.history)
      - Structured JSON output enforcement
      - Cost budget tracking + alerts
    """

    name: str = "base_agent"

    def __init__(
        self,
        agent_id: str | None = None,
        *,
        tenant_id: str | None = None,
        cost_budget_usd: float = DEFAULT_COST_BUDGET_USD,
    ) -> None:
        self.agent_id = agent_id or generate_id(self.name)
        self.tenant_id = tenant_id
        self.created_at: datetime = utcnow()
        self.router = get_router()
        self.log = logger.bind(agent=self.name, agent_id=self.agent_id)

        # ── Revenue Memory ────────────────────────────────────────
        from core.memory.revenue_memory import RevenueMemory
        self.memory = RevenueMemory()

        # ── Tool registry ─────────────────────────────────────────
        from core.agents.tools import Tool
        self._tools: dict[str, Tool] = {}

        # ── Episodic conversation history ─────────────────────────
        self.history: list[Message] = []

        # ── Cost budget ───────────────────────────────────────────
        self._cost_budget_usd: float = cost_budget_usd
        self._cost_usd: float = 0.0

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the agent's core work."""
        ...

    # ── Tool management ────────────────────────────────────────────

    def register_tool(self, tool: Tool) -> None:
        """Register a single tool | سجّل أداة واحدة."""
        self._tools[tool.name] = tool
        self.log.debug("tool_registered", tool=tool.name)

    def register_tools(self, tools: list[Tool]) -> None:
        """Register multiple tools at once | سجّل عدة أدوات."""
        for tool in tools:
            self.register_tool(tool)

    def use_default_tools(self) -> None:
        """
        Register all built-in Dealix tools.
        تسجيل جميع الأدوات المدمجة في Dealix.
        """
        from core.agents.tools import TOOL_REGISTRY
        for tool in TOOL_REGISTRY.values():
            self.register_tool(tool)

    # ── Episodic memory ────────────────────────────────────────────

    def add_message(self, role: str, content: str) -> None:
        """Append a message to the episodic history | أضف رسالة للذاكرة."""
        self.history.append(Message(role=role, content=content))  # type: ignore[arg-type]

    def clear_history(self) -> None:
        """Clear episodic history | امسح الذاكرة المؤقتة."""
        self.history.clear()

    def history_messages(self) -> list[Message]:
        """Return current conversation history."""
        return list(self.history)

    # ── Tool-use loop ──────────────────────────────────────────────

    async def run_with_tools(
        self,
        task: Task,
        prompt: str,
        *,
        system: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.3,
        max_tool_rounds: int = 5,
        force_json: bool = False,
    ) -> str:
        """
        Execute a prompt with tool-use / function-calling loop.
        تنفيذ طلب مع حلقة استدعاء الأدوات.

        The loop continues until:
          1. The LLM produces a plain-text response (no tool calls), OR
          2. max_tool_rounds is exhausted.

        Returns the final text response from the LLM.
        """
        # Build system prompt with tool awareness
        tools_desc = self._tools_description()
        full_system = self._build_system(system, tools_desc, force_json)

        # Seed messages with history + new user turn
        messages: list[Message] = list(self.history)
        messages.append(Message(role="user", content=prompt))
        self.add_message("user", prompt)

        last_content = ""

        for round_num in range(1, max_tool_rounds + 1):
            self._check_budget()

            response = await self.router.run(
                task,
                messages=messages,
                system=full_system,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            self._track_cost(response)

            content = response.content
            last_content = content

            # Check for tool call request in the response
            tool_call = self._extract_tool_call(content)
            if tool_call is None:
                # Plain response — done
                self.add_message("assistant", content)
                break

            # Execute tool
            tool_name = tool_call.get("tool")
            tool_args = tool_call.get("arguments", {})
            tool_result = await self._invoke_tool(tool_name, tool_args)

            self.log.info(
                "tool_invoked",
                tool=tool_name,
                round=round_num,
                result_keys=list(tool_result.keys()) if isinstance(tool_result, dict) else "scalar",
            )

            # Append tool exchange to messages for next round
            messages.append(Message(role="assistant", content=content))
            messages.append(
                Message(
                    role="user",
                    content=f"Tool result for `{tool_name}`:\n{json.dumps(tool_result, ensure_ascii=False, indent=2)}",
                )
            )
        else:
            self.log.warning("tool_loop_max_rounds_reached", max_rounds=max_tool_rounds)
            self.add_message("assistant", last_content)

        return last_content

    async def _invoke_tool(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Call a registered tool function.
        استدعاء وظيفة أداة مسجّلة.
        """
        tool = self._tools.get(tool_name)
        if tool is None:
            return {"error": f"Unknown tool: {tool_name}", "available": list(self._tools.keys())}
        try:
            return await tool.function(**arguments)
        except Exception as exc:
            self.log.warning("tool_invocation_error", tool=tool_name, error=str(exc))
            return {"error": str(exc), "tool": tool_name}

    # ── Structured output ──────────────────────────────────────────

    async def run_structured(
        self,
        task: Task,
        prompt: str,
        *,
        system: str | None = None,
        max_tokens: int = 2048,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        """
        Run LLM and enforce JSON output.
        تشغيل النموذج مع إلزامية إخراج JSON.
        """
        json_system = (
            (system + "\n\n" if system else "")
            + "You MUST respond with valid JSON only. No prose, no markdown fences."
        )
        response = await self.router.run(
            task,
            messages=[Message(role="user", content=prompt)],
            system=json_system,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        self._track_cost(response)
        return self.parse_json_response(response.content)

    # ── Cost budget ────────────────────────────────────────────────

    def _track_cost(self, response: Any) -> None:
        """Accumulate USD cost from an LLM response."""
        input_cost = (getattr(response, "input_tokens", 0) / 1000) * _COST_INPUT_PER_1K
        output_cost = (getattr(response, "output_tokens", 0) / 1000) * _COST_OUTPUT_PER_1K
        self._cost_usd += input_cost + output_cost

        if self._cost_budget_usd > 0:
            pct = self._cost_usd / self._cost_budget_usd * 100
            if pct >= 80:
                self.log.warning(
                    "cost_budget_alert",
                    spent_usd=round(self._cost_usd, 4),
                    budget_usd=self._cost_budget_usd,
                    pct=round(pct, 1),
                    tenant_id=self.tenant_id,
                )

    def _check_budget(self) -> None:
        """Raise AgentError if cost budget is exceeded."""
        if self._cost_budget_usd > 0 and self._cost_usd >= self._cost_budget_usd:
            raise AgentError(
                f"Cost budget exceeded: spent ${self._cost_usd:.4f} of "
                f"${self._cost_budget_usd:.4f} for tenant={self.tenant_id}"
            )

    @property
    def cost_usd(self) -> float:
        """Total USD spent by this agent instance."""
        return round(self._cost_usd, 6)

    # ── Utilities ──────────────────────────────────────────────────

    @staticmethod
    def parse_json_response(text: str) -> dict[str, Any]:
        """
        Safely parse JSON from an LLM response that may have prose around it.
        يستخرج JSON بأمان حتى لو كان فيه نص حوله.
        """
        if not text:
            return {}

        # 1. Try raw parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 2. Try extracting fenced block ```json ... ```
        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fenced:
            try:
                return json.loads(fenced.group(1))
            except json.JSONDecodeError:
                pass

        # 3. Try largest {...} block
        largest = re.search(r"\{[\s\S]*\}", text)
        if largest:
            try:
                return json.loads(largest.group(0))
            except json.JSONDecodeError:
                pass

        raise AgentError(f"Could not parse JSON from LLM response: {text[:300]}")

    # ── Private helpers ────────────────────────────────────────────

    def _tools_description(self) -> str:
        """Build a text description of registered tools for the system prompt."""
        if not self._tools:
            return ""
        lines = ["Available tools (call via JSON with {\"tool\": ..., \"arguments\": {...}}):"]
        for tool in self._tools.values():
            lines.append(f"  - {tool.name}: {tool.description}")
        return "\n".join(lines)

    def _build_system(
        self, base_system: str | None, tools_desc: str, force_json: bool
    ) -> str | None:
        parts = []
        if base_system:
            parts.append(base_system)
        if tools_desc:
            parts.append(tools_desc)
            parts.append(
                "To call a tool, respond ONLY with JSON: "
                "{\"tool\": \"<tool_name>\", \"arguments\": {<params>}}"
            )
        if force_json:
            parts.append(
                "IMPORTANT: Your final response MUST be valid JSON only. "
                "No markdown, no prose outside JSON."
            )
        return "\n\n".join(parts) if parts else None

    @staticmethod
    def _extract_tool_call(text: str) -> dict[str, Any] | None:
        """
        Detect if LLM response is a tool-call JSON.
        Returns parsed dict or None if it's a plain response.
        """
        stripped = text.strip()
        if not stripped.startswith("{"):
            return None
        try:
            parsed = json.loads(stripped)
            if "tool" in parsed:
                return parsed
        except json.JSONDecodeError:
            pass
        return None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.agent_id}>"
