#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

REPO_SLUG="${DEALIX_REPO_SLUG:-Dealix-sa/dealix}"
REPO="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
ROOT="${DEALIX_ENGINEER_ROOT:-/opt/dealix/project-engineer}"
PROOF_ROOT="${ROOT}/proof"
WORKTREE_ROOT="${ROOT}/worktrees"
LOCK_FILE="${ROOT}/engineer.lock"
MODE="${1:-daily}"
TARGET_PR="${2:-}"
MAX_PRS="${DEALIX_ENGINEER_MAX_PRS:-8}"
AUTOBUILD="${DEALIX_ENGINEER_AUTOBUILD:-0}"
HERMES="${DEALIX_HERMES_BIN:-/home/dealix/.local/bin/hermes}"
STAMP="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="${PROOF_ROOT}/${STAMP}"

if [[ "$(id -u)" -eq 0 ]]; then
  exec sudo -iu dealix env \
    DEALIX_REPO_SLUG="$REPO_SLUG" \
    DEALIX_REPO_ROOT="$REPO" \
    DEALIX_ENGINEER_ROOT="$ROOT" \
    DEALIX_ENGINEER_MAX_PRS="$MAX_PRS" \
    DEALIX_ENGINEER_AUTOBUILD="$AUTOBUILD" \
    DEALIX_HERMES_BIN="$HERMES" \
    bash "$0" "$@"
fi
if [[ "$(id -un)" != "dealix" ]]; then
  echo "BLOCKED: Dealix Project Engineer must run as OS user dealix"
  exit 2
fi
for cmd in git gh jq flock timeout systemd-run; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "BLOCKED: missing command: $cmd"; exit 3; }
done
[[ -d "$REPO/.git" ]] || { echo "BLOCKED: repository missing: $REPO"; exit 4; }
mkdir -p "$PROOF_ROOT" "$WORKTREE_ROOT"
chmod 0700 "$ROOT" "$PROOF_ROOT" "$WORKTREE_ROOT" 2>/dev/null || true
exec 9>"$LOCK_FILE"
flock -n 9 || { echo "BLOCKED: another Dealix Project Engineer cycle is running"; exit 5; }
mkdir -p "$RUN_DIR"

export DEALIX_EXTERNAL_OUTREACH_ENABLED=false
export EXTERNAL_OUTREACH_ENABLED=false
export AUTO_SEND_ENABLED=false
export WHATSAPP_ALLOW_LIVE_SEND=false
export DEALIX_LIVE_CHARGE=false
export DEALIX_AUTO_MERGE=false
export DEALIX_PRODUCTION_MUTATION=false
export AGENT_APPROVAL_MODE=required
export DEALIX_PROOF_MODE=verified_only

log() { printf '[%s] %s\n' "$(date -Is)" "$*"; }
run_capture() {
  local out="$1"; shift
  set +e
  timeout 900 "$@" >"$out" 2>&1
  local rc=$?
  set -e
  return "$rc"
}

github_main() {
  gh api "repos/${REPO_SLUG}/commits/main" --jq '.sha'
}

pr_json() {
  gh api "repos/${REPO_SLUG}/pulls/$1"
}

checks_json() {
  local pr="$1"
  gh pr checks "$pr" --repo "$REPO_SLUG" --json name,state,workflow,bucket 2>/dev/null || printf '[]\n'
}

unresolved_threads() {
  local pr="$1"
  gh api graphql \
    -f query='query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){pullRequest(number:$number){reviewThreads(first:100){nodes{isResolved}}}}}' \
    -f owner="${REPO_SLUG%%/*}" \
    -f name="${REPO_SLUG##*/}" \
    -F number="$pr" \
    --jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length' 2>/dev/null || printf '%s\n' '-1'
}

