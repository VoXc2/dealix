# Dealix Public Truth + SEO Reconciliation — 2026-09-08

## Live authority at construction

- Repository: `Dealix-sa/dealix`
- Base: `main@2dedf0a7427d7894379751198cb27b999cdc6812`
- `main` remained unprotected at the latest live branch read.
- Railway Web/API release parity remains behind current main; current-main attempts are still `SKIPPED`.
- Direct front-door probe of `https://dealix.me` returned `404` during this reconciliation.

These facts mean source correctness, deployment parity and public front-door correctness are separate gates.

## Public-truth finding

Search-engine results can still surface older Dealix snippets/offers from previous crawls/releases. Current source already retires the most dangerous old static surfaces:

- `landing/academy.html` is `noindex,nofollow` and redirects to the current commercial path.
- `landing/pricing.html` explicitly states quote-only/no public checkout.
- the canonical Next `/pricing` page is already `Execution Diagnostic -> Qualified Discovery + Customer-Specific Quote -> Outcome Sprint -> Proof Review -> Dealix Runtime` and explicitly rejects public fixed pricing and checkout.
- `apps/web/next.config.js` permanently redirects legacy `/pricing.html`, `/academy.html` and `/checkout.html` URLs into current canonical routes.

Therefore stale indexed snippets do **not** justify resurrecting or editing legacy pricing tiers. The source fix is to align metadata/index policy and then deploy/verify the correct release through the independent Production TRUST path.

## Changes in this branch

1. Root metadata now aligns to current positioning:
   - `Dealix — AI Business Operating System`
   - governed execution / measurable outcomes
   - removes stale `Revenue OS in one week`, paid-diagnostic and `AI writes, you send` metadata.

2. Sitemap now publishes only public/indexable surfaces that are consistent with `robots.ts`.
   - internal operating pages blocked by robots are no longer advertised in sitemap.
   - redirecting `/ar/*` URLs are not advertised as hreflang language alternates.
   - `/offers` is omitted because it redirects to `/pricing`; sitemap should list canonical targets, not redirect sources.

3. `scripts/ops/verify_public_truth_seo.py` creates a fail-closed static contract for:
   - sitemap/robots consistency;
   - canonical positioning metadata;
   - quote-only/customer-specific pricing truth;
   - legacy HTML redirect/noindex retirement;
   - no fake hreflang for redirecting locale routes.

4. `scripts/ops/accept_public_truth_seo_v1.sh` binds source acceptance to an exact SHA and runs:
   - Python verifier compile;
   - public-truth verifier;
   - `apps/web` typecheck;
   - `apps/web` production build;
   - clean-worktree and stable-head checks.

The acceptance script has all external/material flags fail-closed and cannot deploy or publish.

## Consolidation

Historical Draft PR #1560 contained the useful sitemap/hreflang and metadata correction, but it was based on an older main snapshot. This branch is constructed directly from current main and is the single current public-truth/SEO source owner. #1560 should be closed without merge after this source branch is established.

## Independent gates after source acceptance

A source PASS does not imply public correctness. Remaining independent TRUST gates are:

1. merge authority for this PR, if exact current source acceptance is good;
2. Railway Web/API exact-main release parity;
3. custom-domain verification/routing/TLS;
4. public route acceptance for `/`, `/pricing`, `/services`, `/book`, `/robots.txt`, `/sitemap.xml`, and legacy redirects;
5. search-engine recrawl/index cleanup, which is not instantaneous proof of deployment.

`PR Merge != Production Green` remains mandatory.
