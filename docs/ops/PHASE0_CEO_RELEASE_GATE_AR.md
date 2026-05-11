# بوابة المرحلة 0 — دمج، CI، تحقق (قرار رئيس تنفيذي)

قبل اعتبار `main` «جاهزاً للخطوة التالية» راجع أيضاً [مؤشرات التشغيل التنفيذي](../strategic/CEO_OPERATING_METRICS_AR.md):

## 1. دمج الفروع

- ادمج PRs ذات الأولوية (إصلاحات تعطل الاستيراد، وثائق استراتيجية، ميزات معتمدة) إلى `main`.
- لا تترك عملاً حرجاً على فرع طويل دون دمج — راجع [docs/COMPREHENSIVE_COMPLETION_PLAN_AR.md](../COMPREHENSIVE_COMPLETION_PLAN_AR.md) (مرحلة Git).

## 2. CI

- تأكد أن workflow [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) أخضر على آخر commit لـ `main`.

## 3. تحقق محلي (أو على runner)

```bash
bash scripts/revenue_os_master_verify.sh
# متوقع: DEALIX_REVENUE_OS_VERDICT=PASS

APP_ENV=test APP_DEBUG=false \
  ANTHROPIC_API_KEY=test-anthropic-key DEEPSEEK_API_KEY=test-deepseek-key \
  GROQ_API_KEY=test-groq-key GLM_API_KEY=test-glm-key GOOGLE_API_KEY=test-google-key \
  python scripts/smoke_inprocess.py
# متوقع: SMOKE_INPROCESS_OK
```

## 4. قاعدة البيانات

- اتبع [ALEMBIC_MIGRATION_POLICY.md](ALEMBIC_MIGRATION_POLICY.md) لأي ترحيل في staging/production.

## 5. تعارض `api.middleware`

- يجب ألا يوجد ملف `api/middleware.py` يظلّل حزمة `api/middleware/` — الوسائط HTTP في `api/middleware/http_stack.py` مع إعادة تصدير من `__init__.py`.
