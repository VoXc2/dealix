"""
DocuSign e-signature integration for enterprise contract execution.
دمج DocuSign للتوقيع الإلكتروني لتنفيذ العقود المؤسسية.

Supports envelope creation, status checking, signed document retrieval,
and webhook verification for DocuSign Connect.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class Signer:
    name: str
    email: str
    role: str = "signer"
    routing_order: int = 1
    embedded_signing_url: str | None = None


@dataclass
class EnvelopeResult:
    envelope_id: str
    status: str  # created / sent / delivered / signed / completed / declined / voided
    uri: str = ""
    created_at: str = ""


@dataclass
class EnvelopeStatus:
    envelope_id: str
    status: str
    signers: list[dict[str, Any]] = field(default_factory=list)
    completed_at: str | None = None
    voided_at: str | None = None
    void_reason: str | None = None


class DocuSignClient:
    """DocuSign eSignature REST API client.

    Uses OAuth 2.0 JWT Grant for authentication (server-to-server).
    Supports embedded and remote signing workflows.
    """

    BASE_URL = "https://demo.docusign.net/restapi/v2.1"
    PROD_URL = "https://www.docusign.net/restapi/v2.1"
    ACCOUNT_BASE = "https://account-d.docusign.com"
    PROD_ACCOUNT_BASE = "https://account.docusign.com"

    def __init__(self, sandbox: bool = True) -> None:
        self.sandbox = sandbox
        self.base = self.BASE_URL if sandbox else self.PROD_URL
        self.account_base = self.ACCOUNT_BASE if sandbox else self.PROD_ACCOUNT_BASE
        self.client_id = os.getenv("DOCUSIGN_CLIENT_ID", "")
        self.client_secret = os.getenv("DOCUSIGN_CLIENT_SECRET", "")
        self.impersonated_user_id = os.getenv("DOCUSIGN_IMPERSONATED_USER_ID", "")
        self.private_key = os.getenv("DOCUSIGN_PRIVATE_KEY", "")
        self._access_token: str | None = None
        self._account_id: str | None = None
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=30)
        return self._client

    async def _authenticate(self) -> str:
        """Authenticate with DocuSign using JWT Grant."""
        if self._access_token:
            return self._access_token

        if not self.client_id or not self.private_key:
            log.warning("docusign not configured; returning mock token")
            self._access_token = "mock-token"
            return self._access_token

        import jwt as pyjwt

        now = datetime.now(UTC)
        expiry = int(now.timestamp()) + 3600

        assertion = pyjwt.encode(
            {
                "iss": self.client_id,
                "sub": self.impersonated_user_id,
                "aud": self.account_base + "/oauth/token",
                "iat": int(now.timestamp()),
                "exp": expiry,
                "scope": "signature impersonation",
            },
            self.private_key,
            algorithm="RS256",
        )

        client = await self._get_client()
        resp = await client.post(
            f"{self.account_base}/oauth/token",
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": assertion,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        data = resp.json()
        self._access_token = data.get("access_token", "")

        # Get account ID
        await self._get_account_id()

        return self._access_token

    async def _get_account_id(self) -> str:
        """Retrieve the DocuSign account ID."""
        if self._account_id:
            return self._account_id

        client = await self._get_client()
        resp = await client.get(
            f"{self.account_base}/oauth/userinfo",
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        resp.raise_for_status()
        data = resp.json()
        accounts = data.get("accounts", [])
        for acc in accounts:
            if acc.get("is_default", False):
                self._account_id = acc.get("account_id", "")
                break
        if not self._account_id and accounts:
            self._account_id = accounts[0].get("account_id", "")

        return self._account_id or ""

    def _api_url(self, path: str) -> str:
        aid = self._account_id or "{accountId}"
        return f"{self.base}/accounts/{aid}{path}"

    async def send_for_signature(
        self,
        document_path: str,
        signers: list[Signer],
        email_subject: str = "Please sign your Dealix contract",
        email_body: str = "Dear {signer}, please review and sign the attached agreement.",
    ) -> EnvelopeResult:
        """Create and send an envelope for signature.

        Args:
            document_path: Local file path or URL to the document
            signers: List of signers with name, email, role
            email_subject: Email subject line
            email_body: Email body (use {signer} for signer name)

        Returns:
            EnvelopeResult with envelope_id and status
        """
        token = await self._authenticate()
        client = await self._get_client()

        # Read document
        try:
            if document_path.startswith(("http://", "https://")):
                doc_resp = await client.get(document_path)
                doc_resp.raise_for_status()
                doc_bytes = doc_resp.content
            else:
                with open(document_path, "rb") as f:
                    doc_bytes = f.read()
        except Exception as exc:
            log.warning("docusign_document_read_failed", path=document_path, error=str(exc))
            raise

        doc_b64 = base64.b64encode(doc_bytes).decode()

        envelope_definition: dict[str, Any] = {
            "emailSubject": email_subject,
            "emailBlurb": email_body,
            "status": "sent",
            "documents": [
                {
                    "documentBase64": doc_b64,
                    "name": document_path.split("/")[-1].split("\\")[-1] or "Contract.pdf",
                    "fileExtension": "pdf",
                    "documentId": "1",
                }
            ],
            "recipients": {
                "signers": [
                    {
                        "name": s.name,
                        "email": s.email,
                        "roleName": s.role,
                        "routingOrder": s.routing_order,
                        "recipientId": str(idx + 1),
                        "tabs": {
                            "signHereTabs": [
                                {
                                    "documentId": "1",
                                    "pageNumber": "1",
                                    "xPosition": "200",
                                    "yPosition": "500",
                                }
                            ]
                        },
                    }
                    for idx, s in enumerate(signers)
                ]
            },
        }

        resp = await client.post(
            self._api_url("/envelopes"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=envelope_definition,
        )
        resp.raise_for_status()
        data = resp.json()

        envelope_id = data.get("envelopeId", "")
        log.info(
            "docusign_envelope_sent",
            envelope_id=envelope_id,
            signers=[s.email for s in signers],
        )

        return EnvelopeResult(
            envelope_id=envelope_id,
            status=data.get("status", "sent"),
            uri=data.get("uri", ""),
            created_at=datetime.now(UTC).isoformat(),
        )

    async def check_status(self, envelope_id: str) -> EnvelopeStatus:
        """Check the status of an envelope."""
        token = await self._authenticate()
        client = await self._get_client()

        try:
            resp = await client.get(
                self._api_url(f"/envelopes/{envelope_id}"),
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            data = resp.json()

            recipients_data = data.get("recipients", {}).get("signers", [])
            signers = [
                {
                    "name": s.get("name", ""),
                    "email": s.get("email", ""),
                    "status": s.get("status", "unknown"),
                    "signed_at": s.get("signedDateTime"),
                }
                for s in recipients_data
            ]

            return EnvelopeStatus(
                envelope_id=envelope_id,
                status=data.get("status", "unknown"),
                signers=signers,
                completed_at=data.get("completedDateTime"),
                voided_at=data.get("voidedDateTime"),
                void_reason=data.get("voidedReason"),
            )

        except httpx.HTTPStatusError as exc:
            log.error(
                "docusign_status_failed",
                envelope_id=envelope_id,
                status_code=exc.response.status_code,
            )
            return EnvelopeStatus(
                envelope_id=envelope_id,
                status="error",
            )

    async def get_signed_document(self, envelope_id: str) -> bytes:
        """Download the signed document from a completed envelope.

        Returns the combined PDF with all signatures applied.
        """
        token = await self._authenticate()
        client = await self._get_client()

        resp = await client.get(
            self._api_url(f"/envelopes/{envelope_id}/documents/combined"),
            headers={"Authorization": f"Bearer {token}"},
        )
        resp.raise_for_status()

        log.info("docusign_document_downloaded", envelope_id=envelope_id)
        return resp.content

    async def get_embed_signing_url(self, envelope_id: str, signer_email: str) -> str:
        """Get an embedded signing URL for a signer.

        The signer can complete signing without leaving the Dealix platform.
        """
        token = await self._authenticate()
        client = await self._get_client()

        # Get recipient ID for this signer
        status = await self.check_status(envelope_id)
        recipient = next(
            (s for s in status.signers if s.get("email") == signer_email),
            None,
        )
        if not recipient:
            raise ValueError(f"Signer not found in envelope: {signer_email}")

        resp = await client.post(
            self._api_url(f"/envelopes/{envelope_id}/views/recipient"),
            headers={"Authorization": f"Bearer {token}"},
            json={
                "returnUrl": os.getenv("DOCUSIGN_RETURN_URL", "https://dealix.ai/contracts"),
                "authenticationMethod": "email",
                "email": signer_email,
                "userName": recipient.get("name", ""),
                "clientUserId": str(uuid.uuid4()),
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("url", "")

    async def void_envelope(self, envelope_id: str, reason: str = "Contract cancelled") -> bool:
        """Void an envelope that hasn't been completed yet."""
        token = await self._authenticate()
        client = await self._get_client()

        try:
            resp = await client.put(
                self._api_url(f"/envelopes/{envelope_id}"),
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "status": "voided",
                    "voidedReason": reason,
                },
            )
            resp.raise_for_status()
            log.info("docusign_envelope_voided", envelope_id=envelope_id, reason=reason)
            return True
        except httpx.HTTPStatusError as exc:
            log.error(
                "docusign_void_failed",
                envelope_id=envelope_id,
                error=str(exc),
            )
            return False

    async def verify_webhook(
        self,
        body: dict[str, Any],
        signature: str,
        expected_secret: str | None = None,
    ) -> bool:
        """Verify a DocuSign Connect webhook signature.

        DocuSign uses HMAC-SHA256 with a shared secret.
        """
        secret = expected_secret or os.getenv("DOCUSIGN_CONNECT_SECRET", "")
        if not secret:
            log.warning("docusign_webhook_secret_not_configured")
            return False

        payload = json.dumps(body, separators=(",", ":"))
        expected = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(signature, expected)

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
