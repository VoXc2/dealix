"""HermesAgent — abstract base for all Hermes agents.

Standalone base class; does not inherit from BaseAgent to avoid coupling to
the core LLM router. Uses HermesEngine directly for native Anthropic tool-use.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import structlog

from dealix.hermes.config import HermesConfig, get_hermes_config
from dealix.hermes.engine import HermesEngine, build_tool_schema

logger = structlog.get_logger(__name__)


class HermesAgent(ABC):
    """Abstract base for all Hermes agents.

    Subclasses must declare:
      - ``name: str`` — snake_case identifier
      - ``description: str`` — one-sentence description
      - Implement :meth:`run`

    The base class provides:
      - Native Anthropic tool registration and dispatch
      - Built-in ``log_event`` and ``get_current_datetime`` tools
      - :meth:`run_with_tools` agentic loop entry point
    """

    name: str = "hermes_agent"
    description: str = "Generic Hermes agent"

    def __init__(self, config: HermesConfig | None = None) -> None:
        self._config = config or get_hermes_config()
        self._engine = HermesEngine(config=self._config)
        self._tools: dict[str, dict[str, Any]] = {}
        self._tool_fns: dict[str, Callable[..., Any]] = {}
        self.log = logger.bind(agent=self.name)

        # Register built-in tools available to every agent
        self._register_builtin_tools()

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent's primary task.

        Parameters
        ----------
        input_data:
            Arbitrary input dict specific to each agent subclass.

        Returns
        -------
        dict
            Structured output specific to the agent.
        """

    # ------------------------------------------------------------------
    # Tool registration
    # ------------------------------------------------------------------

    def register_hermes_tool(
        self,
        name: str,
        description: str,
        properties: dict[str, Any],
        required: list[str],
        fn: Callable[..., Any],
    ) -> None:
        """Register a callable as an Anthropic-compatible tool.

        Parameters
        ----------
        name:
            Snake_case tool name.
        description:
            Plain-English description of what the tool does.
        properties:
            JSON-Schema properties dict.
        required:
            List of required property names.
        fn:
            Async function to call when the LLM invokes this tool.
        """
        schema = build_tool_schema(name, description, properties, required)
        self._tools[name] = schema
        self._tool_fns[name] = fn
        self.log.debug("hermes_tool_registered", tool=name)

    @property
    def tools_schema(self) -> list[dict[str, Any]]:
        """List of Anthropic tool dicts for the current agent."""
        return list(self._tools.values())

    # ------------------------------------------------------------------
    # Agentic loop
    # ------------------------------------------------------------------

    async def run_with_tools(
        self,
        system: str,
        user_msg: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run the Anthropic tool-use loop for this agent.

        Parameters
        ----------
        system:
            System prompt passed to the LLM.
        user_msg:
            Initial user message.
        context:
            Optional extra context merged into the initial message.

        Returns
        -------
        dict
            ``{response: str, messages: list, usage: dict}``
        """
        messages: list[dict[str, Any]] = []
        full_user = user_msg
        if context:
            ctx_str = json.dumps(context, ensure_ascii=False, indent=2)
            full_user = f"{user_msg}\n\nContext:\n{ctx_str}"

        messages.append({"role": "user", "content": full_user})

        final_text, history = await self._engine.run_agent_loop(
            system=system,
            messages=messages,
            tools=self.tools_schema,
            max_rounds=self._config.hermes_max_tool_rounds,
            tool_dispatcher=self._dispatch_tool,
        )

        return {
            "response": final_text,
            "messages": history,
            "usage": self._engine.last_usage.to_dict(),
        }

    # ------------------------------------------------------------------
    # Tool dispatch
    # ------------------------------------------------------------------

    async def _dispatch_tool(self, tool_name: str, tool_input: dict[str, Any]) -> str:
        """Call a registered tool function and return its result as a JSON string."""
        fn = self._tool_fns.get(tool_name)
        if fn is None:
            return json.dumps(
                {"error": f"unknown_tool: {tool_name}", "available": list(self._tool_fns.keys())}
            )
        try:
            result = await fn(**tool_input)
            return json.dumps(result, ensure_ascii=False, default=str)
        except Exception as exc:
            self.log.warning("hermes_tool_dispatch_error", tool=tool_name, error=str(exc))
            return json.dumps({"error": str(exc), "tool": tool_name})

    # ------------------------------------------------------------------
    # Built-in tools
    # ------------------------------------------------------------------

    def _register_builtin_tools(self) -> None:
        self.register_hermes_tool(
            name="log_event",
            description="Log a structured event for observability and audit.",
            properties={
                "event": {"type": "string", "description": "Event name/type"},
                "data": {
                    "type": "object",
                    "description": "Arbitrary key-value data for the event",
                },
            },
            required=["event"],
            fn=self._tool_log_event,
        )
        self.register_hermes_tool(
            name="get_current_datetime",
            description="Return the current UTC date and time.",
            properties={},
            required=[],
            fn=self._tool_get_current_datetime,
        )

    async def _tool_log_event(
        self, event: str, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        payload = data or {}
        self.log.info("hermes_agent_event", event=event, **payload)
        return {"logged": True, "event": event}

    @staticmethod
    async def _tool_get_current_datetime() -> dict[str, str]:
        now = datetime.now(UTC)
        return {
            "utc_iso": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"


__all__ = ["HermesAgent"]
