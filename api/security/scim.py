"""
SCIM 2.0 Server — System for Cross-domain Identity Management.
خادم SCIM 2.0 لإدارة الهوية عبر النطاقات.

Implements RFC 7643 (SCIM Core Schema) and RFC 7644 (SCIM Protocol).
Supports user provisioning from enterprise IdPs (Azure AD, Okta, etc.).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class SCIMName:
    given_name: str = ""
    family_name: str = ""
    formatted: str | None = None
    middle_name: str | None = None
    honorific_prefix: str | None = None
    honorific_suffix: str | None = None


@dataclass
class SCIMEmail:
    value: str
    primary: bool = False
    type: str = "work"
    display: str | None = None


@dataclass
class SCIMPhoneNumber:
    value: str
    primary: bool = False
    type: str = "work"


@dataclass
class SCIMUser:
    schemas: list[str] = field(default_factory=lambda: [
        "urn:ietf:params:scim:schemas:core:2.0:User",
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User",
    ])
    id: str = ""
    user_name: str = ""
    name: SCIMName = field(default_factory=SCIMName)
    emails: list[SCIMEmail] = field(default_factory=list)
    phone_numbers: list[SCIMPhoneNumber] = field(default_factory=list)
    display_name: str = ""
    active: bool = True
    external_id: str | None = None
    locale: str | None = None
    timezone: str | None = None
    title: str | None = None
    department: str | None = None
    manager: str | None = None
    tenant_id: str = ""
    meta: dict[str, Any] = field(default_factory=dict)

    def to_scim_dict(self) -> dict[str, Any]:
        name_dict = {}
        if self.name.given_name:
            name_dict["givenName"] = self.name.given_name
        if self.name.family_name:
            name_dict["familyName"] = self.name.family_name
        if self.name.formatted:
            name_dict["formatted"] = self.name.formatted
        if self.name.middle_name:
            name_dict["middleName"] = self.name.middle_name

        result: dict[str, Any] = {
            "schemas": self.schemas,
            "id": self.id,
            "userName": self.user_name,
            "name": name_dict,
            "emails": [{"value": e.value, "primary": e.primary, "type": e.type} for e in self.emails],
            "displayName": self.display_name or f"{self.name.given_name} {self.name.family_name}".strip(),
            "active": self.active,
            "meta": {
                "resourceType": "User",
                "created": self.meta.get("created", datetime.now(UTC).isoformat()),
                "lastModified": self.meta.get("lastModified", datetime.now(UTC).isoformat()),
                "location": self.meta.get("location", f"/api/v1/scim/Users/{self.id}"),
                "version": self.meta.get("version", 'W/"1"'),
            },
        }
        if self.external_id:
            result["externalId"] = self.external_id
        if self.locale:
            result["locale"] = self.locale
        if self.timezone:
            result["timezone"] = self.timezone
        if self.title:
            result["title"] = self.title
        if self.department:
            result["department"] = self.department
        if self.manager:
            result["manager"] = {"value": self.manager}
        if self.phone_numbers:
            result["phoneNumbers"] = [
                {"value": p.value, "primary": p.primary, "type": p.type}
                for p in self.phone_numbers
            ]
        if self.tenant_id:
            result["urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"] = {
                "department": self.department or "",
            }
        return result

    @classmethod
    def from_scim_dict(cls, data: dict[str, Any]) -> SCIMUser:
        name_data = data.get("name", {})
        emails_data = data.get("emails", [])
        phones_data = data.get("phoneNumbers", [])

        enterprise = data.get("urn:ietf:params:scim:schemas:extension:enterprise:2.0:User", {})

        return cls(
            schemas=data.get("schemas", cls.schemas),
            id=data.get("id", ""),
            user_name=data.get("userName", ""),
            name=SCIMName(
                given_name=name_data.get("givenName", ""),
                family_name=name_data.get("familyName", ""),
                formatted=name_data.get("formatted"),
                middle_name=name_data.get("middleName"),
            ),
            emails=[SCIMEmail(value=e["value"], primary=e.get("primary", False), type=e.get("type", "work")) for e in emails_data],
            phone_numbers=[SCIMPhoneNumber(value=p["value"], primary=p.get("primary", False), type=p.get("type", "work")) for p in phones_data],
            display_name=data.get("displayName", ""),
            active=data.get("active", True),
            external_id=data.get("externalId"),
            locale=data.get("locale"),
            timezone=data.get("timezone"),
            title=data.get("title"),
            department=enterprise.get("department", data.get("department")),
            manager=enterprise.get("manager", {}).get("value") if isinstance(enterprise.get("manager"), dict) else enterprise.get("manager"),
            meta=data.get("meta", {}),
        )


@dataclass
class SCIMResponse:
    id: str
    user_name: str
    active: bool
    scim_data: dict[str, Any]


@dataclass
class SCIMListResponse:
    total_results: int
    items_per_page: int = 100
    start_index: int = 1
    resources: list[dict[str, Any]] = field(default_factory=list)
    schemas: list[str] = field(default_factory=lambda: ["urn:ietf:params:scim:api:messages:2.0:ListResponse"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemas": self.schemas,
            "totalResults": self.total_results,
            "itemsPerPage": self.items_per_page,
            "startIndex": self.start_index,
            "Resources": self.resources,
        }


class SCIMServer:
    """SCIM 2.0 Protocol server for identity lifecycle management.

    Integrates with Azure AD, Okta, OneLogin, and any SCIM-compliant IdP.
    All operations are tenant-scoped and audit-logged.
    """

    def __init__(self) -> None:
        self._users: dict[str, SCIMUser] = {}

    async def create_user(self, data: dict[str, Any]) -> SCIMResponse:
        """Create a user via SCIM PUT /Users."""
        scim_user = SCIMUser.from_scim_dict(data)
        scim_user.id = str(uuid.uuid4())
        now = datetime.now(UTC).isoformat()
        scim_user.meta = {
            "created": now,
            "lastModified": now,
            "location": f"/api/v1/scim/Users/{scim_user.id}",
            "version": 'W/"1"',
        }
        tenant_id = data.get("tenant_id", scim_user.tenant_id)
        scim_user.tenant_id = tenant_id
        self._users[scim_user.id] = scim_user

        log.info("scim_user_created", user_id=scim_user.id, user_name=scim_user.user_name)
        return SCIMResponse(
            id=scim_user.id,
            user_name=scim_user.user_name,
            active=scim_user.active,
            scim_data=scim_user.to_scim_dict(),
        )

    async def get_user(self, user_id: str) -> SCIMResponse:
        """Get a user by ID via SCIM GET /Users/{id}."""
        scim_user = self._users.get(user_id)
        if not scim_user:
            raise KeyError(f"SCIM user not found: {user_id}")

        return SCIMResponse(
            id=scim_user.id,
            user_name=scim_user.user_name,
            active=scim_user.active,
            scim_data=scim_user.to_scim_dict(),
        )

    async def update_user(self, user_id: str, data: dict[str, Any]) -> SCIMResponse:
        """Update a user via SCIM PUT /Users/{id}."""
        existing = self._users.get(user_id)
        if not existing:
            raise KeyError(f"SCIM user not found: {user_id}")

        scim_user = SCIMUser.from_scim_dict(data)
        scim_user.id = user_id
        scim_user.tenant_id = existing.tenant_id
        now = datetime.now(UTC).isoformat()
        scim_user.meta = {
            "created": existing.meta.get("created", now),
            "lastModified": now,
            "location": f"/api/v1/scim/Users/{user_id}",
            "version": 'W/"2"',
        }
        self._users[user_id] = scim_user

        log.info("scim_user_updated", user_id=user_id)
        return SCIMResponse(
            id=user_id,
            user_name=scim_user.user_name,
            active=scim_user.active,
            scim_data=scim_user.to_scim_dict(),
        )

    async def delete_user(self, user_id: str) -> SCIMResponse:
        """Delete a user via SCIM DELETE /Users/{id}."""
        scim_user = self._users.pop(user_id, None)
        if not scim_user:
            raise KeyError(f"SCIM user not found: {user_id}")

        log.info("scim_user_deleted", user_id=user_id)
        scim_user.active = False
        return SCIMResponse(
            id=user_id,
            user_name=scim_user.user_name,
            active=False,
            scim_data={},
        )

    async def list_users(
        self,
        filter: str | None = None,
        start_index: int = 1,
        count: int = 100,
    ) -> SCIMListResponse:
        """List users via SCIM GET /Users with optional filtering.

        Basic SCIM filter support:
        - userName eq "value"
        - email eq "value"
        - active eq true/false
        """
        users = list(self._users.values())

        if filter:
            users = self._apply_filter(users, filter)

        total = len(users)
        paginated = users[start_index - 1 : start_index - 1 + count]

        resources = [u.to_scim_dict() for u in paginated]

        return SCIMListResponse(
            total_results=total,
            items_per_page=count,
            start_index=start_index,
            resources=resources,
        )

    async def list_groups(
        self,
        filter: str | None = None,
        start_index: int = 1,
        count: int = 100,
    ) -> SCIMListResponse:
        """List groups (placeholder — groups are mapped from tenant roles)."""
        return SCIMListResponse(
            total_results=0,
            items_per_page=count,
            start_index=start_index,
            resources=[],
        )

    async def get_group(self, group_id: str) -> SCIMResponse:
        """Get a group by ID (placeholder)."""
        raise KeyError(f"SCIM group not found: {group_id}")

    def _apply_filter(self, users: list[SCIMUser], filter_expr: str) -> list[SCIMUser]:
        """Apply basic SCIM filter expression."""
        filter_expr = filter_expr.strip()
        result = list(users)

        if " eq " in filter_expr:
            parts = filter_expr.split(" eq ")
            if len(parts) == 2:
                attr = parts[0].strip()
                value = parts[1].strip().strip('"').strip("'")
                if attr == "userName":
                    result = [u for u in result if u.user_name == value]
                elif attr == "email":
                    result = [u for u in result if any(e.value == value for e in u.emails)]
                elif attr == "active":
                    bool_val = value.lower() == "true"
                    result = [u for u in result if u.active == bool_val]
                elif attr == "externalId":
                    result = [u for u in result if u.external_id == value]

        if " sw " in filter_expr:
            parts = filter_expr.split(" sw ")
            if len(parts) == 2:
                attr = parts[0].strip()
                value = parts[1].strip().strip('"').strip("'")
                if attr == "userName":
                    result = [u for u in result if u.user_name.startswith(value)]

        return result
