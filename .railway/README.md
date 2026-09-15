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

`checkSuites` remains true for both production services. A normal GitHub push must
not become production merely because hosted checks are noisy or unavailable. The
trusted release path is separate: accept an exact source SHA on the VPS, then use an
explicit action-bound production deployment for that exact SHA. Third-party failures
(such as a stale Vercel Hobby check) are not Dealix acceptance evidence, but they are
also not bypassed globally by weakening the production source trigger.
