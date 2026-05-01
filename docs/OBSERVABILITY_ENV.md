# مراقبة البيئة — Staging / Production

## متغيرات (اختياري)

| المتغير | الغرض |
|---------|--------|
| `SENTRY_DSN` | أخطاء واستثناءات |
| `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` | تتبع prompts وتقييم |
| `LANGFUSE_HOST` | افتراضي `https://cloud.langfuse.com` |

## مبدأ

- لا تُفعّل في **test** أو **CI** إلا إن رغبت بمشروع Langfuse منفصل.
- staging أولاً، ثم production.

## الكود

`api/main.py` يحاول استيراد `dealix.observability` — إن لم يكن الحزمة مثبتة يتجاهل بهدوء.
