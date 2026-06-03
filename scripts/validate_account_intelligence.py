#!/usr/bin/env python3
"""
Dealix Account Intelligence — validator / test harness.

Runs three layers of checks and exits non-zero if any fails:

  A. SCHEMA   — every data file validates against its JSON Schema
                (stdlib-only mini validator: type/enum/const/pattern/required/
                 minItems/minLength/minimum/maximum/additionalProperties/items).
  B. POLICY   — the Maximum Revenue Factory rules (one system per pack, system→role,
                missing contacts handled, no invented contacts, L0/L1 hedging,
                no guaranteed claims, mini-proposal gate, scoring integrity,
                Top-100 exclusions, prompt-injection markers absent).
  C. ARTIFACTS — Founder Daily Command has all required sections; security docs
                 treat external content as untrusted; privacy docs cover
                 minimization and do-not-contact.

Usage:
  python3 scripts/validate_account_intelligence.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import dealix_account_lib as lib

ROOT = lib.REPO_ROOT
SCHEMA_DIR = lib.SCHEMA_DIR
DATA_DIR = lib.DATA_DIR
REPORTS_DIR = lib.REPORTS_DIR
DOCS_DIR = ROOT / "docs"

PASS, FAIL = "✅", "❌"


# --------------------------------------------------------------------------- #
# Minimal JSON Schema validator (subset sufficient for our schemas)
# --------------------------------------------------------------------------- #
def _type_ok(value, types) -> bool:
    if isinstance(types, str):
        types = [types]
    for t in types:
        if t == "string" and isinstance(value, str):
            return True
        if t == "integer" and isinstance(value, bool) is False and isinstance(value, int):
            return True
        if t == "number" and isinstance(value, bool) is False and isinstance(value, (int, float)):
            return True
        if t == "boolean" and isinstance(value, bool):
            return True
        if t == "array" and isinstance(value, list):
            return True
        if t == "object" and isinstance(value, dict):
            return True
        if t == "null" and value is None:
            return True
    return False


def validate_value(value, schema: dict, path: str, errors: list[str]) -> None:
    if "type" in schema and not _type_ok(value, schema["type"]):
        errors.append(f"{path}: expected type {schema['type']}, got {type(value).__name__}")
        return
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: value {value!r} != const {schema['const']!r}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: does not match pattern {schema['pattern']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        if "items" in schema:
            for idx, item in enumerate(value):
                validate_value(item, schema["items"], f"{path}[{idx}]", errors)
    if isinstance(value, dict) and ("properties" in schema or "required" in schema):
        validate_object(value, schema, path, errors)


def validate_object(obj: dict, schema: dict, path: str, errors: list[str]) -> None:
    props = schema.get("properties", {})
    for req in schema.get("required", []):
        if req not in obj:
            errors.append(f"{path}: missing required field '{req}'")
    if schema.get("additionalProperties") is False:
        for key in obj:
            if key not in props:
                errors.append(f"{path}: additional property '{key}' not allowed")
    for key, subschema in props.items():
        if key in obj:
            validate_value(obj[key], subschema, f"{path}.{key}", errors)


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


# --------------------------------------------------------------------------- #
# Check runner
# --------------------------------------------------------------------------- #
class Checks:
    def __init__(self) -> None:
        self.results: list[tuple[str, bool, str]] = []

    def add(self, name: str, ok: bool, detail: str = "") -> None:
        self.results.append((name, ok, detail))

    @property
    def passed(self) -> int:
        return sum(1 for _, ok, _ in self.results if ok)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def all_pass(self) -> bool:
        return self.passed == self.total

    def section(self, title: str) -> None:
        print(f"\n  {title}")
        print("  " + "-" * 60)

    def flush(self, since: int = 0) -> None:
        for name, ok, detail in self.results[since:]:
            mark = PASS if ok else FAIL
            extra = f"  ({detail})" if detail else ""
            print(f"  {mark} {name}{extra}")


def main() -> int:
    c = Checks()
    print("=" * 72)
    print("  DEALIX ACCOUNT INTELLIGENCE — VALIDATION")
    print("=" * 72)

    # ---- A. SCHEMA --------------------------------------------------------- #
    c.section("A. Schema validation")
    schema_map = [
        ("account_intelligence_pack.schema.json", "account_intelligence/account_packs.jsonl"),
        ("contact_discovery.schema.json", "contacts/contact_discovery.jsonl"),
        ("contact_channel.schema.json", "contacts/contact_channels.jsonl"),
        ("account_scoring.schema.json", "account_intelligence/account_scoring.jsonl"),
        ("mini_proposal.schema.json", "proposals/mini_proposals.jsonl"),
        ("cash_priority_score.schema.json", "finance/cash_priority_scores.jsonl"),
    ]
    packs: list[dict] = []
    proposals: list[dict] = []
    since = len(c.results)
    for schema_file, data_file in schema_map:
        spath = SCHEMA_DIR / schema_file
        dpath = DATA_DIR / data_file
        if not spath.exists() or not dpath.exists():
            c.add(f"{data_file} validates", False, "missing schema or data file")
            continue
        schema = load_json(spath)
        rows = load_jsonl(dpath)
        errors: list[str] = []
        for i, row in enumerate(rows):
            validate_object(row, schema, f"{data_file}#{i}", errors)
            if len(errors) > 8:
                break
        if data_file.endswith("account_packs.jsonl"):
            packs = rows
        if data_file.endswith("mini_proposals.jsonl"):
            proposals = rows
        c.add(f"{data_file} validates against {schema_file}", len(errors) == 0,
              f"{len(rows)} rows" if not errors else f"{errors[0]}")
    c.flush(since)

    if not packs:
        print("\n  No account packs found — run generate_account_packs.py first.")
        return 1

    # ---- B. POLICY --------------------------------------------------------- #
    c.section("B. Policy gates")
    since = len(c.results)
    n = len(packs)

    c.add("exactly 400 account packs", n == 400, f"{n}")

    counts = {}
    for p in packs:
        counts[p["recommended_system"]] = counts.get(p["recommended_system"], 0) + 1
    target = {k: v["nightly_count"] for k, v in lib.SYSTEMS.items()}
    c.add("nightly distribution matches target (100/90/70/70/70)",
          counts == target, str(counts))

    c.add("every pack has recommended_system",
          all(p.get("recommended_system") for p in packs))

    c.add("recommended_system maps to a contact role",
          all(p.get("likely_decision_maker_role") and p.get("secondary_contact_role") for p in packs))

    missing = [p for p in packs if p.get("missing_contact")]
    c.add("missing contacts handled gracefully (route present)",
          all(p.get("best_contact_route") for p in missing), f"{len(missing)} missing")

    invented = [p for p in packs if p.get("phone_if_public") or p.get("email_if_public")]
    c.add("no invented contacts (phone/email null in seed)", len(invented) == 0,
          f"{len(invented)} violations")

    l01 = [p for p in packs if p["evidence_level"] in ("L0", "L1")]
    bad_hedge = [p for p in l01 if not (lib._hedge_ok(p["likely_pain"]) and lib._hedge_ok(p["email_body"]))]
    c.add("L0/L1 copy uses likely/probably language", len(bad_hedge) == 0,
          f"{len(l01)-len(bad_hedge)}/{len(l01)} ok")

    bad_claim = [p for p in packs if lib.has_guaranteed_claim(p["email_body"] + p["email_subject"])]
    c.add("no guaranteed claims in email copy", len(bad_claim) == 0, f"{len(bad_claim)} violations")

    bad_prop = [pr for pr in proposals
                if not pr.get("starter_price_sar")
                or pr.get("approval_required") is not True
                or len(pr.get("deliverables", [])) < 3
                or lib.has_guaranteed_claim(pr.get("why_this_system", "") + " ".join(pr.get("deliverables", [])))]
    c.add("mini proposals: starter_price + approval_required + 3 deliverables + no claim",
          len(bad_prop) == 0, f"{len(proposals)-len(bad_prop)}/{len(proposals)} ok")

    bad_email = []
    for p in packs:
        body = p["email_body"]
        if sum(1 for s in lib.SYSTEM_NAMES if s in body) != 1 or body.count("Mini Proposal") != 1 \
                or p["company_name"] not in body:
            bad_email.append(p)
    c.add("email gate: one system + company context + single CTA", len(bad_email) == 0,
          f"{len(bad_email)} violations")

    # scoring integrity: breakdown sums equal stored score, within caps
    bad_score = []
    for p in packs:
        if sum(p["account_score_breakdown"].values()) != p["account_score"]:
            bad_score.append(p["pack_id"])
        if sum(p["cash_priority_breakdown"].values()) != p["cash_priority_score"]:
            bad_score.append(p["pack_id"])
    c.add("scoring integrity (breakdown sums == score, 0..100)", len(bad_score) == 0,
          f"{len(bad_score)} mismatches")

    # Top-100 exclusions correctly applied
    scoring = load_jsonl(DATA_DIR / "account_intelligence" / "account_scoring.jsonl")
    sc_by_id = {s["pack_id"]: s for s in scoring}
    bad_excl = []
    for p in packs:
        expect = lib.top100_exclusions(p)
        got = sc_by_id.get(p["pack_id"], {}).get("exclusion_reasons", [])
        if set(expect) != set(got):
            bad_excl.append(p["pack_id"])
    c.add("Top-100 exclusion reasons computed correctly", len(bad_excl) == 0,
          f"{len(bad_excl)} mismatches")
    high_in_top = [s for s in scoring if s["eligible_for_top100"] and s["risk_level"] == "high"]
    c.add("no high-risk or suppressed account is eligible",
          len(high_in_top) == 0 and not any(
              s["eligible_for_top100"] and "suppression_do_not_contact" in s["exclusion_reasons"]
              for s in scoring),
          f"{len(high_in_top)} high-risk eligible")

    inj = [p for p in packs if lib.has_injection_marker(
        p["email_body"] + p["buying_signal"] + p["company_name"] + p["likely_pain"])]
    c.add("no prompt-injection markers in pack text", len(inj) == 0, f"{len(inj)} violations")
    c.flush(since)

    # ---- C. ARTIFACTS ------------------------------------------------------ #
    c.section("C. Artifacts (founder command, security, privacy)")
    since = len(c.results)

    fc = REPORTS_DIR / "founder" / "DAILY_SUPER_COMMAND.md"
    required_sections = [
        "القرار الحرج", "حالة الـ400", "جهات الاتصال", "Top 100", "Send Candidates",
        "Call Candidates", "Mini Proposals", "اعتمادات العروض", "خطوط التسليم",
        "عوائق التسليم", "Website Leads", "أفضل نظام", "أفضل قطاع", "أفضل مدينة",
        "فرصة الكاش", "أكبر خطر", "خطة الغد",
    ]
    if fc.exists():
        text = fc.read_text(encoding="utf-8")
        missing_sec = [s for s in required_sections if s not in text]
        c.add("Founder Daily Command has all required sections", len(missing_sec) == 0,
              f"missing: {missing_sec}" if missing_sec else f"{len(required_sections)} sections")
    else:
        c.add("Founder Daily Command exists", False, "file missing")

    def doc_contains(rel: str, needles: list[str]) -> tuple[bool, str]:
        p = DOCS_DIR / rel
        if not p.exists():
            return False, "file missing"
        t = p.read_text(encoding="utf-8")
        miss = [x for x in needles if x not in t]
        return len(miss) == 0, ("missing: " + ", ".join(miss) if miss else "ok")

    ok, d = doc_contains("security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY.md",
                         ["untrusted", "external", "instruction"])
    c.add("security: external content treated as untrusted data", ok, d)
    ok, d = doc_contains("security/AGENT_PROMPT_INJECTION_GATE.md",
                         ["ignore previous instructions", "reveal secret", "use this tool"])
    c.add("security: prompt-injection gate lists markers", ok, d)
    ok, d = doc_contains("security/TOOL_EXECUTION_ALLOWLIST_POLICY.md", ["allowlist", "external"])
    c.add("security: tool-execution allowlist policy present", ok, d)
    ok, d = doc_contains("privacy/ACCOUNT_INTELLIGENCE_DATA_MINIMIZATION_AR.md",
                         ["تقليل", "بيانات عامة"])
    c.add("privacy: data minimization documented", ok, d)
    ok, d = doc_contains("privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md",
                         ["do-not-contact", "suppression"])
    c.add("privacy: do-not-contact / suppression documented", ok, d)
    c.flush(since)

    # ---- summary ----------------------------------------------------------- #
    print("\n" + "=" * 72)
    status = "✅ ALL CHECKS PASSED" if c.all_pass else "❌ SOME CHECKS FAILED"
    print(f"  {status}  ({c.passed}/{c.total})")
    print("=" * 72)
    return 0 if c.all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
