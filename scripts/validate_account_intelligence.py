#!/usr/bin/env python3
"""
Dealix Account Intelligence Validator

Validates the Account Intelligence-to-Revenue Factory data against its schemas
and enforces the quality + safety gates documented in:
  - docs/account_intelligence/ACCOUNT_PACK_OUTPUT_CONTRACT_AR.md
  - docs/account_intelligence/EVIDENCE_LEVELS_AR.md
  - docs/contacts/CONTACT_DISCOVERY_POLICY_AR.md
  - docs/security/EXTERNAL_CONTENT_UNTRUSTED_AR.md

It is dependency-free (no jsonschema needed) so it runs anywhere with python3.
It also computes the Top-100 scoring model so reports use real numbers.

Exit code 0 = all CRITICAL checks passed, 1 = at least one CRITICAL failure.
"""

import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SCHEMAS = BASE / "schemas"
DATA = BASE / "data"
REPORTS = BASE / "reports"
DOCS = BASE / "docs"

# ---------------------------------------------------------------------------
# Canonical configuration (single source of truth, mirrors docs/systems)
# ---------------------------------------------------------------------------

SYSTEMS = {
    "revenue_os": {
        "name": "Revenue Operating System",
        "sprint": "Revenue Leakage Sprint",
        "price": 4500,
        "quota": 100,
        "roles": ["head of sales", "sales", "founder", "ceo", "gm",
                  "general manager", "managing director", "marketing manager", "marketing"],
    },
    "executive_command_os": {
        "name": "Executive Command OS",
        "sprint": "Daily Command Sprint",
        "price": 5500,
        "quota": 70,
        "roles": ["founder", "ceo", "gm", "general manager", "managing director",
                  "operations", "coo", "partner"],
    },
    "followup_recovery_os": {
        "name": "Follow-up Recovery OS",
        "sprint": "7-Day Follow-up Recovery Sprint",
        "price": 3500,
        "quota": 90,
        "roles": ["sales manager", "sales", "marketing manager", "marketing",
                  "founder", "head of sales"],
    },
    "whatsapp_client_os": {
        "name": "WhatsApp Client OS",
        "sprint": "WhatsApp Flow Sprint",
        "price": 4500,
        "quota": 70,
        "roles": ["operations", "customer service", "customer experience",
                  "support", "founder", "clinic manager", "branch manager"],
    },
    "proposal_proof_os": {
        "name": "Proposal & Proof OS",
        "sprint": "Proposal & Proof Sprint",
        "price": 3000,
        "quota": 70,
        "roles": ["founder", "bd", "business development", "sales lead", "sales",
                  "marketing manager", "marketing", "partner", "ceo"],
    },
}

# Arabic + English hedging language required for low-evidence (L0/L1) claims.
HEDGES = ["غالبًا", "غالباً", "قد ", "يُحتمل", "يحتمل", "عادةً", "عادة",
          "في الغالب", "في هذا النوع", "ربما", "يميل", "نعتقد", "احتمال",
          "likely", "probably", "often", "typically", "may ", "tend", "usually"]

# Absolute, unproven accusations that must never appear (especially at L0/L1).
BANNED_ABSOLUTE = ["واضح أن عندكم", "أنتم تخسرون", "فريقكم لا يتابع",
                   "أنتم تفقدون", "you are losing", "your team fails"]

# Guarantee language that must never appear in any outbound copy.
BANNED_GUARANTEE = ["نضمن", "مضمون", "نتيجة مؤكدة", "بنسبة 100", "100%",
                    "guarantee", "guaranteed"]

# Internal artifacts that must never leak into outbound email copy.
BANNED_INTERNAL = list(SYSTEMS.keys()) + [".md", ".jsonl", "schema.json",
                                          "ACCOUNT_", "CH-0", "L0", "L1", "CC0"]

RE_FWD_PREFIXES = ("re:", "fwd:", "fw:", "رد:", "إعادة توجيه:")