failed_run_step_triage() {
  local head="$1" runs run_id jobs_json executed=0 prestep=0 unknown=0
  if ! runs="$(gh api "repos/${REPO_SLUG}/actions/runs?head_sha=${head}&event=pull_request&per_page=100" --jq '.workflow_runs[] | select(.conclusion == "failure") | .id' 2>/dev/null)"; then
    printf '0|0|1\n'
    return 0
  fi
  if [[ -z "$runs" ]]; then
    printf '0|0|1\n'
    return 0
  fi
  while IFS= read -r run_id; do
    [[ -n "$run_id" ]] || continue
    if ! jobs_json="$(gh api "repos/${REPO_SLUG}/actions/runs/${run_id}/jobs?per_page=100" 2>/dev/null)"; then
      unknown=1
      continue
    fi
    if jq -e '[.jobs[]?.steps[]?] | length > 0' >/dev/null 2>&1 <<<"$jobs_json"; then
      executed=1
    else
      prestep=1
    fi
  done <<<"$runs"
  printf '%s|%s|%s\n' "$executed" "$prestep" "$unknown"
}

behind_current_main() {
  local head="$1" main compare
  main="$(github_main 2>/dev/null || true)"
  [[ -n "$main" ]] || { printf '%s\n' '-1'; return 0; }
  compare="$(gh api "repos/${REPO_SLUG}/compare/${head}...${main}" --jq '.ahead_by' 2>/dev/null || true)"
  [[ "$compare" =~ ^[0-9]+$ ]] || { printf '%s\n' '-1'; return 0; }
  printf '%s\n' "$compare"
}

priority_score() {
  local title="$1" score=0 lowered
  lowered="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]')"
  [[ "$lowered" =~ production|security|trust|runtime|python|pydantic ]] && ((score+=50)) || true
  [[ "$lowered" =~ revenue|money|commercial|business|negotiation ]] && ((score+=45)) || true
  [[ "$lowered" =~ hermes|openclaw|ollama|founder|vps|autopilot ]] && ((score+=35)) || true
  [[ "$lowered" =~ fix|repair|hardening ]] && ((score+=20)) || true
  [[ "$lowered" =~ docs|chore ]] && ((score-=10)) || true
  printf '%s\n' "$score"
}

