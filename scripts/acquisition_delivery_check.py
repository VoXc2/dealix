#!/usr/bin/env python3
"""
Dealix Acquisition → Delivery quality check.

Validates every data/**/*.jsonl record against its JSON Schema in schemas/,
then runs the hard checks required by the operating model (see AGENTS.md):

  1. every company intelligence pack has a valid recommended_system
  2. every recommended_system maps to an allowed contact role
  3. every call brief has an opening line and discovery questions
  4. every mini proposal has deliverables and a starter price
  5. delivery cannot start without required inputs
  6. no guaranteed claims in email / proposal templates
  7. no secrets or PII in reports (and no secret-named fields in data)
  8. L0/L1 evidence is not phrased as certainty

Dependency-free (stdlib only). Exit code 0 = all checks pass, 1 = failures.
Run:  python3 scripts/acquisition_delivery_check.py
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHEMAS = REPO / "schemas"
DATA = REPO / "data"
REPORTS = REPO / "reports"

# system_id -> allowed contact roles (best + alternates). See AGENTS.md §3.
SYSTEM_ROLES = {
    "revenue_os": {"Head of Sales", "Founder", "GM", "Marketing Manager"},
    "executive_command_os": {"Founder", "CEO", "GM", "Operations Manager"},
    "followup_recovery_os": {"Sales Manager", "Marketing Manager", "Founder"},
    "whatsapp_client_os": {"Operations Manager", "Customer Service Manager", "Founder"},
    "proposal_proof_os": {"Founder", "Sales Lead", "BD Manager", "Marketing Manager"},
}

VALID_SYSTEMS = set(SYSTEM_ROLES.keys())

# states at or after delivery_started require inputs to be received first.
STARTED_STATES = {
    "delivery_started", "first_output_ready", "client_review",
    "accepted", "weekly_value_report", "renewal_candidate",
}

# guarantee / over-claim language forbidden inside outreach & proposal templates.
GUARANTEE_AR = ["مضمون", "نضمن", "ضمان", "نضاعف", "سنضاعف"]
GUARANTEE_EN = ["guarantee", "guaranteed", "double your", "100% "]

# hedge tokens that make an L0/L1 statement a likelihood, not a certainty.
HEDGES = ["غالبًا", "غالبا", "قد ", "يُحتمل", "محتمل", "عادةً", "عادة", "ربما", "في الغالب", "في هذا النوع"]

# secret / PII signatures that must never appear in generated reports.
SECRET_PATTERNS = [
    re.compile(r"(sk-[A-Za-z0-9]{12,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{12,})"),
    re.compile(r"(OPENAI_API_KEY|OPENROUTER|DEEPSEEK|RAILWAY_TOKEN)", re.IGNORECASE),
    re.compile(r"\b05\d{8}\b"),  # Saudi mobile number
]
SECRET_FIELD_NAMES = {"secret", "api_key", "apikey", "password", "token", "access_key", "private_key"}

# schema file -> data file (relative to repo)
PAIRS = [
    ("company_intelligence_pack.schema.json", "data/acquisition/company_intelligence_packs.jsonl"),
    ("client_need_card.schema.json", "data/acquisition/client_need_cards.jsonl"),
    ("contact_target.schema.json", "data/acquisition/contact_targets.jsonl"),
    ("call_brief.schema.json", "data/acquisition/call_briefs.jsonl"),
    ("mini_proposal.schema.json", "data/acquisition/mini_proposals.jsonl"),
    ("follow_up_sequence.schema.json", "data/acquisition/follow_up_sequences.jsonl"),
    ("objection_response.schema.json", "data/acquisition/objection_responses.jsonl"),
    ("delivery_pipeline.schema.json", "data/delivery/pipelines.jsonl"),
    ("delivery_task.schema.json", "data/delivery/tasks.jsonl"),
    ("weekly_value_report.schema.json", "data/delivery/weekly_value_reports.jsonl"),
    ("delivery_acceptance_gate.schema.json", "data/delivery/acceptance_gates.jsonl"),
]

failures = []
notes = []


def fail(check, detail):
    failures.append((check, detail))


# ---------------------------------------------------------------- mini validator
def _type_ok(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    return True


def validate(instance, schema, path="$"):
    """Minimal JSON-Schema (2020-12 subset) validator -> list of error strings."""
    errs = []

    if "type" in schema and not _type_ok(instance, schema["type"]):
        errs.append(f"{path}: expected type {schema['type']}, got {type(instance).__name__}")
        return errs  # type mismatch -> stop deeper checks

    if "enum" in schema and instance not in schema["enum"]:
        errs.append(f"{path}: value {instance!r} not in enum {schema['enum']}")
    if "const" in schema and instance != schema["const"]:
        errs.append(f"{path}: value {instance!r} != const {schema['const']!r}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errs.append(f"{path}: string shorter than minLength {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errs.append(f"{path}: {instance!r} does not match pattern {schema['pattern']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errs.append(f"{path}: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errs.append(f"{path}: {instance} > maximum {schema['maximum']}")

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errs.append(f"{path}: missing required property '{req}'")
        props = schema.get("properties", {})
        if schema.get("additionalProperties", True) is False:
            for key in instance:
                if key not in props:
                    errs.append(f"{path}: additional property '{key}' not allowed")
        for key, subschema in props.items():
            if key in instance:
                errs.extend(validate(instance[key], subschema, f"{path}.{key}"))

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errs.append(f"{path}: array shorter than minItems {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errs.append(f"{path}: array longer than maxItems {schema['maxItems']}")
        if "items" in schema:
            for i, item in enumerate(instance):
                errs.extend(validate(item, schema["items"], f"{path}[{i}]"))

    return errs


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                fail("schema", f"{path.relative_to(REPO)}:{n}: invalid JSON ({e})")
    return rows


def find_text(value):
    """Yield all string leaves of a value."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from find_text(v)
    elif isinstance(value, list):
        for v in value:
            yield from find_text(v)