EVIDENCE_LEVELS = ["L0", "L1", "L2", "L3", "L4"]
CONTACT_CONFIDENCE = ["CC0", "CC1", "CC2", "CC3"]

# ---------------------------------------------------------------------------
# Result collection
# ---------------------------------------------------------------------------

results = []  # (severity, name, ok, detail)


def record(name, ok, detail="", severity="CRITICAL"):
    results.append((severity, name, ok, detail))


# ---------------------------------------------------------------------------
# Minimal JSON-Schema validator (subset: type/enum/const/required/properties/
# items/minItems/minLength/minimum/maximum/additionalProperties)
# ---------------------------------------------------------------------------

def _type_ok(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    return True


def validate_schema(instance, schema, path="$"):
    errors = []

    if "type" in schema:
        types = schema["type"]
        if isinstance(types, str):
            types = [types]
        if not any(_type_ok(instance, t) for t in types):
            errors.append(f"{path}: expected type {schema['type']}, got {type(instance).__name__}")
            return errors  # type mismatch -> stop deeper checks

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum")

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: value {instance!r} != const {schema['const']!r}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength {schema['minLength']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: {instance} > maximum {schema['maximum']}")

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required '{req}'")
        props = schema.get("properties", {})
        if schema.get("additionalProperties", True) is False:
            for key in instance:
                if key not in props:
                    errors.append(f"{path}: additional property '{key}' not allowed")
        for key, val in instance.items():
            if key in props:
                errors.extend(validate_schema(val, props[key], f"{path}.{key}"))

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        if "items" in schema:
            for i, item in enumerate(instance):
                errors.extend(validate_schema(item, schema["items"], f"{path}[{i}]"))

    return errors


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            rows.append((n, json.loads(line)))
    return rows


# ---------------------------------------------------------------------------
# Scoring model (Top-100)
# ---------------------------------------------------------------------------

def score_pack(p):
    ev = p["evidence_level"]
    cc = p.get("contact_confidence", "CC0")
    risk = p["risk_level"]
    has_signal = bool(p.get("buying_signal"))
    has_services = bool(p.get("services_detected"))

    pain = min(25, {"L0": 8, "L1": 14, "L2": 20, "L3": 23, "L4": 25}[ev] + (2 if has_signal else 0))
    contact = {"CC0": 0, "CC1": 10, "CC2": 15, "CC3": 20}[cc]
    if p.get("best_contact_route") == "none_found":
        contact = 0
    fit = {"L0": 12, "L1": 16, "L2": 18, "L3": 20, "L4": 20}[ev]
    atp = min(15, {"low": 12, "medium": 9, "high": 5}[risk] + (3 if has_services else 0))
    evidence = {"L0": 2, "L1": 5, "L2": 8, "L3": 9, "L4": 10}[ev]
    low_risk = {"low": 10, "medium": 6, "high": 2}[risk]

    components = {
        "pain_clarity": pain,
        "contact_availability": contact,
        "system_fit": fit,
        "ability_to_pay": atp,
        "evidence_level": evidence,
        "low_risk": low_risk,
    }
    total = sum(components.values())

    if p.get("best_contact_route") == "none_found" or p.get("status") == "do_not_contact":
        tier = "hold"
    elif total >= 78 and contact >= 10:
        tier = "top_20_send"
    elif total >= 66:
        tier = "top_30_call"
    elif total >= 50:
        tier = "top_100"
    else:
        tier = "backlog"
    return components, total, tier


def role_valid(role, system):
    rl = role.lower()
    return any(tok in rl for tok in SYSTEMS[system]["roles"])


def contains_any(text, needles):
    t = (text or "")
    return [n for n in needles if n in t]


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def main():
    print("=" * 84)
    print("  DEALIX ACCOUNT INTELLIGENCE VALIDATOR")
    print("=" * 84)

    # Load schemas
    try:
        pack_schema = load_json(SCHEMAS / "account_intelligence_pack.schema.json")
        channel_schema = load_json(SCHEMAS / "contact_channel.schema.json")
        discovery_schema = load_json(SCHEMAS / "contact_discovery.schema.json")
        scoring_schema = load_json(SCHEMAS / "account_scoring.schema.json")
        proposal_schema = load_json(SCHEMAS / "mini_proposal.schema.json")
    except Exception as e:  # noqa: BLE001
        print(f"FATAL: could not load schemas: {e}")
        return 1

    # Load data
    packs = load_jsonl(DATA / "account_intelligence" / "account_packs.jsonl")
    channels = load_jsonl(DATA / "contacts" / "contact_channels.jsonl")
    discovery = load_jsonl(DATA / "contacts" / "contact_discovery.jsonl")
    proposals = load_jsonl(DATA / "proposals" / "mini_proposals.jsonl")

    print(f"  Loaded: {len(packs)} packs, {len(channels)} channels, "
          f"{len(discovery)} discovery records, {len(proposals)} mini proposals\n")

    # Index channels by company
    channels_by_company = {}
    channel_ids = set()
    for n, ch in channels:
        channels_by_company.setdefault(ch["company_name"], []).append(ch)
        channel_ids.add(ch["channel_id"])

    # --- Check: distribution sums to 400
    total_quota = sum(s["quota"] for s in SYSTEMS.values())
    record("Nightly distribution sums to 400", total_quota == 400,
           f"sum={total_quota}")

    # --- Schema validation: channels
    ch_errors = []
    for n, ch in channels:
        ch_errors += [f"channel line {n}: {e}" for e in validate_schema(ch, channel_schema)]
        if ch.get("is_public") is not True:
            ch_errors.append(f"channel line {n}: is_public must be true")
    record("Contact channels validate against schema (+ all public)",
           not ch_errors, "; ".join(ch_errors[:6]))

    # --- Schema validation: discovery
    disc_errors = []
    for n, d in discovery:
        disc_errors += [f"discovery line {n}: {e}" for e in validate_schema(d, discovery_schema)]
        if d["status"] in ("role_only", "no_public_channel") and d["person_found"]:
            disc_errors.append(f"discovery line {n}: person_found true under {d['status']}")
        if d["person_found"] is False and d.get("person_name"):
            disc_errors.append(f"discovery line {n}: person_name set while person_found false")
        if d["best_contact_route"] == "none_found" and d["channels_found"]:
            disc_errors.append(f"discovery line {n}: none_found but channels listed")
        if not role_valid(d["target_role"], d["recommended_system"]):
            disc_errors.append(f"discovery line {n}: role '{d['target_role']}' invalid for {d['recommended_system']}")
    record("Contact discovery validates (role targeting + no invented names)",
           not disc_errors, "; ".join(disc_errors[:6]))

    # --- Schema validation: packs + all the content gates
    pack_schema_errors = []
    missing_system = []
    bad_role = []
    invented_contact = []
    hedge_errors = []
    guarantee_errors = []
    absolute_errors = []
    subject_errors = []
    internal_leak = []
    bad_channel_ref = []
    graceful_errors = []

    scoring_records = []

    for n, p in packs:
        pack_schema_errors += [f"pack line {n} ({p.get('company_name','?')}): {e}"
                               for e in validate_schema(p, pack_schema)]

        sysslug = p.get("recommended_system")
        if not sysslug:
            missing_system.append(f"line {n}")
            continue

        # recommended_system maps to a valid contact role
        if not role_valid(p["likely_decision_maker_role"], sysslug):
            bad_role.append(f"{p['company_name']}: '{p['likely_decision_maker_role']}' invalid for {sysslug}")

        # no invented contact fields: phone/email only when a matching public channel exists
        company_channels = channels_by_company.get(p["company_name"], [])
        has_phone_channel = any(c["channel_type"] == "main_phone" for c in company_channels)
        has_email_channel = any(c["channel_type"] in ("generic_email", "role_email") for c in company_channels)
        if p.get("phone_if_public") and not has_phone_channel:
            invented_contact.append(f"{p['company_name']}: phone set without a public phone channel")
        if p.get("email_if_public") and not has_email_channel:
            invented_contact.append(f"{p['company_name']}: email set without a public email channel")

        # referenced channel ids must exist
        for cid in p.get("public_contact_channels", []):
            if cid not in channel_ids:
                bad_channel_ref.append(f"{p['company_name']}: unknown channel {cid}")

        # missing contacts handled gracefully
        if not company_channels:
            if p.get("phone_if_public") or p.get("email_if_public"):
                graceful_errors.append(f"{p['company_name']}: contact fields set with no channels")
            if p.get("best_contact_route") != "none_found":
                graceful_errors.append(f"{p['company_name']}: no channels but route != none_found")
            if p.get("status") in ("approved", "sent"):
                graceful_errors.append(f"{p['company_name']}: advanced status with no contact")

        # L0/L1 must hedge and avoid absolute accusations
        copy_blob = f"{p.get('likely_pain','')}\n{p.get('email_body','')}\n{p.get('why_this_system','')}"
        if p["evidence_level"] in ("L0", "L1"):
            if not any(h in copy_blob for h in HEDGES):
                hedge_errors.append(f"{p['company_name']} ({p['evidence_level']}): no hedging language")
        hit = contains_any(copy_blob, BANNED_ABSOLUTE)
        if hit:
            absolute_errors.append(f"{p['company_name']}: absolute claim {hit}")

        # no guarantee language anywhere in outbound-facing copy
        guarantee_blob = " ".join(str(p.get(k, "")) for k in
                                  ("email_subject", "email_body", "why_this_system",
                                   "proof_angle", "mini_proposal_angle", "likely_pain"))
        ghit = contains_any(guarantee_blob.lower(), [g.lower() for g in BANNED_GUARANTEE])
        if ghit:
            guarantee_errors.append(f"{p['company_name']}: guarantee term {ghit}")

        # no misleading Re:/Fwd:
        if p.get("email_subject", "").strip().lower().startswith(RE_FWD_PREFIXES):
            subject_errors.append(f"{p['company_name']}: subject uses Re:/Fwd:")

        # no internal artifacts in email body
        ihit = contains_any(p.get("email_body", ""), BANNED_INTERNAL)
        if ihit:
            internal_leak.append(f"{p['company_name']}: internal token {ihit}")

        # scoring
        comps, total, tier = score_pack(p)
        rec = {
            "company_name": p["company_name"],
            "recommended_system": sysslug,
            "components": comps,
            "total": total,
            "rank_tier": tier,
        }
        sc_err = validate_schema(rec, scoring_schema)
        if sc_err:
            pack_schema_errors.append(f"scoring {p['company_name']}: {sc_err}")
        scoring_records.append(rec)

    record("Account packs validate against schema", not pack_schema_errors,
           "; ".join(pack_schema_errors[:6]))
    record("Every pack has recommended_system", not missing_system,
           "; ".join(missing_system))
    record("Every recommended_system maps to a valid contact role", not bad_role,
           "; ".join(bad_role[:6]))
    record("No invented contact fields (phone/email backed by public channel)",
           not invented_contact, "; ".join(invented_contact[:6]))
    record("All referenced contact channels exist", not bad_channel_ref,
           "; ".join(bad_channel_ref[:6]))
    record("Missing contacts handled gracefully", not graceful_errors,
           "; ".join(graceful_errors[:6]))
    record("L0/L1 claims use likely/probably language", not hedge_errors,
           "; ".join(hedge_errors[:6]))
    record("No absolute unproven accusations", not absolute_errors,
           "; ".join(absolute_errors[:6]))
    record("No guaranteed claims in email copy", not guarantee_errors,
           "; ".join(guarantee_errors[:6]))
    record("No misleading Re:/Fwd: subjects", not subject_errors,
           "; ".join(subject_errors[:6]))
    record("No internal module names leak into email", not internal_leak,
           "; ".join(internal_leak[:6]))

    # --- Mini proposals
    prop_errors = []
    for n, mp in proposals:
        prop_errors += [f"proposal line {n}: {e}" for e in validate_schema(mp, proposal_schema)]
        if mp.get("approval_required") is not True:
            prop_errors.append(f"proposal line {n}: approval_required must be true")
        if not mp.get("starter_price_sar"):
            prop_errors.append(f"proposal line {n}: missing starter_price_sar")
        ghit = contains_any(" ".join(str(mp.get(k, "")) for k in
                                     ("why_this_system", "likely_pain", "expected_first_proof", "next_step")).lower(),
                            [g.lower() for g in BANNED_GUARANTEE])
        if ghit:
            prop_errors.append(f"proposal line {n}: guarantee term {ghit}")
    record("Mini proposals have starter price + approval_required + no guarantees",
           not prop_errors, "; ".join(prop_errors[:6]))

    # --- Founder command sections
    founder_path = REPORTS / "founder" / "DAILY_SUPER_COMMAND.md"
    required_sections = [
        "critical decision", "400 account packs", "contacts found", "missing contacts",
        "top 100", "top 20 send", "top 30 call", "mini proposals", "delivery pipelines",
        "website leads", "best system", "best sector", "best city", "biggest risk",
        "cash opportunity", "tomorrow plan",
    ]
    if founder_path.exists():
        txt = founder_path.read_text(encoding="utf-8").lower()
        missing = [s for s in required_sections if s not in txt]
        record("Founder command has all required sections", not missing,
               "missing: " + ", ".join(missing))
    else:
        record("Founder command has all required sections", False,
               "DAILY_SUPER_COMMAND.md not found")

    # --- Security doc treats external content as untrusted
    sec_path = DOCS / "security" / "EXTERNAL_CONTENT_UNTRUSTED_AR.md"
    if sec_path.exists():
        s = sec_path.read_text(encoding="utf-8").lower()
        need = ["untrusted", "prompt injection", "غير موثوق"]
        miss = [t for t in need if t.lower() not in s]
        record("Security doc treats external content as untrusted", not miss,
               "missing markers: " + ", ".join(miss))
    else:
        record("Security doc treats external content as untrusted", False,
               "EXTERNAL_CONTENT_UNTRUSTED_AR.md not found")

    # -----------------------------------------------------------------------
    # Report
    # -----------------------------------------------------------------------
    print("  CHECK RESULTS")
    print("  " + "-" * 80)
    crit_fail = 0
    warn_fail = 0
    for severity, name, ok, detail in results:
        icon = "✅" if ok else ("❌" if severity == "CRITICAL" else "⚠️")
        line = f"  {icon} {name}"
        if not ok and detail:
            line += f"\n        → {detail}"
        print(line)
        if not ok:
            if severity == "CRITICAL":
                crit_fail += 1
            else:
                warn_fail += 1

    print()
    print("  TOP-100 SCORING (computed from packs)")
    print("  " + "-" * 80)
    print(f"  {'Company':<28}{'System':<22}{'Score':>6}  Tier")
    for r in sorted(scoring_records, key=lambda x: x["total"], reverse=True):
        print(f"  {r['company_name']:<28}{r['recommended_system']:<22}{r['total']:>6}  {r['rank_tier']}")

    tiers = {}
    for r in scoring_records:
        tiers[r["rank_tier"]] = tiers.get(r["rank_tier"], 0) + 1
    print()
    print("  Tier distribution: " + ", ".join(f"{k}={v}" for k, v in sorted(tiers.items())))

    print()
    print("  " + "=" * 80)
    passed = sum(1 for *_, ok, _ in [(r[0], r[1], r[2], r[3]) for r in results] if ok)
    total_checks = len(results)
    print(f"  SUMMARY: {passed}/{total_checks} checks passed | "
          f"critical failures: {crit_fail} | warnings: {warn_fail}")
    if crit_fail == 0:
        print("  OVERALL: ✅ PASS")
    else:
        print("  OVERALL: ❌ FAIL")
    print("  " + "=" * 80)

    return 1 if crit_fail else 0


if __name__ == "__main__":
    sys.exit(main())
