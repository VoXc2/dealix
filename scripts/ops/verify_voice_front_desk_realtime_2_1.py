#!/usr/bin/env python3
"""Offline acceptance verifier for Dealix Voice Front Desk / GPT-Realtime-2.1."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Entry-point invariant: this verifier must work from any cwd.  Executing a
# script under scripts/ops directly otherwise leaves only scripts/ops on
# sys.path and makes imports of api/ and dealix/ depend on PYTHONPATH.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"VOICE_FRONT_DESK=FAIL reason={message}")


def main() -> int:
    os.environ["VOICE_AI_ENABLED"] = "false"
    os.environ["VOICE_OUTBOUND_ENABLED"] = "false"
    os.environ["VOICE_RECORDING_ENABLED"] = "false"

    from api.routers.domains.ops import get_routers as get_ops_routers
    from api.routers.domains.webhooks import get_routers as get_webhook_routers
    from api.security.api_key import PUBLIC_PREFIXES
    from dealix.voice_ai.front_desk import (
        VoiceAIConfig,
        build_realtime_tools,
        build_voice_instructions,
        get_voice_readiness,
    )
    from dealix.voice_ai.sip_runtime import (
        VOICE_MODEL,
        VOICE_OUTPUT_VOICE,
        canonical_positioning_overlay,
        normalized_reasoning_effort,
        realtime_audio_config,
        realtime_truncation_config,
    )

    checks = 0

    cfg = VoiceAIConfig.from_env()
    require(VOICE_MODEL == "gpt-realtime-2.1", "model_constant_not_2_1")
    require(cfg.model == "gpt-realtime-2.1", "runtime_model_not_locked_2_1")
    require(VOICE_OUTPUT_VOICE == "cedar", "voice_not_pinned_to_cedar")
    checks += 1

    require(cfg.enabled is False, "voice_must_default_fail_closed")
    require(cfg.outbound_enabled is False, "outbound_must_default_off")
    require(cfg.recording_enabled is False, "recording_must_default_off")
    checks += 1

    instructions = f"{build_voice_instructions(cfg)}\n{canonical_positioning_overlay()}"
    for required in (
        "official Dealix AI Voice Front Desk",
        "Revenue + Proof + Command",
        "not Sami",
        "Never invent customers",
        "customer-specific quote",
        "save_qualification",
        "Dealix — AI Business Operating System",
        "Signals into Action. Execution with Governance. Measurable Outcomes.",
        "From Opportunity to Outcome.",
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

    audio = realtime_audio_config()
    require(audio["output"]["voice"] == "cedar", "cedar_voice_missing")
    require(audio["input"]["turn_detection"]["type"] == "semantic_vad", "semantic_vad_missing")
    require(
        audio["input"]["turn_detection"]["interrupt_response"] is True,
        "barge_in_not_enabled",
    )
    require(normalized_reasoning_effort(cfg) == "medium", "reasoning_default_not_medium")
    truncation = realtime_truncation_config()
    require(truncation["type"] == "retention_ratio", "retention_truncation_missing")
    require(truncation["token_limits"]["post_instructions"] == 16000, "context_budget_drift")
    checks += 1

    webhook_prefixes = {route.prefix for route in get_webhook_routers()}
    require(
        "/api/v1/webhooks/openai" in webhook_prefixes,
        "openai_webhook_router_not_registered",
    )
    checks += 1

    ops_prefixes = {route.prefix for route in get_ops_routers()}
    require("/api/v1/ops/voice-ai" in ops_prefixes, "voice_ops_router_not_registered")
    checks += 1

    require("/api/v1/webhooks/" in PUBLIC_PREFIXES, "webhook_prefix_not_public")
    require("/api/v1/ops/" not in PUBLIC_PREFIXES, "ops_prefix_must_not_be_public")
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
        ROOT / "dealix/voice_ai/sip_runtime.py",
        ROOT / "api/routers/openai_realtime_webhook.py",
        ROOT / "api/routers/ops_voice_ai.py",
        ROOT / "docs/ops/VOICE_FRONT_DESK_OPENAI_REALTIME_2_1_AR.md",
    ]
    for path in source_paths:
        text = path.read_text(encoding="utf-8")
        require("sk-proj-" not in text and "sk-" not in text, f"possible_secret_literal:{path.name}")
    checks += 1

    required_tests = [
        ROOT / "tests/unit/test_voice_front_desk.py",
        ROOT / "tests/unit/test_openai_realtime_webhook.py",
        ROOT / "tests/unit/test_voice_sip_runtime.py",
        ROOT / "tests/unit/test_ops_voice_ai.py",
    ]
    require(all(path.exists() for path in required_tests), "voice_tests_missing")
    checks += 1

    print(f"VOICE_FRONT_DESK_CHECKS={checks}")
    print("VOICE_FRONT_DESK_MODEL=gpt-realtime-2.1")
    print("VOICE_FRONT_DESK_VOICE=cedar")
    print("VOICE_FRONT_DESK_PUBLIC_READINESS=false")
    print("VOICE_FRONT_DESK_EXTERNAL_EFFECTS=NONE")
    print("VOICE_FRONT_DESK=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
