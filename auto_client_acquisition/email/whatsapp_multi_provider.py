"""
Governed multi-provider WhatsApp send adapter.

Canonical production target: Meta WhatsApp Cloud API.
Transitional transport: GREEN-API while the official Meta Business Platform
sender is being verified and activated.

CRITICAL:
- GREEN-API / Ultramsg / Fonnte are not the canonical official Meta Cloud path.
- Never silently fall back from a configured Meta sender to an unofficial
  transport after a Meta error; that could bypass template/window/compliance
  semantics.
- Live sends remain globally blocked unless ``WHATSAPP_ALLOW_LIVE_SEND=true``.
- Durable channel-purpose consent and suppression remain independent gates in
  Dealix; transport configuration is never consent authority.

Environment variables:
    GREEN_API_INSTANCE_ID, GREEN_API_TOKEN
    ULTRAMSG_INSTANCE_ID, ULTRAMSG_TOKEN
    FONNTE_TOKEN
    WHATSAPP_GRAPH_API_VERSION

Canonical Meta names:
    WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_ACCESS_TOKEN

Legacy Meta names are read only for migration compatibility:
    META_WHATSAPP_PHONE_NUMBER_ID, META_WHATSAPP_ACCESS_TOKEN

Provider selection:
    WHATSAPP_PROVIDER_PREFERENCE=auto|meta_cloud|green_api|ultramsg|fonnte

``auto`` is fail-safe official-first behavior:
- if Meta credentials exist, only Meta is attempted;
- otherwise transitional providers are attempted in Green -> Ultramsg ->
  Fonnte order.

Set ``WHATSAPP_MOCK_MODE=true`` to short-circuit all providers in CI/dev.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import asdict, dataclass
from typing import Any, Awaitable, Callable

import httpx

from integrations.whatsapp import meta_graph_base_url

log = logging.getLogger(__name__)

_NON_DIGIT = re.compile(r"\D+")


@dataclass
class WhatsAppSendResult:
    status: str  # ok | no_keys | http_error | timeout | mock | blocked | all_providers_failed
    provider: str | None = None
    message_id: str | None = None
    error: str | None = None
    fallback_chain_tried: list[str] = None  # type: ignore[assignment]

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["fallback_chain_tried"] = self.fallback_chain_tried or []
        return d


def _normalize_phone(phone: str) -> str:
    """Strip non-digits. Saudi numbers expected to start with 966 or 05."""
    digits = _NON_DIGIT.sub("", phone or "")
    if digits.startswith("00966"):
        digits = digits[2:]
    elif digits.startswith("05") and len(digits) == 10:
        digits = "966" + digits[1:]
    elif digits.startswith("5") and len(digits) == 9:
        digits = "966" + digits
    elif digits.startswith("0") and len(digits) == 10:
        digits = "966" + digits[1:]
    return digits


def _meta_credentials() -> tuple[str, str]:
    """Return canonical Meta credentials, retaining legacy names as fallback."""
    phone_id = (
        os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()
        or os.getenv("META_WHATSAPP_PHONE_NUMBER_ID", "").strip()
    )
    token = (
        os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip()
        or os.getenv("META_WHATSAPP_ACCESS_TOKEN", "").strip()
    )
    return phone_id, token


def _provider_preference() -> str:
    return os.getenv("WHATSAPP_PROVIDER_PREFERENCE", "auto").strip().lower() or "auto"


# ── Provider implementations ──────────────────────────────────────
async def _send_via_green_api(
    client: httpx.AsyncClient, phone: str, message: str
) -> WhatsAppSendResult | None:
    instance = os.getenv("GREEN_API_INSTANCE_ID", "").strip()
    token = os.getenv("GREEN_API_TOKEN", "").strip()
    if not (instance and token):
        return None
    url = f"https://api.green-api.com/waInstance{instance}/sendMessage/{token}"
    try:
        r = await client.post(
            url, json={"chatId": f"{phone}@c.us", "message": message}, timeout=15.0
        )
    except Exception as exc:
        return WhatsAppSendResult(status="http_error", provider="green_api", error=str(exc))
    if r.status_code == 200:
        body = r.json() or {}
        return WhatsAppSendResult(
            status="ok", provider="green_api", message_id=body.get("idMessage")
        )
    return WhatsAppSendResult(
        status="http_error",
        provider="green_api",
        error=f"HTTP {r.status_code}: {r.text[:200]}",
    )


async def _send_via_ultramsg(
    client: httpx.AsyncClient, phone: str, message: str
) -> WhatsAppSendResult | None:
    instance = os.getenv("ULTRAMSG_INSTANCE_ID", "").strip()
    token = os.getenv("ULTRAMSG_TOKEN", "").strip()
    if not (instance and token):
        return None
    url = f"https://api.ultramsg.com/{instance}/messages/chat"
    try:
        r = await client.post(
            url, data={"token": token, "to": phone, "body": message}, timeout=15.0
        )
    except Exception as exc:
        return WhatsAppSendResult(status="http_error", provider="ultramsg", error=str(exc))
    if r.status_code in (200, 201):
        body = r.json() or {}
        if body.get("sent") in (True, "true", "True"):
            return WhatsAppSendResult(
                status="ok",
                provider="ultramsg",
                message_id=str(body.get("id") or ""),
            )
    return WhatsAppSendResult(
        status="http_error",
        provider="ultramsg",
        error=f"HTTP {r.status_code}: {r.text[:200]}",
    )


async def _send_via_fonnte(
    client: httpx.AsyncClient, phone: str, message: str
) -> WhatsAppSendResult | None:
    token = os.getenv("FONNTE_TOKEN", "").strip()
    if not token:
        return None
    try:
        r = await client.post(
            "https://api.fonnte.com/send",
            headers={"Authorization": token},
            data={"target": phone, "message": message},
            timeout=15.0,
        )
    except Exception as exc:
        return WhatsAppSendResult(status="http_error", provider="fonnte", error=str(exc))
    if r.status_code == 200:
        body = r.json() or {}
        if body.get("status") in (True, "true"):
            return WhatsAppSendResult(
                status="ok", provider="fonnte", message_id=str(body.get("id") or "")
            )
    return WhatsAppSendResult(
        status="http_error",
        provider="fonnte",
        error=f"HTTP {r.status_code}: {r.text[:200]}",
    )


async def _send_via_meta_cloud(
    client: httpx.AsyncClient, phone: str, message: str
) -> WhatsAppSendResult | None:
    phone_id, token = _meta_credentials()
    if not (phone_id and token):
        return None
    url = f"{meta_graph_base_url()}/{phone_id}/messages"
    try:
        r = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "text",
                "text": {"body": message, "preview_url": False},
            },
            timeout=15.0,
        )
    except Exception as exc:
        return WhatsAppSendResult(status="http_error", provider="meta_cloud", error=str(exc))
    if r.status_code == 200:
        body = r.json() or {}
        msgs = body.get("messages") or []
        return WhatsAppSendResult(
            status="ok", provider="meta_cloud", message_id=msgs[0].get("id") if msgs else None
        )
    return WhatsAppSendResult(
        status="http_error",
        provider="meta_cloud",
        error=f"HTTP {r.status_code}: {r.text[:200]}",
    )


ProviderFn = Callable[
    [httpx.AsyncClient, str, str], Awaitable[WhatsAppSendResult | None]
]

# Static declaration is canonical priority, useful for inspection/tests. Runtime
# selection below deliberately prevents Meta -> unofficial silent fallback.
PROVIDER_CHAIN: list[tuple[str, ProviderFn]] = [
    ("meta_cloud", _send_via_meta_cloud),
    ("green_api", _send_via_green_api),
    ("ultramsg", _send_via_ultramsg),
    ("fonnte", _send_via_fonnte),
]
_PROVIDER_MAP = dict(PROVIDER_CHAIN)
_ALLOWED_PREFERENCES = {"auto", *_PROVIDER_MAP.keys()}


def configured_providers() -> list[str]:
    """Return configured transports in canonical inspection order."""
    out: list[str] = []
    phone_id, token = _meta_credentials()
    if phone_id and token:
        out.append("meta_cloud")
    if os.getenv("GREEN_API_INSTANCE_ID") and os.getenv("GREEN_API_TOKEN"):
        out.append("green_api")
    if os.getenv("ULTRAMSG_INSTANCE_ID") and os.getenv("ULTRAMSG_TOKEN"):
        out.append("ultramsg")
    if os.getenv("FONNTE_TOKEN"):
        out.append("fonnte")
    return out


def runtime_provider_chain() -> list[tuple[str, ProviderFn]]:
    """Resolve the live transport chain without bypassing official Meta policy."""
    preference = _provider_preference()
    if preference not in _ALLOWED_PREFERENCES:
        return []
    if preference != "auto":
        return [(preference, _PROVIDER_MAP[preference])]

    configured = configured_providers()
    if "meta_cloud" in configured:
        # Meta configured means Meta is the sole automatic transport. A Meta
        # failure must be surfaced, not silently rerouted to WhatsApp Web.
        return [("meta_cloud", _send_via_meta_cloud)]

    return [
        (name, fn)
        for name, fn in PROVIDER_CHAIN
        if name in {"green_api", "ultramsg", "fonnte"}
    ]


async def send_whatsapp_smart(phone: str, message: str) -> WhatsAppSendResult:
    """Send through the governed provider selected for this runtime."""
    if os.getenv("WHATSAPP_MOCK_MODE", "").lower() in {"true", "1", "yes"}:
        log.info("whatsapp_mock_mode phone_prefix=%s msg_len=%d", _normalize_phone(phone)[:5], len(message))
        return WhatsAppSendResult(status="mock", provider="mock")

    normalized = _normalize_phone(phone)
    if not normalized:
        return WhatsAppSendResult(status="http_error", error="invalid_phone")

    from core.config.settings import get_settings

    if not get_settings().whatsapp_allow_live_send:
        log.info("whatsapp_send_blocked_by_policy phone_prefix=%s", normalized[:5])
        return WhatsAppSendResult(
            status="blocked",
            provider="policy",
            error="whatsapp_allow_live_send_false",
            fallback_chain_tried=[],
        )

    preference = _provider_preference()
    if preference not in _ALLOWED_PREFERENCES:
        return WhatsAppSendResult(
            status="http_error",
            provider="policy",
            error="invalid_whatsapp_provider_preference",
            fallback_chain_tried=[],
        )

    tried: list[str] = []
    last: WhatsAppSendResult | None = None
    async with httpx.AsyncClient() as client:
        for name, fn in runtime_provider_chain():
            result = await fn(client, normalized, message)
            if result is None:
                continue
            tried.append(name)
            if result.status == "ok":
                result.fallback_chain_tried = tried
                return result
            last = result
            log.info("whatsapp_provider_failed provider=%s status=%s", name, result.status)

    if not tried:
        return WhatsAppSendResult(
            status="no_keys",
            error="no_selected_whatsapp_provider_configured",
            fallback_chain_tried=[],
        )
    if last:
        last.fallback_chain_tried = tried
        return last
    return WhatsAppSendResult(
        status="all_providers_failed", fallback_chain_tried=tried
    )
