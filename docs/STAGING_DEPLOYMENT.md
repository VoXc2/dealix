# نشر Staging — Dealix API

## منصة موصى بها

**Railway** (أو **Render** كبديل).

## أمر التشغيل

```bash
uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

على Railway غالباً `PORT` يُحقن تلقائياً.

## Healthcheck

- المسار: **`GET /health`**
- يتوقع `200` وJSON فيه `status`.

## متغيرات بيئة (مثال)

- `APP_ENV=staging`
- `DATABASE_URL` / إعدادات DB إن وُجدت
- `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` (سيرفر فقط)
- مفاتيح LLM إن لزم للتجارب
- **لا** تضع `MOYASAR_SECRET` أو أسرار في المتغيرات العامة للواجهة

## Smoke بعد النشر

من جهازك:

```bash
python scripts/smoke_local_api.py --base-url https://<staging-host>
```

أو `curl` على `/` و`/health` ومسارات الـ API الحرجة.

## Rollback

- إعادة نشر commit سابق في Railway/Render.
- إبقاء migration منفصلة عن كود التطبيق؛ عند الحاجة تراجع SQL يدوياً.

## ملاحظة

لا يُرفع ملف `railway.toml` هنا حتى لا يتعارض مع إعداد موجود لديك؛ أنشئ الخدمة من لوحة Railway واربط الريبو.
