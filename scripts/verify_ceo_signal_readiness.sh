#!/usr/bin/env bash
# Routes to the correct verification gate (CEO Signal Readiness helper).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3)"

usage() {
  cat <<'EOF'
Usage: bash scripts/verify_ceo_signal_readiness.sh [target]

  (no arg)          same as transformation — fast default
  all               transformation bundle + enterprise control plane (default verify_global_ai_transformation.sh)
  transformation    python scripts/verify_global_ai_transformation.py only
  control_plane     bash scripts/verify_enterprise_control_plane.sh
  revenue_os        bash scripts/revenue_os_master_verify.sh
  category_gates    python scripts/verify_global_ai_transformation.py --check-category-expansion

Pick one gate based on what changed; avoid running unrelated heavy suites.
EOF
}

cmd="${1:-transformation}"
if [[ "$cmd" == "-h" || "$cmd" == "--help" || "$cmd" == "help" ]]; then
  usage
  exit 0
fi

case "$cmd" in
  all)
    bash "${ROOT}/scripts/verify_global_ai_transformation.sh"
    ;;
  transformation)
    "$PYTHON_BIN" "${ROOT}/scripts/verify_global_ai_transformation.py"
    ;;
  control_plane)
    bash "${ROOT}/scripts/verify_enterprise_control_plane.sh"
    ;;
  revenue_os)
    bash "${ROOT}/scripts/revenue_os_master_verify.sh"
    ;;
  category_gates)
    "$PYTHON_BIN" "${ROOT}/scripts/verify_global_ai_transformation.py" --check-category-expansion
    ;;
  *)
    usage
    exit 2
    ;;
esac
