#!/usr/bin/env bash
# Single-shot dev-environment bootstrap. Runs inside the devcontainer
# (post-create), or locally when a contributor hits `make hooks`.
#
# What it does:
#   1. Installs Python deps (runtime + dev).
#   2. Installs pre-commit hooks.
#   3. Pulls fresh Mintlify / Fern / Spectral CLIs.
#   4. Prints a "next steps" message.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

step() { printf '\n\033[1;34m→ %s\033[0m\n' "$1"; }

step "1. Python deps (runtime)"
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt 2>/dev/null || true
pip install -e . 2>/dev/null || true

step "2. Pre-commit hooks"
pip install pre-commit
pre-commit install --install-hooks

step "3. Node / Mintlify / Fern / Spectral CLIs (optional)"
if command -v npm >/dev/null 2>&1; then
  npm install -g mintlify fern-api @stoplight/spectral-cli 2>/dev/null || \
    echo "   (npm globals failed; non-blocking)"
fi

step "4. Done"
cat <<'EOF'
Next:
  - Copy .env.example to .env and fill in the keys you have today.
  - `uvicorn api.main:app --reload`           # backend
  - `cd frontend && npm install && npm run dev`  # frontend
  - `docker compose -f docker-compose.yml up`    # services

Docs:
  - docs/QA_REVIEW.md         — what the codebase is + isn't.
  - docs/adr/index.md         — architectural decisions.
  - docs/sla.md               — service-level commitments.
  - docs/compliance/CONTROLS.md — SOC 2 controls map.
EOF
