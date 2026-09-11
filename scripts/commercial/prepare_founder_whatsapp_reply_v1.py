#!/usr/bin/env python3
"""Prepare one Founder Office WhatsApp reply from a normalized inbound event.

Input and output are files so n8n / queue workers can call this process without
placing customer message bodies or phone numbers in command arguments or stdout.
This process never invokes a messaging provider.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.company_os.founder_reply_bot import (
    InboundConversationEvent,
    prepare_founder_reply,
)


def _args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Normalized inbound event JSON file")
    parser.add_argument("--out", required=True, help="Destination JSON receipt/draft file")
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Disable cloud fallback and require the canonical local model path",
    )
    return parser.parse_args()


def _load_event(path: Path) -> InboundConversationEvent:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("input must be one JSON object")
    return InboundConversationEvent.model_validate(payload)


def main() -> int:
    args = _args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.out).expanduser().resolve()

    event = _load_event(input_path)
    result = prepare_founder_reply(
        event,
        cloud_fallback_enabled=not args.local_only,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_name(f".{output_path.name}.{os.getpid()}.tmp")
    temp_path.write_text(
        json.dumps(result.model_dump(mode="json"), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    os.chmod(temp_path, 0o600)
    temp_path.replace(output_path)

    print("FOUNDER_WHATSAPP_REPLY_PREPARED=1")
    print(f"EVENT_ID={event.event_id}")
    print(f"INTENT={result.intent}")
    print(f"LANGUAGE={result.language}")
    print(f"MODEL_STATUS={result.model_status}")
    print(f"APPROVAL_PACKET_READY={int(result.approval_packet is not None)}")
    print("PROVIDER_EXECUTION_ALLOWED=0")
    print(f"NEXT_ACTION={result.next_action}")
    print(f"OUTPUT={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
