#!/bin/bash
# SessionStart hook — prepares the workspace for Claude Code on the web.
# Installs Python dev dependencies so linters and tests are runnable.
# Idempotent and non-interactive. Runs synchronously (session waits for it).
set -euo pipefail

# Only run inside Claude Code on the web; local sessions manage their own env.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo "[session-start] Installing Python dev dependencies (pyproject [dev] extra)..."
python3 -m pip install -e ".[dev]" --quiet

echo "[session-start] Workspace ready. Lint: 'ruff check . && black --check .' | Tests: 'python3 -m pytest tests/unit -q --no-cov'"
