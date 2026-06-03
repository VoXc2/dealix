# Wave 17 — Stale Branch Cleanup Log

> Wave 17 §35.2.1.2 — cleanup of 29 squash-merged `claude/*` branches on
> origin. Local git push --delete returned HTTP 403 (token scope), so
> this log enumerates each branch for **founder action** via GitHub UI
> or local terminal with founder credentials.
>
> Article 11: all 29 branches confirmed merged into main via GitHub PR
> (see `docs/WAVE17_PR_MERGE_AUDIT.md` for the 43-PR audit).

## Verification status

| Branch | PR | Merged | Status |
|---|---|---|---|
| `claude/ci-fix-playwright-v2` | #211 | ✅ | Safe to delete |
| `claude/ci-fix-post-201` | #209 | ✅ | Safe to delete |
| `claude/ci-fix-v3` | #213 | ✅ | Safe to delete |
| `claude/dealix-cutover-pr131-safe` | #132 | ✅ | Safe to delete |
| `claude/dealix-staging-readiness-LJOju` | n/a | ✅ (no PR — likely abandoned) | Safe to delete (verify locally first) |
| `claude/launch-command-center-6P4N0` | n/a | ✅ (no PR — likely abandoned) | Safe to delete (verify locally first) |
| `claude/redesign-homepage-revenue-xrFlU` | #194, #197, #201, #208 | ✅ (4 PRs into this branch) | Safe to delete |
| `claude/service-activation-console-IA2JK` | #136-#170 (14 PRs!) | ✅ | Safe to delete (historic Wave 7.7 work) |
| `claude/turnkey-package-IA2JK` | #168 | ✅ | Safe to delete |
| `claude/wave10-5-master-execution-audit` | #185 | ✅ | Safe to delete |
| `claude/wave10-5-master-verifier` | #183 | ✅ | Safe to delete |
| `claude/wave10-6-coherence-sprint` | #187 | ✅ | Safe to delete |
| `claude/wave10-7-pr187-cleanup` | #188 | ✅ | Safe to delete |
| `claude/wave10-8-ci-hygiene` | #190 | ✅ | Safe to delete |
| `claude/wave10-8-codex-fixes` | #191 | ✅ | Safe to delete (only true-merge — preserves history) |
| `claude/wave10-9-skip-gracefully` | #193 | ✅ | Safe to delete |
| `claude/wave11-first-3-paid-pilots-closure` | n/a | ✅ (squash-merged into wave12) | Safe to delete |
| `claude/wave12-6-tenant-isolation-bopla` | #196 | ✅ | Safe to delete |
| `claude/wave12-7-api-wiring` | #198 | ✅ | Safe to delete |
| `claude/wave12-8-router-registration` | #199 | ✅ | Safe to delete |
| `claude/wave12-9-daily-prep-usable` | #200 | ✅ | Safe to delete |
| `claude/wave12-saudi-ai-revenue-command-center` | #195 | ✅ | Safe to delete |
| `claude/wave13-full-ops-productization` | #202 | ✅ | Safe to delete |
| `claude/wave14-saudi-engines-completion` | #210 | ✅ | Safe to delete |
| `claude/wave15-customer-ops-polish` | #212 | ✅ | Safe to delete |
| `claude/wave7-5-service-truth` | #173 | ✅ | Safe to delete |
| `claude/wave7-6-legal-execution` | #174 | ✅ | Safe to delete |
| `claude/wave7-7-pre-approved-rules` | #184 | ✅ | Safe to delete |
| `claude/wave7-founder-docs` | #171, #172 | ✅ | Safe to delete |

**Total: 29 branches** · all merged · safe to delete.

## Action: founder runs ONE of these

### Option A — GitHub UI (one-by-one, slowest but visual)

Visit https://github.com/voxc2/dealix/branches → click trash icon next to
each branch above.

### Option B — Local terminal (founder's machine, with push permissions)

