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
