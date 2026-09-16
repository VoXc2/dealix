# Dealix Railway IaC authority

This directory is the source candidate for Railway Infrastructure as Code.
It was imported read-only from the linked Dealix production project and is
reviewed with `railway config plan`; it does not grant apply/deploy authority.

Legacy `railway.json` / `railway.toml` Config-as-Code remains provider-bound
until a separate exact action-bound migration clears each service Config File
setting. Railway documents a hard legacy cutoff of 2026-12-01.

Safe workflow:
1. `npm install --prefix .railway --ignore-scripts`
2. `python3 scripts/ops/verify_railway_iac_source.py`
3. `railway config plan --file .railway/railway.ts`

Never run `railway config apply`, `railway config migrate --apply`, redeploy,
or provider mutations from unattended source acceptance.

`checkSuites` is intentionally true for both production services as a conservative
source-level HOLD while Railway GitHub autodeploy remains enabled.
Do not set `checkSuites: false` while normal pushes to `main` can trigger production builds;
that would let an unaccepted revision bypass the canonical exact-SHA VPS acceptance.

The target release design is separate and explicit: first disable Railway GitHub autodeploy
as an action-bound provider change, then deploy only an explicit accepted commit SHA after
canonical VPS verification. Provider apply/redeploy, source disconnect/reconnect, billing,
and production cutover remain independent L5 actions.
