#!/usr/bin/env python3
"""
Dealix Acquisition-to-Delivery Check
====================================
Validates the acquisition + delivery operating layer against the hard rules.
Modeled on scripts/governance_check.py. Exits non-zero on any CRITICAL/HIGH
finding so it can be wired into CI.

Checks:
  C01 every company intelligence pack has a valid recommended_system
  C02 every recommended_system maps to a contact role (contact_targets.jsonl)
  C03 every call brief has an opening line and discovery questions
  C04 every mini proposal has deliverables and a starter price
  C05 delivery cannot start (stage >= delivery_started) without the five things
  C06 no guaranteed-revenue claims in email/proposal templates
  C07 no secrets in generated reports or data
  C08 every email/proposal/weekly-report stays a draft (approval_required = true)
  C09 no fake Re:/Fwd: email subjects
  C10 call briefs are for human callers (automated_calling = false)
  C11 required schema fields present (validated against schemas/*.schema.json)
  C12 packs / need cards / call briefs / mini proposals cover the same companies
"""

import json
import re
from pathlib import Path

VALID_SYSTEMS = {
    "Revenue Operating System",
    "Executive Command OS",
    "Follow-up Recovery OS",
    "WhatsApp Client OS",
    "Proposal & Proof OS",
}

DELIVERY_STAGES = [
    "interested", "qualified", "mini_proposal_ready", "proposal_sent",
    "payment_handoff", "won", "intake_required", "delivery_started",
    "first_output_ready", "client_review", "accepted",
    "weekly_value_report", "renewal_candidate",
]
DELIVERY_START_INDEX = DELIVERY_STAGES.index("delivery_started")

# Guarantee / overpromise terms that must not appear in outreach templates.
GUARANTEE_TERMS = [
    "نضمن", "مضمون", "نضاعف", "نضمن لك", "عائد مضمون", "أرباح مضمونة",
    "guarantee", "guaranteed", "double your revenue", "triple your revenue",
    "100% roi", "risk-free",
]

# Precise secret patterns (avoid matching ordinary prose like "no secrets policy").
SECRET_PATTERNS = [
    r"api[_\-]?key", r"\bapi key\b", r"client[_\-]?secret", r"\bclient secret\b",
    r"access[_\-]?token", r"\baccess token\b", r"\bpassword\b", r"\bpasswd\b",
    r"bearer\s+[a-z0-9._\-]{8,}", r"-----begin [a-z ]*private key",
]
SECRET_RE = re.compile("|".join(SECRET_PATTERNS), re.IGNORECASE)

FILE_SCHEMA = {
    "data/acquisition/company_intelligence_packs.jsonl": "company_intelligence_pack.schema.json",
    "data/acquisition/client_need_cards.jsonl": "client_need_card.schema.json",
    "data/acquisition/call_briefs.jsonl": "call_brief.schema.json",
    "data/acquisition/mini_proposals.jsonl": "mini_proposal.schema.json",
    "data/acquisition/contact_targets.jsonl": "contact_target.schema.json",
    "data/delivery/pipelines.jsonl": "delivery_pipeline.schema.json",
    "data/delivery/tasks.jsonl": "delivery_task.schema.json",
    "data/delivery/weekly_value_reports.jsonl": "weekly_value_report.schema.json",
}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.exists():
        return rows
    with open(path, "r", encoding="utf-8") as f:
        for n, line in enumerate(f, start=1):
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    rows.append({"__parse_error__": f"line {n}: {e}"})
    return rows


def load_schema(base: Path, name: str) -> dict:
    with open(base / "schemas" / name, "r", encoding="utf-8") as f:
        return json.load(f)


def add(findings, check, severity, detail):
    findings.append({"check": check, "severity": severity, "detail": detail})


