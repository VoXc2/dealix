"""
Workflow 3: Onboarded Customer → Healthy / Renewing.

Drives the four-step self-serve onboarding API, then reads the tenant
health summary that the daily Inngest watcher uses to flag at-risk
customers.
"""

from __future__ import annotations

import os

import httpx

BASE = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me").rstrip("/")


def run_wizard(email: str, company: str) -> str:
    start = httpx.post(
        f"{BASE}/api/v1/onboarding/start",
        json={"email": email, "company": company, "name": "Owner", "locale": "ar"},
        timeout=10,
    ).json()
    tenant_id = start["tenant_id"]

    httpx.post(
        f"{BASE}/api/v1/onboarding/integrations",
        json={"onboarding_id": tenant_id, "integrations": ["hubspot", "whatsapp"]},
        timeout=10,
    )
    httpx.post(
        f"{BASE}/api/v1/onboarding/dpa",
        json={"onboarding_id": tenant_id, "accept": True, "signer_name": "Owner"},
        timeout=10,
    )
    final = httpx.post(
        f"{BASE}/api/v1/onboarding/finalize",
        json={"onboarding_id": tenant_id, "plan": "starter"},
        timeout=10,
    ).json()
    print("api key (one-time):", final["api_key"][:14], "...")
    return tenant_id


def health(tenant_id: str) -> dict:
    api_key = os.environ.get("DEALIX_API_KEY", "")
    r = httpx.get(
        f"{BASE}/api/v1/customer-success/tenant-health/{tenant_id}",
        headers={"X-API-Key": api_key},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    tid = run_wizard("owner@example.sa", "Example Co.")
    print("health:", health(tid))
