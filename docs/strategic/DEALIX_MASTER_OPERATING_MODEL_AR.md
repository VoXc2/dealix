# Dealix — نموذج التشغيل التجاري الأعظم (مرجع استراتيجي)

هذا المستند يثبت **كيف تفكر Dealix كشركة تشغيل نمو** وليس كمجموعة endpoints.  
المعادلة المرجعية:

```text
Dealix = ذكاء الإيرادات + تنفيذ تشغيلي + محرك إثبات + نجاح عميل + طبقة ثقة + حلقة تعلّم
```

مرجع CEO/Board التنفيذي المختصر (positioning + gates + state machine):
[`GOVERNED_REVENUE_AI_OPS_EXECUTION_AR.md`](GOVERNED_REVENUE_AI_OPS_EXECUTION_AR.md)

## السلسلة الذهبية

```text
إشارة → Lead → Decision Passport → إجراء معتمد → تسليم → Proof → توسعة → تعلّم
```

**قاعدة المنتج:** بدون Decision Passport لا يُنفَّذ إجراء خارجي (الحوكمة في Trust Plane + Approval Center).

واجهات API ثابتة (السلسلة الذهبية):

- `GET /api/v1/decision-passport/golden-chain`
- `GET /api/v1/decision-passport/evidence-levels`
- `GET /api/v1/revenue-os/catalog` — سجل المصادر + waterfall + كتالوج الإجراءات + مراجع الوحدات
- `POST /api/v1/revenue-os/signals/normalize` — تحويل `MarketSignal` القادمة من المؤسس/عملية بحث إلى هيكل Why Now / Offer / Proof
- `POST /api/v1/revenue-os/dedupe/hint`, `POST …/expansion/next-offer`, `POST …/anti-waste/check`
- `GET /api/v1/revenue-os/learning/weekly-template` — هيكل تقرير التعلّم الأسبوعي
- `GET /api/v1/revenue-os/scores/pricing-power-demo` — مثال تسويق داخلي للدرجة فقط
- كل استجابة `POST /api/v1/leads` تتضمن `decision_passport` و `customer_readiness`.

التحقق السريع: `bash scripts/revenue_os_master_verify.sh` — يطبع `DEALIX_REVENUE_OS_VERDICT` وملخص فروع المعمارية.

## الثمانية المحركات ↔ الكود (خريطة تنفيذ)

| المحرك | مسارات / وحدات في الريبو |
|--------|---------------------------|
| **1 — Market Radar** | إشارات آمنة: `growth_beast/market_radar.py` (بدون HTTP داخل الوحدة). التطبيع إلى Why Now / Offer / Proof: `revenue_os/signal_normalizer.py`. كاشف الشراء من المحتوى: `intelligence/signals.py`. |
| **2 — Lead Intelligence** | مسارات الليدز + مس prospect؛ السجلُّ المصدر والسياسات: `revenue_os/source_registry.py`. Waterfall الإثراء: `revenue_os/enrichment_waterfall.py`. Dedupe: `revenue_os/dedupe.py`. |
| **3 — Decision Engine** | **Decision Passport** `decision_passport/` + ICP/BANT في الوكلاء. لوحة درجات في جواز القرار (`scores`). |
| **4 — Action & Approval** | كتالوج أنماط الإجراء: `revenue_os/action_catalog.py` (افتراضي draft_only / approval_required). تنفيذ فعلي: `approval_center`, `tool_guardrail_gateway`, `channel_policy_gateway`. |
| **5 — Delivery OS** | `delivery_os`, `delivery_factory`, **`service_sessions`** — كل خدمة = جلسة بمهام وdeadlines (استمر بالتماسك مع الـ Portal). |
| **6 — Customer Portal** | `customer_company_portal`, `customer_loop`, Next.js؛ فارغات مقروءة بالعربية (لم يبدأ بعد / سيظهر Proof بعد الإجراء المعتمد). |
| **7 — Proof & Expansion** | سجل الأحداث: `proof_ledger/ProofEvent`. شكل منتج غني للأحداث داخل `payload`: **`revenue_os/proof_canonical.py`**. مستويات L0–L5: `proof_engine/evidence.py`. التوسعة: `revenue_os/expansion_engine.py` (** gated بدون proof **). |
| **8 — Learning Flywheel** | هيكل تقرير أسبوعي: `revenue_os/learning_weekly.py` + تقارير أخرى (`growth_beast/weekly_learning.py`, `self_improvement_os`). |

### لماذا Workflow وليس «ذكاء عام»؟

الاتجاه الاستراتيجي (McKinsey/BCG — ملخص عملي): عائد قوي من AI يأتي من **تركيز على workflows قليلة عالية الأثر + حوكمة + بيانات موثوقة + إثبات نتائج**، وليس من نشر نماذج عامة في كل الإدارات. Dealix يطبّق ذلك عبر السلسلة الذهبية وقياس Proof.

### Tier-1 Lead Machine — ما الذي صار في الكود؟

- **Source Registry**: كل مصدر مع `allowed_use`, `risk_level`, موافقة، تخزين، اتصال، احتفاظ (`Tier1LeadSource` + `SourcePolicy`).
- **محظورات ثابتة**: مصادر في قائمة `forbidden_sources()` — لا معالجة إنتاجية لـ cold WhatsApp / scraping / قوائم مشتراة / أتمتة LinkedIn.
- **Enrichment waterfall**: ترتيب مراحل موحّد + كائن `FactFieldProvenance` لكل حقيقة (مصدر، ثقة، `allowed_use`).
- **Dedupe**: بصمة اقتراحية + تطبيع اسم/نطاق/هاتف — القرار النهائي عند التخزين.
- **Anti-Waste**: `validate_pipeline_step` — لا إجراء خارجي بدون جواز قرار؛ لا upsell بدون Proof؛ لا تسويق عام تحت L4.

