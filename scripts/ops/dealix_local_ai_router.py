#!/usr/bin/env python3
"""Dealix loopback compatibility router under canonical NO_DEEPSEEK authority.

This is the source-managed replacement for the historical hybrid runtime at
/opt/dealix/ai-router/router.py. It preserves the existing loopback API surface
but cannot select or call a remote model. Explicit historical cloud aliases
fail closed and point callers to the canonical broker/Session Factory.
"""
from __future__ import annotations

import json
import os
import sqlite3
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

HOST = "127.0.0.1"
PORT = int(os.getenv("DEALIX_ROUTER_PORT", "11999"))
LOCAL_MODEL = os.getenv("DEALIX_LOCAL_MODEL", "qwen3:4b-instruct-2507-q4_K_M")
LOCAL_CTX = int(os.getenv("DEALIX_LOCAL_NUM_CTX", "8192"))
DB = Path(os.getenv("DEALIX_ROUTER_DB", "/opt/dealix/ai-router/state/router.sqlite3"))
OLLAMA = "http://127.0.0.1:11434/api/chat"
OLLAMA_TAGS = "http://127.0.0.1:11434/api/tags"
LOCAL_ALIASES = frozenset({"dealix-auto", "dealix-local"})
HELD_ALIASES = frozenset({"dealix-flash", "dealix-think", "dealix-pro"})


def request_json(url: str, payload: dict[str, Any] | None = None, timeout: int = 300) -> dict[str, Any]:
    if not url.startswith("http://127.0.0.1:"):
        raise RuntimeError("LOOPBACK_ONLY")
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="GET" if payload is None else "POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_model_name(value: str) -> str:
    return value[:-7] if value.endswith(":latest") else value


def local_availability() -> dict[str, Any]:
    try:
        payload = request_json(OLLAMA_TAGS, timeout=2)
        models = {
            normalize_model_name(str(item.get("name") or item.get("model") or ""))
            for item in payload.get("models", [])
            if isinstance(item, dict)
        }
        present = normalize_model_name(LOCAL_MODEL) in models
        return {
            "ollama_reachable": True,
            "local_model_present": present,
            "local_inference_ready": "NOT_PROVEN_BY_HEALTH",
        }
    except Exception as exc:
        return {
            "ollama_reachable": False,
            "local_model_present": False,
            "local_inference_ready": "NOT_PROVEN_BY_HEALTH",
            "readiness_error_type": type(exc).__name__,
        }


def route_alias(alias: str) -> str:
    if alias in LOCAL_ALIASES:
        return "local"
    if alias in HELD_ALIASES:
        return "hold"
    return "invalid"


def local_chat(messages: list[dict[str, Any]], max_tokens: int = 512, tools: Any = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": LOCAL_MODEL,
        "stream": False,
        "think": False,
        "messages": messages,
        "options": {
            "num_ctx": LOCAL_CTX,
            "temperature": 0.1,
            "num_predict": max_tokens,
        },
    }
    if tools:
        payload["tools"] = tools
    result = request_json(OLLAMA, payload, timeout=300)
    message = result.get("message") or {}
    choice_message: dict[str, Any] = {
        "role": "assistant",
        "content": message.get("content", ""),
    }
    if message.get("tool_calls"):
        choice_message["tool_calls"] = message["tool_calls"]
    prompt_tokens = int(result.get("prompt_eval_count") or 0)
    output_tokens = int(result.get("eval_count") or 0)
    return {
        "id": "dealix-local",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": LOCAL_MODEL,
        "choices": [{"index": 0, "message": choice_message, "finish_reason": "stop"}],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": prompt_tokens + output_tokens,
        },
        "dealix_route": "local",
        "dealix_estimated_usd": 0.0,
        "no_deepseek": True,
    }


