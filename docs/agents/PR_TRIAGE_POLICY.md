# Dealix PR Triage Policy — سياسة فرز طلبات الدمج

A repo with many open PRs needs a deterministic way to sort them so nothing
valuable is lost and nothing risky merges by accident. This policy plus
`scripts/triage_open_prs.py` produce one read-only triage report; humans decide.

---

## Buckets

`scripts/triage_open_prs.py` sorts every open PR into exactly one bucket (first match wins):

| Bucket | Signal | Default action |
|---|---|---|
| `draft` | PR marked draft | leave until author marks ready |
| `security` | title/label mentions security/auth/secret | review first, with care |
| `dependencies` | dependabot / bump / `deps` label | batch-review, let CI decide |
| `agent` | title mentions claude / codex / agent | check against the registry |
| `docs` | docs-only / `docs` label | fast-track if CI green |
| `needs_review` | everything else | rank by staleness |

Within each bucket, PRs are ordered by last-updated, with the most stale surfaced
first for a rebase, supersession, hold, or close decision.

## Portfolio signals

The report also emits deterministic review flags. These flags are evidence only;
they never close, merge, comment on, or retarget a PR automatically.

| Flag | Meaning | Human review question |
|---|---|---|
| `stale_<N>d` | no update for at least 30 days | rebase, supersede, hold, or close? |
| `merge_conflict` | GitHub reports `mergeStateStatus=DIRTY` | rebuild on current `main` or retire? |
| `duplicate_title` | normalized title intent appears on 2+ open PRs | which PR is canonical? |
| `stacked_on:<branch>` | base branch is not `main` | is the dependency current and explicit? |

Duplicate-title matching ignores conventional prefixes such as `feat(scope):`,
`fix:`, `docs:`, punctuation, case, and embedded PR references. A duplicate flag
does not prove identical code; compare changed files and dependencies before any
disposition.

## Human decisions

For each PR the operator picks one evidence-backed disposition: **merge candidate ·
needs tests · needs rebase/rebuild · superseded · historical reference · risky
hold · docs-only fast-track**. No PR is merged to `main` or closed solely from the
triage flags; file-level/dependency evidence is required first (see
[`AGENT_PERMISSION_MATRIX.md`](AGENT_PERMISSION_MATRIX.md) and Control Tower #938).

## Hygiene rules

- A PR with no update in **30+ days** and conflicts should be proposed for a
  documented close or clean reconstruction; it is never closed automatically.
- Duplicate-title groups require changed-file and dependency comparison before
  selecting a canonical PR.
- A stacked PR must identify its base dependency and be retargeted/reverified
  after the dependency lands.
- A `security`-bucket PR is never fast-tracked; it gets a real review.
- An `agent`-bucket PR must keep `.claude/agents/` ↔ `.codex/agents/` parity
  (`make agents-audit`).
- Dependency PRs merge only when attributable CI is fully green.
- A current branch with unique value on unsafe ancestry should be rebuilt from
  current `main` instead of resolving broad historical conflicts.

## Run it

```bash
make pr-triage      # or: python scripts/triage_open_prs.py
```

Output: `reports/pr_triage/OPEN_PR_TRIAGE.md` + `open_pr_triage.json`.

The JSON report contains per-PR age, bucket, base/head, merge state, flags, and
normalized duplicate-title groups so other internal dashboards can consume the
same evidence without reimplementing the policy.

- **Locally / in CI:** the script uses the `gh` CLI when available. If `gh` is
  unavailable or unauthenticated it writes a SKIPPED report — it never fails the
  build or prompts for mutation.
- **From an operator session with GitHub tools:** use the live PR list, inspect
  file-level value, and apply this policy. Signals are inputs to judgment, never
  automatic dispositions.

A weekly snapshot runs via [`.github/workflows/pr-triage.yml`](../../.github/workflows/pr-triage.yml).
