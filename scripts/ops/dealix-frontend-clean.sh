#!/usr/bin/env bash
# dealix-frontend-clean — safe cache cleanup for Dealix frontend (no sudo, no root-owned delete via sudo)
set -Eeuo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT/frontend"
echo "=== Frontend clean (safe, no sudo) ==="
# Remove only dealix-owned cache; root-owned .next/diagnostics is left for next successful build to overwrite
if [[ -d .next/cache ]]; then
  rm -rf .next/cache && echo "cleaned .next/cache"
fi
if [[ -d .next/static && -w .next/static ]]; then
  echo ".next/static exists and writable"
fi
# Check for root-owned pollution
if [[ -d .next/diagnostics ]]; then
  owner=$(stat -c %U .next/diagnostics 2>/dev/null || echo unknown)
  if [[ "$owner" == "root" ]]; then
    echo "WARN: .next/diagnostics owned by root — next build will fail EACCES"
    echo "FIX: requires host cleanup via approved L5:"
    echo "  rm -rf $REPO_ROOT/frontend/.next"
    echo "  (run as dealix after ensuring no build in progress, or via CI with correct ownership)"
    echo "WORKAROUND: typecheck still passes (no .next write), use for verification"
  fi
fi
echo "---Running typecheck (no .next write)---"
npm run typecheck
echo "CLEAN_DONE"
