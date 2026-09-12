#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

# DEALIX Ω∞ — Agentic Holding / Sector Company Mesh launcher
#
# Purpose:
# - Continue from live canonical Dealix state.
# - Create an isolated migration worktree from current origin/main.
# - Ask OpenCode to implement the adopted architecture in
#   docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md.
# - Keep repository mutation on an isolated branch.
#
# This launcher is L0-L4 only. It does not authorize production deploy,
# protected-main merge, DNS/DB/secret/firewall mutation, payment/spend,
# contract/tender submission, live customer send, or public publishing.

export TZ="${TZ:-Asia/Riyadh}"
export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
export GH_PROMPT_DISABLED=1
export GIT_TERMINAL_PROMPT=0

RUN_USER="${DEALIX_RUN_USER:-dealix}"
RUN_HOME="${DEALIX_RUN_HOME:-/home/dealix}"
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
WORKTREES="${DEALIX_WORKTREES:-/opt/dealix/worktrees}"
ARCH_DOC="docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md"
REPO_FULL="${DEALIX_REPO_FULL:-Dealix-sa/dealix}"

if [ "$(id -u)" -ne 0 ]; then
  echo "ERROR=RUN_AS_ROOT"
  exit 1
fi

if ! id "$RUN_USER" >/dev/null 2>&1; then
  echo "ERROR=RUN_USER_NOT_FOUND user=$RUN_USER"
  exit 1
fi

if [ ! -d "$REPO/.git" ]; then
  echo "ERROR=CANONICAL_REPO_NOT_FOUND repo=$REPO"
  exit 1
fi

install -d -m 0750 "$CONTROL/logs/agentic-holding" "$CONTROL/state/agentic-holding" "$WORKTREES"
chown -R "$RUN_USER:$RUN_USER" "$CONTROL/logs/agentic-holding" "$CONTROL/state/agentic-holding" "$WORKTREES"

run_dealix() {
  sudo -H -u "$RUN_USER" \
    env \
      HOME="$RUN_HOME" \
      TZ="$TZ" \
      LANG="$LANG" \
      LC_ALL="$LC_ALL" \
      GH_PROMPT_DISABLED=1 \
      GIT_TERMINAL_PROMPT=0 \
    "$@"
}

STAMP="$(date +%Y%m%dT%H%M%S)"
BRANCH="${DEALIX_BRANCH:-work/agentic-holding-sector-mesh-${STAMP}}"
WT="${DEALIX_WORKTREE:-$WORKTREES/agentic-holding-${STAMP}}"
LOG="$CONTROL/logs/agentic-holding/run-${STAMP}.log"

run_dealix git -C "$REPO" fetch origin --prune
BASE_SHA="$(run_dealix git -C "$REPO" rev-parse origin/main)"

printf '%s\n' \
  "DEALIX_AGENTIC_HOLDING_BOOTSTRAP" \
  "timestamp=$(date -Is)" \
  "base_sha=$BASE_SHA" \
  "branch=$BRANCH" \
  "worktree=$WT"

if run_dealix git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "ERROR=BRANCH_ALREADY_EXISTS branch=$BRANCH"
  exit 1
fi

run_dealix git -C "$REPO" worktree add -b "$BRANCH" "$WT" "$BASE_SHA"

if [ ! -f "$WT/$ARCH_DOC" ]; then
  echo "ERROR=ARCHITECTURE_DOCUMENT_MISSING path=$WT/$ARCH_DOC"
  exit 1
fi

cat > "$WT/.dealix-agentic-holding-run.env" <<EOF
DEALIX_AGENTIC_HOLDING_BASE_SHA=$BASE_SHA
DEALIX_AGENTIC_HOLDING_BRANCH=$BRANCH
DEALIX_AGENTIC_HOLDING_WORKTREE=$WT
DEALIX_AGENTIC_HOLDING_TIMESTAMP=$STAMP
DEALIX_AGENTIC_HOLDING_AUTHORITY=L0-L4_ONLY
EOF
chown "$RUN_USER:$RUN_USER" "$WT/.dealix-agentic-holding-run.env"

OPENCODE="${DEALIX_OPENCODE:-$RUN_HOME/.opencode/bin/opencode}"
if [ ! -x "$OPENCODE" ]; then
  OPENCODE="$(run_dealix bash -lc 'command -v opencode || true')"
fi

if [ -z "${OPENCODE:-}" ] || [ ! -x "$OPENCODE" ]; then
  echo "ERROR=OPENCODE_NOT_FOUND"
  echo "worktree=$WT"
  echo "architecture=$WT/$ARCH_DOC"
  exit 1
