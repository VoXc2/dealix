# Layer 2 — Multi-Tenancy (As-Built) — العزل متعدد المستأجرين

**EN.** This documents tenant isolation **as it exists in the repo today** — not
a target spec. Multi-tenancy is implemented. This file records what is there,
how it works, and the specific residual gaps that keep it from a clean `PASS`.

**AR.** توثّق هذه الوثيقة العزل بين المستأجرين **كما هو موجود في المستودع اليوم**
— لا كمواصفات مستهدفة. العزل مُنفَّذ بالفعل؛ هنا نسجّل ما هو قائم، وكيف يعمل،
والفجوات المتبقية المحدّدة التي تمنع تقييم `PASS` نظيفًا.

Owner: Platform Engineer · Defends: OWASP API1:2023 BOLA.

---

## 1. As-built — ما هو منفّذ فعلاً

### Tenant model
`db/models.py` → `TenantRecord` (`tenants` table). One row = one subscribing
enterprise client. Carries `plan`, `status`, `max_users`, `max_leads_per_month`,
`features`, soft-delete (`deleted_at`). Every tenant-scoped table
(`LeadRecord`, `DealRecord`, `AccountRecord`, `ContactRecord`) has a
`tenant_id` foreign key to `tenants.id`, plus composite indexes
(`ix_leads_tenant_status`, `ix_deals_tenant_stage`).

### Isolation middleware
`api/middleware/tenant_isolation.py` provides:

| Symbol | Role |
|--------|------|
| `TenantContext` | Frozen dataclass: `tenant_id`, `source`, `user_id`, `is_super_admin`. |
| `resolve_tenant_context(...)` | Resolves `tenant_id` in priority order (below). |
| `assert_tenant_match(...)` | Per-object guard — raises on mismatch. Defense in depth. |
| `filter_tenant_scoped_list(...)` | Filters collections; excludes items of unknown ownership. |
| `CrossTenantAccessDenied` | Generic exception → route layer converts to HTTP 403. |

### Resolution order (priority high → low)
1. `test_override` kwarg (testing only)
2. JWT claim `tenant_id`
3. `X-Tenant-ID` header (B2B API-key auth)
4. API-key prefix (`apikey_<tenant>_<random>` → tenant)
5. Subdomain (`<tenant>.api.dealix.me` → tenant)

No tenant resolved **and** not super-admin → `CrossTenantAccessDenied`. There is
**no silent fallback** — missing tenant on either side of a comparison blocks.

### Super-admin path
`is_super_admin=True` bypasses tenant scoping for system operations. The code
comments require every super-admin access to be **separately audit-logged** by
the caller (see [`audit_logging.md`](audit_logging.md)).

### Tests
`tests/test_tenant_isolation_v1.py`, `tests/test_admin_tenants.py`,
`tests/test_tenant_theming.py`.

---

## 2. Readiness checklist — قائمة التحقق

Release 1 acceptance: **1 tenant · 3 users · 2 roles · every API resolves
`tenant_id` · every action audit-logged · rollback drilled.**

| # | Check | Evidence | State |
|---|-------|----------|-------|
| 1 | Tenant model with `tenant_id` on all customer tables | `db/models.py` `TenantRecord` + FKs | ✅ Met |
| 2 | Middleware resolves `tenant_id` on every request | `tenant_isolation.py` `resolve_tenant_context` | ✅ Met |
| 3 | Per-object guard before returning customer data | `assert_tenant_match` | ⚠️ Partial — guard exists; **call-site coverage unproven** |
| 4 | Cross-tenant access raises and is denied (403) | `CrossTenantAccessDenied` | ✅ Met |
| 5 | No silent fallback on missing tenant | `assert_tenant_match` empty-check | ✅ Met |
| 6 | Super-admin access is separately audit-logged | code comment requires it | ⚠️ Partial — **enforcement not evidenced** |
| 7 | Collections are tenant-filtered | `filter_tenant_scoped_list` | ⚠️ Partial — helper exists; not proven used everywhere |
| 8 | `pytest` fails on a cross-tenant leak | `test_tenant_isolation_v1.py` | ✅ Met |

---

## 3. Residual gaps — الفجوات المتبقية

1. **Endpoint-coverage proof.** The repo has 100+ routers. There is no automated
   proof that *every* customer-scoped endpoint calls `assert_tenant_match` /
   `filter_tenant_scoped_list`. Needed: a coverage test or lint that fails CI if
   a customer-scoped route skips the guard.
2. **Super-admin audit enforcement.** Audit-logging of super-admin cross-tenant
   reads is a code-comment convention, not an enforced control. Needed: a
   wrapper that makes the audit log non-optional on the super-admin path.
3. **DB-level row security.** `TenantRecord`'s docstring says "row-level security
   policies enforce this at DB level in production" — confirm Postgres RLS is
   actually applied, or downgrade the claim.

These three are the work that moves Layer 2 from a strong-but-partial score to a
clean `PASS`. They are tracked in [`gap_analysis.md`](gap_analysis.md).

---

## ملخص بالعربية

العزل متعدد المستأجرين منفّذ: نموذج `TenantRecord`، و`tenant_id` على كل جداول
العملاء، ووسيط `tenant_isolation.py` يحلّ المستأجر بترتيب أولوية واضح ويمنع
الوصول العابر دون أي تراجع صامت. الفجوات المتبقية ثلاث: إثبات تغطية كل النقاط
الطرفية بالحارس، وفرض تدقيق وصول المشرف الأعلى، والتأكد من تفعيل RLS على مستوى
قاعدة البيانات.
