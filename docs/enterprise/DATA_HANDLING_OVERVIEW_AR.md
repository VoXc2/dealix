# Data Handling Overview — Dealix (AR)

> يُكمّل `PRIVACY_OVERVIEW_AR.md` بالتفاصيل التشغيلية.

---

## 1. Data Lifecycle (لكل dataset)

```
[Collect] → [Classify] → [Store] → [Use] → [Share (allowlist)] → [Archive] → [Delete]
   ↓           ↓            ↓        ↓             ↓                  ↓           ↓
 T-class    D-class    Encrypted  Purpose    Sub-processor      Retention    Audit
            recorded   at-rest    limited    list              rule
```

## 2. Data Classification (D0–D6)

| Class | الوصف | Examples | Default handling |
|-------|-------|----------|------------------|
| D0 | Public | marketing copy, public pricing | أي مكان |
| D1 | Business metadata | company name, sector | analytics، reports |
| D2 | Business contact | email business, phone business | مع purpose |
| D3 | Client operational | draft content, approval logs | client-scoped |
| D4 | Sensitive client | pricing strategy, internal notes | redacted unless needed |
| D5 | Secrets | API keys, payment, tokens | **never in prompts/logs** |
| D6 | Forbidden | لا يُجمع أصلاً | blocked at intake |

**راجع:** `docs/governance/DATA_HANDLING_RULES.md` (يوجد) و `docs/governance/DATA_RETENTION.md`.

## 3. Data Minimization Rules

- **Intake forms:** حقول اختيارية بقدر الإمكان
- **Lead capture:** فقط ما يكفي للتواصل (لا DOB، لا national ID)
- **AI inputs:** يرسل للنموذج فقط الحقول الضرورية للمهمة، مع redaction صريحة
- **Logs:** لا نُسجّل prompt content، فقط metadata

## 4. Storage

| Tier | Storage | Encryption | Access |
|------|---------|------------|--------|
| Operational | Postgres (managed) | at-rest (provider) | service tokens |
| Audit | JSONL append-only | at-rest | read-only بعد الكتابة |
| Backups | Provider-managed | at-rest | founder + ops |
| Object (uploads) | Object storage (مُخطط) | at-rest + signed URLs | client-scoped |

## 5. Access Patterns

- **Default:** least privilege
- **Client data:** tenant-scoped، cross-tenant access requires founder approval + audit
- **Audit logs:** read by security officer + founder فقط
- **Secrets:** no human access in production؛ rotation via env/vault

## 6. Sharing (Sub-Processors)

راجع `PRIVACY_OVERVIEW_AR.md` § 9. كل مشاركة:
- موثّقة في DPA
- مذكورة في قائمة sub-processors
- معلنة للعميل

## 7. Retention

| Data class | Retention | Deletion method |
|------------|-----------|-----------------|
| D0 public | غير محدود | N/A |
| D1 metadata | 24 شهر بعد آخر interaction | anonymize |
| D2 contact | 24 شهر بعد opt-out | delete + audit |
| D3 operational | طول العقد + 90 يوم | delete + audit |
| D4 sensitive | طول العقد + 30 يوم | secure delete + audit |
| D5 secrets | مدة الصلاحية فقط | auto-rotate |
| Audit logs | 7 سنوات (compliance) | append-only |

**Deletion right:** خلال 30 يوم من الطلب (PDPL).

## 8. Subject Rights Implementation

- **Access:** portal export (JSON)
- **Rectification:** portal update
- **Erasure:** admin task + audit
- **Restriction:** opt-out flag في كل entity
- **Portability:** JSON/CSV export
- **Objection:** suppression list

## 9. Data Quality (RULES)

- حقول مطلوبة محددة
- validation على intake (regex, type)
- dedup logic على leads
- drift detection شهري
- مذكور في `docs/data/SOVEREIGN_DATA_MODEL.md` (يوجد)

## 10. Honesty Statement

لا نبيع بيانات. لا نشاركها مع أطراف غير مذكورة. لا نستخدمها لتدريب نماذج على بيانات العميل بدون موافقة صريحة.

---

> **Owner:** Founder + Data Lead · **Review:** كل 90 يوم
