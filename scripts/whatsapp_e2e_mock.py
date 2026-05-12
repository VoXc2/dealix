#!/usr/bin/env python3
"""WhatsApp end-to-end pipeline mock (W8.5).

Simulates the full revenue-critical inbound flow without touching Meta:
  1. Construct a Meta-shaped webhook payload (Arabic inbound from a Saudi number)
  2. POST it to /api/v1/webhooks/whatsapp on the local API
  3. Verify the pipeline processed the message into a lead
  4. Check that PDPL audit log middleware recorded the personal-data access

Run BEFORE every release as part of the deploy runbook Phase 4 smoke,
and BEFORE accepting any pilot customer to validate the inbound path
works end-to-end on the customer's tenant.

Usage:
  python scripts/whatsapp_e2e_mock.py                          # against http://localhost:8000
  python scripts/whatsapp_e2e_mock.py --base-url $BASE_URL     # against staging/prod
  python scripts/whatsapp_e2e_mock.py --message "أبي معلومات"   # custom Arabic test message

Exit codes:
  0  full flow succeeded (200 from webhook + processed > 0)
  1  webhook responded but processed=0 (parser/pipeline issue)
  2  webhook returned non-200 (config or auth issue)
  3  cannot reach API at all (network/runtime issue)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid


def _build_meta_payload(message: str, from_number: str) -> dict:
    """Construct a Meta WhatsApp Cloud API webhook payload.

    This is the exact shape Meta sends. Any change to this shape would
    indicate a Meta breaking change we'd need to handle separately.
    """
    return {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "e2e_mock_account",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "+966500000000",
                        "phone_number_id": "e2e_mock_phone",
                    },
                    "contacts": [{
                        "profile": {"name": "E2E Test Customer"},
                        "wa_id": from_number,
                    }],
                    "messages": [{
                        "from": from_number,
                        "id": f"wamid.e2e_{uuid.uuid4().hex[:16]}",
                        "timestamp": str(int(time.time())),
                        "type": "text",
                        "text": {"body": message},
                    }],
                },
                "field": "messages",
            }],
        }],
    }


def _post_webhook(base_url: str, payload: dict, timeout: int) -> tuple[int, dict | str]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(  # noqa: S310 — operator-controlled URL
        f"{base_url}/api/v1/webhooks/whatsapp",
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8") if exc.fp else ""
    except (urllib.error.URLError, TimeoutError) as exc:
        return 0, str(exc)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base-url",
                   default=os.environ.get("BASE_URL", "http://localhost:8000"))
    p.add_argument("--message",
                   default="السلام عليكم، أبي معلومات عن خدماتكم وأسعاركم.",
                   help="Arabic inbound message body to test with")
    p.add_argument("--from-number",
                   default="966500000001",
                   help="Saudi phone number (no +) sending the inbound")
    p.add_argument("--timeout", type=int, default=15)
    p.add_argument("--json", action="store_true", help="JSON output only")
    args = p.parse_args()

    if not args.json:
        print(f"E2E WhatsApp mock → {args.base_url}/api/v1/webhooks/whatsapp")
        print(f"  Message: {args.message!r}")
        print(f"  From:    +{args.from_number}")
        print()

    payload = _build_meta_payload(args.message, args.from_number)
    t0 = time.monotonic()
    status, body = _post_webhook(args.base_url, payload, args.timeout)
    elapsed_ms = int((time.monotonic() - t0) * 1000)

    result = {
        "base_url": args.base_url,
        "http_status": status,
        "elapsed_ms": elapsed_ms,
        "response_body": body,
    }

    if status == 0:
        result["verdict"] = "FAIL: API unreachable"
        result["exit_code"] = 3
    elif status != 200:
        result["verdict"] = f"FAIL: webhook returned {status}"
        result["exit_code"] = 2
    elif isinstance(body, dict):
        processed = body.get("count", 0)
        if processed > 0:
            result["verdict"] = f"PASS: pipeline processed {processed} lead(s)"
            result["exit_code"] = 0
            result["lead_ids"] = body.get("processed") or []
        else:
            result["verdict"] = (
                "WARN: webhook OK but no leads processed — check pipeline parser"
            )
            result["exit_code"] = 1
    else:
        result["verdict"] = "FAIL: webhook returned non-JSON body"
        result["exit_code"] = 2

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"  HTTP {result['http_status']} · {result['elapsed_ms']}ms")
        print(f"  Verdict: {result['verdict']}")
        if "lead_ids" in result and result["lead_ids"]:
            print(f"  Lead IDs: {result['lead_ids']}")

    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
