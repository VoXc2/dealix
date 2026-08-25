# DEALIX SESSION 23 — TRUTH RECOVERY + FINAL ACCEPTANCE REOPEN

**Date:** 2026-08-26 Asia/Riyadh  
**Requested baseline main:** `e51ba1b9c3818a2b7abbc4349aea3c2999dd789e`  
**Current main after Session-23 operator incident/revert:** `1cefd1c54cb3735e8a5ddcabf8e154c381b1c32c`  
**Tree equivalence:** current main tree = original `e51ba1b...` tree `63647cfc04fb3d24090d3bd198db19527bc5cee3` (net content unchanged).  
**Recovery branch:** `fix/session23-public-truth-recovery`

## Executive verdict

**Corrected acceptance score: 52/100 — PARTIAL / DEGRADED, NOT FINAL ACCEPTANCE.**

Fresh-evidence rubric:

| Area | Score | Evidence-based reason |
|---|---:|---|
| Governance / approval boundaries | 14/15 | ACTION_HASH/hard-deny model exists; external effects remain approval-gated. Main branch itself is not protected, which is a governance gap exposed by this session. |
| Railway production/service truth | 11/15 | Current main combined status reports Railway success. Session-23 accidental main push caused an unintended Railway-trigger side effect even though the resulting tree is identical to the original baseline. |
| Public commercial truth | 4/15 | Canonical pages are strong and a bounded source repair exists on this branch, but `pages-public` still exposes stale legacy content and was not published/changed due the explicit NO PUBLIC PUBLISH boundary. |
| CI / release trust | 3/15 | #1253 current CI jobs are created but have no executed steps; runner/execution-plane trust is not restored. |
| Engineering / Living Fleet | 6/10 | #1253 is useful but still Draft; two edge tests remain skipped, including superseded-handoff shared-fixture/state-dir sequencing. |
| Commercial readiness | 6/10 | Diagnostic/pilot/approval assets exist; iMini is warm but is separate creator income and remains unsent. |
| Verified Dealix revenue / customer proof | 0/10 | No verified paid Dealix pilot/payment/delivery/customer ROI evidence in the current evidence set. |
| B2G / partner readiness | 4/5 | Etimad opportunity is real and time-bounded; repository decision remains PARTNER_FIRST. |
| Evidence / process discipline | 4/5 | Proof-first reporting is strong, but this session recorded an operator write mistake to main and its immediate revert. |
| **TOTAL** | **52/100** | **No inflation.** |

## Operator incident — mandatory disclosure

During Session 23 an incorrect GitHub write call created `noop` on `main` (`25eef1e...`). It was immediately removed by revert commit `1cefd1c...`. The resulting tree SHA equals the original `e51ba1b...` tree, so net repository content is unchanged. However Git history contains both commits. The push also produced a new Railway success status, so it is recorded as an **unintended production-trigger side effect** even though no manual deployment command was run and no source-tree delta remained.

No history rewrite or force push was attempted.

## P0 blockers

1. **P0 — Live public truth drift remains on `pages-public`.** Example verified: `pages-public/academy.html` still contains old accreditation/customer-count/pricing/testimonial claims. This branch repairs source truth only; public publish is explicitly prohibited in this session.
2. **P0 — GitHub Actions execution plane is not trustworthy/runnable.** On current #1253 head, CI jobs exist but return no executed steps. Red checks therefore cannot be treated as code-regression evidence, and green exact-head proof cannot be produced.
3. **P0 strategic — no verified paid Dealix customer proof.** No payment + delivery + customer-value evidence chain is present in current evidence.

## P1 blockers

1. **P1 — PR #1253 remains Draft/unmerged.** It contains valuable Living Fleet v3 work but is not production truth; state-dir/superseded-handoff edge remains skipped and CI cannot execute.
2. **P1 — Vercel check remains red for a separate provider-plan/integration reason.** Railway is the current production core; do not conflate this with Railway health or GitHub Actions capacity.
3. **P1 — Main branch governance is insufficiently fail-closed.** The accidental write was possible because repository-level protection/ruleset enforcement did not prevent a direct content write.
4. **P1 — Etimad 260839004837 is time-sensitive and still PARTNER_FIRST.** Clarification deadline 2026-08-30; submission deadline 2026-09-03. No purchase/outreach was executed.

