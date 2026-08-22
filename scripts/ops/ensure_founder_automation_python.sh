#!/usr/bin/env bash
# Ensure Dealix VPS/founder automation has a repository-local Python runtime
# with the declared application + development dependency contract.
set -Eeuo pipefail
umask 027

ROOT="${DEALIX_REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
VENV="${DEALIX_AUTOMATION_VENV:-$ROOT/.venv}"
REQ="$ROOT/requirements-dev.txt"
REQ_BASE="$ROOT/requirements.txt"
PYTHON_BOOTSTRAP="${DEALIX_BOOTSTRAP_PYTHON:-python3}"
STAMP="$VENV/.dealix-requirements-dev.sha256"
LOCK="$VENV/.dealix-bootstrap.lock"

fail() {
  echo "DEALIX_AUTOMATION_PYTHON=FAIL_CLOSED"
  echo "$*"
  exit 1
}

[[ -f "$REQ" ]] || fail "missing dependency contract: $REQ"
[[ -f "$REQ_BASE" ]] || fail "missing production dependency contract: $REQ_BASE"
command -v "$PYTHON_BOOTSTRAP" >/dev/null 2>&1 || fail "bootstrap python not found: $PYTHON_BOOTSTRAP"
command -v flock >/dev/null 2>&1 || fail "flock is required for dependency bootstrap locking"

# Protect both virtualenv creation and dependency synchronization. mkdir -p is
# concurrency-safe, and Python's venv can initialize the already-created empty
# directory after this process owns the lock.
mkdir -p "$VENV"
exec 9>"$LOCK"
flock -w 300 9 || fail "timed out waiting for automation python bootstrap lock"

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "automation_python_bootstrap=CREATE_VENV path=$VENV"
  "$PYTHON_BOOTSTRAP" -m venv "$VENV" || fail "could not create virtualenv; install the OS python venv package during VPS provisioning"
fi

# requirements-dev.txt includes requirements.txt, so both files are part of the
# effective dependency contract. Hash both explicitly: changing production
# pins must invalidate the VPS automation runtime even when the dev file itself
# did not change.
REQ_HASH="$(sha256sum "$REQ" "$REQ_BASE" | sha256sum | awk '{print $1}')"
INSTALLED_HASH="$(cat "$STAMP" 2>/dev/null || true)"

runtime_ok() {
  "$VENV/bin/python" - <<'PY' >/dev/null 2>&1
import fastapi
import httpx
import pydantic
import pytest
import yaml
PY
}

if [[ "$INSTALLED_HASH" != "$REQ_HASH" ]] || ! runtime_ok; then
  echo "automation_python_dependencies=SYNC_REQUIRED"
  # The systemd company service intentionally has ProtectHome=read-only.
  # Avoid pip's user-cache path and install only inside the ignored repo venv.
  PIP_DISABLE_PIP_VERSION_CHECK=1 "$VENV/bin/python" -m pip install \
    --no-input --no-cache-dir -r "$REQ" \
    || fail "dependency sync failed; existing timers remain fail-closed"
  runtime_ok || fail "automation runtime is missing required modules after dependency sync"
  printf '%s\n' "$REQ_HASH" >"$STAMP"
  chmod 0640 "$STAMP" 2>/dev/null || true
else
  echo "automation_python_dependencies=UNCHANGED"
fi

"$VENV/bin/python" - <<'PY'
import sys
import fastapi
import pydantic
import pytest
print(f"automation_python={sys.executable}")
print(f"automation_python_version={sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print(f"fastapi_version={fastapi.__version__}")
print(f"pydantic_version={pydantic.__version__}")
print(f"pytest_version={pytest.__version__}")
PY

echo "DEALIX_AUTOMATION_PYTHON=PASS"
printf '%s\n' "$VENV/bin/python"