def has_guarantee(text):
    low = text.lower()
    for w in GUARANTEE_AR:
        if w in text:
            return w
    for w in GUARANTEE_EN:
        if w in low:
            return w
    return None


def has_hedge(text):
    return any(h in text for h in HEDGES)


def find_secret_field(value):
    if isinstance(value, dict):
        for k, v in value.items():
            if k.lower() in SECRET_FIELD_NAMES:
                return k
            found = find_secret_field(v)
            if found:
                return found
    elif isinstance(value, list):
        for v in value:
            found = find_secret_field(v)
            if found:
                return found
    return None


# ---------------------------------------------------------------- run
def main():
    datasets = {}  # data rel path -> rows

    print("=" * 72)
    print("DEALIX ACQUISITION → DELIVERY CHECK")
    print("=" * 72)

    # ---- 0: schema validation -------------------------------------------------
    print("\n[schema] validating data against schemas/ ...")
    for schema_name, data_rel in PAIRS:
        schema_path = SCHEMAS / schema_name
        data_path = REPO / data_rel
        if not schema_path.exists():
            fail("schema", f"missing schema {schema_name}")
            continue
        if not data_path.exists():
            fail("schema", f"missing data file {data_rel}")
            continue
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        rows = load_jsonl(data_path)
        datasets[data_rel] = rows
        for i, row in enumerate(rows):
            rid = row.get("id", f"row{i}")
            for err in validate(row, schema):
                fail("schema", f"{data_rel} [{rid}] {err}")
        print(f"  - {data_rel}: {len(rows)} records")

    cips = datasets.get("data/acquisition/company_intelligence_packs.jsonl", [])
    cards = datasets.get("data/acquisition/client_need_cards.jsonl", [])
    targets = datasets.get("data/acquisition/contact_targets.jsonl", [])
    briefs = datasets.get("data/acquisition/call_briefs.jsonl", [])
    proposals = datasets.get("data/acquisition/mini_proposals.jsonl", [])
    sequences = datasets.get("data/acquisition/follow_up_sequences.jsonl", [])
    objections = datasets.get("data/acquisition/objection_responses.jsonl", [])
    pipelines = datasets.get("data/delivery/pipelines.jsonl", [])
    tasks = datasets.get("data/delivery/tasks.jsonl", [])
    weeklies = datasets.get("data/delivery/weekly_value_reports.jsonl", [])

    # ---- 1: every CIP has a valid recommended_system --------------------------
    for r in cips:
        if r.get("recommended_system") not in VALID_SYSTEMS:
            fail("check1", f"CIP {r.get('id')} has invalid recommended_system {r.get('recommended_system')!r}")

    # ---- 2: recommended_system maps to allowed contact role -------------------
    def check_role(kind, rid, system, role, field):
        allowed = SYSTEM_ROLES.get(system)
        if allowed is None:
            fail("check2", f"{kind} {rid}: unknown system {system!r}")
        elif role not in allowed:
            fail("check2", f"{kind} {rid}: {field} '{role}' not allowed for {system} (allowed: {sorted(allowed)})")

    for r in cips:
        check_role("CIP", r.get("id"), r.get("recommended_system"), r.get("best_contact_role"), "best_contact_role")
    for r in targets:
        check_role("contact_target", r.get("id"), r.get("recommended_system"), r.get("best_contact_role"), "best_contact_role")
        for alt in r.get("alternate_roles", []):
            check_role("contact_target", r.get("id"), r.get("recommended_system"), alt, "alternate_role")
    for r in briefs:
        check_role("call_brief", r.get("id"), r.get("recommended_system"), r.get("contact_role"), "contact_role")

    # ---- 3: every call brief has opening line + discovery questions -----------
    for r in briefs:
        if not (r.get("opening_line") or "").strip():
            fail("check3", f"call_brief {r.get('id')} missing opening_line")
        if not r.get("discovery_questions"):
            fail("check3", f"call_brief {r.get('id')} missing discovery_questions")

    # ---- 4: every mini proposal has deliverables + starter price -------------
    for r in proposals:
        if not r.get("deliverables"):
            fail("check4", f"mini_proposal {r.get('id')} missing deliverables")
        sp = r.get("starter_price") or {}
        if not (isinstance(sp, dict) and isinstance(sp.get("amount"), int) and sp["amount"] > 0):
            fail("check4", f"mini_proposal {r.get('id')} missing/invalid starter_price")

    # ---- 5: delivery cannot start without required inputs ---------------------
    pl_by_id = {p.get("id"): p for p in pipelines}
    for p in pipelines:
        if p.get("current_state") in STARTED_STATES:
            if not p.get("required_inputs_received"):
                fail("check5", f"pipeline {p.get('id')} is in '{p.get('current_state')}' but required_inputs_received is false")
            if not p.get("required_inputs"):
                fail("check5", f"pipeline {p.get('id')} is in '{p.get('current_state')}' but has empty required_inputs")
    for t in tasks:
        if t.get("depends_on_inputs") and t.get("status") in {"in_progress", "done"}:
            pl = pl_by_id.get(t.get("pipeline_id"))
            if pl is None:
                fail("check5", f"task {t.get('id')} references unknown pipeline {t.get('pipeline_id')}")
            elif not pl.get("required_inputs_received"):
                fail("check5", f"task {t.get('id')} ({t.get('status')}) depends on inputs but pipeline {pl.get('id')} has not received them")

    # ---- 6: no guaranteed claims in email / proposal templates ----------------
    template_sets = [
        ("CIP", cips, ["email_subject", "email_draft", "why_this_system", "proof_angle", "mini_proposal_angle"]),
        ("need_card", cards, ["email_angle", "why_this_system", "proof_angle", "CTA"]),
        ("mini_proposal", proposals, None),       # all string leaves
        ("follow_up_step", sequences, None),
        ("weekly_value_report", weeklies, None),
        ("objection", objections, ["response"]),
    ]
    for kind, rows, fields in template_sets:
        for r in rows:
            texts = []
            if fields is None:
                texts = list(find_text(r))
            else:
                for fld in fields:
                    if fld in r:
                        texts.extend(find_text(r[fld]))
            for txt in texts:
                w = has_guarantee(txt)
                if w:
                    fail("check6", f"{kind} {r.get('id')} contains guarantee-language {w!r}: {txt[:60]}...")

    # ---- 7: no secrets / PII in reports, no secret fields in data -------------
    report_files = sorted(REPORTS.rglob("*.md")) if REPORTS.exists() else []
    for rf in report_files:
        content = rf.read_text(encoding="utf-8", errors="ignore")
        for pat in SECRET_PATTERNS:
            m = pat.search(content)
            if m:
                fail("check7", f"report {rf.relative_to(REPO)} contains secret/PII pattern: {m.group(0)[:20]}")
    if not report_files:
        notes.append("check7: no reports/*.md found yet (run report generators first to scan them)")
    for data_rel, rows in datasets.items():
        for r in rows:
            k = find_secret_field(r)
            if k:
                fail("check7", f"{data_rel} [{r.get('id')}] has secret-named field '{k}'")

    # ---- 8: L0/L1 evidence not phrased as certainty --------------------------
    for kind, rows in (("CIP", cips), ("need_card", cards)):
        for r in rows:
            if r.get("evidence_level") in {"L0", "L1"}:
                pain = r.get("likely_pain", "")
                if pain and not has_hedge(pain):
                    fail("check8", f"{kind} {r.get('id')} is {r.get('evidence_level')} but likely_pain is phrased as certainty (no hedge): {pain[:50]}")

    # ---- summary --------------------------------------------------------------
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    by_check = {}
    for c, d in failures:
        by_check.setdefault(c, []).append(d)

    labels = {
        "schema": "0. schema validation",
        "check1": "1. CIP has recommended_system",
        "check2": "2. system maps to contact role",
        "check3": "3. call brief opening + questions",
        "check4": "4. mini proposal deliverables + price",
        "check5": "5. delivery blocked until inputs",
        "check6": "6. no guaranteed claims in templates",
        "check7": "7. no secrets/PII in reports",
        "check8": "8. L0/L1 not phrased as certainty",
    }
    for key in ["schema", "check1", "check2", "check3", "check4", "check5", "check6", "check7", "check8"]:
        issues = by_check.get(key, [])
        status = "PASS" if not issues else f"FAIL ({len(issues)})"
        print(f"  [{status:>8}] {labels[key]}")
        for d in issues:
            print(f"             - {d}")

    for n in notes:
        print(f"  [note] {n}")

    total = len(failures)
    print("-" * 72)
    if total == 0:
        print("RESULT: ALL CHECKS PASS")
    else:
        print(f"RESULT: {total} issue(s) found")
    print("=" * 72)
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
