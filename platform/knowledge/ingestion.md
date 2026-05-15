# العربية

# الاستيعاب — طبقة المعرفة (الطبقة الرابعة)

> كيف تدخل المستندات والمحادثات والأحداث إلى ذاكرة Dealix بأمان، مع تحقّق من الملكيّة والصلاحيّات والأساس القانوني.

## 1. الغرض

بوّابة الاستيعاب هي نقطة الدخول الوحيدة لطبقة المعرفة. مسؤوليّتها: قبول المحتوى المسموح فقط، ربطه بمستأجر واحد، وتسجيل نسبه قبل الفهرسة. لا يدخل أي محتوى الذاكرة دون المرور بهذه البوّابة.

## 2. مصادر الاستيعاب المسموحة

- مستندات يرفعها المستخدم: عقود، عروض، سياسات، أدلّة تشغيل.
- محادثات واردة عبر قنوات معتمدة، عبر `auto_client_acquisition/customer_data_plane/`.
- أحداث الأعمال من سجلّ الإيرادات `auto_client_acquisition/revenue_memory/`.
- ملفّات الدروس الاستراتيجيّة المعرّفة في `auto_client_acquisition/intelligence_os/strategic_memory.py`.

## 3. مصادر ممنوعة صراحةً

- كسح المواقع الخارجيّة أو استخراج البيانات منها.
- جهات اتصال جُمعت من رسائل واتساب باردة أو أتمتة LinkedIn.
- أي بيانات شخصيّة بلا أساس قانوني مُسجَّل.

## 4. خطوات المعالجة

1. **التحقق من المستأجر:** كل وحدة محتوى تُختم بـ `tenant_id` واحد لا يتغيّر.
2. **التحقق من الأساس القانوني:** فحص الموافقة عبر سجلّ الموافقات في `customer_data_plane`.
3. **حجب البيانات الحسّاسة:** تمرير المحتوى عبر `pii_redactor.py` قبل التخزين حسب السياسة.
4. **استخلاص الوسوم:** تحديد وسوم الصلاحيّة وحالة الحداثة ونوع المصدر.
5. **التسليم للتقطيع:** تمرير المحتوى النظيف لمحرّك التقطيع.

## 5. الحوكمة

- محتوى بلا `tenant_id` يُرفض، لا يُخزَّن في نطاق افتراضي.
- محتوى بلا أساس قانوني واضح يدخل قائمة مراجعة بشريّة، لا الفهرسة المباشرة.
- كل عمليّة استيعاب تُسجَّل كحدث قابل للتدقيق.

## 6. الحداثة

كل وحدة مستوعَبة تحمل طابعًا زمنيًّا وحالة حداثة أوليّة `fresh`. تتحوّل لاحقًا إلى `aging` ثم `stale` حسب سياسة المصدر، دون حذف صامت.

روابط: `architecture.md` · `chunking.md` · `source_lineage.md`

---

# English

# Ingestion — Knowledge Layer (Layer 4)

> How documents, conversations, and events enter Dealix memory safely, with ownership, permission, and lawful-basis checks.

## 1. Purpose

The ingestion gateway is the only entry point into the knowledge layer. Its job: accept only permitted content, bind it to a single tenant, and record its lineage before indexing. No content enters memory without passing this gateway.

## 2. Permitted ingestion sources

- User-uploaded documents: contracts, proposals, policies, operating manuals.
- Inbound conversations over approved channels, via `auto_client_acquisition/customer_data_plane/`.
- Business events from the revenue ledger `auto_client_acquisition/revenue_memory/`.
- Strategic lesson files defined in `auto_client_acquisition/intelligence_os/strategic_memory.py`.

## 3. Explicitly prohibited sources

- Scraping external sites or extracting data from them.
- Contacts gathered through cold WhatsApp messages or LinkedIn automation.
- Any personal data without a recorded lawful basis.

## 4. Processing steps

1. **Tenant check:** Every content unit is stamped with a single, immutable `tenant_id`.
2. **Lawful-basis check:** Consent is verified through the consent registry in `customer_data_plane`.
3. **Sensitive-data redaction:** Content passes through `pii_redactor.py` before storage, per policy.
4. **Tag extraction:** Permission tags, freshness status, and source type are determined.
5. **Handoff to chunking:** Clean content is passed to the chunking engine.

## 5. Governance

- Content without a `tenant_id` is rejected, not stored under a default scope.
- Content without a clear lawful basis enters a human review queue, not direct indexing.
- Every ingestion operation is recorded as an auditable event.

## 6. Freshness

Every ingested unit carries a timestamp and an initial freshness status of `fresh`. It later transitions to `aging` then `stale` per source policy, with no silent deletion.

Links: `architecture.md` · `chunking.md` · `source_lineage.md`
