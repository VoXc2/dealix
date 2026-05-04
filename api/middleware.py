"""FastAPI middleware — request ID, structured logging, timing, role guard."""

from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from auto_client_acquisition.revenue_company_os.role_action_policy import evaluate
from core.logging import get_logger

logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a unique request ID to each request and bind it to logs."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception("request_unhandled_error", error=str(e))
            raise
        duration_ms = (time.perf_counter() - start) * 1000

        response.headers["X-Request-ID"] = request_id
        logger.info(
            "request_completed",
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        return response


class RoleActionGuardMiddleware(BaseHTTPMiddleware):
    """Block (role, method, path) combinations the vision policy forbids.

    Opt-in via the X-Dealix-Role header. Without that header the policy
    is bypassed — public/unauthenticated endpoints stay open.

    Blocked requests get a 403 with a JSON body:
        {"detail": "role_action_blocked", "role": "...", "reason_ar": "..."}

    Audit-logged via structlog so we can reconstruct who tried what.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        role = request.headers.get("X-Dealix-Role")
        allowed, reason = evaluate(role, request.method, request.url.path)
        if not allowed:
            logger.warning(
                "role_action_blocked",
                role=role,
                method=request.method,
                path=request.url.path,
                reason_ar=reason,
            )
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "role_action_blocked",
                    "role": role,
                    "reason_ar": reason,
                },
            )
        return await call_next(request)
