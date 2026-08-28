#!/usr/bin/env python3
"""Legacy Moyasar adapter.

Live invoice/payment-link creation is intentionally fail-closed until Dealix has a
single durable Controlled Execution path that can consume and revalidate an exact,
revocable payment execution-authority receipt.
"""

import base64
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "company" / "runtime"

PAYMENT_WRITE_BLOCK_REASON = "LIVE_PAYMENT_REQUIRES_DURABLE_CONTROLLED_EXECUTION_AUTHORITY"


class MoyasarPayments:
    """Compatibility adapter for Moyasar provider reads and fail-closed writes."""

    def __init__(self):
        self.api_key = os.getenv("MOYASAR_API_KEY", "")
        self.api_secret = os.getenv("MOYASAR_API_SECRET", "")
        self.base_url = "https://api.moyasar.com/v1"
        # Retained as an observable legacy setting only. It is never execution authority.
        self.live_mode = os.getenv("MOYASAR_LIVE_MODE", "false").lower() == "true"

    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_secret)

    def get_auth_header(self) -> dict:
        credentials = f"{self.api_key}:{self.api_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

    def create_payment_link(
        self,
        customer_email: str,
        customer_phone: str,
        customer_name: str,
        description: str,
        amount_sar: Optional[int],
        pilot_id: Optional[str] = None,
    ) -> dict:
        """Fail closed for all provider write operations.

        Presence of provider credentials, ``MOYASAR_LIVE_MODE``, a quote ID, or a
        caller-supplied amount is not durable Dealix payment execution authority.
        This compatibility adapter must not POST to Moyasar.
        """
        del customer_email, customer_phone, customer_name, description
        return {
            "status": "blocked",
            "reason": PAYMENT_WRITE_BLOCK_REASON,
            "payment_url": None,
            "amount_sar": amount_sar,
            "pilot_id": pilot_id,
            "provider_write_executed": False,
            "execution_authority_created": False,
            "payment_proof_created": False,
            "revenue_created": False,
            "legacy_live_mode_observed": self.live_mode,
        }

    def check_payment_status(self, invoice_id: str) -> dict:
        """Read provider invoice status as raw evidence only.

        A provider status response is not by itself Dealix revenue truth. The
        canonical payment/proof path must bind provider evidence to the approved
        customer-specific quote and verify it before revenue is recognized.
        """
        if not self.is_configured():
            return {
                "status": "not_configured",
                "error": "Moyasar API not configured",
                "evidence_class": "PROVIDER_STATUS_NOT_REVENUE_PROOF",
            }

        url = f"{self.base_url}/invoices/{invoice_id}"
        headers = self.get_auth_header()

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            invoice = data.get("invoice", {})

            return {
                "status": invoice.get("status"),
                "invoice_id": invoice.get("id"),
                "amount_sar": invoice.get("amount", 0) / 100,
                "paid_amount_sar": invoice.get("paid_amount", 0) / 100,
                "customer_name": invoice.get("customer", {}).get("name"),
                "created_at": invoice.get("created_at"),
                "updated_at": invoice.get("updated_at"),
                "evidence_class": "PROVIDER_STATUS_NOT_REVENUE_PROOF",
                "revenue_verified": False,
            }
        except requests.exceptions.RequestException as exc:
            return {
                "status": "error",
                "error": str(exc),
                "evidence_class": "PROVIDER_STATUS_NOT_REVENUE_PROOF",
            }

    def create_pilot_invoice(
        self,
        customer_name: str,
        company_name: str,
        customer_email: str,
        customer_phone: str,
        pilot_id: str,
        price_sar: Optional[int] = None,
    ) -> dict:
        """Compatibility wrapper that cannot create a live customer invoice.

        No default/fixed Pilot price or retired delivery duration is authoritative.
        A price, when supplied by an old caller, remains inert input and cannot
        authorize a provider write.
        """
        return self.create_payment_link(
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_name=customer_name,
            description=f"Customer-specific Dealix quote for {company_name}",
            amount_sar=price_sar,
            pilot_id=pilot_id,
        )

    def log_payment(self, payment_info: dict) -> Path:
        """Log a local payment evidence record; this never proves revenue."""
        log_path = RUNTIME_DIR / "payments.jsonl"
        with open(log_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(payment_info, ensure_ascii=False) + "\n")
        return log_path


def main() -> int:
    print("Moyasar legacy adapter: provider writes are fail-closed")
    print(
        json.dumps(
            {
                "status": "blocked",
                "reason": PAYMENT_WRITE_BLOCK_REASON,
                "provider_write_executed": False,
                "payment_proof_created": False,
                "revenue_created": False,
                "checked_at": datetime.now().isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