# PUBLIC_SURFACE_TRUTH_MATRIX

| URL / path | Baseline state | Live/index evidence | Forbidden/current issue | Canonical replacement | Session-23 branch action |
|---|---|---|---|---|---|
| `/` / `landing/index.html` | Canonical | promoted by sitemap | none established in this audit | current homepage | KEEP |
| `/diagnostic.html` | Canonical | promoted by sitemap | none established | Free Mini Diagnostic | KEEP |
| `/pricing.html` | Canonical | promoted by sitemap | quote-only current path | itself | KEEP |
| `/services.html` | Canonical | promoted by sitemap | current one-product path | itself | KEEP |
| `/proof.html` | Canonical | promoted by sitemap | evidence-methodology page | itself | KEEP |
| `/trust-center.html` | Canonical | promoted by sitemap | explicitly limits unsupported claims | itself | KEEP |
| `/privacy.html` | Canonical | promoted by sitemap | no issue established | itself | KEEP |
| `/terms.html` | Canonical | promoted by sitemap | no issue established | itself | KEEP |
| `/checkout.html` | reviewed fail-closed | robots noindex; not sitemap-promoted | no live checkout; no public fixed price | quote/discovery path | KEEP |
| `/customer-portal.html` | reviewed supporting | not sitemap-promoted | no stale commercial claim established | supporting only | KEEP |
| `/workflow.html` | reviewed supporting | not sitemap-promoted | current governed workflow wording | supporting only | KEEP |
| `/ai-team.html` | reviewed supporting | robots disallow; not sitemap-promoted | no stale fixed-price claim established in current source | supporting only | KEEP / DO NOT PROMOTE |
| `/annual-pricing.html` | retired | previously fixed by #1252 | old annual/fixed-price authority must not return | `/pricing.html` | HARMONIZED TO RETIRED STUB |
| `/academy.html` | **STALE** | **verified stale on `pages-public`** | accreditation, 47+, 12 certificates, fixed prices, testimonials, `$299` | `/pricing.html` | RETIRED STUB ON RECOVERY BRANCH; LIVE P0 REMAINS |
| `/community.html` | **STALE** | source had 47+ / old pricing | unsupported count / fixed-price authority | `/pricing.html` | RETIRED STUB |
| `/data-pack.html` | **STALE** | direct public-deployable source | fixed 1,500 SAR, KPI/refund terms, residency wording | `/pricing.html` | RETIRED STUB |
| `/roi.html` | **STALE** | direct public-deployable source | 499/999, ROI assumptions, refund/guarantee language | `/proof.html` | RETIRED STUB |
| `/security.html` | **STALE** | direct public-deployable source | unsupported live-control/residency/SLA/compliance claims | `/trust-center.html` | RETIRED STUB |
| `/trust.html` | **STALE** | direct public-deployable source | unsupported PDPL/residency/readiness claims | `/trust-center.html` | RETIRED STUB |
| `/why-saudi-ai.html` | **STALE** | direct public-deployable source | retired pricing + competitor/compliance/residency claims | `/trust-center.html` | RETIRED STUB |
| `/case-study.html` | **STALE** | direct public-deployable source | unverified customer-proof authority + legacy pricing | `/proof.html` | RETIRED STUB |
| `/verticals.html` | **STALE** | direct public-deployable source | fixed legacy pricing | `/pricing.html` | RETIRED STUB |
| `/founder.html` | legacy/private-intent but deployable | robots disallow | historical fixed-price/public authority leakage | `/` | RETIRED STUB |
| `/systems-catalog.html` | **STALE** | direct public-deployable source | historical fixed pricing/product authority | `/` | RETIRED STUB |
| `/pay-per-result.html` | **STALE** | direct public-deployable source | 999 legacy price/result model | `/pricing.html` | RETIRED STUB |
| `/start.html` | declared retired/unaudited | robots disallow | legacy experiment may not be public authority | `/` | RETIRED STUB |
| `/sprint-sample.html` | declared retired/unaudited | robots disallow | legacy sprint authority | `/` | RETIRED STUB |
| `/case-study-pilot-example.html` | declared retired/unaudited | robots disallow | synthetic/example proof + refund language | `/` | RETIRED STUB |
| `/compare-gong.html` | declared retired/unaudited | robots disallow | unsupported comparison authority | `/` | RETIRED STUB |
| `/compare-hubspot.html` | declared retired/unaudited | robots disallow | unsupported comparison authority | `/` | RETIRED STUB |
| `/compare-salesloft.html` | declared retired/unaudited | robots disallow | unsupported comparison authority | `/` | RETIRED STUB |
| `/status.html` | declared retired/unaudited | robots disallow | stale product/status authority | `/` | RETIRED STUB |
| `/styleguide.html` | declared retired/unaudited | robots disallow | not public commercial authority | `/` | RETIRED STUB |
| `/dealix-beast-power.html` | declared retired/unaudited | robots disallow | legacy capability/claim authority | `/` | RETIRED STUB |
| `/agency-partner.html` | declared retired/unaudited | robots disallow | legacy partner commercial authority | `/` | RETIRED STUB |
| `/partners.html` | declared retired/unaudited | robots disallow | legacy partner commercial authority | `/` | RETIRED STUB |
| `/llms.txt` | canonical machine-readable support | public support file | phrase `Saudi data residency` occurs only in an explicit **do-not-claim** rule; not a positive claim | itself | KEEP |
| `/sitemap.xml` | canonical | exactly 8 promoted surfaces | no retired URLs | canonical allowlist | KEEP |
| `/sitemap_dealix.xml` | compatibility canonical | same 8 promoted surfaces | no retired URLs | canonical allowlist | KEEP |
| `/robots.txt` | governance support | public | baseline omitted some newly retired paths | current retired set | UPDATED ON BRANCH |
| any other `landing/*.html` | UNCLASSIFIED until proven | direct file may be deployable | if high-risk pattern appears, test must fail closed | classify or retire | NEW GLOBAL GUARD |

