#!/bin/bash
# SessionStart hook — installs dependencies so the CEO one-session
# readiness gate (scripts/run_ceo_one_session_readiness.sh) and the
# verification suite are runnable in Claude Code on the web sessions.
#
# Without this, a fresh web container has no Python/Node deps and
# verify_global_ai_transformation.py fails with import errors that
# look like app failures but are pure environment blockers.
set -uo pipefail

# Only run in the remote (web) environment; local dev manages its own venv.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

echo "[session-start] installing Dealix dependencies..."

# Persist PYTHONPATH so module imports resolve from the repo root.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'export PYTHONPATH="."' >> "$CLAUDE_ENV_FILE"
fi

python3 -m pip install --quiet --upgrade pip 2>/dev/null || true

# Install runtime + dev deps, skipping ummalqura (a hijri-calendar
# package whose legacy build breaks on modern setuptools). It is only
# used by auto_client_acquisition/market_intelligence/saudi_seasons.py
# and is not on the verification path. The dev file's "-r" include is
# stripped so the filter applies to the runtime deps too.
grep -v -i 'ummalqura' requirements.txt > /tmp/dealix-runtime.txt
grep -v -i -E '^(#|-r )' requirements-dev.txt | grep -v -i 'ummalqura' > /tmp/dealix-dev.txt
# Single invocation so the resolver unifies runtime + dev constraints.
python3 -m pip install --quiet --ignore-installed \
  -r /tmp/dealix-runtime.txt -r /tmp/dealix-dev.txt

# ummalqura is best-effort: never let it fail the hook.
python3 -m pip install --quiet ummalqura 2>/dev/null \
  && echo "[session-start] ummalqura installed" \
  || echo "[session-start] ummalqura skipped (non-blocking)"

# Frontend deps (idempotent; cached after first run).
if [ -d frontend ]; then
  (cd frontend && npm install --silent --no-audit --no-fund) || \
    echo "[session-start] frontend npm install failed (non-blocking)"
fi

echo "[session-start] dependency install complete"
