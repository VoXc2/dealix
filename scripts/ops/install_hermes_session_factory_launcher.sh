#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

REPO=/opt/dealix/workspace/dealix
TARGET=/home/dealix/.hermes/scripts/dealix_autonomous_development_factory.sh
ACCEPTED_SHA=""
APPLY=0
SELF_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

usage() {
  cat <<'EOF'
Usage: install_hermes_session_factory_launcher.sh --accepted-sha <40hex> [--repo PATH] [--target PATH] [--apply]
Default mode is DRY_RUN. --apply mutates the target and is a material runtime action.
EOF
}

while (($#)); do
  case "$1" in
    --accepted-sha) ACCEPTED_SHA="${2:-}"; shift 2 ;;
    --repo) REPO="${2:-}"; shift 2 ;;
    --target) TARGET="${2:-}"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "UNKNOWN_ARGUMENT=$1" >&2; usage >&2; exit 64 ;;
  esac
done
PY="${DEALIX_PYTHON_BIN:-$REPO/.venv/bin/python}"
[[ "$ACCEPTED_SHA" =~ ^[0-9a-f]{40}$ ]] || {
  echo "HOLD_INVALID_ACCEPTED_SHA" >&2
  exit 64
}
[[ -x "$PY" ]] || {
  echo "HOLD_CANONICAL_PYTHON_MISSING=$PY" >&2
  exit 75
}

ACTUAL_SHA="$(git -C "$REPO" rev-parse HEAD 2>/dev/null || true)"
if [[ "$ACTUAL_SHA" != "$ACCEPTED_SHA" ]]; then
  echo "HOLD_SOURCE_IDENTITY expected=$ACCEPTED_SHA actual=${ACTUAL_SHA:-UNKNOWN}" >&2
  exit 75
fi
if [[ -n "$(git -C "$REPO" status --porcelain --untracked-files=no)" ]]; then
  echo "HOLD_DIRTY_SOURCE=$REPO" >&2
  exit 75
fi

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
"$PY" "$SELF_DIR/render_hermes_session_factory_launcher.py" \
  --accepted-sha "$ACCEPTED_SHA" --repo "$REPO" --output "$TMP" >/dev/null
"$PY" "$SELF_DIR/verify_hermes_session_factory_launcher.py" "$TMP" \
  --accepted-sha "$ACCEPTED_SHA" --repo "$REPO"
bash -n "$TMP"

echo "SOURCE_SHA=$ACCEPTED_SHA"
echo "TARGET=$TARGET"
if ((APPLY == 0)); then
  echo "HERMES_SESSION_FACTORY_LAUNCHER_INSTALL=DRY_RUN_PASS"
  exit 0
fi

install -d -m 0750 "$(dirname -- "$TARGET")"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP=""
if [[ -e "$TARGET" ]]; then
  BACKUP="${TARGET}.bak-${STAMP}"
  cp -a -- "$TARGET" "$BACKUP"
fi
install -m 0750 "$TMP" "$TARGET"

"$PY" "$SELF_DIR/verify_hermes_session_factory_launcher.py" "$TARGET" \
  --accepted-sha "$ACCEPTED_SHA" --repo "$REPO"
echo "HERMES_SESSION_FACTORY_LAUNCHER_INSTALL=APPLIED"
if [[ -n "$BACKUP" ]]; then
  echo "BACKUP=$BACKUP"
  printf 'ROLLBACK=install -m 0750 %q %q\n' "$BACKUP" "$TARGET"
else
  printf 'ROLLBACK=rm -f %q\n' "$TARGET"
fi
