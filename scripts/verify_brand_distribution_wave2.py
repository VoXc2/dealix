#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative: str) -> dict:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"MISSING={relative}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"INVALID_JSON={relative}:{exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"WAVE2_FAIL={message}")


def main() -> int:
    launch = (ROOT / "dealix/config/first_launch_offer_gate.yaml").read_text(encoding="utf-8")
    require("external_send_allowed: false" in launch, "current main external send authority changed")
    require("audience: warm_consented_only" in launch, "current main audience authority changed")

    brand = load_json("data/brand/dealix_brand_system_v2.json")
    require(brand.get("schema") == "dealix.brand-system.v2", "brand schema")
    colors = brand.get("colors", {})
    require(colors.get("ink_navy") == "#0F172A", "Ink Navy token")
    require(colors.get("deep_teal") == "#164E63", "Deep Teal token")
    require(colors.get("signal_cyan") == "#22D3EE", "Signal Cyan token")
    require(brand.get("typography", {}).get("arabic_primary") == "IBM Plex Sans Arabic", "Arabic font")
    require(brand.get("typography", {}).get("latin_primary") == "Inter", "Latin font")
    require(brand.get("governance", {}).get("canva_is_renderer_not_authority") is True, "Canva authority boundary")

    channels = load_json("data/commercial/channel_readiness_registry.json")
    require(channels.get("global_rules", {}).get("phone_is_not_global_blocker") is True, "phone global blocker")
    channel_map = channels.get("channels", {})
    require(channel_map.get("whatsapp", {}).get("phone_dependency") is True, "WhatsApp phone dependency")
    for name, row in channel_map.items():
        if name != "whatsapp":
            require(row.get("phone_dependency") is False, f"unexpected phone dependency: {name}")
    require(channels.get("activation_switches", {}).get("PAID_MEDIA") == "PAUSED_DRAFT_ONLY", "paid media authority")

    canva = load_json("data/commercial/canva_asset_audit_2026-08-28.json")
    assets = {row.get("canva_design_id"): row for row in canva.get("assets", [])}
    legacy = assets.get("DAHPFUhUr1g", {})
    require(legacy.get("classification") == "BLOCKED_FOR_EXTERNAL_USE", "legacy Canva deck not blocked")
    require(legacy.get("external_use") == "BLOCKED", "legacy Canva external use")

    content_schema = load_json("data/commercial/content_asset_registry.schema.json")
    item = content_schema["properties"]["assets"]["items"]
    required = set(item.get("required", []))
    expected = {"content_id", "source_evidence_refs", "brand_version", "claim_version", "channel", "publish_class", "status"}
    require(expected.issubset(required), "content registry required evidence/governance fields")

    identity = load_json("data/commercial/platform_identity_matrix.json")
    rules = identity.get("rules", {})
    require(rules.get("website") == "https://dealix.me/", "canonical website")
    require(rules.get("public_phone_placeholder") is False, "phone placeholder")
    require(rules.get("phone_cta_state") == "DEFERRED_PHONE_ACTIVATION", "phone state")
    require(rules.get("primary_cta_now") == "Free Mini Diagnostic", "current CTA")

    quarantine = load_json("data/commercial/legacy_marketing_quarantine.json")
    require(quarantine.get("authority", {}).get("public_fixed_pilot_price_authorized") is False, "legacy public price authority")
    blocked = {str(x).lower() for x in quarantine.get("blocked_tokens_case_insensitive", [])}
    require("guaranteed revenue" in blocked and "7-day pilot" in blocked and "499 sar" in blocked, "legacy token firewall")

    seeds = load_json("data/commercial/content_seed_pack_2026-08-28.json")
    require(seeds.get("schema") == "dealix.content-asset-registry.v1", "seed pack schema")
    seed_assets = seeds.get("assets", [])
    require(len(seed_assets) >= 6, "seed pack minimum asset count")
    for seed in seed_assets:
        require(seed.get("status") == "DRAFT", f"seed not draft: {seed.get('content_id')}")
        require(seed.get("published_url") is None, f"seed falsely published: {seed.get('content_id')}")
        require(seed.get("provider_receipt_ref") is None, f"seed has provider receipt before execution: {seed.get('content_id')}")
        if seed.get("content_id", "").startswith(("DX-BIG5-", "DX-LEAP-", "DX-AI-")):
            require(seed.get("freshness", {}).get("recheck_before_publish") is True, f"event seed freshness: {seed.get('content_id')}")

    experiments = load_json("data/commercial/marketing_experiment_portfolio.json")
    experiment_ids = {row.get("id") for row in experiments.get("experiments", [])}
    required_experiments = {
        "BIG5_QR_DIAGNOSTIC",
        "BIG5_SAME_DAY_FOLLOWUP",
        "LEAP_INBOUND_NETWORKING",
        "FOUNDER_LINKEDIN_PROBLEM_TEARDOWN",
        "PROOF_LED_ARTICLE_REUSE",
    }
    require(required_experiments.issubset(experiment_ids), "Wave 2 must reuse canonical marketing experiment portfolio")

    manifest = load_json("data/commercial/marketing_agent_bootstrap_manifest.json")
    order = {row["path"]: row["priority"] for row in manifest.get("load_order", [])}
    require(order["dealix/config/first_launch_offer_gate.yaml"] < order["data/brand/dealix_brand_system_v2.json"], "authority must load before brand")
    require(order["data/brand/dealix_brand_system_v2.json"] < order["data/commercial/canva_asset_audit_2026-08-28.json"], "brand must load before Canva")
    require("data/commercial/content_seed_pack_2026-08-28.json" in order, "seed pack absent from bootstrap")
    hard_rules = "\n".join(manifest.get("hard_rules", []))
    require("Current main authority overrides" in hard_rules, "Draft authority firewall")
    require("Phone readiness may block WhatsApp only" in hard_rules, "phone isolation rule")
    require("freshness recheck" in hard_rules, "event freshness rule")

    print("DEALIX_BRAND_DISTRIBUTION_WAVE2=PASS")
    print(f"CHANNELS={len(channel_map)}")
    print(f"CANVA_ASSETS={len(assets)}")
    print(f"CONTENT_SEEDS={len(seed_assets)}")
    print(f"CANONICAL_EXPERIMENTS={len(experiment_ids)}")
    print("MAIN_EXTERNAL_SEND_AUTHORITY=FAIL_CLOSED")
    print("PHONE_GLOBAL_BLOCKER=NO")
    print("DUPLICATE_EXPERIMENT_SYSTEM=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