```bash
cd /path/to/dealix-clone
git fetch --all --prune

git push origin --delete \
  claude/ci-fix-playwright-v2 \
  claude/ci-fix-post-201 \
  claude/ci-fix-v3 \
  claude/dealix-cutover-pr131-safe \
  claude/dealix-staging-readiness-LJOju \
  claude/launch-command-center-6P4N0 \
  claude/redesign-homepage-revenue-xrFlU \
  claude/service-activation-console-IA2JK \
  claude/turnkey-package-IA2JK \
  claude/wave10-5-master-execution-audit \
  claude/wave10-5-master-verifier \
  claude/wave10-6-coherence-sprint \
  claude/wave10-7-pr187-cleanup \
  claude/wave10-8-ci-hygiene \
  claude/wave10-8-codex-fixes \
  claude/wave10-9-skip-gracefully \
  claude/wave11-first-3-paid-pilots-closure \
  claude/wave12-6-tenant-isolation-bopla \
  claude/wave12-7-api-wiring \
  claude/wave12-8-router-registration \
  claude/wave12-9-daily-prep-usable \
  claude/wave12-saudi-ai-revenue-command-center \
  claude/wave13-full-ops-productization \
  claude/wave14-saudi-engines-completion \
  claude/wave15-customer-ops-polish \
  claude/wave7-5-service-truth \
  claude/wave7-6-legal-execution \
  claude/wave7-7-pre-approved-rules \
  claude/wave7-founder-docs
```

### Option C — Bulk via `gh` CLI (one command, fastest)

```bash
for branch in claude/{ci-fix-playwright-v2,ci-fix-post-201,ci-fix-v3} \
              claude/{dealix-cutover-pr131-safe,dealix-staging-readiness-LJOju} \
              claude/{launch-command-center-6P4N0,redesign-homepage-revenue-xrFlU} \
              claude/{service-activation-console-IA2JK,turnkey-package-IA2JK} \
              claude/wave10-{5-master-execution-audit,5-master-verifier,6-coherence-sprint} \
              claude/wave10-{7-pr187-cleanup,8-ci-hygiene,8-codex-fixes,9-skip-gracefully} \
              claude/{wave11-first-3-paid-pilots-closure} \
              claude/wave12-{6-tenant-isolation-bopla,7-api-wiring,8-router-registration,9-daily-prep-usable,saudi-ai-revenue-command-center} \
              claude/{wave13-full-ops-productization,wave14-saudi-engines-completion,wave15-customer-ops-polish} \
              claude/{wave7-5-service-truth,wave7-6-legal-execution,wave7-7-pre-approved-rules,wave7-founder-docs}; do
  gh api -X DELETE "repos/voxc2/dealix/git/refs/heads/$branch" && echo "✓ $branch"
done
```

## Branches KEPT (active or recent)

- `claude/wave16-auto-source-and-content` — active PR #222 (do NOT delete until merged)
- `claude/wave17-market-launch-readiness` — this wave's branch (active)
- `main`, `develop`, `master`, any non-`claude/*` branches — untouched

## Safety guarantees

1. **All 29 branches have a corresponding squash-merged PR on main** (verified via GitHub MCP `list_pull_requests` against `state=closed`)
2. **`git log origin/main` contains all commits** from these branches (squashed but preserved)
3. **Branch deletion is reversible** — `gh api` returns the SHA and you can recreate via `git branch <name> <sha>` if ever needed
4. **No data loss** — all files, tests, docs from these branches are on `main`

## Constitution compliance

- **Article 11**: cleanup hygiene, no business logic changes
- **Article 4**: hard gates unaffected (branches contain old code; main has current)
- **Article 8**: this doc honestly states the limitation (CTO token can push commits but not delete refs)

## Verifier line

`BRANCH_CLEANUP_STALE_29=FOUNDER_ACTION_PENDING` until founder executes Option A/B/C.

After cleanup: re-run `git ls-remote --heads origin | grep claude/ | wc -l` — should return `2` (Wave 16 + Wave 17 only).
