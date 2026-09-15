#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

# DEALIX Ω∞ — legacy Agentic Holding launcher compatibility adapter
#
# This executable MUST NOT create worktrees or launch OpenCode directly.
# Canonical path:
#   launcher -> Session Factory queue -> ResourceGovernor -> isolated worktree
#   -> broker-authorized OpenCode -> tests -> independent verifier -> receipt
#
# L0-L4 repository work may be queued autonomously. L5 material effects remain
# exact-action governed by the canonical approval path.

export TZ="${TZ:-Asia/Riyadh}"
export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
export GH_PROMPT_DISABLED=1
export GIT_TERMINAL_PROMPT=0

RUN_USER="${DEALIX_RUN_USER:-dealix}"
RUN_HOME="${DEALIX_RUN_HOME:-/home/dealix}"
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
FACTORY_STATE="${DEALIX_SESSION_FACTORY_STATE:-/opt/dealix/control/state/session_factory}"
FACTORY="$REPO/scripts/ops/session_factory.py"
PYTHON="${DEALIX_PYTHON:-$REPO/.venv/bin/python}"
CURRENT_USER="$(id -un)"

if ! id "$RUN_USER" >/dev/null 2>&1; then
  echo "ERROR=RUN_USER_NOT_FOUND user=$RUN_USER"
  exit 1
fi
if [ "$CURRENT_USER" != "$RUN_USER" ] && [ "$(id -u)" -ne 0 ]; then
  echo "ERROR=RUN_AS_CANONICAL_USER_OR_ROOT current=$CURRENT_USER expected=$RUN_USER"
  exit 1
fi
if [ ! -d "$REPO/.git" ] && [ ! -f "$REPO/.git" ]; then
  echo "ERROR=CANONICAL_REPO_NOT_FOUND repo=$REPO"
  exit 1
fi
if [ ! -f "$FACTORY" ]; then
  echo "ERROR=CANONICAL_SESSION_FACTORY_NOT_FOUND path=$FACTORY"
  exit 1
fi

run_dealix() {
  if [ "$(id -un)" = "$RUN_USER" ]; then
    env \
      HOME="$RUN_HOME" \
      TZ="$TZ" LANG="$LANG" LC_ALL="$LC_ALL" \
      GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 \
      "$@"
  elif [ "$(id -u)" -eq 0 ]; then
    sudo -H -u "$RUN_USER" env \
      HOME="$RUN_HOME" \
      TZ="$TZ" LANG="$LANG" LC_ALL="$LC_ALL" \
      GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 \
      "$@"
  else
    echo "ERROR=CANONICAL_USER_SWITCH_UNAVAILABLE" >&2
    return 77
  fi
}

if [ ! -x "$PYTHON" ]; then
  PYTHON="$(run_dealix bash -lc 'command -v python3 || true')"
fi
if [ -z "${PYTHON:-}" ] || [ ! -x "$PYTHON" ]; then
  echo "ERROR=PYTHON_NOT_FOUND"
  exit 1
fi

# Freeze the exact live canonical base. No frozen historical SHA is accepted for
# this modifying job.
run_dealix git -C "$REPO" fetch origin main --quiet
BASE_SHA="$(run_dealix git -C "$REPO" rev-parse origin/main)"
[ -n "$BASE_SHA" ] || { echo "ERROR=LIVE_BASE_UNAVAILABLE"; exit 1; }

PROMPT=$(cat <<'EOF'
Continue the existing Dealix Omega V3 Company Machine from live repository truth.

Mission: improve the canonical Agentic Holding / Sector Company / Arm Pod / Specialist Logical Agent architecture only where current source still has evidence-backed gaps.

Mandatory rules:
- Reuse the one Company Machine, one Session Factory, one ResourceGovernor, one model broker, one approval/proof/economic truth plane.
- Do not create a second scheduler, router, CRM, agent fleet or proof system.
- Logical agents are registry identities, not one OS process per agent.
- Runtime modifying capacity belongs to ResourceGovernor; historical DEEP_WIP_MAX=3 is economic-focus compatibility only, never worker capacity authority.
- Historical five agent names are compatibility aliases only, never current logical-agent-count authority.
- OpenCode model/provider selection belongs only to the canonical broker. No caller/env/default may mint cost/privacy/data/model authority and no silent paid spill.
- Builder and independent Verifier must remain separate.
- Use the isolated exact-head worktree provided by Session Factory.
- Execute safe L0-L4 repo work end-to-end with focused tests and git diff --check.
- Never execute merge, production deploy/cutover, DNS/DB/schema/secret/firewall mutation, payment/spend, contract/tender action, live customer send or public publish.
- Research != Relationship; Draft != Sent; Quote != Revenue; HTTP 200 != release identity.

Read docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md if present, but current source/runtime contracts outrank historical prose.
Return a concise evidence receipt and the exact remaining blockers. Do not stop at a plan if a safe source fix can be completed.
EOF
)

RESULT="$(run_dealix "$PYTHON" - "$FACTORY" "$FACTORY_STATE" "$BASE_SHA" "$PROMPT" <<'PY'
from __future__ import annotations
import importlib.util
import json
import sys
from pathlib import Path

factory_path = Path(sys.argv[1])
state_dir = Path(sys.argv[2])
base_sha = sys.argv[3]
prompt = sys.argv[4]

spec = importlib.util.spec_from_file_location("dealix_session_factory_launcher", factory_path)
if spec is None or spec.loader is None:
    raise SystemExit("ERROR=SESSION_FACTORY_IMPORT_FAILED")
factory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(factory)

job = factory.make_job(
    owner_agent="dealix-engineer",
    business_goal="AGENTIC_HOLDING_SAFE_CONTINUATION",
    job_class="ENGINEERING",
    authority_level="L4",
    economic_reason="Improve autonomous company execution without bypassing canonical admission or creating parallel control planes",
    priority=95.0,
    urgency="high",
    base_sha=base_sha,
    modifying=True,
    executor={"prompt": prompt},
    acceptance={"criteria": "bounded engineering executor succeeds and returns evidence", "checks": [{"kind": "exit_zero"}]},
    tests=["focused tests for changed contracts", "git diff --check"],
    files_in_scope=[],
    context_refs=["omega-v3", "agentic-holding", "canonical-session-factory", f"exact-base:{base_sha}"],
    next_action="independent verifier reviews evidence; L5 remains action-bound",
)
result = factory.submit_job(state_dir, job)
payload = {
    "ok": bool(result.get("ok")),
    "job_id": job.get("JOB_ID"),
    "status": job.get("STATUS"),
    "base_sha": job.get("BASE_SHA"),
    "execution_mode": job.get("EXECUTION_MODE"),
    "authority_level": job.get("AUTHORITY_LEVEL"),
    "modifying": job.get("MODIFYING"),
    "errors": result.get("errors") or [],
}
print(json.dumps(payload, sort_keys=True))
raise SystemExit(0 if result.get("ok") else 2)
PY
)"

printf '%s\n' \
  "DEALIX_AGENTIC_HOLDING_QUEUE_RECEIPT" \
  "base_sha=$BASE_SHA" \
  "factory=$FACTORY" \
  "factory_state=$FACTORY_STATE" \
  "result=$RESULT" \
  "DIRECT_OPENCODE_EXECUTION=DENIED" \
  "DIRECT_WORKTREE_CREATION=DENIED" \
  "L5_EXECUTED=NONE"
