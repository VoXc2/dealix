# Security Questionnaire (Template)

> Fill this for every enterprise buyer. Save as `business/enterprise/runs/YYYY-MM-DD-<buyer>.md`.

## 1. Identity & Access
- [ ] SSO support: planned (V11+)
- [ ] MFA support: planned
- [ ] RBAC: V1 single-role (founder) only

## 2. Data
- [ ] Data residency: KSA (V1)
- [ ] PII: minimum (industry + city + visible signal only)
- [ ] Retention: see `docs/data/DATA_RETENTION_POLICY.md`

## 3. Encryption
- [ ] At rest: AES-256 (database-level)
- [ ] In transit: TLS 1.2+

## 4. Audit
- [ ] Audit log: every mutation
- [ ] Retention: 12 months
- [ ] Format: JSONL

## 5. AI
- [ ] Provider: optional, defaults to deterministic
- [ ] Human review: required for every output
- [ ] Banned claims: enforced

## 6. Backup
- [ ] Manual: `python3 scripts/backup_business_data.py`
- [ ] Auto: every JSON write
- [ ] RTO: 1 hour / RPO: 24 hours

## 7. Incident response
- [ ] Severity levels: P0 / P1 / P2 / P3
- [ ] On-call: founder
- [ ] Communication: 24h SLA
