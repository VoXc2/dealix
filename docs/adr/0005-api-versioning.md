---
title: ADR-0005 API Versioning — URI versioning /api/v1/, 12-month deprecation policy, preview headers for beta
doc_id: W4.T21.adr-0005-api-versioning
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T21.adr-0002, W4.T21.adr-0004, W4.T12.event-taxonomy]
kpi: { metric: breaking_change_incidents_per_quarter, target: 0, window: quarterly }
rice: { reach: 0, impact: 2, confidence: 0.9, effort: 3pw, score: engineering }
---

# ADR-0005: API Versioning

> **Decision: We adopt URI-based major versioning (`/api/v1/`, `/api/v2/`); deprecation guarantees a minimum 12-month overlap; experimental endpoints live under `/api/v1/` but require an `X-Dealix-Preview: <feature>` request header until they are promoted.**

## Context

Dealix API surface today: ~38 endpoints under `api/v1/revenue-os/*`, `api/routers/decision_passport.py`, and adjacent routers. Consumers:

- The Dealix SPA (tightly coupled, can be force-updated).
- Customer-side integrations (CRMs, Make.com, Zapier, custom scripts) — **loosely coupled, cannot be force-updated**.
- Partner agencies running batch jobs against the API.
- Internal scripts.

Existing pain:

- Two minor breaking changes shipped in Q1 2026 caused 6 support tickets and 1 paying-customer escalation.
- No documented deprecation window. Customers had between 0 and 14 days notice on the past 2 changes.
- Experimental endpoints have been promoted to GA without a sunset path for early adopters.

Constraints:

- Most customers integrate via low-code platforms (Make/Zapier) where header manipulation is awkward — URI versioning is more practical than header versioning.
- Compliance teams at Sovereign tenants require a written deprecation policy in the DPA.
- Engineering capacity: small team — we cannot afford to maintain more than two concurrent major versions.

## Decision

1. **Major versioning in the URI**: `/api/v{N}/...`. Major N increments only on breaking changes. v1 is the current production surface.
2. **Minor and patch are not in the URI**. They appear in:
   - Response header `X-Dealix-API-Version: 1.7.2`.
   - The `/api/v1/meta` endpoint.
3. **Backward-compatible changes** (new endpoints, new optional fields, new enum values declared additive) ship freely within a major.
4. **Breaking change definition** (any of):
   - Removing or renaming a field, endpoint, or enum value.
   - Tightening a validation rule.
   - Changing the semantics of a field (units, sign, type).
   - Changing default behavior of an optional parameter.
   - Adding a new required request field.
5. **Deprecation policy**:
   - Announce in CHANGELOG and via email to integration owners.
   - Emit `Deprecation: <date>` and `Sunset: <date>` response headers per RFC 8594 on every call to the deprecated endpoint.
   - Minimum overlap: **12 months** from announcement to sunset for paid customers; **6 months** for free / trial.
   - During overlap, both versions are fully maintained (bug fixes, security patches).
   - SLO applies equally to deprecated versions until sunset.
6. **Preview / experimental endpoints**:
   - Live under `/api/v1/` (no separate `/preview/` namespace).
   - Require request header `X-Dealix-Preview: <feature-flag>` (e.g. `X-Dealix-Preview: lead-engine-v3`).
   - Without the header, the endpoint returns `404`. With the header but feature not allow-listed for the tenant, returns `403`.
   - No SLO. No deprecation guarantee — preview can be removed or changed with 14 days' notice.
   - Promotion to GA: header is no longer required; full SLO applies.
7. **v2 planning trigger**: when ≥ 3 breaking changes are queued, or a regulatory mandate forces a non-additive change.

Owner of record: CTO. CHANGELOG owner: Product.

## Status

`Proposed` — pending CTO + CEO sign-off (CEO sign-off because deprecation language goes into customer contracts). Target acceptance: 2026-05-21. Effective: immediately upon acceptance.

## Consequences

### Positive

- Clear contract reduces customer churn risk on breaking changes.
- 12-month overlap aligns with Sovereign customer annual contract cycle.
- Preview header pattern unlocks fast iteration on new endpoints without committing to support.
- Audit-friendly: every deprecated endpoint self-announces via headers.

### Negative

- Engineering load: two majors in flight could mean carrying duplicated code for up to 12 months. Mitigation — code reuse via shared service layer; routers diverge, business logic does not.
- Preview header is awkward for low-code platforms; mitigated by documenting the header pattern in the integrations guide.
- 12-month overlap is longer than industry norm (6 months); cost is the maintenance burden vs. customer-trust benefit.

### Neutral / Follow-ups

- Add CI check: any PR that modifies an `api/v1/` schema in a breaking way must include a `BREAKING:` line in the commit and an updated CHANGELOG.
- Add response middleware to emit `Deprecation` / `Sunset` headers from a single config source.
- Add admin endpoint to allow-list preview features per tenant.
- Document the policy publicly in `docs/API_REFERENCE.md` and link from the DPA.

## Alternatives Considered

| Alternative | Reason rejected |
|---|---|
| **A. Header-based versioning (`Accept: application/vnd.dealix.v2+json`)** | Awkward for Make/Zapier integrations; harder to debug in browsers; doesn't match customer expectations from Stripe/Twilio/GitHub patterns. |
| **B. Date-based versioning (Stripe-style)** | Powerful but heavyweight; requires per-call version pinning; overkill at our endpoint count (~38) and team size. |
| **C. No formal versioning, ship breaking changes with notice** | Status quo; produced 2 incidents in 90 days; will not scale past 50 paying tenants. |
| **D. Separate `/preview/` namespace** | Promotion requires URL change for early adopters — friction discourages early adoption; preview header is cleaner. |
| **E. Shorter (6-month) deprecation window** | Customer feedback says 6 months is insufficient for procurement-gated changes at Sovereign tenants. |

## References

- Code: `api/routers/decision_passport.py`, `api/v1/revenue-os/*`, `api/v1/meta.py` (to be created).
- RFC 8594 Sunset HTTP Header.
- `docs/API_REFERENCE.md`.
- Related ADRs: ADR-0002 (async boundaries), ADR-0004 (observability).
- Industry references: Stripe API versioning, GitHub API previews.

## Review Cadence

Quarterly. Re-evaluate when v2 reaches GA, or when deprecated-endpoint maintenance exceeds 0.2 engineer-month / quarter.