def run(base: Path) -> list[dict]:
    findings: list[dict] = []

    packs = load_jsonl(base / "data/acquisition/company_intelligence_packs.jsonl")
    cards = load_jsonl(base / "data/acquisition/client_need_cards.jsonl")
    briefs = load_jsonl(base / "data/acquisition/call_briefs.jsonl")
    proposals = load_jsonl(base / "data/acquisition/mini_proposals.jsonl")
    targets = load_jsonl(base / "data/acquisition/contact_targets.jsonl")
    pipelines = load_jsonl(base / "data/delivery/pipelines.jsonl")
    wvrs = load_jsonl(base / "data/delivery/weekly_value_reports.jsonl")

    target_systems = {t.get("system"): t for t in targets}

    # C11 — required schema fields present (real use of schemas/*.schema.json)
    for rel, schema_name in FILE_SCHEMA.items():
        schema = load_schema(base, schema_name)
        required = schema.get("required", [])
        rows = load_jsonl(base / rel)
        for i, row in enumerate(rows, start=1):
            if "__parse_error__" in row:
                add(findings, "C11", "CRITICAL", f"{rel} row {i}: invalid JSON ({row['__parse_error__']})")
                continue
            for key in required:
                if key not in row or row[key] in (None, "", []):
                    add(findings, "C11", "HIGH", f"{rel} row {i}: missing required field '{key}'")

    # C01 — packs have a valid recommended_system
    for i, p in enumerate(packs, start=1):
        sysname = p.get("recommended_system")
        if not sysname:
            add(findings, "C01", "CRITICAL", f"pack {p.get('pack_id', i)}: no recommended_system")
        elif sysname not in VALID_SYSTEMS:
            add(findings, "C01", "CRITICAL", f"pack {p.get('pack_id', i)}: invalid system '{sysname}'")

    # C02 — every used system maps to a non-empty contact role
    for s in VALID_SYSTEMS:
        if s not in target_systems:
            add(findings, "C02", "CRITICAL", f"system '{s}' has no contact_targets mapping")
        elif not target_systems[s].get("primary_roles"):
            add(findings, "C02", "CRITICAL", f"system '{s}' has empty primary_roles")
    used_systems = {p.get("recommended_system") for p in packs} | {p.get("system") for p in pipelines}
    for s in used_systems:
        if s and s not in target_systems:
            add(findings, "C02", "CRITICAL", f"used system '{s}' missing from contact_targets")

    # C03 — call briefs have opening line + questions
    for i, b in enumerate(briefs, start=1):
        if not str(b.get("opening_line", "")).strip():
            add(findings, "C03", "HIGH", f"call brief {b.get('brief_id', i)}: empty opening_line")
        if not b.get("discovery_questions"):
            add(findings, "C03", "HIGH", f"call brief {b.get('brief_id', i)}: no discovery_questions")

    # C04 — mini proposals have deliverables + starter price
    for i, p in enumerate(proposals, start=1):
        if not p.get("deliverables"):
            add(findings, "C04", "HIGH", f"mini proposal {p.get('proposal_id', i)}: no deliverables")
        price = p.get("starter_price_sar")
        if not isinstance(price, (int, float)) or price <= 0:
            add(findings, "C04", "HIGH", f"mini proposal {p.get('proposal_id', i)}: invalid starter_price_sar")
        if not str(p.get("starter_price", "")).strip():
            add(findings, "C04", "HIGH", f"mini proposal {p.get('proposal_id', i)}: empty starter_price label")

    # C05 — delivery cannot start without the five required things
    for i, p in enumerate(pipelines, start=1):
        stage = p.get("stage")
        idx = DELIVERY_STAGES.index(stage) if stage in DELIVERY_STAGES else -1
        if idx >= DELIVERY_START_INDEX:
            missing = []
            for key in ("system", "scope", "success_metric", "delivery_owner"):
                if not str(p.get(key, "")).strip():
                    missing.append(key)
            inputs = p.get("required_inputs", [])
            if not inputs or any(not ri.get("provided") for ri in inputs):
                missing.append("required_inputs not all provided")
            if missing:
                add(findings, "C05", "CRITICAL",
                    f"pipeline {p.get('pipeline_id', i)} at stage '{stage}' started without: {', '.join(missing)}")

    # C06 — no guarantee claims in templates
    def scan_terms(text: str) -> list[str]:
        low = str(text).lower()
        return [t for t in GUARANTEE_TERMS if t.lower() in low]

    for p in packs:
        for field in ("email_subject", "email_draft", "why_this_system", "proof_angle", "mini_proposal_angle"):
            hits = scan_terms(p.get(field, ""))
            if hits:
                add(findings, "C06", "CRITICAL", f"pack {p.get('pack_id')}: guarantee term {hits} in {field}")
    for p in proposals:
        for field in ("why_this_system", "first_sprint", "current_likely_pain", "expected_first_proof"):
            hits = scan_terms(p.get(field, ""))
            if hits:
                add(findings, "C06", "CRITICAL", f"proposal {p.get('proposal_id')}: guarantee term {hits} in {field}")
    for r in wvrs:
        for field in ("value_delivered", "next_week_focus"):
            hits = scan_terms(r.get(field, ""))
            if hits:
                add(findings, "C06", "CRITICAL", f"weekly report {r.get('report_id')}: guarantee term {hits} in {field}")

    # C07 — no secrets in generated reports or data files
    scan_paths = list((base / "reports").rglob("*.md")) + list((base / "data").rglob("*.jsonl"))
    for path in scan_paths:
        if path.name == "ACQUISITION_TO_DELIVERY_AUTOMATION_FINAL_REPORT.md":
            continue  # narrative report; scanned separately below with the same rule
        text = path.read_text(encoding="utf-8")
        m = SECRET_RE.search(text)
        if m:
            add(findings, "C07", "CRITICAL", f"{path.relative_to(base)}: possible secret '{m.group(0)}'")
    final = base / "reports/acquisition/ACQUISITION_TO_DELIVERY_AUTOMATION_FINAL_REPORT.md"
    if final.exists():
        m = SECRET_RE.search(final.read_text(encoding="utf-8"))
        if m:
            add(findings, "C07", "CRITICAL", f"final report: possible secret '{m.group(0)}'")

    # C08 — outreach stays a draft
    for p in packs:
        if p.get("approval_required") is not True:
            add(findings, "C08", "CRITICAL", f"pack {p.get('pack_id')}: approval_required must be true")
    for p in proposals:
        if p.get("approval_required") is not True:
            add(findings, "C08", "CRITICAL", f"proposal {p.get('proposal_id')}: approval_required must be true")
    for r in wvrs:
        if r.get("approval_required") is not True:
            add(findings, "C08", "CRITICAL", f"weekly report {r.get('report_id')}: approval_required must be true")

    # C09 — no fake reply/forward subjects
    fake_re = re.compile(r"^\s*(re|fwd|fw)\s*:", re.IGNORECASE)
    for p in packs:
        if fake_re.match(str(p.get("email_subject", ""))):
            add(findings, "C09", "HIGH", f"pack {p.get('pack_id')}: fake Re:/Fwd: subject")

    # C10 — call briefs are for human callers only
    for p in briefs:
        if p.get("automated_calling") is not False:
            add(findings, "C10", "CRITICAL", f"call brief {p.get('brief_id')}: automated_calling must be false")
        if p.get("caller_type") != "human":
            add(findings, "C10", "CRITICAL", f"call brief {p.get('brief_id')}: caller_type must be 'human'")

    # C12 — same companies across the four acquisition artifacts
    def companies(rows):
        return {r.get("company") for r in rows}
    base_companies = companies(packs)
    for label, rows in (("client_need_cards", cards), ("call_briefs", briefs), ("mini_proposals", proposals)):
        if companies(rows) != base_companies:
            missing = base_companies - companies(rows)
            extra = companies(rows) - base_companies
            add(findings, "C12", "WARN", f"{label} company set differs (missing={missing or '∅'}, extra={extra or '∅'})")

    return findings


def main() -> int:
    base = Path(__file__).resolve().parent.parent
    findings = run(base)

    critical = [f for f in findings if f["severity"] == "CRITICAL"]
    high = [f for f in findings if f["severity"] == "HIGH"]
    warn = [f for f in findings if f["severity"] == "WARN"]

    print("=" * 80)
    print("  DEALIX ACQUISITION-TO-DELIVERY CHECK")
    print("=" * 80)
    print(f"  Findings — 🔴 Critical: {len(critical)}  🟠 High: {len(high)}  🟡 Warn: {len(warn)}")
    print()
    for bucket, label in ((critical, "CRITICAL"), (high, "HIGH"), (warn, "WARN")):
        if bucket:
            print(f"  {label}:")
            for f in bucket:
                print(f"    [{f['check']}] {f['detail']}")
            print()

    checks = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C12"]
    print("  CHECK STATUS:")
    for c in checks:
        failed = [f for f in (critical + high) if f["check"] == c]
        status = "🔴 FAIL" if failed else "✅ PASS"
        print(f"    {c}: {status}")
    print()

    ok = not critical and not high
    print("  OVERALL:", "✅ PASS" if ok else "🔴 FAIL")
    print("=" * 80)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
