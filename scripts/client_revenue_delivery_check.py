#!/usr/bin/env python3
"""
Dealix Client + Revenue + Delivery Safety Check (Agent #2)

Stdlib-only (PyYAML optional). Enforces the non-negotiable invariants from AGENTS.md
across the WhatsApp / Portal / Revenue Execution / Delivery / Renewal data layers.

Used by:
  - CI (.github/workflows/client-revenue-delivery-check.yml)
  - tests/ (imports decide(), find_secret_like(), load_* helpers)

Exit code 0 = compliant, 1 = violations found. Does not modify any data.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

EVIDENCE_LEVELS = ["none", "assumption", "benchmark", "client_reported", "client_data", "measured", "verified"]
DELIVERED_VALUE_EVIDENCE = {"client_data", "measured", "verified"}
ALLOWED_CONSENT = {"explicit_optin", "positive_reply", "booking", "form_submission", "existing_client"}
COLD_CONSENT = {None, "", "none", "cold", "scraped", "unknown"}

# --------------------------------------------------------------------------------------
# Loaders (reused by tests)
# --------------------------------------------------------------------------------------

def load_jsonl(path: Path) -> list[dict]:
    out: list[dict] = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def valid_product_ids() -> set[str]:
    cat = load_json(DATA / "catalog" / "product_catalog.json") or {}
    ids = set(cat.get("valid_product_ids", []))
    for p in cat.get("products", []):
        if "product_id" in p:
            ids.add(p["product_id"])
    return ids


# --------------------------------------------------------------------------------------
# Secret / PII detector (reused by tests)
# --------------------------------------------------------------------------------------

SECRET_PATTERNS = [
    ("openai_key", re.compile(r"sk-[A-Za-z0-9]{16,}")),
    ("stripe_key", re.compile(r"sk_(?:live|test)_[A-Za-z0-9]{16,}")),
    ("aws_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("google_key", re.compile(r"AIza[0-9A-Za-z_\-]{20,}")),
    ("github_pat", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("api_key_kv", re.compile(r"(?i)\bapi[_-]?key\s*[:=]\s*[^\s\"'`]{8,}")),
    ("password_kv", re.compile(r"(?i)\bpassword\s*[:=]\s*[^\s\"'`]{6,}")),
    ("secret_kv", re.compile(r"(?i)\bsecret\s*[:=]\s*[^\s\"'`]{8,}")),
    ("bearer_token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-]{16,}")),
    ("authorization", re.compile(r"(?i)authorization\s*:\s*bearer\b")),
]

# Fully numeric KSA mobile (unmasked). Masked numbers use X and are fine.
UNMASKED_PHONE = re.compile(r"\+9665\d{8}\b")
# Personal email not on the company domain.
EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@(?!dealix\.sa\b)[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")


def find_secret_like(text: str) -> list[str]:
    """Return names of secret-like patterns found in text. Empty list = clean."""
    hits = []
    for name, pat in SECRET_PATTERNS:
        if pat.search(text):
            hits.append(name)
    return hits


def find_unmasked_pii(text: str) -> list[str]:
    hits = []
    if UNMASKED_PHONE.search(text):
        hits.append("unmasked_phone")
    if EMAIL.search(text):
        hits.append("personal_email")
    return hits


# --------------------------------------------------------------------------------------
# Decision brain (reused by tests + eval cases)
# --------------------------------------------------------------------------------------

def decide(case: dict) -> str:
    """Return 'allow' or 'reject' for a structured scenario. See data/evals/."""
    inp = case.get("input", case)

    # 1. WhatsApp must be post-consent, never cold, never carry secret requests.
    if inp.get("channel") == "whatsapp":
        if inp.get("consent_basis") in COLD_CONSENT:
            return "reject"
        if inp.get("message_requests_secret"):
            return "reject"

    # 2. Payments: no send without approval.
    if inp.get("type") == "payment_handoff":
        if inp.get("send_enabled") and not inp.get("approved"):
            return "reject"

    # 3. Proposals must map to the product catalog.
    if inp.get("type") == "proposal":
        if inp.get("product_id") not in valid_product_ids():
            return "reject"

    # 4. Positive reply routes to booking/WhatsApp/proof, never any direct payment action.
    if inp.get("event") == "positive_reply":
        if inp.get("proposed_route") in {"direct_payment", "send_payment_link", "payment", "payment_link", "collect_payment"}:
            return "reject"

    # 5. Renewals/upsells require delivered value.
    if inp.get("type") in ("renewal", "upsell"):
        if inp.get("evidence_level") not in DELIVERED_VALUE_EVIDENCE:
            return "reject"
        if not inp.get("cites_delivered_value"):
            return "reject"

    # 6. Won deal requires a delivery handoff.
    if inp.get("deal_status") == "won" and not inp.get("has_delivery_handoff"):
        return "reject"

    # 7. Delivery requires a weekly value report template.
    if inp.get("deal_status") == "in_delivery" and not inp.get("weekly_value_report_template"):
        return "reject"

    return "allow"


# --------------------------------------------------------------------------------------
# Data-file invariant checks
# --------------------------------------------------------------------------------------

def _f(rule, detail):
    return {"rule": rule, "detail": detail}


def check_secrets() -> list[dict]:
    findings = []
    scan_roots = [DATA, ROOT / "reports", ROOT / "schemas"]
    for base in scan_roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            # eval fixtures are intentionally adversarial scenario descriptions (no real secrets)
            if "evals" in path.parts:
                continue
            if path.suffix.lower() not in {".json", ".jsonl", ".yaml", ".yml", ".md", ".csv"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            rel = path.relative_to(ROOT)
            for name in find_secret_like(text):
                findings.append(_f("no_secrets", f"secret-like pattern '{name}' in {rel}"))
            for name in find_unmasked_pii(text):
                findings.append(_f("no_pii", f"{name} in {rel}"))
    return findings


def check_whatsapp() -> list[dict]:
    findings = []
    for s in load_jsonl(DATA / "whatsapp" / "sessions.jsonl"):
        cb = (s.get("consent") or {}).get("consent_basis")
        if cb not in ALLOWED_CONSENT:
            findings.append(_f("no_cold_whatsapp", f"session {s.get('id')} has invalid consent_basis '{cb}'"))
        if s.get("send_enabled") is True:
            findings.append(_f("send_disabled_v1", f"session {s.get('id')} has send_enabled=true (must be false in v1)"))
    for c in load_jsonl(DATA / "whatsapp" / "action_cards.jsonl"):
        if c.get("send_enabled") is True:
            findings.append(_f("send_disabled_v1", f"action card {c.get('id')} send_enabled=true"))
        if c.get("dry_run") is not True:
            findings.append(_f("dry_run_default", f"action card {c.get('id')} dry_run!=true"))
        if c.get("evidence_level") not in EVIDENCE_LEVELS:
            findings.append(_f("evidence_required", f"action card {c.get('id')} missing/invalid evidence_level"))
        if c.get("type") in ("recommendation",):
            labels = [o.get("value") for o in c.get("options", [])]
            if "dont_know_suggest" not in labels:
                findings.append(_f("dont_know_option", f"recommendation card {c.get('id')} missing 'ما أعرف — اقترح علي' option"))
    for a in load_jsonl(DATA / "whatsapp" / "client_assessments.jsonl"):
        if a.get("recommended_product_id") not in valid_product_ids():
            findings.append(_f("proposal_maps_to_catalog", f"assessment {a.get('id')} recommends unknown product '{a.get('recommended_product_id')}'"))
        if a.get("evidence_level") not in EVIDENCE_LEVELS:
            findings.append(_f("evidence_required", f"assessment {a.get('id')} missing evidence_level"))
    for p in load_jsonl(DATA / "whatsapp" / "permissions.jsonl"):
        if p.get("via") != "secure_portal":
            findings.append(_f("permissions_via_portal", f"permission {p.get('id')} not via secure_portal"))
        sref = p.get("secret_ref")
        if sref and not str(sref).startswith("portal://"):
            findings.append(_f("no_secrets", f"permission {p.get('id')} secret_ref is not a portal:// reference"))
    return findings


def check_payments() -> list[dict]:
    findings = []
    for p in load_jsonl(DATA / "payments" / "payment_handoffs.jsonl"):
        if p.get("approval_required") is not True:
            findings.append(_f("payment_requires_approval", f"payment {p.get('id')} approval_required!=true"))
        if p.get("send_enabled") is True and p.get("approved") is not True:
            findings.append(_f("payment_requires_approval", f"payment {p.get('id')} send_enabled=true while approved=false"))
        link = p.get("payment_link_ref")
        if link and not str(link).startswith("portal://"):
            findings.append(_f("no_secrets", f"payment {p.get('id')} payment_link_ref is not a portal:// reference"))
    return findings


def check_proposals() -> list[dict]:
    findings = []
    ids = valid_product_ids()
    for p in load_jsonl(DATA / "proposals" / "proposals.jsonl"):
        if p.get("product_id") not in ids:
            findings.append(_f("proposal_maps_to_catalog", f"proposal {p.get('id')} product_id '{p.get('product_id')}' not in catalog"))
        if p.get("evidence_level") not in EVIDENCE_LEVELS:
            findings.append(_f("evidence_required", f"proposal {p.get('id')} missing evidence_level"))
        pr = p.get("price_range_sar") or {}
        if pr.get("is_final") and not p.get("founder_approved"):
            findings.append(_f("no_final_price_without_approval", f"proposal {p.get('id')} marks price final without founder_approved"))
    return findings


def check_proof_packs() -> list[dict]:
    findings = []
    ids = valid_product_ids()
    for pp in load_jsonl(DATA / "proof_packs" / "proof_packs.jsonl"):
        if pp.get("guaranteed_roi") is True:
            findings.append(_f("no_guaranteed_roi", f"proof pack {pp.get('id')} sets guaranteed_roi=true"))
        if pp.get("recommended_pilot_product_id") not in ids:
            findings.append(_f("proposal_maps_to_catalog", f"proof pack {pp.get('id')} pilot product not in catalog"))
        for lp in pp.get("leakage_points", []):
            if lp.get("evidence_level") not in EVIDENCE_LEVELS:
                findings.append(_f("evidence_required", f"proof pack {pp.get('id')} leakage point missing evidence_level"))
    return findings


def check_renewals_upsells() -> list[dict]:
    findings = []
    for r in load_jsonl(DATA / "renewals" / "renewals.jsonl"):
        if r.get("evidence_level") not in DELIVERED_VALUE_EVIDENCE:
            findings.append(_f("renewal_requires_delivered_value", f"renewal {r.get('id')} evidence_level too weak"))
        if not r.get("cites_delivered_value"):
            findings.append(_f("renewal_requires_delivered_value", f"renewal {r.get('id')} cites no delivered value"))
        if r.get("approval_required") is not True:
            findings.append(_f("renewal_requires_approval", f"renewal {r.get('id')} approval_required!=true"))
    for u in load_jsonl(DATA / "renewals" / "upsell_opportunities.jsonl"):
        if u.get("evidence_level") not in DELIVERED_VALUE_EVIDENCE:
            findings.append(_f("renewal_requires_delivered_value", f"upsell {u.get('id')} evidence_level too weak"))
        if not u.get("cites_delivered_value"):
            findings.append(_f("renewal_requires_delivered_value", f"upsell {u.get('id')} cites no delivered value"))
    return findings


def check_delivery() -> list[dict]:
    findings = []
    ids = valid_product_ids()
    for d in load_jsonl(DATA / "delivery" / "handoffs.jsonl"):
        if not d.get("weekly_value_report_template"):
            findings.append(_f("weekly_report_required", f"delivery handoff {d.get('id')} missing weekly_value_report_template"))
        if d.get("product_id") not in ids:
            findings.append(_f("proposal_maps_to_catalog", f"delivery handoff {d.get('id')} product not in catalog"))
    return findings


def check_evals_consistency() -> list[dict]:
    """The decide() brain must agree with every committed eval case."""
    findings = []
    for c in load_jsonl(DATA / "evals" / "client_revenue_delivery_cases.jsonl"):
        got = decide(c)
        exp = c.get("expected_decision")
        if got != exp:
            findings.append(_f("eval_mismatch", f"{c.get('id')} expected {exp} got {got}"))
    return findings


CHECKS = [
    ("secrets/PII", check_secrets),
    ("whatsapp", check_whatsapp),
    ("payments", check_payments),
    ("proposals", check_proposals),
    ("proof_packs", check_proof_packs),
    ("renewals/upsells", check_renewals_upsells),
    ("delivery", check_delivery),
    ("evals", check_evals_consistency),
]


def run() -> bool:
    print("=" * 78)
    print("  DEALIX CLIENT + REVENUE + DELIVERY SAFETY CHECK")
    print("=" * 78)
    total = []
    for name, fn in CHECKS:
        findings = fn()
        status = "OK" if not findings else f"{len(findings)} issue(s)"
        print(f"  [{ 'PASS' if not findings else 'FAIL' }] {name:<18} {status}")
        for f in findings:
            print(f"        - [{f['rule']}] {f['detail']}")
        total.extend(findings)
    print("-" * 78)
    if total:
        print(f"  RESULT: NON-COMPLIANT ({len(total)} finding(s))")
    else:
        print("  RESULT: COMPLIANT ✓  (approval-first, dry-run, no secrets, catalog-mapped)")
    print("=" * 78)
    return not total


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
