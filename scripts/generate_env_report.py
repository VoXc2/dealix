"""Generate a redacted env report (no values printed)."""
from __future__ import annotations

import datetime as dt
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "reports" / "ops"
OUT_DIR.mkdir(parents=True, exist_ok=True)


CHECKED_VARS = [
    "APP_ENV",
    "APP_SECRET_KEY",
    "DATABASE_URL",
    "ENVIRONMENT",
    "DEALIX_ADMIN_TOKEN",
    "DEALIX_ADMIN_PASSWORD",
    "GOOGLE_PLACES_API_KEY",
    "HUBSPOT_PRIVATE_APP_TOKEN",
    "WHATSAPP_BUSINESS_TOKEN",
    "EMAIL_PROVIDER_API_KEY",
    "OPENAI_API_KEY",
    "MINIMAX_API_KEY",
    "KIMI_API_KEY",
    "DEEPSEEK_API_KEY",
    "OPENROUTER_API_KEY",
    "AI_PROVIDER_DEFAULT",
    "AI_MODE_DEMO",
    "NEXT_PUBLIC_DEMO_MODE",
    "NEXT_PUBLIC_API_URL",
]


def main() -> int:
    today = dt.date.today().isoformat()
    lines: list[str] = []
    lines.append(f"# Dealix Env Report — {today}")
    lines.append("")
    lines.append("Values redacted. Only shows whether var is set.")
    lines.append("")
    lines.append("| Var | Set |")
    lines.append("|-----|-----|")
    for v in CHECKED_VARS:
        is_set = "yes" if os.environ.get(v) else "no"
        lines.append(f"| {v} | {is_set} |")
    out = OUT_DIR / f"env-report-{today}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
