#!/bin/bash
# SessionStart hook — installs Python deps so the API imports and tests run.
# The Claude Code on the web container is ephemeral and starts with nothing
# installed. Synchronous: the session waits until deps are ready.
set -euo pipefail

# Only the remote (web) container needs this; local machines already have deps.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Idempotent: if the API already imports, deps are present — nothing to do.
if python -c "from api.main import app" >/dev/null 2>&1; then
  exit 0
fi

bash "${CLAUDE_PROJECT_DIR:-.}/scripts/web_session_setup.sh"