review_pr() {
  local pr="$1"
  local packet="${RUN_DIR}/PR_${pr}_MERGE_PACKET.md"
  local meta checks threads failing pending check_count recommendation reason title head mergeable draft changed additions deletions base
  local triage executed_failed prestep_failed triage_unknown behind
  meta="$(pr_json "$pr")" || { log "PR #$pr unavailable"; return 1; }
  title="$(jq -r '.title' <<<"$meta")"
  head="$(jq -r '.head.sha' <<<"$meta")"
  base="$(jq -r '.base.sha' <<<"$meta")"
  mergeable="$(jq -r '.mergeable // false' <<<"$meta")"
  draft="$(jq -r '.draft' <<<"$meta")"
  changed="$(jq -r '.changed_files' <<<"$meta")"
  additions="$(jq -r '.additions' <<<"$meta")"
  deletions="$(jq -r '.deletions' <<<"$meta")"
  checks="$(checks_json "$pr")"
  threads="$(unresolved_threads "$pr")"
  check_count="$(jq 'length' <<<"$checks" 2>/dev/null || echo 0)"
  failing="$(jq '[.[] | select((.state|ascii_downcase) == "failure" or (.bucket|ascii_downcase) == "fail")] | length' <<<"$checks" 2>/dev/null || echo 0)"
  pending="$(jq '[.[] | select((.state|ascii_downcase) == "pending" or (.bucket|ascii_downcase) == "pending")] | length' <<<"$checks" 2>/dev/null || echo 0)"
  behind="$(behind_current_main "$head")"
  triage="0|0|0"
  if (( failing > 0 )); then triage="$(failed_run_step_triage "$head")"; fi
  IFS='|' read -r executed_failed prestep_failed triage_unknown <<<"$triage"

  recommendation="HOLD"
  reason="verification incomplete"
  if [[ "$mergeable" != "true" ]]; then
    recommendation="RETHINK"
    reason="GitHub reports the PR as not mergeable; rebase/rebuild or supersession analysis required"
  elif (( threads < 0 )); then
    recommendation="HOLD"
    reason="review-thread evidence could not be retrieved; fail closed"
  elif (( behind < 0 )); then
    recommendation="HOLD"
    reason="current-main comparison could not be verified; fail closed"
  elif (( behind > 0 )); then
    recommendation="HOLD"
    reason="PR head is behind current main by ${behind} commit(s); synchronize before repair/readiness"
  elif (( check_count == 0 )); then
    recommendation="HOLD"
    reason="no exact-head check evidence was returned; fail closed rather than infer green"
  elif (( failing > 0 && executed_failed == 1 )); then
    recommendation="FIX_FIRST"
    reason="$failing failing check(s) include workflow jobs with real step execution; bounded repair may investigate attributable failures"
  elif (( failing > 0 )); then
    recommendation="HOLD"
    reason="$failing failing check(s) have only pre-step or unverifiable execution evidence; treat as runner/account/control-plane blocker, not code"
  elif (( pending > 0 )); then
    recommendation="HOLD"
    reason="$pending check(s) still pending"
  elif (( threads > 0 )); then
    recommendation="FIX_FIRST"
    reason="$threads unresolved review thread(s)"
  elif [[ "$draft" == "true" ]]; then
    recommendation="SHIP_REVIEW"
    reason="mergeable with exact-head checks present, no detected red/pending checks, no unresolved threads, and no main drift; still Draft and requires fresh review + founder merge approval"
  else
    recommendation="MERGE_CANDIDATE"
    reason="repository gates appear clear; merge remains explicit founder approval only"
  fi

  {
    echo "# Dealix Project Engineer - PR #${pr}"
    echo
    echo "- Timestamp: $(date -Is)"
    echo "- Title: ${title}"
    echo "- Exact head: \`${head}\`"
    echo "- Base snapshot: \`${base}\`"
    echo "- Changed files: ${changed} (+${additions}/-${deletions})"
    echo "- Draft: ${draft}"
    echo "- GitHub mergeable: ${mergeable}"
    echo "- Exact-head checks returned: ${check_count}"
    echo "- Failing checks: ${failing}"
    echo "- Pending checks: ${pending}"
    echo "- Failed runs with executed job steps: ${executed_failed}"
    echo "- Failed runs with pre-step/no-step evidence: ${prestep_failed}"
    echo "- Failed-run triage unknown: ${triage_unknown}"
    echo "- Commits behind current main: ${behind}"
    echo "- Unresolved review threads: ${threads}"
    echo "- Recommendation: **${recommendation}**"
    echo "- Why: ${reason}"
    echo
    echo "## Safety boundary"
    echo "No merge, deployment, production mutation, secret change, payment, deletion, or external send was performed."
    echo
    echo "## Checks"
    jq -r '.[] | "- \(.workflow // "") / \(.name): \(.state)"' <<<"$checks" 2>/dev/null || true
  } >"$packet"
  printf '%s|%s|%s|%s\n' "$pr" "$recommendation" "$head" "$packet"
}

changed_files_for_pr() {
  gh api --paginate "repos/${REPO_SLUG}/pulls/$1/files?per_page=100" --jq '.[].filename'
}

