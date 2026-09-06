#!/usr/bin/env python3
"""Offline acceptance verifier for Dealix Voice Front Desk / GPT-Realtime-2.1."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"VOICE_FRONT_DESK=FAIL reason={message}")


def main() -> int:
    os.environ["VOICE_AI_ENABLED"] = "false"
    os.environ["VOICE_OUTBOUND_ENABLED"] = "false"
    os.environ["VOICE_RECORDING_ENABLED"] = "false"

    from api.routers.domains.webhooks import get_routers
    from api.security.api_key import PUBLIC_PREFIXES
    from dealix.voice_ai.front_desk import (
        VOICE_MODEL,
        VoiceAIConfig,
        build_realtime_tools,
        build_voice_instructions,
        get_voice_readiness,
    )

    checks = 0

    cfg = VoiceAIConfig.from_env()
    require(VOICE_MODEL == "gpt-realtime-2.1", "model_constant_not_2_1")
    require(cfg.model == "gpt-realtime-2.1", "runtime_model_not_locked_2_1")
    checks += 1

    require(cfg.enabled is False, "voice_must_default_fail_closed")
    require(cfg.outbound_enabled is False, "outbound_must_default_off")
    require(cfg.recording_enabled is False, "recording_must_default_off")
    checks += 1

    instructions = build_voice_instructions(cfg)
    for required in (
        "official Dealix AI Voice Front Desk",
        "Revenue + Proof + Command",
        "not Sami",
        "Never invent customers",
        "customer-specific quote",
        "save_qualification",
    ):
        require(required in instructions, f"missing_prompt_contract:{required}")
    checks += 1

    tool_names = {item["name"] for item in build_realtime_tools(cfg)}
    require(
        tool_names
        == {
            "lookup_dealix_capabilities",
            "get_booking_link",
            "save_qualification",
            "request_human_handoff",
        },
        "unexpected_tool_surface",
    )
    checks += 1

    prefixes = {route.prefix for route in get_routers()}
    require("/api/v1/webhooks/openai" in prefixes, "openai_webhook_router_not_registered")
    checks += 1

    require("/api/v1/webhooks/" in PUBLIC_PREFIXES, "webhook_prefix_not_public")
    checks += 1

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    require('"openai[realtime]>=3.8.0,<4"' in pyproject, "realtime_sdk_floor_missing")
    checks += 1

    readiness = get_voice_readiness(cfg)
    require(readiness["ready_for_inbound_sip"] is False, "readiness_must_be_false_without_enable")
    require(readiness["model"] == "gpt-realtime-2.1", "readiness_model_drift")
    checks += 1

    source_paths = [
        ROOT / "dealix/voice_ai/front_desk.py",
        ROOT / "api/routers/openai_realtime_webhook.py",
        ROOT / "docs/ops/VOICE_FRONT_DESK_OPENAI_REALTIME_2_1_AR.md",
    ]
    for path in source_paths:
        text = path.read_text(encoding="utf-8")
        require("sk-proj-" not in text and "sk-" not in text, f"possible_secret_literal:{path.name}")
    checks += 1

    require(
        (ROOT / "tests/unit/test_voice_front_desk.py").exists()
        and (ROOT / "tests/unit/test_openai_realtime_webhook.py").exists(),
        "voice_tests_missing",
    )
    checks += 1

    print(f"VOICE_FRONT_DESK_CHECKS={checks}")
    print("VOICE_FRONT_DESK_MODEL=gpt-realtime-2.1")
    print("VOICE_FRONT_DESK_EXTERNAL_EFFECTS=NONE")
    print("VOICE_FRONT_DESK=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
