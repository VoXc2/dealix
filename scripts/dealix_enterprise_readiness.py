import json
import urllib.request
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

URLS = {
    "api_health": "https://api.dealix.me/healthz",
    "web_demo": "https://web-production-380c3.up.railway.app/ar/demo",
    "web_revenue": "https://web-production-380c3.up.railway.app/revenue-os",
    "web_zatca": "https://web-production-380c3.up.railway.app/ar/zatca-readiness",
}

FILES = [
    "docs/company_os/enterprise/ENTERPRISE_OPERATING_MODEL_AR.md",
    "docs/company_os/enterprise/SERVICE_CATALOG_AR.md",
    "docs/company_os/enterprise/SLA_AND_SUPPORT_MODEL_AR.md",
    "docs/company_os/enterprise/INCIDENT_RESPONSE_RUNBOOK_AR.md",
    "docs/company_os/security/AI_AGENT_SECURITY_MODEL_AR.md",
    "docs/company_os/security/SECRET_ROTATION_RUNBOOK_AR.md",
    "docs/company_os/customer_success/CUSTOMER_SUCCESS_OS_AR.md",
    "docs/company_os/quality/QUALITY_GATE_MODEL_AR.md",
    "docs/commercial/offers/P1_REVENUE_INTELLIGENCE_SPRINT_AR.md",
    "docs/proof_factory/P1_PROOF_PACK_TEMPLATE_AR.md",
]

def check_url(url: str) -> dict:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "dealix-enterprise-readiness/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return {"ok": 200 <= r.status < 400, "status": r.status}
    except Exception as exc:
        return {"ok": False, "error": repr(exc)}

def main() -> int:
    url_results = {name: check_url(url) for name, url in URLS.items()}
    file_results = {path: Path(path).exists() for path in FILES}

    score_items = []
    score_items.extend(bool(v.get("ok")) for v in url_results.values())
    score_items.extend(file_results.values())

    passed = sum(1 for item in score_items if item)
    total = len(score_items)
    score = round((passed / total) * 100, 2)

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "score": score,
        "passed": passed,
        "total": total,
        "urls": url_results,
        "files": file_results,
        "result": "PASS" if score >= 95 else "NEEDS_ATTENTION",
    }

    out = ROOT / "reports" / "company_os" / "daily"
    out.mkdir(parents=True, exist_ok=True)
    (out / "ENTERPRISE_READINESS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "ENTERPRISE_READINESS.md").write_text(f'''# Dealix Enterprise Readiness

Generated: {payload["generated_at"]}

Score: {score}%

Result: {payload["result"]}

Passed: {passed}/{total}

## URLs

{json.dumps(url_results, ensure_ascii=False, indent=2)}

## Files

{json.dumps(file_results, ensure_ascii=False, indent=2)}
''', encoding="utf-8")

    print("DEALIX_ENTERPRISE_READINESS=" + payload["result"])
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["result"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
