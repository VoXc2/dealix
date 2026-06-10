# إدارة الأسرار — Dealix Secrets Management

> **وثيقة تشغيلية.** الأسرار لا تُطبع ولا تُلتقط في التقارير ولا تظهر
> في الـ prompts.

**الحالة:** مسودة — Phase 1 من Agent #12
**التاريخ:** 2026-06-03

---

## 1. التصنيف

| الفئة | الأمثلة | الموقع |
| --- | --- | --- |
| **Critical Production** | `APP_SECRET_KEY`, `DATABASE_URL`, `MOYASAR_SECRET_KEY`, `MOYASAR_WEBHOOK_SECRET`, `BACKUP_ENCRYPTION_KEY`, `ADMIN_API_KEYS` | 1Password vault `Dealix Production` + Railway environment `production` |
| **Production Channel** | `WHATSAPP_APP_SECRET`, `WHATSAPP_ACCESS_TOKEN`, `META_PAGE_ACCESS_TOKEN`, `SENDGRID_API_KEY`, `GMAIL_REFRESH_TOKEN`, `HUBSPOT_ACCESS_TOKEN` | 1Password + Railway environment |
| **Production Optional** | `SENTRY_DSN`, `POSTHOG_API_KEY`, `CALENDLY_WEBHOOK_SECRET` | 1Password + Railway |
| **Staging** | sandbox Moyasar key, mock-mode WhatsApp, test Gmail, test HubSpot | Railway environment `staging` |
| **LLM Provider** | `ANTHROPIC_API_KEY`, `MINIMAX_API_KEY`, `GROQ_API_KEY`, `OPENAI_API_KEY`, `HERMES_API_KEY` | 1Password + Railway |
| **Backup Infra** | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | 1Password + cron host only (not Railway) |

## 2. القواعد غير القابلة للتفاوض

1. **لا أسرار في git.** `.env*` (غير `.example`) في `.gitignore`.
2. **لا أسرار في GitHub Actions secrets** للقيم التي لا تحتاجها CI.
   Railway environment variables هي المصدر الوحيد للإنتاج.
3. **لا أسرار في logs** — `scripts/security_smoke.py` يفحص.
4. **لا أسرار في reports/** — `tests/test_no_pii_in_logs.py` يفحص.
5. **لا أسرار في prompts** — لا agent ينشر prompt فيه secret.
6. **لا أسرار في PR** — PR title/body/branch لا يحتوي أسرار
   (`agentic-security-gate.yml` يفحص).
7. **لا أسرار في الـ commits** — `.gitleaks.toml` + `pre-commit` hook.
8. **لا طباعة أسرار في stdout** — حتى في debug mode.
9. **Secret rotation:** ربع سنوي (كل 90 يوم). تسجيل في
   `reports/infra/secret_rotation_log.md`.
10. **ممنوع** استخدام نفس secret لأكثر من بيئة (staging ≠ production).

## 3. الوصول

| الفئة | من يصل؟ |
| --- | --- |
| Critical Production | المؤسس فقط |
| Production Channel | المؤسس فقط |
| Staging | المؤسس + Agent #2 (read في dry-run) |
| LLM Provider | المؤسس فقط |
| Backup Infra | المؤسس فقط + cron host IAM role |
| Railway deployment tokens | المؤسس فقط (GitHub Environments) |

## 4. أدوات الكشف

| الأداة | الموقع | ما يفحص |
| --- | --- | --- |
| `.gitleaks.toml` + `.secrets.baseline` | repo root | git history + working tree |
| `pre-commit-config.yaml` | repo root | قبل كل commit |
| `scripts/security_smoke.py` | scripts/ | عند كل push (في CI) |
| `tests/test_no_pii_in_logs.py` | tests/ | logs |
| `tests/test_v7_secret_leakage_guard.py` | tests/ | PR diff + branches |
| `agentic-security-gate.yml` | `.github/workflows/` | PR body/branch untrusted input |
| `detect-secrets scan --baseline .secrets.baseline` | local + CI | baseline drift |

## 5. السرّ المفقود (Leaked Secret) — بروتوكول

1. **اكتشاف:** أداة كشف (gitleaks, Sentry, security review).
2. **إيقاف:** إعادة توليد الـ secret فوراً في المزوّد (Moyasar dashboard
   مثلاً).
3. **تنظيف:** حذف الـ secret من أي مكان ظهر فيه (git history requires
   `git filter-repo` + force-push — يحتاج موافقة المؤسس).
4. **تدوير:** تحديث 1Password + Railway environment.
5. **إبلاغ:** تسجيل الحادثة في
   `docs/SECURITY_RUNBOOK.md` incident log.
6. **مراجعة:** هل الـ secret استُخدم؟ فحص logs في Sentry/PostHog.
7. **close:** تحديث `reports/infra/secret_incidents.md`.

## 6. GitHub Actions — أسرار CI فقط

- `DEALIX_API_KEY` (read-only API key لسكريبتات smoke)
- `DEALIX_ADMIN_API_KEY` (admin key لسكريبتات founder)
- `RAILWAY_TOKEN` (للنشر فقط، في GitHub Environment)
- `GITLEAKS_LICENSE` (لو استُخدم gitleaks enterprise)

**ممنوع** تخزين production secret في GitHub Actions secrets. الـ source
of truth هو Railway environment variables.

## 7. أسرار الباك اب

- `BACKUP_ENCRYPTION_KEY` يُولَّد مرة واحدة: `python -c "import secrets;
  print(secrets.token_hex(32))"`.
- **يُحفظ في 1Password فقط**، لا في repo ولا في Railway.
- `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` يُمنحان IAM role مع
  صلاحية `s3:PutObject` + `s3:GetObject` على bucket معين فقط.
- rotation كل 90 يوم (مُسجَّل في secret_rotation_log).

## 8. ما يجب أن يفعله Agent جديد

أي agent جديد يعمل في هذا الـ repo:

- لا يطبع secret في stdout، stderr، log، report، prompt.
- يستخدم `os.getenv("...")` فقط، لا `print(os.environ)` ولا `dict(env)`.
- يحترم الـ read-only access list أعلاه.
- لو احتاج secret جديد: يسأل المؤسس، يضيفه إلى `.env.example`
  (placeholder فقط)، يضيف الفئة في هذا الـ doc.

## 9. المراجع

- `docs/SECURITY_RUNBOOK.md` — incident response
- `docs/security/` — security policies
- `docs/privacy/` — privacy / PDPL
- `.gitleaks.toml` — secret scanner config
- `scripts/check_env_contract.py` — env contract enforcement
- `scripts/security_smoke.py` — security smoke
- `docs/infra/ENVIRONMENT_POLICY_AR.md` — environment policy
- `docs/infra/STAGING_PRODUCTION_POLICY_AR.md` — staging/production split