fi

PROMPT=$(cat <<'EOF'
You are the primary Dealix migration executor inside an isolated Git worktree.

This is a CONTINUATION of the existing Dealix company, not a greenfield rebuild.

Read completely before making changes:
- .dealix-agentic-holding-run.env
- docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md

Mission:
Implement the adopted Agentic Holding / Sector Company / Arm Pod architecture safely and incrementally on this branch.

Mandatory operating rules:
1. Inspect live repository truth first. Do not trust historical assumptions when code differs.
2. Do not create a second Company Brain, CRM, Economic Truth system, scheduler, model router, approval system or financial ledger.
3. Migrate the legacy exactly-five-agent invariant deliberately into the hierarchical Agent Registry model.
4. Migrate global DEEP_WIP_MAX=3 into a tested resource-aware concurrency governor; do not replace it with uncontrolled concurrency.
5. Treat every canonical sector as a virtual Sector Company under Dealix.
6. Treat every applicable canonical arm as an owned Agent Pod under its Sector Company.
7. Separate logical-agent identities from active runtime workers. Never spawn one permanent process per logical agent.
8. Preserve Economic Truth, consent/channel law, exact-release production truth, local-model privacy and material-action authority gates.
9. Use isolated worktrees for concurrent repository writers.
10. Reuse existing Hermes/OpenCode/Session Factory/Software Evolution components wherever possible.
11. Add migration adapters when needed rather than destructively rewriting all interfaces at once.
12. Add tests for hierarchy, parentage, no-orphans, sector/arm ownership, resource governance, worktree isolation, Economic Truth and authority gates.
13. Execute safe L0-L4 repository work end-to-end: inspect, edit, test, lint, compile/type-check as relevant, and verify the final diff.
14. Never execute L5 material effects in this run: no protected-main merge, production deploy/cutover, DNS, production DB/schema, secrets/keys, firewall/root infrastructure mutation, payment/spend, contract/tender action, live customer send or public publishing.
15. Never expose or print secrets.
16. Do not stop at a plan. Implement the strongest coherent bounded migration that can be verified on this exact head.

Before committing, run focused acceptance and then the broadest relevant bounded tests available. Always run git diff --check.

When coherent, commit on this isolated branch and push ONLY this branch if authenticated. Create or update ONE Draft PR if possible. Do not merge it.

Finish with this exact receipt header:
DEALIX_AGENTIC_HOLDING_RECEIPT

Include:
BASE_SHA=
HEAD_SHA=
BRANCH=
SECTORS_DISCOVERED=
SECTOR_COMPANIES_CREATED=
ARMS_DISCOVERED=
ARM_PODS_CREATED=
GROUP_AGENT_TEMPLATES=
SECTOR_AGENT_TEMPLATES=
ARM_AGENT_TEMPLATES=
TOTAL_LOGICAL_AGENTS=
MAX_SIMULTANEOUS_RUNTIME_AGENTS=
RESOURCE_GOVERNOR_STATUS=
LEGACY_FIVE_AGENT_INVARIANT=
LEGACY_DEEP_WIP_3_INVARIANT=
AGENT_HIERARCHY_TESTS=
ECONOMIC_TRUTH_TESTS=
AUTHORITY_TESTS=
WORKTREE_TESTS=
FULL_RELEVANT_ACCEPTANCE=
HERMES_STATUS=
OPENCODE_STATUS=
MODEL_ROUTER_STATUS=
DRAFT_PR=
L5_EXECUTED=NONE
TOP_10_NEXT_ECONOMIC_ACTIONS=
BLOCKERS=
APPROVAL_QUEUE=
EOF
)

set +e
run_dealix "$OPENCODE" run \
  --auto \
  --title "Dealix Agentic Holding Sector Company Mesh" \
  --dir "$WT" \
  "$PROMPT" 2>&1 | tee "$LOG"
RC="${PIPESTATUS[0]}"
set -e

printf '%s\n' \
  "DEALIX_AGENTIC_HOLDING_LAUNCHER_RECEIPT" \
  "opencode_rc=$RC" \
  "base_sha=$BASE_SHA" \
  "branch=$BRANCH" \
  "worktree=$WT" \
  "architecture=$WT/$ARCH_DOC" \
  "log=$LOG" \
  "L5_EXECUTED=NONE"

run_dealix git -C "$WT" status --short || true
run_dealix git -C "$WT" log --oneline --decorate -10 || true

if command -v gh >/dev/null 2>&1; then
  run_dealix gh pr list --repo "$REPO_FULL" --head "$BRANCH" --state all --limit 3 || true
fi

exit "$RC"
