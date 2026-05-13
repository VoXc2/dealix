# نموذج التشغيل القائم على الأحداث — نموذج التركيب القابض

**الطبقة:** Holding · Compound Holding Model
**المالك:** رئيس Dealix Core (CTO)
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [EVENT_DRIVEN_OPERATING_MODEL.md](./EVENT_DRIVEN_OPERATING_MODEL.md)

## السياق
تعمل دياليكس وفق **نموذج تشغيل قائم على الأحداث**: كل تغيّر حالة ذي مغزى داخل Core OS يُصدر حدث مجال مهيكَلاً. الأحداث هي العمود الفقري الذي يربط طبقات التطبيق والتحكم بالذكاء والحوكمة والبيانات والتكامل والتعلم دون اقترانها. هذا ما يُتيح للقابض البقاء وحداتياً اليوم والتحوّل لميكروسيرفس غداً دون إعادة كتابة منطق الأعمال. المعمارية في `docs/BEAST_LEVEL_ARCHITECTURE.md`، وموقف الموثوقية في `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`، وأصل التشغيل في `docs/ledgers/AI_RUN_LEDGER.md`.

## ما الذي تُمكّنه الأحداث

- **التدقيق** — كل إجراء قابل لإعادة البناء.
- **التحليلات** — لوحات المجلس والوحدات تُشترك بدل الاستطلاع.
- **سجل الإثبات** — أحداث الإثبات تتراكم كسجل قانوني للقيمة.
- **الأتمتة** — المسارات تُحفَّز بالحدث لا بالمؤقّت.
- **التنبيهات** — العملاء والمشغّلون يتلقّون تحديثات سياقية.
- **برج التحكم بالذكاء** — أحداث Gateway تُحرّك الكلفة والتقييم والانحراف.
- **قياس المنتج** — أحداث ترشّح الميزات تُغذّي Productization Ledger.

## مظروف الحدث المشترك

كل حدث يستخدم هذا المظروف (مع حقول خاصّة بنوع الحمولة):

```json
{
  "event_type": "<string>",
  "event_id": "<uuid>",
  "project_id": "<string>",
  "tenant_id": "<string>",
  "actor": { "type": "<user|agent|system>", "id": "<string>" },
  "created_at": "<ISO-8601 UTC>",
  "schema_version": "1"
}
```

الحقول الخاصّة بكل نوع مذكورة أدناه.

## تصنيف أحداث المجال

| نوع الحدث | متى يُصدَر | المستهلك الرئيسي |
|---|---|---|
| `dataset_uploaded` | استيعاب مجموعة في Data OS | Data OS، Data BU |
| `data_quality_scored` | حساب DRS لمصدر | Data OS، لوحات الوحدات |
| `pii_detected` | وسم PII يكتشف PII جديدة | Governance Runtime |
| `governance_check_passed` | فحص سياسة يوافق خطوة | Audit Log |
| `account_scored` | تسجيل حساب في Revenue Workspace | Revenue BU |
| `draft_generated` | إنتاج مسودة تواصل/رد | Revenue / Support |
| `approval_required` | خطوة تحتاج موافقة | Approval Matrix |
| `approval_granted` | بشر يوافق على خطوة | Audit Log |
| `proof_event_created` | التقاط دليل عائد/نتيجة | Proof Ledger |
| `report_delivered` | تقرير يُسلَّم للعميل | BU + العلامة |
| `capital_asset_created` | أصل قابل لإعادة الاستخدام في Capital Ledger | رئيس Core |
| `feature_candidate_created` | خطوة متكرّرة مرشّحة للتنميط | مجلس المنتج |
| `retainer_recommended` | تحليل CSM يوصي بعرض احتفاظ | مساحة CSM |

## أمثلة الأحداث

### 1. `account_scored`

```json
{
  "event_type": "account_scored",
  "event_id": "evt_01HV2K8Z9X",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "agent", "id": "revenue.scoring-v3" },
  "created_at": "2026-05-13T10:00:00Z",
  "schema_version": "1",
  "account_id": "ACC-443",
  "score": 87,
  "governance_status": "approved_with_review",
  "policy_id": "pol_rev_scoring_v2",
  "model_id": "claude-opus-4-7",
  "input_hash": "sha256:9a8b…"
}
```