## Token audit — baseline vs recovery branch

Counts below are **file-hit counts on baseline `e51ba1b...` for exact high-confidence searches**, not business outcomes.

| Query | Baseline file hits | Classification | Recovery-branch changed-surface result |
|---|---:|---|---|
| `499 ريال` | 6 | all were legacy public pages | 0 in the six retired replacements by construction |
| `999 ريال` | 7 | all were legacy public pages | 0 in the seven retired replacements by construction |
| `$299` | 1 | `academy.html` | 0 in retired Academy stub |
| `47+` | 2 | `academy.html`, `community.html` | 0 in both retired stubs |
| `شهادات معتمدة` | 1 | `academy.html` | 0 in retired Academy stub |
| `Saudi data residency` | 4 raw hits | three positive/unsafe legacy contexts were identified and retired; `llms.txt` uses the phrase negatively to forbid the claim | positive stale contexts targeted to 0; negative llms rule intentionally remains |
| `1500` | 5 raw hits | not a valid standalone commercial detector; one result is `script.js` 1500ms timeout | semantic guard does not treat bare number as proof of pricing |
| `refund` | 12 raw hits | mixed legacy/demo/negative contexts; not all are commercial claims | declared retired examples fail-closed; global guard catches high-confidence refund guarantees |

**Important:** GitHub code-search indexes the default branch and cannot provide a reliable immediate after-count for this unmerged branch. Therefore repository-wide AFTER is **NOT CLAIMED AS VERIFIED ZERO**. Exact branch files/manifest were written and fetched, while full guard execution remains blocked until a local checkout or GitHub Actions runner executes the new test.

## Regression guard added

`tests/test_public_surface_truth_recovery.py` + `landing/public-surface-manifest.json`

