#!/usr/bin/env bash
# Curated ruff pass — avoids repo-wide drift until incremental cleanup.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PATH="$HOME/.local/bin:$PATH"

ruff check \
  core/config/settings.py \
  api/routers/revenue_os.py \
  api/routers/proof_ledger.py \
  auto_client_acquisition/revenue_memory/async_facade.py \
  tests/test_revenue_memory_async_facade.py \
  tests/test_proof_ledger_tenant_context.py \
  tests/test_revenue_os_events_tenant.py
