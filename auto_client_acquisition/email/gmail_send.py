"""Legacy Gmail OAuth compatibility adapter.

SECURITY / AUTHORITY CONTRACT
-----------------------------
Live Gmail sending through this legacy module is QUARANTINED. The historical
``send_email`` callable remains only so old callers fail closed instead of
crashing during the trust incident. It performs no token refresh and no Gmail
send request.

Draft creation remains available for founder-reviewed draft-only workflows. A
future live provider must bind directly to Dealix's canonical Governance /
Approval owner, fresh ACTION_HASH authority, and durable idempotency boundary.
This module must not become that authority by accepting caller-projected flags.
"""
from __future__ import annotations

import base64
import logging
import os
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Any

import httpx

log = logging.getLogger(__name__)

OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_DRAFTS_URL = "https://gmail.googleapis.com/gmail/v1/users/me/drafts"
LIVE_SEND_QUARANTINE_REASON = (
    "LIVE_GMAIL_SEND_QUARANTINED_CANONICAL_GOVERNANCE_PROVIDER_NOT_WIRED"
)

# Canonical alias expected by api/routers/email_send.py and
# scripts/verify_p0_trust_remediation_v1.py. Bound to the exact same
# quarantine value; single source of truth for the live Gmail quarantine.
LIVE_GMAIL_SEND_QUARANTINE_REASON = LIVE_SEND_QUARANTINE_REASON


@dataclass
class GmailSendResult:
    status: str  # quarantined
    gmail_message_id: str | None = None
    error: str | None = None


@dataclass
class GmailDraftResult:
    status: str  # ok | no_keys | auth_error | http_error
    draft_id: str | None = None
    message_id: str | None = None
    error: str | None = None


def is_configured() -> bool:
    """Return whether OAuth credentials exist for draft-only Gmail access."""
    return all(
        os.getenv(k, "").strip()
        for k in (
            "GMAIL_CLIENT_ID",
            "GMAIL_CLIENT_SECRET",
            "GMAIL_REFRESH_TOKEN",
            "GMAIL_SENDER_EMAIL",
        )
    )


async def _refresh_access_token(client: httpx.AsyncClient) -> str | None:
    cid = os.getenv("GMAIL_CLIENT_ID", "").strip()
    csec = os.getenv("GMAIL_CLIENT_SECRET", "").strip()
    rtok = os.getenv("GMAIL_REFRESH_TOKEN", "").strip()
    if not (cid and csec and rtok):
        return None
    data = {
        "client_id": cid,
        "client_secret": csec,
        "refresh_token": rtok,
        "grant_type": "refresh_token",
    }
    try:
        response = await client.post(OAUTH_TOKEN_URL, data=data, timeout=10.0)
    except Exception as exc:
        log.warning("gmail_oauth_refresh_failed err=%s", exc)
        return None
    if response.status_code != 200:
        log.warning("gmail_oauth_refresh_status=%s", response.status_code)
        return None
    payload = response.json() or {}
    return payload.get("access_token")


def _build_rfc822(
    *,
    sender_name: str,
    sender_email: str,
    to_email: str,
    subject: str,
    body_plain: str,
    reply_to: str | None = None,
    list_unsubscribe_email: str | None = None,
) -> bytes:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = to_email
    if reply_to:
        msg["Reply-To"] = reply_to
    if list_unsubscribe_email:
        msg["List-Unsubscribe"] = (
            f"<mailto:{list_unsubscribe_email}?subject=unsubscribe>"
        )
        msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    msg.attach(MIMEText(body_plain, "plain", "utf-8"))
    return msg.as_bytes()


async def send_email(
    *,
    to_email: str,
    subject: str,
    body_plain: str,
    reply_to: str | None = None,
    sender_name: str = "Sami | Dealix",
) -> GmailSendResult:
    """Fail closed. Legacy callers can no longer create a Gmail side effect."""
    # Keep the compatibility signature without allowing caller inputs, runtime
    # switches, OAuth presence, or fabricated approvals to grant authority.
    _ = (to_email, subject, body_plain, reply_to, sender_name)
    return GmailSendResult(
        status="quarantined",
        error=LIVE_SEND_QUARANTINE_REASON,
    )


async def create_draft(
    *,
    to_email: str,
    subject: str,
    body_plain: str,
    sender_name: str = "Sami | Dealix",
    reply_to: str | None = None,
) -> GmailDraftResult:
    """Create a Gmail draft for explicit human review; never sends it."""
    if not is_configured():
        return GmailDraftResult(status="no_keys", error="GMAIL_* env vars not set")

    sender_email = os.getenv("GMAIL_SENDER_EMAIL", "").strip()
    list_unsub = os.getenv("GMAIL_LIST_UNSUBSCRIBE", sender_email)

    async with httpx.AsyncClient() as client:
        access_token = await _refresh_access_token(client)
        if not access_token:
            return GmailDraftResult(
                status="auth_error",
                error="failed_to_refresh_access_token",
            )

        raw = _build_rfc822(
            sender_name=sender_name,
            sender_email=sender_email,
            to_email=to_email,
            subject=subject,
            body_plain=body_plain,
            reply_to=reply_to,
            list_unsubscribe_email=list_unsub,
        )
        encoded = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
        try:
            response = await client.post(
                GMAIL_DRAFTS_URL,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json={"message": {"raw": encoded}},
                timeout=15.0,
            )
        except Exception as exc:
            return GmailDraftResult(status="http_error", error=str(exc))

    if response.status_code == 200:
        body = response.json() or {}
        message = body.get("message") or {}
        return GmailDraftResult(
            status="ok",
            draft_id=body.get("id"),
            message_id=message.get("id"),
        )
    return GmailDraftResult(
        status="http_error",
        error=f"HTTP {response.status_code}: {response.text[:300]}",
    )


# OAuth setup helper: founder runs once locally for draft-only capability.
def get_oauth_setup_instructions() -> dict[str, Any]:
    return {
        "authority": "DRAFT_ONLY_LIVE_SEND_QUARANTINED",
        "needed_scope": "https://www.googleapis.com/auth/gmail.compose",
        "steps": [
            "1. Open https://console.cloud.google.com/apis/credentials",
            "2. Create OAuth 2.0 Client ID — type: Desktop app — name: Dealix Gmail Drafts",
            "3. Download client_secret.json. Note CLIENT_ID + CLIENT_SECRET.",
            "4. Run locally: pip install google-auth-oauthlib",
            "5. Mint refresh_token using the snippet below; keep it out of Git/logs.",
            "6. Store GMAIL_CLIENT_ID / GMAIL_CLIENT_SECRET / GMAIL_REFRESH_TOKEN / GMAIL_SENDER_EMAIL as deployment secrets.",
            "7. Review deployment changes explicitly.",
            "8. Verify draft creation only; live sending remains quarantined.",
        ],
        "snippet": (
            "from google_auth_oauthlib.flow import InstalledAppFlow\n"
            "flow = InstalledAppFlow.from_client_secrets_file(\n"
            "    'client_secret.json',\n"
            "    scopes=['https://www.googleapis.com/auth/gmail.compose'],\n"
            ")\n"
            "creds = flow.run_local_server(port=0, prompt='consent', access_type='offline')\n"
            "print('REFRESH_TOKEN:', creds.refresh_token)"
        ),
    }
