# Saudi Layer — Saudi Layer / تميز محلي

| ملف | موضوع |
|------|--------|
| [SAUDI_SECTOR_TAXONOMY.md](SAUDI_SECTOR_TAXONOMY.md) | تصنيف قطاعات — 30+ قطاعاً مع رموز NAICS/ISIC |
| [SAUDI_SECTOR_INTELLIGENCE.md](SAUDI_SECTOR_INTELLIGENCE.md) | ذكاء قطاعات سعودي — حجم السوق، النمو، الفرص |
| [CITY_REGION_NORMALIZATION.md](CITY_REGION_NORMALIZATION.md) | 46+ مدينة في 13 منطقة مع الإحداثيات |
| [SAUDI_B2B_CONTEXT.md](SAUDI_B2B_CONTEXT.md) | سياق الأعمال B2B السعودي — الثقافة والموسم |
| [SAUDI_OPEN_DATA_USAGE.md](SAUDI_OPEN_DATA_USAGE.md) | مصادر البيانات المفتوحة السعودية |
| [ARABIC_EXECUTIVE_QA.md](ARABIC_EXECUTIVE_QA.md) | QA عربي تنفيذي — 12 بُعداً مع 50+ مثالاً |
| [ARABIC_STYLE_GUIDE.md](ARABIC_STYLE_GUIDE.md) | دليل أسلوب عربي — 25+ قاعدة |
| [FORBIDDEN_ARABIC_CLAIMS.md](FORBIDDEN_ARABIC_CLAIMS.md) | ممنوعات لغوية — 40+ ادعاء مع الأساس القانوني |
| [PROOF_SAFE_ARABIC_LANGUAGE.md](PROOF_SAFE_ARABIC_LANGUAGE.md) | عربي آمن للإثبات — مستويات L0-L5 |
| [BILINGUAL_REPORTING.md](BILINGUAL_REPORTING.md) | تقارير ثنائية اللغة — معالجة RTL/LTR |
| [CITY_REGION_NORMALIZATION.md](CITY_REGION_NORMALIZATION.md) | تطبيع المدن والمناطق |

## Architecture

السعودية طبقة_السعودية ← الخليج توسع → دول الخليج

```
auto_client_acquisition/saudi_layer/   — Python intelligence layer
integrations/mc.py, qiwa.py, etc.     — Government API clients
integrations/uae.py, qatar.py, etc.   — GCC country modules
dealix/payments/currency_engine.py     — Multi-currency engine
dealix/compliance/vat_engine.py        — Multi-VAT engine
docs/37_saudi_layer/                   — Documentation
```

## ملاحظة

هذه الطبقة جزء من مسار التوسع من MVP إلى شركة تشغيل؛ راجع الموجات في
[DEALIX_EXECUTION_WAVES_AR.md](../strategic/DEALIX_EXECUTION_WAVES_AR.md).
