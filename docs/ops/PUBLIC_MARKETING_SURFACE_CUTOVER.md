# Dealix Public Marketing Surface Cutover

## Why this gate exists

The repository can contain the correct commercial truth while `dealix.me` or a search index still exposes an older deployment. Marketing must not drive event, SEO, content or paid traffic into a public surface that contradicts current `main`.

Current canonical public truth is defined by `landing/public-surface-manifest.json` and the reviewed launch pages.

## Current P0 observation — 2026-08-28

Repository `main` is aligned to:

`Free Mini Diagnostic -> qualified discovery -> customer-specific quote -> 30-Day Revenue Command Pilot -> Proof -> Stop/Expand/Redesign`

However external crawl/search evidence observed on 2026-08-28 still exposed older versions of multiple routes, including legacy public pricing, 7-day pilot/refund language, and unsupported historical claims. This is classified as:

`PUBLIC_SURFACE_INDEX_DRIFT`

Do not treat stale search snippets or an older public deployment as current Dealix commercial authority.

## Pre-cutover acceptance

Run locally against the repository:

```bash
python scripts/verify_public_marketing_surface.py
```

Expected:

```text
DEALIX_PUBLIC_MARKETING_SURFACE=PASS
LIVE_CHECK=OFF
```

This confirms:
- every canonical-indexable file exists;
- canonical pages contain no known retired commercial markers;
- canonical pages are present in sitemap;
- retired routes are absent from sitemap;
- retired routes are quarantined in robots.

## Live cutover acceptance

After the public host is updated to the intended `main` SHA, run:

```bash
python scripts/verify_public_marketing_surface.py \
  --live-base-url https://dealix.me
```

The live gate checks:
- all canonical routes return successfully;
- canonical responses contain no known legacy pricing/refund/claim markers;
- canonical responses stay on the expected domain;
- retired routes redirect to the manifest target, return 404/410, or are explicitly `noindex` and free of legacy claims.

A FAIL is a marketing/reputation blocker. Do not deliberately increase traffic until resolved.

## Search-index cleanup after live PASS

Only after live content is correct:
1. Confirm `robots.txt` and both sitemaps are the intended current versions.
2. Confirm retired URLs do not serve old 200/indexable commercial content.
3. Submit/refresh the canonical sitemap in Google Search Console.
4. Request recrawl for the highest-risk changed canonical pages (`/`, `/pricing.html`, `/services.html`).
5. Use temporary removal only when a stale URL is materially harmful and the underlying redirect/noindex/removal is already fixed.
6. Recheck indexed snippets; search-engine cache lag is not source authority.

## Hosting ownership check

Do not assume a provider owns `dealix.me` because the repository has preview deployments there. Before production cutover, prove:
- current DNS/hosting target for `dealix.me`;
- which artifact/branch/SHA it serves;
- rollback path;
- exact public SHA/content after cutover.

Vercel project deployment state and the `dealix.me` domain must be verified independently if the domain is not attached to that Vercel project.

## Authority

A public deployment, DNS cutover, domain mutation, or production promotion is a separate production action. This runbook and verifier prepare and prove the action; they do not silently perform it.
