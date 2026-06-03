#!/usr/bin/env bash
# Dealix — Interactive first-time setup
# إعداد تفاعلي لأول مرة
#
# Walks a fresh clone through:
#   1. Python venv + dev deps
#   2. .env generation (interactive prompts for the keys that matter)
#   3. Pre-commit hooks
#   4. Alembic single-head check
#   5. Smoke import of api.main
#
# Idempotent — re-running it skips steps already done.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

CYAN="\033[36m"; GREEN="\033[32m"; YELLOW="\033[33m"; RED="\033[31m"; RESET="\033[0m"

say() { printf "${CYAN}→${RESET} %s\n" "$*"; }
ok()  { printf "${GREEN}✓${RESET} %s\n" "$*"; }
warn(){ printf "${YELLOW}⚠${RESET} %s\n" "$*"; }
err() { printf "${RED}✗${RESET} %s\n" "$*" >&2; }

ask() {
    local prompt="$1" default="${2:-}" var
    if [ -n "$default" ]; then
        read -r -p "  $prompt [$default]: " var
        echo "${var:-$default}"
    else
        read -r -p "  $prompt: " var
        echo "$var"
    fi
}

# ── 1. Python + venv ───────────────────────────────────────────
say "Checking Python version"
PYTHON="${PYTHON:-python3}"
if ! "$PYTHON" -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"; then
    err "Python 3.11+ required (got: $("$PYTHON" --version 2>&1))"
    exit 1
fi
ok "$("$PYTHON" --version)"

# ── 2. Dev dependencies ────────────────────────────────────────
say "Installing dev dependencies (pip install -e \".[dev]\")"
"$PYTHON" -m pip install --quiet --upgrade pip
"$PYTHON" -m pip install --quiet -e ".[dev]"
ok "Dev dependencies installed"

# ── 3. .env generation ─────────────────────────────────────────
if [ -f .env ]; then
    warn ".env already exists — skipping interactive generation"
    warn "Delete it first if you want to regenerate: rm .env"
else
    say "Generating .env (interactive — press Enter to accept defaults)"
    echo
    echo "  Required keys: ENVIRONMENT, APP_SECRET_KEY, DATABASE_URL, APP_URL,"
    echo "  ADMIN_API_KEYS, CORS_ORIGINS. Everything else can stay blank for now."
    echo

    ENV_CHOICE=$(ask "Environment (development|staging|production)" "development")
    APP_SECRET=$("$PYTHON" -c "import secrets; print(secrets.token_hex(32))")
    JWT_SECRET=$("$PYTHON" -c "import secrets; print(secrets.token_hex(32))")
    ADMIN_KEY=$("$PYTHON" -c "import secrets; print('admin_'+secrets.token_urlsafe(24))")
    API_KEY=$("$PYTHON" -c "import secrets; print('dealix_'+secrets.token_urlsafe(24))")

    DB_URL=$(ask "DATABASE_URL" "postgresql+asyncpg://dealix:dealix@localhost:5432/dealix")
    APP_URL=$(ask "APP_URL (public base for callbacks)" "http://localhost:8000")
    CORS=$(ask "CORS_ORIGINS (comma-separated)" "http://localhost:3000,http://localhost:8000")

    echo
    say "Optional integrations (press Enter to skip — you can fill these later)"
    OPENAI=$(ask "OPENAI_API_KEY (optional)" "")
    ANTHROPIC=$(ask "ANTHROPIC_API_KEY (optional)" "")
    MOYASAR=$(ask "MOYASAR_SECRET_KEY (optional)" "")

    cp .env.example .env

    # Inline edits — portable sed via python (avoids BSD/GNU differences)
    "$PYTHON" - <<PYEOF
from pathlib import Path
p = Path(".env")
text = p.read_text()
subs = {
    "ENVIRONMENT=production": "ENVIRONMENT=$ENV_CHOICE",
    "APP_SECRET_KEY=CHANGE_ME_to_64_byte_hex": "APP_SECRET_KEY=$APP_SECRET",
    "DATABASE_URL=postgresql://user:pass@host:5432/dealix": "DATABASE_URL=$DB_URL",
    "APP_URL=https://dealix.sa": "APP_URL=$APP_URL",
    "API_KEYS=REPLACE_with_comma_separated_keys": "API_KEYS=$API_KEY",
    "ADMIN_API_KEYS=REPLACE_with_admin_only_key": "ADMIN_API_KEYS=$ADMIN_KEY",
    "CORS_ORIGINS=https://dealix.sa,https://www.dealix.sa,http://localhost:3000": "CORS_ORIGINS=$CORS",
}
for old, new in subs.items():
    text = text.replace(old, new)
# Append a JWT secret if not already present
if "JWT_SECRET_KEY=" not in text:
    text += f"\nJWT_SECRET_KEY=$JWT_SECRET\n"
# Optional keys
if "$OPENAI":
    text = text.replace("OPENAI_API_KEY=", f"OPENAI_API_KEY=$OPENAI", 1)
if "$ANTHROPIC":
    text = text.replace("ANTHROPIC_API_KEY=", f"ANTHROPIC_API_KEY=$ANTHROPIC", 1)
if "$MOYASAR":
    text = text.replace("MOYASAR_SECRET_KEY=sk_live_REPLACE_ME", f"MOYASAR_SECRET_KEY=$MOYASAR", 1)
p.write_text(text)
PYEOF

    chmod 600 .env || true
    ok ".env created (chmod 600)"
fi

# ── 4. Pre-commit hooks ────────────────────────────────────────
say "Installing pre-commit hooks"
if command -v pre-commit >/dev/null 2>&1; then
    pre-commit install --install-hooks >/dev/null 2>&1 || warn "pre-commit install failed (non-fatal)"
    ok "Pre-commit hooks installed"
else
    warn "pre-commit not on PATH; skipping (will be available after dev deps install)"
fi

# ── 5. Alembic single-head check ───────────────────────────────
say "Checking Alembic migration heads"
if "$PYTHON" scripts/check_alembic_single_head.py >/dev/null 2>&1; then
    ok "Single Alembic head ✓"
else
    warn "Multiple heads or alembic not yet reachable — run 'alembic heads' to inspect"
fi

# ── 6. Smoke import ────────────────────────────────────────────
say "Smoke-importing api.main"
if "$PYTHON" -c "from api.main import app; print('routes:', len(app.routes))" 2>&1 | tail -5; then
    ok "api.main imports cleanly"
else
    err "api.main import failed — see traceback above"
fi

echo
ok "Setup complete."
echo
echo "Next:"
echo "  • Run the API:        make run"
echo "  • Run the test suite: make test"
echo "  • Daily founder brief: python scripts/dealix_founder_daily_brief.py"
echo "  • Read what to do next: less docs/playbooks/FOUNDER_NEXT_STEPS.md"
