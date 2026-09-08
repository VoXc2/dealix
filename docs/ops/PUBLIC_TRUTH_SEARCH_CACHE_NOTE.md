# Public search-cache note

Search-engine snippets are evidence of what a crawler previously observed, not proof of the release currently serving `dealix.me`.

For Dealix public-truth decisions use this order:

1. current source at exact commit;
2. current provider deployment identity;
3. direct front-door route/redirect/metadata response;
4. search-engine crawl/index state.

If search results show a retired price/claim while current source and the serving release have retired it, classify the result as `SEARCH_INDEX_STALE_PENDING_RECRAWL` rather than editing source back toward the stale snippet.

If the serving release itself still exposes the retired claim, classify it as `PRODUCTION_RELEASE_OR_ROUTING_DRIFT` and close release parity/front-door before making SEO indexing claims.

Never treat a cached snippet as current customer proof, production identity or canonical offer authority.
