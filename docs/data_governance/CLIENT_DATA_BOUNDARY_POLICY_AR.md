# Client Data Boundary Policy (AR)

---

## 1. المبدأ الأساسي

**كل client data = tenant-scoped. لا cross-tenant access بدون approval + audit.**

---

## 2. Tenant Scoping (Implementation)

### Database
- كل tenant-scoped table: `tenant_id` column
- كل query: `WHERE tenant_id = :current_tenant`
- Indexes on `tenant_id`
- Composite primary key considerations: `tenant_id + entity_id`

### API
- Auth middleware sets `current_tenant_id`
- All routers check tenant scope
- No "list all" endpoints without explicit scope

### Background Jobs
- Iterate tenants, never cross
- Per-tenant audit rows

### Cache
- Key prefix: `tenant:{tenant_id}:...`
- No cross-tenant cache hit

### Search
- Per-tenant indices
- No shared search results

### File Storage
- Per-tenant prefixes
- Signed URLs scoped to tenant + user

---

## 3. Cross-Tenant Access (when needed)

Use cases:
- Aggregate reporting (anonymized)
- Fraud detection
- Support (with consent)

Process:
1. **Document purpose**
2. **Founder approval** (or designated)
3. **Time-bounded access** (token expires)
4. **Audit row** for every access
5. **Notify affected tenants** (if material)

---

## 4. Data Export (Client to Client)

- **Same client, multiple users:** standard, with permission
- **Different clients:** only via official data exchange (rare)
- **Client to third party:** with explicit consent + audit

---

## 5. Sub-Processors

- See `docs/enterprise/PRIVACY_OVERVIEW_AR.md` §9
- Each sub-processor: tenant-scoped where possible
- Audit trail of sub-processor access

---

## 6. Data Residency

- Default: KSA where possible
- Cross-border: with DPA + redaction
- Per-tenant override: in DPA

---

## 7. Backup Boundaries

- Backups per-tenant logical (same physical, different keys)
- Restore: per-tenant only
- Cross-tenant restore: forbidden without founder + audit

---

## 8. Audit Trail Integration

- Every cross-tenant attempt = audit row (even if denied)
- Aggregated reporting = separate pipeline, no individual data

---

## 9. Tests

- **Tenant isolation test:** try to access other tenant's data → must fail
- **Permission test:** user in tenant A can't see tenant B
- **Background job test:** no cross-tenant query

---

> **Owner:** Tech Lead + Data Lead · **Review:** كل release