The guard:
- checks all classified public surfaces exist;
- forbids current fixed public prices on reviewed surfaces;
- requires every retired surface to be a short `DEALIX_RETIRED_PUBLIC_SURFACE` + `noindex,nofollow` redirect stub;
- scans every other `landing/*.html` and fails if an unclassified page carries high-confidence fixed-price/overclaim patterns;
- verifies sitemap promotion remains limited to canonical indexable pages.

## PR #1253 factual state

- State: OPEN
- Draft: YES
- Merged: NO
- Current head inspected during this session: `3d186c85167a9516024556815f55e8f0d0a350c6`
- Scope remains Living Fleet v3 / Daily Builder / Career Intelligence / Private Founder Ops.
- Current CI jobs were created but showed no executed steps (`steps=null`), consistent with an execution-plane/runner/account gate rather than proven application-code regression.
- Two edge tests remain explicitly skipped in the patch, including `test_superseded_handoff_preserves_history` because cross-dispatch pending/state-dir sharing requires a shared fixture.
- Decision: **valuable, but keep Draft; do not call it accepted/merged.**

## Provider separation

| Plane | Current evidence | Classification |
|---|---|---|
| Railway | combined status on current main = SUCCESS | Production core appears healthy by provider status; direct functional probes were not rerun here |
| GitHub Actions | #1253 jobs created, no executed steps | CI execution-plane blocker; not proven code regression |
| Vercel | status = FAILURE, target points to private-org-to-Hobby upgrade path | separate provider integration/plan blocker; not Railway health and not GitHub Actions capacity |

## Money Now — iMini

Latest real counterpart message remains 2026-08-24:
- 80 USD base
- no prepayment; payment process after draft approval
- +200 USD at 100 verified code subscriptions
- 10% commission
- one short video; no paid ads/whitelisting/exclusivity/raw files

Latest later item is still an **UNSENT DRAFT** counter:
- target 150 USD fixed for one 30–60s video / one platform / one revision / organic only;
- 80 USD only if explicitly their final ceiling;
- retain 200 USD performance bonus + 10% commission;
- tracking/reporting clarity requested.

**Next approval:** AP-006 remains APPROVAL_PENDING. No send executed.

## Etimad 260839004837

Current official tender dates reverified 2026-08-26:
- supplier clarification deadline: 2026-08-30
- bid deadline: 2026-09-03

Repository decision remains **PARTNER_FIRST**. Safe next action is to secure/confirm a qualified consortium lead/partner first, then decide whether booklet purchase and formal clarification are worthwhile. No booklet purchase or MIS outreach executed.

## Founder-only actions genuinely unavoidable

1. Decide whether/when to authorize publishing the vetted retired-page changes to the actual public channel (`pages-public` or the final canonical front door). Until then live public drift remains P0.
2. Resolve/inspect GitHub Actions account/runner/billing-capacity state in the account UI if connector evidence cannot expose the exact pre-step denial reason. Do not change application code merely to clear red checks.
3. Decide AP-006 iMini send/reject; external send remains founder-gated.
4. For Etimad, authorize actual partner outreach and any later booklet purchase separately.
5. Consider enabling an enforceable main-branch ruleset/protection so an operator/tool cannot write directly to main again.

## Explicitly NOT executed

- NO merge to main.
- NO intended production deploy/redeploy command.
- NO DNS mutation.
- NO billing/plan change.
- NO Vercel upgrade.
- NO payment/refund/purchase.
- NO Etimad booklet purchase.
- NO Gmail send.
- NO WhatsApp send.
- NO LinkedIn send.
- NO MIS outreach.
- NO public publish and NO `pages-public` mutation.
- NO secret printing or secret mutation.
- NO repository visibility change or transfer.
- NO force push/history rewrite.
- NO claim that CI tests passed when runner execution did not begin.
- NO claim that the public-live after-count is zero.

## Highest next action

**Restore executable CI and obtain explicit approval for the public-channel truth cutover.** Only after both can the public-truth P0 be called closed. After that, prioritize the first verified paid Dealix pilot rather than adding another platform phase.
