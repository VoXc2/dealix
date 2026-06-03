# طبقة البيانات (Data OS)

## Source Passport

لكل مصدر: نوع، مالك، سياق الجمع، allowed use، حالة PII، حساسية، احتفاظ، هل AI مسموح، هل الاستخدام الخارجي مسموح.

## Data Readiness Score

وضوح المصدر، اكتمال، تكرارات، حقول ناقصة، جودة صيغة، تصنيف PII، وضوح allowed use.

## قواعد

- No Source Passport = no AI use.
- No allowed use = internal analysis only.
- Unknown source = no outreach.
- PII + external use = approval required.

## Saudi Data Layer

تصنيف قطاعات، تطبيع مدن/مناطق، حقول شركات عربية، لغة PDPL-aware، حالة علاقة/موافقة لواتساب.

## تنفيذ

- `auto_client_acquisition/data_os/`، `docs/architecture/SOURCE_PASSPORT.md`

## روابط

- [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md)
