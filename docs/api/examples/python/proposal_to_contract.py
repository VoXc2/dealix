"""
Workflow 2: Proposal → Signed Contract.

Drafts a proposal, lists invoices, and creates a Stripe Checkout
session for an international tier. Wires only the API surface; no
LLM cost paid by the caller.
"""

from __future__ import annotations

import os

import httpx

BASE = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me").rstrip("/")
HEADERS = {"X-API-Key": os.environ.get("DEALIX_API_KEY", "")}


def list_invoices(tenant_id: str) -> list[dict]:
    r = httpx.get(
        f"{BASE}/api/v1/customers/{tenant_id}/invoices", headers=HEADERS, timeout=10
    )
    r.raise_for_status()
    return r.json().get("invoices", [])


def open_stripe_checkout(tenant_id: str, email: str) -> str:
    body = {
        "tenant_id": tenant_id,
        "plan": "growth",
        "amount_cents": 99900,
        "currency": "usd",
        "email": email,
        "success_url": "https://dealix.me/checkout/success",
        "cancel_url": "https://dealix.me/checkout/cancel",
        "mode": "payment",
    }
    r = httpx.post(
        f"{BASE}/api/v1/billing/checkout/stripe",
        headers={**HEADERS, "Content-Type": "application/json"},
        json=body,
        timeout=10,
    )
    if r.status_code == 503:
        raise RuntimeError("stripe not configured on this deployment")
    r.raise_for_status()
    return r.json()["url"]


if __name__ == "__main__":
    tid = os.environ["DEALIX_TENANT_ID"]
    print("invoices:", len(list_invoices(tid)))
    print("checkout:", open_stripe_checkout(tid, "buyer@example.com"))
