# Ops Client Pack — حزمة تشغيل المبيعات (عربي)

حزمة جاهزة لتحويل Phase MAX من عرض تقني إلى آلة تشغيل تجارية.

| ملف | الاستخدام |
| --- | --- |
| [dealix_ops_runbook_ar.md](dealix_ops_runbook_ar.md) | مسار المحادثة، ديمو 12 دقيقة، 72 ساعة، قواعد عدم الهزل |
| [EXECUTIVE_DECK_OUTLINE_AR.md](EXECUTIVE_DECK_OUTLINE_AR.md) | **مصدر الشرائح في Git** — صدّر إلى pptx يدوياً |
| `dealix_ops_sales_kit_ar.pptx` | Executive Deck للعميل — **اختياري خارج Git** |

**pptx:** الملف الثنائي غير مُتتبَّع في المستودع. أنشئه من `EXECUTIVE_DECK_OUTLINE_AR.md` أو ضع نسخة محلية عند  
`docs/commercial/ops_client_pack/dealix_ops_sales_kit_ar.pptx` (أضف إلى `.gitignore` إن كان يحتوي علامة تجارية نهائية).

**تشغيل:** `bash scripts/run_business_now.sh` ثم `/ar/business-now#strategy` مع API على `:8000`.

**API:** `GET /api/v1/business-now/commercial-strategy` → حقل `ops_client_pack`.
