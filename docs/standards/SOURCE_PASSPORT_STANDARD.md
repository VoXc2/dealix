# Source Passport Standard

كل مصدر بيانات له **جواز** يحدد المالك، الاستخدام المسموح، PII، والعلاقة القانونية/التشغيلية.

## قواعد Dealix

```text
No Source Passport = no AI use.
Unknown source = no outreach.
PII + unclear basis = redact or block.
External use = approval required.
```

هذا يفرّق Dealix عن lead scrapers ووكالات أتمتة غير آمنة.

**الكود:** `SOURCE_PASSPORT_REQUIRED_KEYS` · `source_passport_keys_present` — `standards_os/source_passport_standard.py`

**مرجع معماري:** [`../architecture/SOURCE_PASSPORT.md`](../architecture/SOURCE_PASSPORT.md)

**صعود:** [`DATA_READINESS_STANDARD.md`](DATA_READINESS_STANDARD.md)
