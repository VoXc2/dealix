"""
Auth router — passwordless magic-link auth for partners.

Endpoints:
    POST /api/v1/auth/magic-link/send
        body: {"email": "..."}
        Looks up an existing PartnerRecord by contact_email; if found,
        issues a magic token + emails it (or returns it in dev/test).
        SECURITY: do NOT leak whether the email exists — always return
        {"sent": true} so attackers can't enumerate partners.

    GET  /api/v1/auth/magic-link/verify?token=...
        Accepts a 'magic' token; on success exchanges it for a 'session'
        token set as an HttpOnly cookie. Redirects to /agency-partner.html
        when called from the browser, or returns JSON.

    GET  /api/v1/auth/me
        Returns the authenticated partner (200) or 401.

    POST /api/v1/auth/logout
        Clears the session cookie.

The dev/test path returns the magic link URL inside the response so
end-to-end flows can run without an external email provider.
Production sends via Resend, gated by RESEND_ALLOW_LIVE_SEND.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Body, Cookie, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy import select

from api.dependencies import SESSION_COOKIE, get_optional_partner, require_partner
from core.config.settings import get_settings
from db.models import PartnerRecord
from db.session import get_session
from dealix.auth.magic_link import (
    MAGIC_TTL_SECONDS,
    SESSION_TTL_SECONDS,
    MagicLinkPayload,
    issue,
    verify,
)

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# ── Helpers ───────────────────────────────────────────────────────


def _build_magic_url(request: Request, token: str) -> str:
    """Construct the user-facing verify URL.

    Honors X-Forwarded-Proto + X-Forwarded-Host so it works behind
    Railway/Render/Cloudflare tunnels.
    """
    proto = request.headers.get("x-forwarded-proto") or request.url.scheme
    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or "localhost"
    return f"{proto}://{host}/api/v1/auth/magic-link/verify?token={token}"


async def _send_email_safe(to_email: str, magic_url: str) -> dict[str, Any]:
    """Send the magic-link email — gated by RESEND_ALLOW_LIVE_SEND.

    Returns a metadata dict the caller can log; never raises.
    """
    s = get_settings()
    if not s.resend_allow_live_send:
        return {"sent": False, "reason": "live_send_gate_off"}
    if not s.resend_api_key:
        return {"sent": False, "reason": "no_resend_api_key"}
    try:
        # Lazy import — Resend is optional at boot.
        import resend  # type: ignore
        resend.api_key = s.resend_api_key.get_secret_value()
        resend.Emails.send({
            "from": f"{s.email_from_name} <{s.email_from}>",
            "to": [to_email],
            "subject": "Dealix — رابط الدخول الآمن",
            "html": (
                "<p>اضغط الرابط أدناه للدخول إلى بورتال Dealix. الرابط صالح لمدة 15 دقيقة:</p>"
                f"<p><a href='{magic_url}'>{magic_url}</a></p>"
                "<p>إذا لم تطلب هذا، تجاهل الرسالة.</p>"
            ),
        })
        return {"sent": True, "via": "resend"}
    except Exception as exc:
        log.warning("magic_link_email_send_failed err=%s", str(exc)[:120])
        return {"sent": False, "reason": "send_failed"}


def _set_session_cookie(response: Response, token: str) -> None:
    s = get_settings()
    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=SESSION_TTL_SECONDS,
        httponly=True,
        # Secure cookies break local http://localhost dev — only enforce in non-dev.
        secure=(s.app_env in ("staging", "production")),
        samesite="lax",
        path="/",
    )


def _clear_session_cookie(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE, path="/")


# ── Endpoints ─────────────────────────────────────────────────────


@router.post("/magic-link/send")
async def send_magic_link(
    request: Request,
    body: dict[str, Any] = Body(...),
) -> dict[str, Any]:
    email = str(body.get("email") or "").strip().lower()
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="email_required")

    # Look up the partner — but never leak existence.
    async with get_session() as session:
        row = await session.execute(
            select(PartnerRecord).where(PartnerRecord.contact_email == email)
        )
        partner = row.scalar_one_or_none()

    s = get_settings()
    response: dict[str, Any] = {"sent": True, "ttl_seconds": MAGIC_TTL_SECONDS}

    if partner is None:
        log.info("magic_link_send_unknown_email_silent")
        # Still return ok — anti-enumeration.
        return response

    token = issue(partner_id=partner.id, email=email, kind="magic")
    magic_url = _build_magic_url(request, token)
    delivery = await _send_email_safe(email, magic_url)
    log.info("magic_link_issued partner_id=%s delivery=%s", partner.id, delivery)

    # In non-production envs, surface the URL so dev / test / pilot users
    # can verify without an email provider hooked up.
    if s.app_env in ("test", "development", "dev", "local"):
        response["dev_magic_url"] = magic_url
    return response


@router.get("/magic-link/verify")
async def verify_magic_link(
    response: Response,
    token: str = Query(...),
    redirect: str = Query(default=""),
) -> dict[str, Any]:
    try:
        payload = verify(token)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if payload.kind != "magic":
        raise HTTPException(status_code=400, detail="not_magic_token")

    # Exchange for a session token + set cookie
    session_token = issue(partner_id=payload.sub, email=payload.email, kind="session")
    _set_session_cookie(response, session_token)
    return {
        "ok": True,
        "partner_id": payload.sub,
        "email": payload.email,
        "session_ttl_seconds": SESSION_TTL_SECONDS,
        "redirect": redirect or "/agency-partner.html",
    }


@router.get("/me")
async def me(
    payload: MagicLinkPayload = Depends(require_partner),
) -> dict[str, Any]:
    return {
        "partner_id": payload.sub,
        "email": payload.email,
        "kind": payload.kind,
        "expires_at": payload.exp,
    }


@router.post("/logout")
async def logout(response: Response) -> dict[str, Any]:
    _clear_session_cookie(response)
    return {"ok": True}