is_sensitive_path() {
  case "$1" in
    .github/workflows/*|*.env|*.env.*|*secret*|*credential*|*migration*|migrations/*|railway.*|vercel.json|Dockerfile*|*payment*|*billing*) return 0 ;;
    *) return 1 ;;
  esac
}

build_pr() {
  local pr="$1" meta title head branch repo_full draft worktree prompt before after changed allowed_file unsafe=0
  meta="$(pr_json "$pr")" || return 1
  title="$(jq -r '.title' <<<"$meta")"
  head="$(jq -r '.head.sha' <<<"$meta")"
  branch="$(jq -r '.head.ref' <<<"$meta")"
  repo_full="$(jq -r '.head.repo.full_name' <<<"$meta")"
  draft="$(jq -r '.draft' <<<"$meta")"
  [[ "$repo_full" == "$REPO_SLUG" && "$draft" == "true" ]] || { log "AUTOBUILD BLOCKED #$pr: requires same-repo Draft PR"; return 10; }
  [[ -x "$HERMES" ]] || { log "AUTOBUILD BLOCKED #$pr: Hermes missing at $HERMES"; return 11; }

  mapfile -t allowed < <(changed_files_for_pr "$pr")
  ((${#allowed[@]} > 0 && ${#allowed[@]} <= 20)) || { log "AUTOBUILD BLOCKED #$pr: changed-file scope is outside 1..20"; return 12; }
  for allowed_file in "${allowed[@]}"; do
    if is_sensitive_path "$allowed_file"; then
      log "AUTOBUILD BLOCKED #$pr sensitive path $allowed_file"
      return 13
    fi
  done

  git -C "$REPO" fetch --quiet origin "main" "$branch"
  worktree="${WORKTREE_ROOT}/pr-${pr}-${STAMP}"
  rm -rf "$worktree"
  git -C "$REPO" worktree add --detach "$worktree" "$head" >/dev/null
  prompt="${RUN_DIR}/PR_${pr}_BUILD.prompt"
  cat >"$prompt" <<PROMPT
You are the bounded Dealix Project Engineer working on Draft PR #${pr}: ${title}.
Exact starting head: ${head}

Goal: repair only failures that are attributable to this PR with the smallest defensible code/test delta.

Hard boundaries:
- Work only inside the current worktree.
- You may edit only files already changed by this PR, plus focused tests under tests/.
- Do not modify .github/workflows, Railway/Vercel/Docker deployment config, migrations, secrets, credentials, payment/billing, production, DNS, or external communication code.
- Do not weaken or skip tests/security/SEO/CodeQL gates.
- Do not run gh, railway, vercel, ssh, scp, curl to non-local hosts, git push, git commit, git merge, or git rebase.
- Do not inspect .env, credentials, tokens, SSH material, or auth stores.
- External network is unavailable by design; local Ollama is allowed.
- If the failure is shared baseline or needs a disallowed file, make no change and explain that it needs a separate owner.

First inspect the PR diff and local tests. If a safe attributable fix exists, implement it and run focused verification. End with exactly:
ENGINEER_RESULT: PATCHED or NO_SAFE_PATCH
ROOT_CAUSE: ...
VERIFICATION: ...
NEXT_ACTION: ...
PROMPT

  before="$(git -C "$worktree" rev-parse HEAD)"
  set +e
  timeout 1800 systemd-run --quiet --wait --pipe --collect \
    --uid=dealix --gid=dealix \
    -p NoNewPrivileges=yes \
    -p ProtectSystem=strict \
    -p ProtectHome=read-only \
    -p "ReadWritePaths=$worktree $ROOT" \
    -p "InaccessiblePaths=/home/dealix/.config/gh /home/dealix/.ssh /home/dealix/.railway" \
    -p IPAddressDeny=any \
    -p IPAddressAllow=localhost \
    -E HOME=/home/dealix \
    -E DEALIX_EXTERNAL_OUTREACH_ENABLED=false \
    -E AUTO_SEND_ENABLED=false \
    -E DEALIX_AUTO_MERGE=false \
    -E DEALIX_PRODUCTION_MUTATION=false \
    "$HERMES" chat --toolsets terminal --max-turns 10 --query-file "$prompt" \
    >"${RUN_DIR}/PR_${pr}_HERMES.txt" 2>&1
  local hermes_rc=$?
  set -e
  after="$(git -C "$worktree" rev-parse HEAD)"
  [[ "$before" == "$after" ]] || { log "AUTOBUILD BLOCKED #$pr: Hermes created a commit"; unsafe=1; }

  mapfile -t changed < <(git -C "$worktree" diff --name-only)
  if ((${#changed[@]} == 0)); then
    log "AUTOBUILD #$pr no patch produced (Hermes rc=$hermes_rc)"
    git -C "$REPO" worktree remove --force "$worktree" >/dev/null 2>&1 || true
    return 0
  fi
  if ((${#changed[@]} > 12)); then unsafe=1; fi
  for allowed_file in "${changed[@]}"; do
    if is_sensitive_path "$allowed_file"; then unsafe=1; fi
    if [[ "$allowed_file" != tests/* ]]; then
      local found=0 original
      for original in "${allowed[@]}"; do [[ "$allowed_file" == "$original" ]] && found=1; done
      (( found == 1 )) || unsafe=1
    fi
  done
  if git -C "$worktree" diff | grep -Eiq 'AUTO_SEND_ENABLED[[:space:]]*=[[:space:]]*true|WHATSAPP_ALLOW_LIVE_SEND[[:space:]]*=[[:space:]]*true|DEALIX_AUTO_MERGE[[:space:]]*=[[:space:]]*true|railway[[:space:]]+(up|deploy|redeploy)|gh[[:space:]]+pr[[:space:]]+merge|git[[:space:]]+push.*[[:space:]]+main([[:space:]]|$)'; then
    unsafe=1
  fi
  (( unsafe == 0 )) || { log "AUTOBUILD REJECTED #$pr: post-edit safety guard"; git -C "$REPO" worktree remove --force "$worktree" >/dev/null 2>&1 || true; return 14; }

  git -C "$worktree" diff --check
  local f
  for f in "${changed[@]}"; do
    case "$f" in
      *.sh) bash -n "$worktree/$f" ;;
      *.py) python3 -m py_compile "$worktree/$f" ;;
    esac
  done
  mapfile -t py_changed < <(printf '%s\n' "${changed[@]}" | grep -E '\.py$' || true)
  if ((${#py_changed[@]} > 0)) && python3 -m ruff --version >/dev/null 2>&1; then
    (cd "$worktree" && python3 -m ruff check "${py_changed[@]}")
  fi
  mapfile -t test_changed < <(printf '%s\n' "${changed[@]}" | grep -E '^tests/.*\.py$' || true)
  if ((${#test_changed[@]} > 0)) && python3 -m pytest --version >/dev/null 2>&1; then
    (cd "$worktree" && timeout 900 python3 -m pytest -q "${test_changed[@]}")
  fi

  git -C "$worktree" add -- "${changed[@]}"
  git -C "$worktree" commit -m "fix(engineer): bounded repair for PR #${pr}" >/dev/null
  git -C "$worktree" push origin "HEAD:${branch}"
  log "AUTOBUILD PUSHED #$pr branch=$branch changed=${#changed[@]}"
  git -C "$REPO" worktree remove --force "$worktree" >/dev/null 2>&1 || true
}

select_candidates() {
  gh pr list --repo "$REPO_SLUG" --state open --limit 50 --json number,title,isDraft,updatedAt \
    | jq -r '.[] | select(.isDraft == true) | [.number,.title,.updatedAt] | @tsv' \
    | while IFS=$'\t' read -r number title updated; do
        printf '%s\t%s\t%s\t%s\n' "$(priority_score "$title")" "$number" "$updated" "$title"
      done \
    | sort -t$'\t' -k1,1nr -k3,3r \
    | head -n "$MAX_PRS"
}

daily() {
  local table="${RUN_DIR}/DAILY_ENGINEERING_COMMAND.tsv" first_fix=""
  printf 'score\tpr\trecommendation\thead\ttitle\n' >"$table"
  while IFS=$'\t' read -r score pr updated title; do
    local result recommendation head packet
    result="$(review_pr "$pr" || true)"
    IFS='|' read -r _ recommendation head packet <<<"$result"
    printf '%s\t%s\t%s\t%s\t%s\n' "$score" "$pr" "${recommendation:-ERROR}" "${head:-UNKNOWN}" "$title" >>"$table"
    if [[ -z "$first_fix" && "$recommendation" == "FIX_FIRST" ]]; then first_fix="$pr"; fi
  done < <(select_candidates)
  column -t -s $'\t' "$table" 2>/dev/null || cat "$table"
  if [[ "$AUTOBUILD" == "1" && -n "$first_fix" ]]; then
    log "AUTOBUILD candidate: PR #$first_fix"
    build_pr "$first_fix" || true
  fi
  printf '\nENGINEER_PROOF_DIR=%s\n' "$RUN_DIR"
}

case "$MODE" in
  status) select_candidates ;;
  review-pr) [[ "$TARGET_PR" =~ ^[0-9]+$ ]] || { echo "usage: $0 review-pr PR"; exit 64; }; review_pr "$TARGET_PR" ;;
  build-pr) [[ "$TARGET_PR" =~ ^[0-9]+$ ]] || { echo "usage: $0 build-pr PR"; exit 64; }; build_pr "$TARGET_PR" ;;
  daily) daily ;;
  *) echo "usage: $0 {status|daily|review-pr PR|build-pr PR}"; exit 64 ;;
esac
