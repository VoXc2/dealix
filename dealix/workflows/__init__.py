"""
Durable workflow layer — Inngest for long-running, multi-step LLM jobs.

Why durable: in-process LangGraph state is lost when the worker restarts.
Inngest provides step memoization, automatic retries, fan-out, sleep,
and a UI to inspect a stuck run — the things that make a $50k/yr
customer trust their data won't be silently dropped.
"""
from __future__ import annotations
