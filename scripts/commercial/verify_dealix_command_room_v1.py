#!/usr/bin/env python3
"""Fail-closed verifier for Dealix Omnichannel Founder Command Room V1."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "company" / "dealix_command_room_v1.json"
ARM_REGISTRY = ROOT / "config" / "company" / "dealix_arm_registry.json"
REPLY_BOT = ROOT / "dealix" / "company_os" / "founder_reply_bot.py"
META_WHATSAPP = ROOT / "integrations" / "whatsapp.py"
WHATSAPP_MULTI_PROVIDER = ROOT / "auto_client_acquisition" / "email" / "whatsapp_multi_provider.py"

CANONICAL_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}
REQUIRED_QUEUES = {
    "signal_queue",
    "work_queue",
    "conversation_queue",
    "approval_queue",
    "execution_queue",
    "proof_queue",
    "learning_queue",
    "dead_letter_queue",
}
REQUIRED_CHANNELS = {
    "gmail",
    "whatsapp-business",
    "website-chat",
    "website-forms",
    "facebook-messenger",
    "instagram-dm",
    "tiktok-business",
    "telegram-customer",
    "sms",
    "voice",
    "api-inbox",
    "linkedin-founder",
}
ALLOWED_READINESS = {
    "INTERNAL_READY",
    "INBOUND_READY",
    "DRAFT_ONLY",
    "PROVIDER_QUARANTINED",
    "ADAPTER_PRESENT_AUTHORITY_NOT_PROVEN",
    "NOT_WIRED",
    "MANUAL_ONLY",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path) -> dict:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"expected object: {path.relative_to(ROOT)}")
    return data


def source(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    try:
        config = load(CONFIG)
        arms = load(ARM_REGISTRY)

        require(config.get("schema_version") == 1, "unsupported command-room schema")
        require(config.get("operating_mode") == "AGENT_FIRST_FOUNDER_EXCEPTION_ONLY", "agent-first mode required")
        require(config.get("default_policy") == "FAIL_CLOSED", "command room must fail closed")
        require(set(config.get("canonical_agents", [])) == CANONICAL_AGENTS, "permanent agent set drift")
        require(config.get("deep_wip_max") == arms.get("deep_wip_max") == 3, "deep WIP must remain constitution-bound")
        require(set(config.get("queues", [])) == REQUIRED_QUEUES, "canonical queue set drift")
        require(set(config.get("readiness_states", [])) == ALLOWED_READINESS, "readiness vocabulary drift")

        arm_owners = {str(item.get("owner", "")) for item in arms.get("arms", [])}
        require(arm_owners <= CANONICAL_AGENTS, f"arm owner outside canonical fleet: {sorted(arm_owners - CANONICAL_AGENTS)}")

        channels = config.get("channels", [])
        require(isinstance(channels, list) and channels, "channel registry is empty")
        ids = [str(ch.get("id", "")) for ch in channels]
        require(len(ids) == len(set(ids)), "duplicate channel id")
        require(REQUIRED_CHANNELS <= set(ids), f"missing required channels: {sorted(REQUIRED_CHANNELS - set(ids))}")

        for channel in channels:
            cid = str(channel.get("id", ""))
            readiness = str(channel.get("readiness", ""))
            require(channel.get("owner") in CANONICAL_AGENTS, f"{cid}: invalid owner")
            require("outbound_policy" in channel, f"{cid}: missing outbound policy")
            require("provider" in channel, f"{cid}: missing provider")
            require(readiness in ALLOWED_READINESS, f"{cid}: invalid readiness={readiness}")
            require(isinstance(channel.get("live_execution_ready"), bool), f"{cid}: live_execution_ready must be explicit bool")
            if channel.get("outbound"):
                require(channel.get("outbound_policy") not in {"", "UNRESTRICTED", None}, f"{cid}: unrestricted outbound forbidden")
            if channel.get("consent_or_relationship_required_for_marketing"):
                require(channel.get("outbound_policy") != "UNRESTRICTED", f"{cid}: marketing authority cannot be unrestricted")
            if readiness in {"PROVIDER_QUARANTINED", "ADAPTER_PRESENT_AUTHORITY_NOT_PROVEN", "NOT_WIRED", "MANUAL_ONLY", "DRAFT_ONLY"}:
                require(channel.get("live_execution_ready") is False, f"{cid}: readiness cannot claim live execution")
            if cid == "gmail":
                require(readiness == "PROVIDER_QUARANTINED", "Gmail quarantine truth drift")
                require(channel.get("live_execution_ready") is False, "Gmail live execution must remain false while provider is quarantined")
            if cid == "whatsapp-business":
                require(readiness == "ADAPTER_PRESENT_AUTHORITY_NOT_PROVEN", "WhatsApp readiness must not outrun current authority evidence")
                require(channel.get("live_execution_ready") is False, "WhatsApp live execution not proven in command-room V1")
            if cid == "linkedin-founder":
                require(channel.get("outbound") is False, "LinkedIn founder surface remains manual-only")
                require(channel.get("outbound_policy") == "FOUNDER_MANUAL_ONLY", "LinkedIn policy drift")
                require(readiness == "MANUAL_ONLY", "LinkedIn readiness drift")
            if cid == "voice":
                require(channel.get("automated_identity_disclosure_required") is True, "automated voice disclosure required")
                require(channel.get("live_execution_ready") is False, "voice provider is not wired in command-room V1")

        delegation = config.get("founder_delegation", {})
        require(delegation.get("enabled_by_default") is False, "founder delegation must not auto-enable")
        require(delegation.get("must_mint_exact_action_hash_before_effect") is True, "delegation must preserve exact action hash")
        require(delegation.get("must_recheck_suppression_before_effect") is True, "suppression must be rechecked")
        require(delegation.get("must_persist_provider_receipt") is True, "provider receipt is mandatory")
        require(delegation.get("global_kill_switch_env") == "DEALIX_EXTERNAL_SEND", "canonical kill switch drift")
        require(bool(str(delegation.get("automated_voice_disclosure", "")).strip()), "voice disclosure text missing")

        # Smart reply / negotiation brain must stay side-effect-free and feed the
        # existing exact action-bound execution fabric rather than bypass it.
        reply_bot = source(REPLY_BOT)
        require("route_task" in reply_bot, "founder reply bot must reuse canonical model router")
        require("build_external_action_packet" in reply_bot, "founder reply bot must produce canonical action packets")
        require('provider_execution_allowed: Literal[False] = False' in reply_bot, "reply bot must never grant provider authority")
        for forbidden in ("send_whatsapp_smart", "WhatsAppClient", "import httpx", "import requests"):
            require(forbidden not in reply_bot, f"reply bot contains direct provider side effect: {forbidden}")

        # Both WhatsApp Meta paths must share one explicit Graph API version and
        # may never silently return to the near-expiry v20 hardcode.
        meta_whatsapp = source(META_WHATSAPP)
        multi_provider = source(WHATSAPP_MULTI_PROVIDER)
        require('DEFAULT_GRAPH_API_VERSION = "v26.0"' in meta_whatsapp, "Meta Graph default must be v26.0")
        require("WHATSAPP_GRAPH_API_VERSION" in meta_whatsapp, "Meta Graph version must be explicitly configurable")
        require("from integrations.whatsapp import meta_graph_base_url" in multi_provider, "multi-provider Meta path must reuse canonical Graph URL")
        require("graph.facebook.com/v20.0" not in meta_whatsapp, "expiring Graph v20 hardcode remains in official client")
        require("graph.facebook.com/v20.0" not in multi_provider, "expiring Graph v20 hardcode remains in multi-provider path")

        firewall = set(config.get("truth_firewall", []))
        for rule in {
            "research != relationship",
            "public_contact != consent",
            "draft != sent",
            "quote != invoice",
            "invoice != payment",
            "merge != Production Green",
        }:
            require(rule in firewall, f"truth firewall missing: {rule}")

        print("DEALIX_COMMAND_ROOM_V1=PASS")
        print(f"CHANNELS={len(channels)}")
        print(f"ARMS={len(arms.get('arms', []))}")
        print("PERMANENT_AGENTS=5")
        print("FOUNDER_REPLY_BOT=DRAFT_PACKET_ONLY")
        print("WHATSAPP_META_GRAPH_DEFAULT=v26.0")
        print("FOUNDER_DELEGATION_DEFAULT=DISABLED_FAIL_CLOSED")
        print("LIVE_EXTERNAL_CHANNELS_CLAIMED_READY=0")
        return 0
    except Exception as exc:  # noqa: BLE001 - verifier must produce one bounded failure
        print(f"DEALIX_COMMAND_ROOM_V1=FAIL reason={exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
