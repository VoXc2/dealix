from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
import uuid
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/company_os/control"
REPORTS = ROOT / "reports/company_os/control"

URLS = {
    "api_health": "https://api.dealix.me/healthz",
    "web_demo": "https://web-production-380c3.up.railway.app/ar/demo",
    "revenue_os": "https://web-production-380c3.up.railway.app/revenue-os",
    "zatca": "https://web-production-380c3.up.railway.app/ar/zatca-readiness",
}

ASSETS = [
    "docs/company_os/enterprise/ENTERPRISE_OPERATING_MODEL_AR.md",
    "docs/company_os/STRATEGIC_COMMAND_LAYER_AR.md",
    "docs/data_room/DEALIX_COMPANY_ONE_PAGER_AR.md",
    "docs/proof_factory/P1_PROOF_PACK_TEMPLATE_AR.md",
    "docs/partner_os/PARTNER_REFERRAL_SYSTEM_AR.md",
    "docs/brand/DEALIX_VISUAL_IDENTITY_AR.md",
    "docs/pitch/DEALIX_MASTER_PITCH_DECK_AR.md",
    "docs/conversion/DEALIX_HIGH_CONVICTION_SALES_PAGE_AR.md",
]

def now():
    return datetime.now(UTC).isoformat()

def ensure():
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

def append_jsonl(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows

def http(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "dealix-brain-control/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return {"ok": 200 <= r.status < 400, "status": r.status}
    except Exception as e:
        return {"ok": False, "error": repr(e)}

def sh(cmd):
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=60)
        return {"ok": p.returncode == 0, "code": p.returncode, "stdout": p.stdout[-2000:], "stderr": p.stderr[-2000:]}
    except Exception as e:
        return {"ok": False, "error": repr(e)}

def status():
    return {
        "generated_at": now(),
        "production": {k: http(v) for k, v in URLS.items()},
        "repo": {
            "branch": sh(["git", "branch", "--show-current"]).get("stdout", "").strip(),
            "last_commit": sh(["git", "log", "-1", "--oneline"]).get("stdout", "").strip(),
            "status": sh(["git", "status", "--short"]).get("stdout", ""),
        },
        "assets": {p: (ROOT / p).exists() for p in ASSETS},
    }

def classify(text):
    t = text.lower()
    areas = []
    if any(x in t for x in ["بيع", "sales", "عميل", "client", "p1", "p2", "p3", "offer"]):
        areas.append("commercial")
    if any(x in t for x in ["موقع", "web", "api", "deploy", "production", "railway"]):
        areas.append("production")
    if any(x in t for x in ["هوية", "brand", "pitch", "عرض", "presentation"]):
        areas.append("brand")
    if any(x in t for x in ["مخ", "brain", "agent", "hermes", "automation"]):
        areas.append("brain")
    if any(x in t for x in ["أمن", "security", "secret", "governance"]):
        areas.append("governance")
    return areas or ["ceo"]

def plan(text):
    areas = classify(text)
    actions = []
    if "production" in areas:
        actions.append("Run production smoke check: API health, demo, revenue-os, ZATCA.")
    if "commercial" in areas:
        actions.append("Sell P1 first. Create 5 warm manual outreach drafts. Prepare 1 P1 proposal.")
    if "brand" in areas:
        actions.append("Review pitch deck, visual identity, sales page, and objection handling.")
    if "brain" in areas:
        actions.append("Run CEO brain, content factory, and growth scorecard.")
    if "governance" in areas:
        actions.append("Verify no auto-send, no scraping, no exposed secrets, approval required.")
    if not actions:
        actions.append("Generate CEO daily brief and choose one revenue action before building features.")
    return {
        "areas": areas,
        "actions": actions,
        "guardrails": ["no auto-send", "no scraping", "human approval", "no ROI claim without baseline"],
    }

def ask(text, priority="normal"):
    ensure()
    item = {"id": str(uuid.uuid4())[:8], "created_at": now(), "priority": priority, "command": text, "status": "queued"}
    append_jsonl(DATA / "commands.jsonl", item)
    return item

def tick():
    ensure()
    commands = read_jsonl(DATA / "commands.jsonl")
    processed = read_jsonl(DATA / "processed.jsonl")
    done = {x.get("id") for x in processed}
    pending = [c for c in commands if c.get("id") not in done]
    results = []
    for c in pending[-10:]:
        p = plan(c.get("command", ""))
        results.append({"command": c, "plan": p, "status": "planned", "planned_at": now()})
        append_jsonl(DATA / "processed.jsonl", {"id": c.get("id"), "processed_at": now(), "status": "planned"})
    payload = {"status": status(), "processed_now": results}
    write_json(REPORTS / "latest_tick.json", payload)
    md = ["# Dealix Brain Response", "", f"Generated: {now()}", ""]
    if not results:
        md.append("No new commands.")
    for r in results:
        md += [f"## Command {r['command']['id']}", r["command"]["command"], "", "### Actions"]
        md += [f"- {a}" for a in r["plan"]["actions"]]
        md += ["", "### Guardrails"]
        md += [f"- {g}" for g in r["plan"]["guardrails"]]
    (REPORTS / "latest_response.md").write_text("\n".join(md), encoding="utf-8")
    return payload

def doctor():
    s = status()
    checks = []
    checks.extend(v.get("ok", False) for v in s["production"].values())
    checks.extend(s["assets"].values())
    checks.append(not bool(s["repo"]["status"].strip()))
    score = round(sum(1 for x in checks if x) / len(checks) * 100, 2)
    payload = {"score": score, "result": "PASS" if score >= 95 else "NEEDS_ATTENTION", "status": s}
    write_json(REPORTS / "doctor.json", payload)
    return payload

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ask")
    a.add_argument("text", nargs="+")
    a.add_argument("--priority", default="normal")
    sub.add_parser("tick")
    sub.add_parser("status")
    sub.add_parser("inbox")
    sub.add_parser("doctor")
    args = parser.parse_args()

    if args.cmd == "ask":
        out = ask(" ".join(args.text), args.priority)
        print("BRAIN_COMMAND_QUEUED=PASS")
    elif args.cmd == "tick":
        out = tick()
        print("BRAIN_TICK=PASS")
    elif args.cmd == "status":
        out = status()
        print("BRAIN_STATUS=PASS")
    elif args.cmd == "inbox":
        out = {"commands": read_jsonl(DATA / "commands.jsonl"), "processed": read_jsonl(DATA / "processed.jsonl")}
        print("BRAIN_INBOX=PASS")
    else:
        out = doctor()
        print("BRAIN_DOCTOR=" + out["result"])
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
