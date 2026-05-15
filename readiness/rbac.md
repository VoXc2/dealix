# Layer 3 — RBAC (As-Built) — التحكم بالوصول حسب الأدوار

**EN.** Role-based access control **as it exists in the repo today**. RBAC is
implemented, but a notable part of it is a dead stub — this file records both
what works and what does not.

**AR.** التحكم بالوصول حسب الأدوار **كما هو موجود في المستودع اليوم**. RBAC
مُنفَّذ، لكن جزءًا ملحوظًا منه مجرّد كود ميّت — تسجّل هذه الوثيقة ما يعمل وما لا
يعمل.

Owner: Security Engineer.

---

## 1. As-built — ما هو منفّذ فعلاً

### Roles
`api/security/rbac.py` defines four tenant-scoped roles in ascending privilege:

| Role | Permission highlights |
|------|-----------------------|
| `viewer` | `leads:read`, `deals:read`, `reports:read`, `profile:*` |
| `sales_rep` | `+ leads:write/create`, `deals:write/create`, `agents:run` |
| `sales_manager` | `leads:*`, `deals:*`, `agents:*`, `users:read`, `reports:export` |
| `tenant_admin` | `+ tenant:*`, `users:*`, `roles:*`, `settings:*`, `invites:*` |

Plus one system role: `super_admin` (`SystemRole`), permission set `{"*"}`,
spans all tenants.

### Permission engine
- `ROLE_PERMISSIONS` — permission sets per role, glob-style (`leads:*`).
- `has_permission(role_name, permission)` — wildcard-aware check.
- `is_at_least(role_name, minimum)` — hierarchy comparison via `_ROLE_ORDER`.
- `is_super_admin(system_role)` — system-role guard.
- `DEFAULT_TENANT_ROLES` — the four roles bootstrapped for every new tenant.

### Storage
`db/models.py` → `RoleRecord` (`roles` table): `tenant_id` FK, `name`,
`permissions` (JSON list), `is_system` (system roles undeletable),
unique `(tenant_id, name)`. `UserRecord.role_id` FKs to it;
`UserRecord.system_role` carries `super_admin`.

### Route guards
`api/security/auth_deps.py`:
- `get_current_user` / `CurrentUser` — decodes JWT, loads `UserRecord`, rejects
  inactive/deleted users.
- `_make_role_guard(minimum)` — **working** guard: loads role name from
  `RoleRecord` via `role_id`, applies `is_at_least`. Pre-built as
  `require_viewer`, `require_sales_rep`, `require_sales_manager`,
  `require_tenant_admin`.
- `require_super_admin` — strict system-role guard.
- `get_tenant_id` / `TenantID` — effective tenant; super-admin may override via
  `X-Tenant-ID`.

### Tests
`tests/test_admin_tenants.py` and the auth/integration suites.

---

## 2. Readiness checklist — قائمة التحقق

| # | Check | Evidence | State |
|---|-------|----------|-------|
| 1 | ≥ 2 distinct roles exist | `Role` enum — 4 roles | ✅ Met |
| 2 | Permissions are explicit and namespaced | `ROLE_PERMISSIONS` | ✅ Met |
| 3 | Role hierarchy enforced | `is_at_least`, `_ROLE_ORDER` | ✅ Met |
| 4 | Working route guard | `_make_role_guard` + `require_*` | ✅ Met |
| 5 | Super-admin path is separate and strict | `require_super_admin` | ✅ Met |
| 6 | Roles persisted per tenant, system roles undeletable | `RoleRecord.is_system` | ✅ Met |
| 7 | Every sensitive endpoint applies a guard | — | ⚠️ Partial — **coverage unproven** |
| 8 | `pytest` fails when a guard is bypassed | auth suite | ⚠️ Partial — needs explicit deny-case test |

---

## 3. Residual gaps — الفجوات المتبقية

1. **Dead `require_role` factory.** `api/security/auth_deps.py` `require_role()`
   (lines ~118–142) is a non-functional stub: it **raises 403 unconditionally**
   with a placeholder comment, never checking the role. Only `_make_role_guard`
   / the `require_*` callables work. Risk: a developer copying the docstring
   example (`Depends(require_role(Role.SALES_REP))`) wires a broken guard.
   **Action:** either delete `require_role` or make it delegate to
   `_make_role_guard`, and update the module docstring example.
2. **Endpoint-coverage proof.** No automated proof that every sensitive route
   applies a `require_*` guard. Same shape of gap as Layer 2 — needs a CI lint.
3. **Doc/code mismatch.** `RoleRecord`'s docstring lists roles
   `owner, admin, sales_rep, viewer, agent_operator`, which do **not** match the
   actual `Role` enum (`viewer, sales_rep, sales_manager, tenant_admin`). Fix
   the docstring so the source of truth is unambiguous.
4. **Permission-vs-hierarchy clarity.** Guards check the *hierarchy*
   (`is_at_least`); `has_permission` checks *fine-grained* permissions. Document
   which endpoints rely on which, so future routes pick the right check.

Gap 1 is the most important — it is a real correctness defect, not just polish.

---

## ملخص بالعربية

RBAC منفّذ: أربعة أدوار للمستأجر + دور `super_admin` للنظام، ومحرّك صلاحiات
يدعم الأنماط العامة، وحارس مسارات يعمل (`_make_role_guard` و`require_*`).
الفجوة الأهم: مصنع `require_role` في `auth_deps.py` كود ميّت يرفض دائمًا
بـ403 — يجب حذفه أو إصلاحه. وفجوات أخرى: إثبات تغطية كل النقاط الطرفية، وتعارض
بين docstring في `RoleRecord` والأدوار الفعلية.
