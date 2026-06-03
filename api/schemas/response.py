"""
Standard API response envelope.
المغلف القياسي لاستجابة API.

Every public endpoint SHOULD return:
{
    "data": <payload>,
    "meta": {"page": null, "total": null, "per_page": null, "cursor": null},
    "errors": []
}

Usage:
    from api.schemas.response import ok, paginated, error_response
    return ok({"id": "123", "name": "Acme"})
    return paginated(items, total=100, page=1, per_page=20)
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Pagination metadata included in list responses."""

    page: int | None = None
    total: int | None = None
    per_page: int | None = None
    cursor: str | None = None
    next_cursor: str | None = None
    has_more: bool = False


class ApiError(BaseModel):
    """A single structured error."""

    code: str
    message: str
    field: str | None = None


class ApiResponse(BaseModel, Generic[T]):
    """
    Standard API response envelope.
    غلاف استجابة API القياسي.
    """

    data: T | None = None
    meta: PaginationMeta = Field(default_factory=PaginationMeta)
    errors: list[ApiError] = Field(default_factory=list)


# ── Factory helpers ───────────────────────────────────────────────

def ok(data: Any, *, meta: PaginationMeta | None = None) -> dict[str, Any]:
    """Wrap a successful single-object response."""
    return {
        "data": data,
        "meta": (meta or PaginationMeta()).model_dump(),
        "errors": [],
    }


def paginated(
    items: list[Any],
    *,
    total: int | None = None,
    page: int | None = None,
    per_page: int | None = None,
    cursor: str | None = None,
    next_cursor: str | None = None,
    has_more: bool = False,
) -> dict[str, Any]:
    """Wrap a paginated list response."""
    return {
        "data": items,
        "meta": PaginationMeta(
            page=page,
            total=total,
            per_page=per_page,
            cursor=cursor,
            next_cursor=next_cursor,
            has_more=has_more,
        ).model_dump(),
        "errors": [],
    }


def error_response(
    *errors: ApiError | dict[str, Any],
    data: Any = None,
) -> dict[str, Any]:
    """Wrap an error response (still uses the envelope)."""
    normalized: list[dict[str, Any]] = []
    for e in errors:
        if isinstance(e, ApiError):
            normalized.append(e.model_dump())
        else:
            normalized.append(e)
    return {"data": data, "meta": PaginationMeta().model_dump(), "errors": normalized}
