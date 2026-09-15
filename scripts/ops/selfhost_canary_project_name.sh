#!/usr/bin/env bash
set -Eeuo pipefail

dealix_canary_project_name() {
  local sha="${1:-}"
  local run_id="${2:-}"

  if ! [[ "$sha" =~ ^[0-9a-f]{40}$ ]]; then
    echo "HOLD: canary project requires an exact 40-char lowercase SHA" >&2
    return 64
  fi
  if ! [[ "$run_id" =~ ^[a-z0-9][a-z0-9-]{0,23}$ ]]; then
    echo "HOLD: DEALIX_CANARY_RUN_ID must match ^[a-z0-9][a-z0-9-]{0,23}$" >&2
    return 64
  fi

  printf 'dealix-selfhost-%s-%s\n' "${sha:0:12}" "$run_id"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  dealix_canary_project_name "${1:-}" "${2:-}"
fi