def historical_metrics() -> list[dict[str, Any]]:
    if not DB.exists():
        return []
    try:
        with sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=1) as conn:
            rows = conn.execute(
                """
                SELECT model, COUNT(*), COALESCE(SUM(hit),0), COALESCE(SUM(miss),0),
                       COALESCE(SUM(out),0), COALESCE(SUM(cost),0)
                FROM usage GROUP BY model ORDER BY COUNT(*) DESC
                """
            ).fetchall()
    except (sqlite3.Error, OSError):
        return []
    return [
        {
            "model": row[0],
            "calls": row[1],
            "cache_hit_tokens": row[2],
            "cache_miss_tokens": row[3],
            "output_tokens": row[4],
            "estimated_usd": round(float(row[5] or 0), 8),
        }
        for row in rows
    ]


class Handler(BaseHTTPRequestHandler):
    server_version = "DealixLocalOnlyRouter/1"

    def log_message(self, *_: Any) -> None:
        return

    def send_json(self, code: int, obj: dict[str, Any]) -> None:
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        try:
            self.wfile.write(raw)
        except (BrokenPipeError, ConnectionResetError):
            return

    def do_GET(self) -> None:
        if self.path == "/healthz":
            state = local_availability()
            self.send_json(
                200,
                {
                    "ok": bool(state["ollama_reachable"] and state["local_model_present"]),
                    "router_alive": True,
                    "local_model": LOCAL_MODEL,
                    "local_ctx": LOCAL_CTX,
                    "cloud_auto_allowed": False,
                    "no_deepseek": True,
                    "canonical_remote_authority": "BROKER_OR_HOLD",
                    **state,
                },
            )
            return
        if self.path == "/v1/models":
            data = [
                {"id": "dealix-auto", "object": "model", "policy_state": "local_only"},
                {"id": "dealix-local", "object": "model", "policy_state": "local_only"},
            ] + [
                {"id": alias, "object": "model", "policy_state": "hold_canonical_broker_required"}
                for alias in sorted(HELD_ALIASES)
            ]
            self.send_json(200, {"object": "list", "data": data})
            return
        if self.path == "/pricing":
            self.send_json(
                200,
                {
                    "currency": "USD",
                    "prices": {},
                    "automatic_remote_spend_allowed": False,
                    "authority": "CANONICAL_BROKER_OR_HOLD",
                    "note": "Compatibility endpoint; this router has no remote pricing or spend authority.",
                },
            )
            return
        if self.path == "/metrics":
            self.send_json(
                200,
                {
                    "automatic_remote_spend_allowed": False,
                    "historical_models": historical_metrics(),
                    "note": "Historical ledger may include routes retired by current NO_DEEPSEEK policy.",
                },
            )
            return
        self.send_json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        if self.path != "/v1/chat/completions":
            self.send_json(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 2_000_000:
                self.send_json(413, {"error": "invalid_request_size"})
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if payload.get("stream") is True:
                self.send_json(400, {"error": "streaming_disabled", "message": "Use stream=false."})
                return
            alias = str(payload.get("model") or "dealix-auto")
            route = route_alias(alias)
            if route == "hold":
                self.send_json(
                    409,
                    {
                        "error": "policy_hold",
                        "code": "NO_DEEPSEEK_CANONICAL_BROKER_REQUIRED",
                        "model": alias,
                        "dealix_route": "hold",
                        "message": "Remote model authority belongs to the canonical broker; this compatibility router is local-only.",
                    },
                )
                return
            if route == "invalid":
                self.send_json(400, {"error": "unknown_model_alias", "model": alias})
                return
            messages = payload.get("messages") or []
            if not isinstance(messages, list):
                self.send_json(400, {"error": "invalid_messages"})
                return
            max_tokens = min(max(int(payload.get("max_tokens") or 512), 1), 2048)
            result = local_chat(messages, max_tokens=max_tokens, tools=payload.get("tools"))
            self.send_json(200, result)
        except urllib.error.HTTPError as exc:
            self.send_json(503, {"error": "local_model_upstream_http_error", "status": exc.code})
        except Exception as exc:
            self.send_json(503, {"error": "local_model_unavailable", "error_type": type(exc).__name__})


def main() -> None:
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
