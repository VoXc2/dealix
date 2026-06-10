"""
SAML SSO implementation for enterprise single sign-on.
تنفيذ SAML SSO للدخول الموحد للمؤسسات.

Supports multiple IdPs mapped by tenant_id via TenantRecord metadata.
Uses python3-saml (onelogin) under the hood.
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from typing import Any

from core.config.settings import get_settings
from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class SSOInitResult:
    redirect_url: str
    request_id: str
    relay_state: str | None = None


@dataclass
class SAMLResponse:
    user_id: str
    email: str
    name: str
    tenant_id: str
    attributes: dict[str, Any] = field(default_factory=dict)
    session_index: str | None = None


@dataclass
class LogoutResult:
    success: bool
    redirect_url: str | None = None


class SAMLAuth:
    """SAML 2.0 authentication provider.

    Each tenant configures their IdP metadata in tenant settings.
    Uses the HTTP-Redirect binding for SSO init and HTTP-POST for ACS.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

    def _get_app_base(self) -> str:
        return os.getenv("APP_BASE_URL", "http://localhost:8000")

    def _get_saml_cert(self) -> str:
        return os.getenv("SAML_SP_X509_CERT", "")

    def _get_saml_key(self) -> str:
        return os.getenv("SAML_SP_PRIVATE_KEY", "")

    def _get_idp_settings(self, tenant_id: str) -> dict[str, Any]:
        return {
            "entityId": os.getenv(
                f"SAML_IDP_ENTITY_ID_{tenant_id.upper()}",
                os.getenv("SAML_IDP_ENTITY_ID", f"https://idp.{tenant_id}.example.com"),
            ),
            "sso_url": os.getenv(
                f"SAML_IDP_SSO_URL_{tenant_id.upper()}",
                os.getenv("SAML_IDP_SSO_URL", f"https://idp.{tenant_id}.example.com/sso"),
            ),
            "sls_url": os.getenv(
                f"SAML_IDP_SLS_URL_{tenant_id.upper()}",
                os.getenv("SAML_IDP_SLS_URL", f"https://idp.{tenant_id}.example.com/sls"),
            ),
            "x509_cert": os.getenv(
                f"SAML_IDP_X509_CERT_{tenant_id.upper()}",
                os.getenv("SAML_IDP_X509_CERT", ""),
            ),
        }

    def _build_saml_settings(self, tenant_id: str) -> dict[str, Any]:
        """Build python3-saml settings dict for the given tenant."""
        base = self._get_app_base()
        idp = self._get_idp_settings(tenant_id)
        acs_url = f"{base}/api/v1/auth/saml/acs"
        issuer = f"{base}/api/v1/auth/saml/metadata"

        return {
            "sp": {
                "entityId": issuer,
                "assertionConsumerService": {
                    "url": acs_url,
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
                },
                "singleLogoutService": {
                    "url": f"{base}/api/v1/auth/saml/sls",
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
                },
                "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
                "x509cert": self._get_saml_cert(),
                "privateKey": self._get_saml_key(),
            },
            "idp": {
                "entityId": idp["entityId"],
                "singleSignOnService": {
                    "url": idp["sso_url"],
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
                },
                "singleLogoutService": {
                    "url": idp["sls_url"],
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
                },
                "x509cert": idp["x509_cert"],
            },
            "security": {
                "authnRequestsSigned": False,
                "wantAssertionsSigned": True,
                "wantMessagesSigned": False,
                "signatureAlgorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
                "digestAlgorithm": "http://www.w3.org/2001/04/xmlenc#sha256",
            },
            "contactPerson": {
                "technical": {
                    "givenName": "Dealix Support",
                    "emailAddress": "support@dealix.ai",
                }
            },
            "organization": {
                "en": {
                    "name": "Dealix",
                    "displayname": "Dealix",
                    "url": "https://dealix.ai",
                },
                "ar": {
                    "name": "ديلكس",
                    "displayname": "ديلكس",
                    "url": "https://dealix.ai",
                },
            },
        }

    async def init_sso(self, tenant_id: str) -> SSOInitResult:
        """Initiate SAML SSO — returns the IdP redirect URL."""
        try:
            from onelogin.saml2.auth import OneLogin_Saml2_Auth
        except ImportError:
            log.warning("python3-saml not installed; returning mock SSO URL")
            return SSOInitResult(
                redirect_url=f"https://idp.{tenant_id}.example.com/sso?tenant={tenant_id}",
                request_id=str(uuid.uuid4()),
            )

        req = self._build_flask_request(tenant_id)
        saml_settings = self._build_saml_settings(tenant_id)
        auth = OneLogin_Saml2_Auth(req, saml_settings)
        relay_state = f"tenant_id={tenant_id}"
        redirect_url = auth.login(relay_state=relay_state)
        return SSOInitResult(
            redirect_url=redirect_url,
            request_id=auth.get_last_request_id() or str(uuid.uuid4()),
            relay_state=relay_state,
        )

    async def acs(self, request_data: dict) -> SAMLResponse:
        """Handle Assertion Consumer Service — process SAML response."""
        try:
            from onelogin.saml2.auth import OneLogin_Saml2_Auth
        except ImportError:
            log.warning("python3-saml not installed; returning mock ACS response")
            return SAMLResponse(
                user_id=request_data.get("email", "mock-user"),
                email=request_data.get("email", "user@example.com"),
                name=request_data.get("name", "Mock User"),
                tenant_id=request_data.get("relay_state", "").replace("tenant_id=", ""),
            )

        req = self._build_flask_request_from_data(request_data)
        tenant_id = self._extract_tenant_from_relay(request_data)
        saml_settings = self._build_saml_settings(tenant_id)
        auth = OneLogin_Saml2_Auth(req, saml_settings)
        auth.process_response()

        errors = auth.get_errors()
        if errors:
            log.error("saml_acs_errors", errors=errors)
            raise ValueError(f"SAML ACS error: {', '.join(errors)}")

        if not auth.is_authenticated():
            raise PermissionError("SAML authentication failed")

        attributes = auth.get_attributes()
        name_id = auth.get_nameid()
        session_index = auth.get_session_index()

        return SAMLResponse(
            user_id=name_id or attributes.get("email", [""])[0],
            email=attributes.get("email", [name_id or ""])[0],
            name=attributes.get("name", [name_id or ""])[0],
            tenant_id=tenant_id,
            attributes={k: v[0] if len(v) == 1 else v for k, v in attributes.items()},
            session_index=session_index,
        )

    async def sls(self, request_data: dict) -> LogoutResult:
        """Handle Single Logout Service."""
        try:
            from onelogin.saml2.auth import OneLogin_Saml2_Auth
        except ImportError:
            return LogoutResult(success=True)

        req = self._build_flask_request_from_data(request_data)
        tenant_id = self._extract_tenant_from_relay(request_data)
        saml_settings = self._build_saml_settings(tenant_id)
        auth = OneLogin_Saml2_Auth(req, saml_settings)
        redirect_url = auth.process_slo(delete_session_cb=lambda: None)
        return LogoutResult(
            success=not auth.get_errors(),
            redirect_url=redirect_url,
        )

    async def get_metadata(self, tenant_id: str) -> str:
        """Generate SP metadata XML for the given tenant."""
        try:
            from onelogin.saml2.auth import OneLogin_Saml2_Auth
        except ImportError:
            base = self._get_app_base()
            return (
                f"<EntityDescriptor xmlns=\"urn:oasis:names:tc:SAML:2.0:metadata\" "
                f"entityID=\"{base}/api/v1/auth/saml/metadata?tenant={tenant_id}\" />"
            )

        req = self._build_flask_request(tenant_id)
        saml_settings = self._build_saml_settings(tenant_id)
        auth = OneLogin_Saml2_Auth(req, saml_settings)
        metadata = auth.get_settings().get_sp_metadata()
        errors = auth.get_settings().validate_metadata(metadata)
        if errors:
            raise ValueError(f"SAML metadata validation errors: {', '.join(errors)}")
        return metadata

    def _build_flask_request(self, tenant_id: str) -> dict[str, Any]:
        """Build a Flask-style request dict for python3-saml."""
        return {
            "http_host": self.settings.app_host,
            "server_port": self.settings.app_port,
            "https": "off" if self.settings.is_development else "on",
            "script_name": f"/api/v1/auth/saml?tenant={tenant_id}",
            "get_data": {},
            "post_data": {},
        }

    def _build_flask_request_from_data(self, data: dict) -> dict[str, Any]:
        """Build a Flask-style request dict with POST data."""
        return {
            "http_host": self.settings.app_host,
            "server_port": self.settings.app_port,
            "https": "off" if self.settings.is_development else "on",
            "script_name": "/api/v1/auth/saml",
            "get_data": {},
            "post_data": data,
        }

    @staticmethod
    def _extract_tenant_from_relay(data: dict) -> str:
        relay = data.get("RelayState", "")
        if relay.startswith("tenant_id="):
            return relay[len("tenant_id=") :]
        return relay or "default"
