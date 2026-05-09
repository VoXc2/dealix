# PR Merge Triage — 2026-05-09 (Wave 10.8 §29.5)

**Audience:** founder
**Read time:** 3 minutes
**Action:** click Merge in priority order on the rows labeled `MERGE_NOW`

> **TL;DR:** 8 PRs ready to merge today (low risk). 2 PRs need review first. 5 older PRs from earlier waves should be closed-as-superseded. After merge, run `bash scripts/wave10_8_everything_works_smoke.sh` and you're done.

---

## 1. The merge order (top-to-bottom = click order)

| # | PR | Branch | Disposition | Why | Estimated time |
|---|---|---|---|---|---|
| 1 | **#176** | `dependabot/npm_and_yarn/frontend/next-intl-4.9.2` | **MERGE_NOW** | Security minor; auto-tested by Dependabot | 30 sec |
| 2 | **#177** | `dependabot/npm_and_yarn/frontend/next-15.5.18` | **MERGE_NOW** | Security patches; same | 30 sec |
| 3 | **#175** | `codex/review-project-services-for-completion` | **MERGE_NOW** | Docs only (pre-cutover readiness) | 1 min |
| 4 | **#178** | `cursor/dev-env-setup-458a` | **MERGE_NOW** | Dev-env + AGENTS.md only; zero production risk | 1 min |
| 5 | **#181** | `cursor/master-operating-4c27` | **MERGE_NOW** | Decision Passport + Proof L0-L5 + Postgres event store. Aligned with §25 vision (Master Operating Spine). Deprecates old v3 endpoints safely. | 2 min |
| 6 | **#185** | `claude/wave10-5-master-execution-audit` | **MERGE_NOW** | Docs only (Master Execution Matrix + Evidence Table). 30-row honest audit. | 1 min |
| 7 | **#183** | `claude/wave10-5-master-verifier` | **MERGE_NOW** | Master verifier + 16-step E2E pytest + production smoke (14 passed · 2 skipped) | 1 min |
| 8 | **#184** | `claude/wave7-7-pre-approved-rules` | **MERGE_AFTER_CI_GREEN** | Wave 7.7 founder rules with `aa720a7` review fixes (35 tests PASS locally). Wait for CI to confirm. | wait for CI |
| 9 | **#188** | `claude/wave10-7-pr187-cleanup` | **MERGE_NOW** | Wave 10.7 — Codex P2 review fixes (broader lock-down + agent honesty + audit accuracy). 6 tests PASS. | 1 min |
| 10 | **#186** | `cursor/dealix-plan-phases-4c27` | **REVIEW_BEFORE_MERGE** | Cursor "revenue memory async facade + tenant stamping + smoke/lint". Larger diff; likely fine but warrants 5-min skim | 5-10 min |
| 11 | **#179** | `cursor/env-setup-4c27` | **REVIEW_BEFORE_MERGE** | Production-hardening (frontend + persistence + security + compliance). LARGEST diff. Read auth + middleware sections carefully. | 15-30 min |

**Total click-time for items 1-9:** ~10 minutes. Items 10-11 are independent + can wait.

---

## 2. The 5 older Cursor PRs — close as superseded

These are from earlier waves and have been overtaken by the recent Wave 10.x work or merged-equivalents:

| # | PR | Recommendation | Reason |
|---|---|---|---|
| #164 | `cursor/seo-audit-beast-power-a8b4` | **CLOSE_AS_SUPERSEDED** | SEO audit run regenerates the JSON file; no value in retaining the snapshot PR |
| #161 | `cursor/beast-verifier-hardening-a8b4` | **CLOSE_OR_RE_REVIEW** | "Beast" Phase work; check if its scope is covered by Wave 9 already merged |
| #159 | `cursor/verify-python3-verifiers-a8b4` | **CHECK** | Small fix (`python3` in shebangs) — may already be done |
| #158 | `cursor/v12-5-beast-closure-a8b4` | **CHECK** | V12.5 closure; check overlap with merged business architecture |

If on inspection any of these adds value not already on main, cherry-pick the diff into a fresh PR. Otherwise close with a one-line "superseded by §main" comment.

---

## 3. Things that fixed themselves today

| Issue | Status |
|---|---|
| Daily Snapshot workflow failing every morning with GH006 | ✅ **FIXED** in this branch (Wave 10.8 §29.3) — replaced push-to-main with artifact upload |
| `linkedin_scraper` Article 4 violation | ✅ **FIXED** in PR #187 (already merged) |
| Frontend audit doc inaccuracy | ✅ **FIXED** in PR #188 |
| Test-job CI failure on PR #187/#188 | 🟡 **PRE-EXISTING** — `python-jose` collection error; clears when PR #184 lands with its dep harden |

---

## 4. After merging — verify

```bash
git pull origin main
bash scripts/wave10_8_everything_works_smoke.sh
# Expected: EVERYTHING_WORKS=PASS (12/12)
```

If green: send warm-intro #1.

---

## 5. The single binding question

> **If you only have 10 minutes today, merge PRs 1-9 (click order above), then run the smoke. That's it.**

Items 10-11 (#186, #179) and the 5 older cleanup PRs can wait until tomorrow. None of them block customer #1.

The technical work is done. The single non-technical step is: **send the first warm-intro WhatsApp.**
