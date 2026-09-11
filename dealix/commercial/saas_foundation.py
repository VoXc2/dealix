"""SaaS Foundation — full SaaS comprehensive, market control."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class TenantTier(StrEnum):
    FREE = "free"
    STARTER = "starter"
    GROWTH = "growth"
    ENTERPRISE = "enterprise"

class Tenant(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: str
    name: str
    tier: TenantTier = TenantTier.FREE
    sector: str = UNKNOWN
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    data_isolation_key: str = Field(default_factory=lambda: hashlib.sha256(str(datetime.now(UTC).timestamp()).encode()).hexdigest()[:12])
    billing_active: bool = False

class SaaSEntitlement(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: str
    max_users: int = 5
    max_projects: int = 3  # DeepWIP 3
    max_storage_gb: int = 10
    max_api_calls: int = 10000
    features: list[str] = Field(default_factory=lambda: ["diagnostic","proof_ledger","basic_support"])

class BillingRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str
    tenant_id: str
    amount_sar: float
    tier: TenantTier
    period: str = Field(default_factory=lambda: datetime.now(UTC).strftime("%Y-%m"))
    usage_api_calls: int = 0
    status: str = "pending"  # pending, paid, overdue
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

class SaaSControlPlane:
    def __init__(self) -> None:
        self.tenants: dict[str, Tenant] = {}
        self.entitlements: dict[str, SaaSEntitlement] = {}
        self.billing: list[BillingRecord] = []

    def create_tenant(self, name: str, sector: str, tier: TenantTier = TenantTier.FREE) -> Tenant:
        tid = f"tnt_{hashlib.sha256(name.encode()).hexdigest()[:8]}"
        tenant = Tenant(tenant_id=tid, name=name, sector=sector, tier=tier)
        self.tenants[tid] = tenant
        # Entitlement per tier
        ent_map = {
            TenantTier.FREE: SaaSEntitlement(tenant_id=tid, max_users=2, max_projects=1, max_storage_gb=5, max_api_calls=1000, features=["diagnostic"]),
            TenantTier.STARTER: SaaSEntitlement(tenant_id=tid, max_users=5, max_projects=3, max_storage_gb=10, max_api_calls=10000, features=["diagnostic","proof_ledger"]),
            TenantTier.GROWTH: SaaSEntitlement(tenant_id=tid, max_users=20, max_projects=5, max_storage_gb=100, max_api_calls=100000, features=["diagnostic","proof_ledger","advanced_analytics","priority_support"]),
            TenantTier.ENTERPRISE: SaaSEntitlement(tenant_id=tid, max_users=100, max_projects=10, max_storage_gb=1000, max_api_calls=1000000, features=["all"]),
        }
        self.entitlements[tid] = ent_map[tier]
        return tenant

    def bill(self, tenant_id: str, amount_sar: float) -> BillingRecord:
        tenant = self.tenants.get(tenant_id)
        if not tenant:
            raise ValueError("tenant not found")
        rec = BillingRecord(record_id=f"bill_{tenant_id}_{datetime.now(UTC).strftime('%Y%m')}", tenant_id=tenant_id, amount_sar=amount_sar, tier=tenant.tier)
        self.billing.append(rec)
        return rec

    def market_control_score(self) -> float:
        # SaaS comprehensive control: tenants * entitlements * 20 sectors coverage
        sectors_covered = len({t.sector for t in self.tenants.values() if t.sector != UNKNOWN})
        return round((len(self.tenants) * sectors_covered * len(self.entitlements)) / 10, 2) if self.tenants else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "tenants": len(self.tenants),
            "entitlements": len(self.entitlements),
            "billing": len(self.billing),
            "control_score": self.market_control_score(),
            "control_score_basis": "structural_counts_not_financial",
        }

__all__ = ["SaaSControlPlane", "Tenant", "TenantTier", "SaaSEntitlement", "BillingRecord", "UNKNOWN"]
