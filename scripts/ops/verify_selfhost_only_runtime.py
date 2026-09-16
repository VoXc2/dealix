from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
forbidden_paths = [
    ROOT / ".github/workflows",
    ROOT / "railway.json",
    ROOT / "railway.toml",
    ROOT / "railway.web.toml",
    ROOT / "railway.company-brain.toml",
    ROOT / "vercel.json",
    ROOT / "apps/web/railway.json",
    ROOT / "apps/web/railway.toml",
    ROOT / "apps/web/vercel.json",
    ROOT / "frontend/railway.json",
    ROOT / "frontend/railway.toml",
]
present = [str(p.relative_to(ROOT)) for p in forbidden_paths if p.exists()]
compose = (ROOT / "deploy/selfhost/compose.yml").read_text(encoding="utf-8")
health = (ROOT / "apps/web/app/healthz/route.ts").read_text(encoding="utf-8")
required = ["dealix-api:${DEALIX_IMAGE_TAG", "dealix-web:${DEALIX_IMAGE_TAG", "public-cutover", "production-db"]
missing = [x for x in required if x not in compose]
forbidden_health = [x for x in ("RAILWAY_GIT_COMMIT_SHA", "VERCEL_GIT_COMMIT_SHA") if x in health]
if present or missing or forbidden_health:
    print(f"SELFHOST_ONLY_RUNTIME=FAIL present={present} missing={missing} health={forbidden_health}")
    raise SystemExit(1)
print("SELFHOST_ONLY_RUNTIME=PASS")
