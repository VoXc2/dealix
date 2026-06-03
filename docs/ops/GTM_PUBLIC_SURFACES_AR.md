# أسطح الطلب العامة + طبقة ثقة API

**الغرض:** مرجع واحد لقنوات التوزيع العامة (ويب + API) وما يجب أن يبقى عاماً بدون مفتاح.

**مصدر الحقيقة الآلي:** [`dealix/config/gtm_public_surfaces.yaml`](../../dealix/config/gtm_public_surfaces.yaml)

**تحقق:**

```bash
python scripts/verify_gtm_public_surfaces.py
python scripts/verify_gtm_public_surfaces.py --api-base https://api.dealix.me
```

---

## API (`api.dealix.me`)

| المسار | الاستخدام |
|--------|-----------|
| `/healthz` | Railway healthcheck — يعيد `version` + `git_sha` |
| `/health` | ملخص حي + مزودي LLM |
| `/version` | هوية النشر للشركاء والمراقبة |
| `/api/v1/meta` | سجل الأسطح + روابط canonical |
| `/docs` · `/openapi.json` | وثائق المطورين |

**سياسة:** هذه المسارات في `PUBLIC_PATHS` — لا تضف أسراراً في الاستجابة.

---

## ويب عام (Next.js)

| المسار | الدور |
|--------|--------|
| `/[locale]` | صفحة الإطلاق التجاري |
| `/[locale]/dealix-diagnostic` | تشخيص / نية شراء |
| `/[locale]/proof-pack` | قصة الإثبات |
| `/[locale]/risk-score` | قمع المخاطر |
| `/[locale]/learn` | محتوى AEO |
| `/[locale]/partners` | اهتمام شركاء |
| `/[locale]/services` | سلم العروض |

**Ops (غير عام):** `/[locale]/ops/*` — مفتاح إدارة فقط.

---

## بعد كل نشر Railway

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/version
curl -fsS https://api.dealix.me/api/v1/meta
python scripts/verify_railway_production_config.py --skip-live
```

---

## مراجع

- [`RAILWAY_PRODUCTION_SETTINGS_AR.md`](RAILWAY_PRODUCTION_SETTINGS_AR.md)
- [`DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md`](../commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md)