### 2. `proof_event_created`

```json
{
  "event_type": "proof_event_created",
  "event_id": "evt_01HV3R1QPM",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "user", "id": "user_dlx_jane" },
  "created_at": "2026-05-13T12:30:00Z",
  "schema_version": "1",
  "proof_type": "roi_measured",
  "metric": "hours_saved_per_week",
  "baseline": 32,
  "current": 6,
  "value_sar": 18000,
  "evidence_ref": "proof_pack/PRJ-001/v1.pdf"
}
```

### 3. `governance_check_passed`

```json
{
  "event_type": "governance_check_passed",
  "event_id": "evt_01HV3T9NB8",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "system", "id": "governance-runtime" },
  "created_at": "2026-05-13T12:31:00Z",
  "schema_version": "1",
  "policy_id": "pol_pdpl_export_v1",
  "subject": "model_call:mcl_01HV3T9N",
  "decision": "allow",
  "redactions_applied": ["email", "phone"]
}
```

### 4. `capital_asset_created`

```json
{
  "event_type": "capital_asset_created",
  "event_id": "evt_01HV41ZK6Q",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "user", "id": "user_dlx_ops_lead" },
  "created_at": "2026-05-13T14:10:00Z",
  "schema_version": "1",
  "asset_type": "prompt_template",
  "asset_id": "asset_rev_account_score_v3",
  "asset_ref": "capital_ledger/prompt_templates/rev_account_score_v3.md",
  "reusability_tags": ["revenue", "saudi", "b2b"]
}
```

### 5. `retainer_recommended`

```json
{
  "event_type": "retainer_recommended",
  "event_id": "evt_01HV4G7RPC",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "agent", "id": "csm.retainer-radar-v1" },
  "created_at": "2026-05-13T15:45:00Z",
  "schema_version": "1",
  "retainer_readiness_score": 78,
  "recommended_tier": "monthly_revops_os",
  "rationale": "qa_score=92 proof_pack=present value_realization=4.6x"
}
```

## ضمانات التسليم

- **تسليم لمرّة واحدة على الأقل** على الناقل؛ المستهلكون مُتمكِّنون من التكرار عبر `event_id`.
- **إصدارات مخطّط**؛ يحترم المستهلكون `schema_version` ويقبلون الحقول الإضافية.
- **مراعاة PDPL**؛ الأحداث لا تحمل PII خاماً — إشارات وأشكال محذوفة فقط.
- **قابل لإعادة التشغيل** من الناقل لـ 30 يوماً على الأقل.

## الواجهات
| المدخلات | المخرجات | المالك | الإيقاع |
|---|---|---|---|
| تغيّرات الحالة عبر Core OS | أحداث المجال على الناقل | مُصدِرو كل طبقة | لحظي |
| مستهلكون مشترِكون | ردود فعل (تدقيق، أتمتة، قياس) | الوحدات المستهلكة | لحظي |
| تغييرات مخطّط الأحداث | ترقية إصدار مخطّط | رئيس Core | ربع سنوي |

## المقاييس
- **معدّل إصدار الأحداث** — حدث/ساعة لكل نوع.
- **تأخّر المستهلك p95** — ثوانٍ خلف الرأس.
- **انحراف إصدار المخطّط** — عدد المستهلكين على N-1 بعد النافذة.
- **أحداث تسرّب PII** — يجب أن تكون 0.
- **قابلية إعادة التشغيل** — % أحداث قابلة لإعادة التشغيل آخر 30 يوماً.

## ذات صلة
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — الأساس المعماري.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — موقف الموثوقية.
- `docs/ledgers/AI_RUN_LEDGER.md` — سجل التشغيل الشقيق.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — إطار الرصد.
- `docs/product/AI_RUN_PROVENANCE.md` — تصميم الأصل.
- `docs/holding/CORE_OS_ARCHITECTURE.md` — معمارية Core OS.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
