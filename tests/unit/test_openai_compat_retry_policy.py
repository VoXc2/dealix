from __future__ import annotations

import httpx

from core.llm.openai_compat import _retryable_openai_compat_error


def _status_error(status: int) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://api.deepseek.com/v1/chat/completions")
    response = httpx.Response(status, request=request)
    return httpx.HTTPStatusError("provider error", request=request, response=response)


def test_http_402_is_not_retryable() -> None:
    assert _retryable_openai_compat_error(_status_error(402)) is False


def test_auth_and_bad_request_are_not_retryable() -> None:
    assert _retryable_openai_compat_error(_status_error(400)) is False
    assert _retryable_openai_compat_error(_status_error(401)) is False
    assert _retryable_openai_compat_error(_status_error(403)) is False


def test_rate_limit_and_server_errors_are_retryable() -> None:
    assert _retryable_openai_compat_error(_status_error(429)) is True
    assert _retryable_openai_compat_error(_status_error(500)) is True
    assert _retryable_openai_compat_error(_status_error(503)) is True


def test_timeouts_are_retryable() -> None:
    request = httpx.Request("POST", "https://api.deepseek.com/v1/chat/completions")
    assert _retryable_openai_compat_error(httpx.ReadTimeout("timeout", request=request)) is True
