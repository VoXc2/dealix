#!/usr/bin/env bash
# Web session setup — installs Python deps so the API can import and tests
# can run. Wired as a Claude Code SessionStart hook (.claude/settings.json):
# the web execution container is ephemeral and starts with no deps installed.
#
# This container ships a Debian-patched setuptools that (a) cannot build the
# `ummalqura` sdist (AttributeError: install_layout) and (b) refuses to
# uninstall Debian-managed packages (PyYAML, wheel). Both are worked around
# here. On a normal environment (e.g. GitHub CI) the workarounds are no-ops.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== web_session_setup: installing dependencies =="

# 1. ummalqura — pure-python, but its legacy sdist fails to build under the
#    container's patched setuptools. Build its wheel in a throwaway venv that
#    has a clean PyPI setuptools, then install that wheel.
if ! python -c "import ummalqura" >/dev/null 2>&1; then
  echo "== web_session_setup: building ummalqura wheel (workaround) =="
  TMP="$(mktemp -d)"
  python -m venv "$TMP/venv"
  "$TMP/venv/bin/pip" install --quiet --upgrade pip setuptools wheel
  "$TMP/venv/bin/pip" wheel --quiet --no-deps --wheel-dir "$TMP/dist" ummalqura
  pip install --quiet "$TMP"/dist/ummalqura-*.whl
  rm -rf "$TMP"
fi

# 2. Everything else. --ignore-installed makes pip shadow Debian-managed
#    packages in site-packages instead of failing to uninstall them.
#    ummalqura is filtered out (already installed above); the dev file's
#    `-r requirements.txt` include is dropped so ummalqura is not re-pulled.
TMPREQ="$(mktemp -d)"
grep -v '^ummalqura' requirements.txt > "$TMPREQ/req.txt"
grep -v '^-r requirements.txt' requirements-dev.txt > "$TMPREQ/dev.txt"
pip install --quiet --ignore-installed -r "$TMPREQ/req.txt" -r "$TMPREQ/dev.txt"
rm -rf "$TMPREQ"

echo "== web_session_setup: done =="