### Proof Event «شكل المنتج» مقابل السجل الحالي

- السجل الحالي `ProofEvent` في `proof_ledger/schemas.py` يلبي التخزين والمراجعة.
- الحقول التفصيلية التي يصفها الـ Portal (metric قبل/بعد، `evidence_level`, موافقة نشر…) تُنقل ضمن **`ProofEvent.payload`** عبر **`ProofEventCanonical`** لتجنّب كسر التوافق.

## مستويات أدلة الـ Proof (L0–L5)

مُعرَّفة في `auto_client_acquisition/proof_engine/evidence.py` وواجهة `GET .../evidence-levels`.

- L0/L1: لا تسويق خارجي  
- L2–L3: خاص / مبيعات  
- L4: نشر عام بموافقة  
- L5: توسعة إيراد بعد التزام  

الدالة `assert_public_proof_allowed` تمنع النشر دون L4 + موافقة صريحة.

## Customer Comfort & Expansion Readiness

`customer_readiness/scores.py` — **Comfort** و **Expansion Readiness** (0–100)، مع **`compute_pricing_power_score`** كسيّارة بديهية للقوة التسعيرية بعد Proof (لا تُستخدم منفردة بدون هامش وProof حقيقي).

## مبدأ بناء المنتج

لا تُضاف ميزة إلا إذا تخدم السلسلة الذهبية أو تقياسًا تشغيليًا (تحويل، تسليم، إثبات، احتفاظ).

## مراجع داخلية

- [commercial/DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) — حزم Revenue Operations + AI Implementation (تسعير، نطاق، ربط بالكود)
- [ops/DAILY_COMMERCIAL_LOOP_AR.md](../ops/DAILY_COMMERCIAL_LOOP_AR.md) — حلقة يومية/أسبوعية: إكمال، بوابات، scorecard
- `docs/v10/DEALIX_CAPABILITY_GAP_MAP.md` — فجوات قدرات
- `AGENTS.md` — تشغيل الوكلاء السحابيين
- `dealix/registers/no_overclaim.yaml` — سجل عدم المبالغة
- `docs/strategic/ENTERPRISE_OFFER_POSITIONING_AR.md` — طبقات العرض A/B/C للشركات
- `docs/strategic/ENTERPRISE_PILOT_TEMPLATE_AR.md` — قالب Pilot enterprise
- `docs/strategic/ENTERPRISE_P0_GAP_BACKLOG_AR.md` — أولويات P0 وربط checklist الإصدار
- `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md` — حزمة ثقة وامتثال للبيع
- `docs/strategic/CUSTOMER_SUCCESS_PLAYBOOK_HOOKS_AR.md` — ربط محفزات CS بـ customer_readiness
- `docs/strategic/DEALIX_ROLE_SERVICE_LADDER_AR.md` — سلّم الأدوار ↔ كتالوج الخدمات السبع
- `docs/strategic/DEALIX_MARKET_DIFFERENTIATION_AR.md` — تمييز مقابل أنماط السوق
- `docs/strategic/WAVE13_LANDING_PORTAL_ALIGNMENT_AR.md` — محاذاة البوابة مع Wave 13
- `docs/strategic/CEO_OPERATING_METRICS_AR.md` — مؤشرات تشغيل تنفيذي داخلية
- `docs/strategic/GTM_PLAYBOOK_SERVICE_LADDER_AR.md` — كتاب تشغيل GTM على سلّم الخدمات
- `docs/ops/PHASE0_CEO_RELEASE_GATE_AR.md` — بوابة دمج وتحقق قبل التوسع
- `docs/ops/PDPL_CLOSURE_CHECKLIST_AR.md` — قائمة إغلاق فجوات PDPL
- `docs/ops/ALEMBIC_MIGRATION_POLICY.md` — سياسة ترحيل قاعدة البيانات
- `docs/strategic/CEO_ROADMAP_IMPLEMENTATION_INDEX_AR.md` — فهرس ربط خطة CEO بالكود والاختبارات

### Trust Layer (PDPL / ZATCA) — تذكير عدم المبالغة

- PDPL: موافقة واضحة، غرض المعالجة، تقليل البيانات، سجل موافقات نشر Proof — لا ادِّعاء امتثال كامل بدون مراجعة قانونية.
- ZATCA Phase 2: جاهزية workflow وحالة الفاتورة وحقول ضريبة — **لا** عبارة «معتمد ZATCA» إلا بعد تحقق رسمي (`dealix/registers/no_overclaim.yaml`).

### ما الذي لا يزال خارج النطاق (يتطلب أذونات / وقت منتج)

- Temporal أو بدائل workflows طويلة للـ 7-Day Sprint بالكامل.
- تكاملات OAuth حقيقية (Sheets/CRM) كطبقة افتراضية فقط إلى أن توجد أسرار.
- tenant isolation كامل على كل الموارد + مجموعات اختبارات OWASP API المذكورة في خطتك (تابعة مهمة مستقلّة).

---

*آخر تحديث: يتزامن مع طبقة `revenue_os/` + كتالوج API `/api/v1/revenue-os/*`.*
