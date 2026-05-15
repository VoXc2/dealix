# العربية

## نموذج المخاطر — الطبقة الأولى (الأساس)

Owner: قائد المنصة (Platform Lead)

### الغرض

يُحدِّد هذا المستند المخاطر التي تهدد الوعد الأساسي للطبقة الأولى: أن كل مستأجر داخل Dealix معزول وآمن وقابل للإدارة وقابل للاسترجاع. كل خطر مصنّف حسب الاحتمال والأثر، مع ضابط تخفيف يشير إلى كود حقيقي في المستودع.

### سجل المخاطر

| المعرّف | الخطر | الاحتمال | الأثر | الضابط / التخفيف |
|---|---|---|---|---|
| F-R1 | تسرّب بيانات بين المستأجرين بسبب استعلام غير مُقيَّد بـ `tenant_id` | متوسط | حرج | تقييد إجباري في الوسيط، فحوص في `api/security/auth_deps.py`، اختبارات عزل في `platform/multi_tenant/tests.md` |
| F-R2 | سرقة رمز JWT أو إعادة استخدامه | متوسط | عالٍ | انتهاء صلاحية قصير لرمز الوصول، تدوير عبر `refresh_tokens`، إبطال الجلسة في `api/routers/auth.py` |
| F-R3 | تسرّب سرّ إنتاجي (مفتاح، كلمة مرور قاعدة البيانات) | منخفض | حرج | الأسرار في متغيرات بيئة لكل بيئة، فحص `codeql.yml`، قاعدة `no_pii_in_logs` |
| F-R4 | فشل نشر يترك الإنتاج في حالة غير متسقة | متوسط | عالٍ | تراجع آلي عبر `.github/workflows/railway_deploy.yml`، فحص صحة `scheduled_healthcheck.yml` |
| F-R5 | فقدان بيانات بسبب غياب نسخة احتياطية صالحة | منخفض | حرج | لقطات يومية `daily_snapshot.yml`، تمرين استرجاع ربع سنوي |
| F-R6 | إجراء حساس يُنفَّذ بدون موافقة | منخفض | عالٍ | تصنيف A0–A3/R0–R3/S0–S3 في `dealix/classifications/__init__.py`، بوابة الموافقة `dealix/trust/approval.py` |
| F-R7 | حذف مستأجر يؤثر على مستأجرين آخرين | منخفض | حرج | حذف مُقيَّد بـ `tenant_id`، تمرين موثَّق في `platform/multi_tenant/tenant_deletion.md` |
| F-R8 | غياب قيد تدقيق لإجراء (فجوة مساءلة) | متوسط | متوسط | كتابة إجبارية عبر `dealix/trust/audit.py`، تنبيه على فجوات التغطية |
| F-R9 | ادعاء مبالغ فيه في مخرجات موجّهة للعميل | منخفض | عالٍ | سجل `dealix/registers/no_overclaim.yaml`، فحص `auto_client_acquisition/governance_os/claim_safety.py` |

### مصفوفة الاحتمال × الأثر

- الخطر **الحرج عالي الاحتمال**: لا يوجد حاليًا — هدف صريح.
- الخطر **الحرج متوسط الاحتمال**: F-R1 — يخضع لأعلى أولوية اختبار.
- المخاطر **الحرجة منخفضة الاحتمال**: F-R3، F-R5، F-R7 — تخفيفها قائم ويحتاج تمارين دورية موثَّقة.

### المخاطر المتبقية

تمرين حذف المستأجر وتمرين الاسترجاع لم يُوثَّقا دوريًا بعد. هذه فجوة جاهزية معروفة وتفسّر عدم بلوغ الطبقة نطاق "جاهز للمؤسسات".

### الروابط ذات الصلة

- `platform/foundation/readiness.md`
- `platform/foundation/rollback.md`
- `platform/security/incident_response.md`
- `docs/SECURITY_RUNBOOK.md`

# English

## Risk Model — Layer 1 (Foundation)

Owner: Platform Lead

### Purpose

This document identifies the risks that threaten the core promise of Layer 1: that every tenant inside Dealix is isolated, secure, manageable, and recoverable. Each risk is rated by likelihood and impact, with a mitigating control that points to real code in the repository.

### Risk register

| ID | Risk | Likelihood | Impact | Control / Mitigation |
|---|---|---|---|---|
| F-R1 | Cross-tenant data leakage from a query not scoped to `tenant_id` | Medium | Critical | Mandatory scoping in middleware, checks in `api/security/auth_deps.py`, isolation tests in `platform/multi_tenant/tests.md` |
| F-R2 | JWT token theft or replay | Medium | High | Short access-token lifetime, rotation via `refresh_tokens`, session revocation in `api/routers/auth.py` |
| F-R3 | Production secret leak (key, database password) | Low | Critical | Secrets in per-environment variables, `codeql.yml` scan, `no_pii_in_logs` rule |
| F-R4 | Failed deploy leaves production in an inconsistent state | Medium | High | Automated rollback via `.github/workflows/railway_deploy.yml`, healthcheck `scheduled_healthcheck.yml` |
| F-R5 | Data loss due to absence of a valid backup | Low | Critical | Daily snapshots `daily_snapshot.yml`, quarterly restore drill |
| F-R6 | A sensitive action executes without approval | Low | High | A0–A3/R0–R3/S0–S3 classification in `dealix/classifications/__init__.py`, approval gate `dealix/trust/approval.py` |
| F-R7 | Tenant deletion affects other tenants | Low | Critical | Deletion scoped to `tenant_id`, documented drill in `platform/multi_tenant/tenant_deletion.md` |
| F-R8 | Missing audit entry for an action (accountability gap) | Medium | Medium | Mandatory write via `dealix/trust/audit.py`, alert on coverage gaps |
| F-R9 | Overclaim in customer-facing output | Low | High | `dealix/registers/no_overclaim.yaml` register, `auto_client_acquisition/governance_os/claim_safety.py` check |

### Likelihood x Impact matrix

- **Critical, high likelihood**: none currently — an explicit goal.
- **Critical, medium likelihood**: F-R1 — receives the highest testing priority.
- **Critical, low likelihood**: F-R3, F-R5, F-R7 — mitigations exist and need documented periodic drills.

### Residual risk

The tenant-deletion drill and the restore drill are not yet documented on a periodic cadence. This is a known readiness gap and explains why the layer has not reached the "enterprise-ready" band.

### Related docs

- `platform/foundation/readiness.md`
- `platform/foundation/rollback.md`
- `platform/security/incident_response.md`
- `docs/SECURITY_RUNBOOK.md`
