# Technical Proof Checklist

Honest record of what is proven vs. pending. No checks are faked — items not yet
implemented are marked clearly, not ticked.

**Last updated:** 2026-06-03

---

## Proven / runnable now

- [x] `npm run build` passed (vite build + esbuild bundle; verified locally)
- [x] file presence: launch docs exist (`docs/launch/*`)
- [x] file presence: launch reports exist (`reports/launch/*`)
- [x] scorecard has all 12 weighted sections (checker validates)
- [x] Go/No-Go report has decision structure (checker validates)
- [x] No-Go blockers documented (`LAUNCH_BLOCKERS.md`)
- [x] workflow exists with least-privilege permissions (`launch-readiness.yml`)
- [x] no guaranteed claims in prospect-facing artifacts (checker scan)
- [x] no invented contacts (role-based prospects; checker scan)
- [x] security/privacy gate documented (`SECURITY_GO_NO_GO.md`)
- [x] launch score generated (`check_launch_readiness.py`)
- [x] founder command template present (`reports/founder/DAILY_SUPER_COMMAND.md`)

## Partial / pending (not ticked on purpose)

- [ ] pytest — no Python test suite in repo yet
- [ ] vitest — no test files yet (CI runs `--passWithNoTests`, so it is green but empty)
- [ ] standalone schema-contract check — not implemented as a separate script
- [ ] site-routes check — covered indirectly by `npm run build`, no dedicated test
- [ ] business catalog check — system not built
- [ ] need intelligence check — system not built
- [ ] account pack contract check — contract not defined yet
- [ ] email quality gate (executable) — `draft-quality-gate.js` missing
- [ ] proposal gate (executable) — not built
- [ ] delivery gate (executable) — not built
- [ ] founder command dry-run (live generation) — template only
- [ ] account pack dry-run — generator not built

---

## How to reproduce the proven items

```bash
npm install
npm run build                                   # build proof
npx vitest run --passWithNoTests                # test runner (no tests yet)
python scripts/governance_check.py              # founder snapshot (non-zero while approvals pending; informational)
python scripts/checks/check_launch_readiness.py # structural + safety + score (the hard gate)
```

> The same commands run in `.github/workflows/launch-readiness.yml`. The pending
> items above become checks as their underlying systems are built.
