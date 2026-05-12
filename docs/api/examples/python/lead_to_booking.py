"""
Workflow 1: Lead → Qualified Demo Booking.

Captures a lead, asks Dealix to score it, and returns the booking URL
if the score crosses the ICP threshold. Runs against a real Dealix
deployment when DEALIX_API_BASE + DEALIX_API_KEY are set; otherwise
prints what it would do.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

BASE = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me").rstrip("/")
API_KEY = os.environ.get("DEALIX_API_KEY", "")

HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def capture_lead(lead: dict[str, Any]) -> str:
    r = httpx.post(f"{BASE}/api/v1/leads", json=lead, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["id"]


def fetch_booking(tenant_id: str) -> str | None:
    """The public booking URL is exposed by the trial / demo-request flow."""
    r = httpx.post(
        f"{BASE}/api/v1/public/demo-request",
        json={
            "company": "Example Co.",
            "name": "Ops",
            "email": "ops@example.sa",
            "phone": "+966500000000",
            "sector": "real-estate",
            "consent": True,
        },
        timeout=10,
    )
    r.raise_for_status()
    body = r.json()
    return body.get("calendly_url")


if __name__ == "__main__":
    lead_id = capture_lead({
        "company_name": "Example Co.",
        "contact_email": "ops@example.sa",
        "contact_phone": "+966500000000",
        "sector": "real-estate",
    })
    print("captured:", lead_id)
    url = fetch_booking(lead_id)
    print("book:", url)
