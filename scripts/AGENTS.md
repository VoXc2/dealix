# Dealix operational-script agent precedence

This scoped file applies to `scripts/**` and refines the root `AGENTS.md`.

## Current execution authority
Use Omega V3 canonical source/config plus exact current runtime/acceptance evidence for architecture and runtime truth. Issues, PR prose and historical receipts are coordination/provenance only and must not mint current PASS or authority when they conflict with canonical source or live evidence.

- One canonical Company Machine and one Session Factory.
- OpenCode modifying work: Company Operator -> Session Factory -> isolated exact-head worktree/session -> OpenCode -> tests -> independent verifier -> receipt.
- Runtime modifying capacity is ResourceGovernor-derived. Historical `DEEP_WIP_MAX=3` may describe old portfolio focus or provenance but is not a global worker ceiling.
- Historical five executor names are aliases only; canonical logical owners come from Agentic Holding registry.
- Automatic model execution is NO_DEEPSEEK, data-aware, trusted-cost-evidence gated and fail-closed. Never allow caller args/env/stale selected-model files/provider defaults to become model authority.
- Source PASS != runtime PASS != deployed release identity.
- Hosted pre-execution CI failure with no repository steps is not source-test failure.
- `HTTP 200 != release identity`; exact SHA parity is required for Production Green.

## Script migration rule
If a verifier or runner hard-codes fixed sector/arm/agent counts, global DeepWIP=3, old frontend paths, fixed prices/durations, or stale PR/model authority, replace the assertion with the canonical registry/policy check or mark the script historical/non-authoritative.

## Effects
L0-L4 analysis, tests, reports, isolated branches/worktrees and non-production reversible work may run unattended. Main merge, production mutation, DNS, production DB/schema/data, secrets/provider/billing, external send/publish, spend/payment/refund, binding quote/contract/tender and destructive actions remain separately governed material effects.
