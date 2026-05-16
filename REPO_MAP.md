# 🗺️ REPO MAP — خريطة الكود الصادقة

> خريطة صادقة لما هو **حقيقي** في هذا الريبو مقابل ما هو **تصميم لم يُنفَّذ بعد**.
> مكمّلة لـ[`NORTH_STAR.md`](NORTH_STAR.md) — تُنفّذ «وسم الحقيقي مقابل الـstub» توثيقياً.
> آخر مراجعة: 2026-05-16. مبنية على تدقيق شامل للكود.

**سُلّم الحالة:**
- **Production** — مبني، مُختبَر، يعمل افتراضياً.
- **MVP** — يعمل لكن غير مكتمل؛ أساس قائم، تغطية جزئية.
- **Stub** — هيكل/توقيع موجود، التنفيذ بيانات وهمية أو فارغ.
- **Aspirational** — موصوف معمارياً، التنفيذ أقل بكثير من التصميم.

---

## 1. تصنيف الموديولات الرئيسية

| الموديول / الطبقة | الحالة الصادقة | ملاحظة |
|--------------------|----------------|--------|
| `api/` — 138 راوتر · ~787 endpoint | **Production** | FastAPI: CORS، middleware، request IDs، audit. نقطة الدخول `api/main.py`. |
| `db/` — ORM + 14 migration | **Production** | SQLAlchemy 2.0 async · `db/models.py` (~1,034 سطر) · Alembic head واحد. |
| `integrations/pdpl.py` · `integrations/zatca.py` | **Production** | PDPL (~443 سطر) · ZATCA Phase 2 (~659 سطر). |
| `tests/` — 442 ملف اختبار | **Production** | pytest + asyncio · بوابة تغطية CI 70%. |
| `.github/workflows/` — 23 workflow | **Production** | CI، Docker، نشر Railway، CodeQL، pre-commit. |
| Lead Engine — `auto_client_acquisition/agents/` (intake, icp_matcher, pain_extractor, qualification) + `pipeline.py` | **Production** | مُغطّى بـno-overclaim كـProduction. |
| `core/llm/` — توجيه LLM | **Production** | تعدد المزوّدين مع fallback (`core/llm/router.py`). |
| `dealix/contracts/` — DecisionOutput, evidence_pack | **MVP** | العقد موجود، غير مربوط على كل مخرجات الوكلاء. |
| `dealix/trust/` — policy, approval, audit, tool_verification | **MVP** | منطق قائم لكن in-memory فقط؛ لا persistence. |
| AI orchestration / autonomy عبر الوكلاء | **MVP** | الأساس قائم، الاستقلالية الكاملة عبر الموديولات غير مكتملة. |
| تحويل الخدمات لمنتجات (الرتب 1–5) | **MVP** | الراوترات موجودة، التسليمات ليست كلها GA. |
| `auto_client_acquisition/` — 174 موديول «OS» | **Aspirational** | استعارة «نظام تشغيل» موصوفة معمارياً؛ كثير منها 1–5 ملفات أو stubs. |
| `frontend/` — Next.js 14 | **MVP** | لوحة + هبوط؛ تتطلب `NEXT_PUBLIC_API_URL`. |

> القاعدة العامة من التدقيق: **الواجهة الخلفية، قاعدة البيانات، الامتثال، الاختبارات،
> CI/CD، ومحرّك العملاء المحتملين = Production متين.** «نظام التشغيل الذاتي بـ174 موديول»
> = تصميم يفوق التنفيذ.

---

## 2. المسار الحرج للإيراد (Revenue-Critical Path)

هذه فقط هي الموديولات والـendpoints التي تخدم سلّم العروض فعلياً. **كل ما عداها خارج
المسار الحرج** — لا يُطوَّر قبل عبور البوابة 0 (انظر `NORTH_STAR.md §4`).

**Endpoints على المسار الحرج (~14):**
- `GET /health` · `GET /healthz`
- `POST /api/v1/leads` — استقبال العملاء المحوكَم
- `GET /api/v1/pricing/plans`
- `POST /api/v1/checkout` — الدفع عبر Moyasar *(محجوب: account_inactive_error)*
- `POST /api/v1/webhooks/moyasar`
- `POST /api/v1/public/demo-request` · `POST /api/v1/public/partner-application`
- `GET /api/v1/decision-passport/golden-chain` · `/evidence-levels`
- `GET /api/v1/revenue-os/catalog` · `POST /signals/normalize` · `POST /anti-waste/check`
- `/api/v1/compliance/*`

**موديولات على المسار الحرج:**
`api/main.py` + الراوترات أعلاه · `auto_client_acquisition/agents/{intake,icp_matcher,pain_extractor,qualification}` ·
`auto_client_acquisition/pipeline.py` · `core/llm/router.py` · `db/` · `integrations/{pdpl,zatca}.py` +
عميل الدفع Moyasar · `dealix/registers/{no_overclaim,compliance_saudi}.yaml`.

---

## 3. نقاط الدخول والتشغيل

- **نقطة الدخول:** `api/main.py` — `uvicorn api.main:app`.
- **تفاصيل التشغيل والاختبار الكاملة:** انظر [`AGENTS.md`](AGENTS.md) — لا تُكرَّر هنا.
- **حزمة الانحدار السريعة (quick regression):** معرّفة في `AGENTS.md`.
- **التشغيل المحلي:** `QUICK_START.md`.

---

## 4. جرد الـStubs و TODOs

من التدقيق: ~21 TODO · ~12 stub — **كلها مقصودة وموثّقة، ليست أعطالاً.**

| الموقع | النوع | ملاحظة |
|--------|-------|--------|
| `auto_client_acquisition/orchestrator/tools.py` | 8 stubs | `_stub_discover/_signal/_enrich/_compliance/_personalize/_send/_classify/_brief` — مشغّلات مهام placeholder. |
| `auto_client_acquisition/intelligence/dealix_model_router.py` | stub | `_attempt_cloud_call_stub()`. |
| `auto_client_acquisition/v3/compliance_os.py` | stub | `ropa_stub()`. |
| `auto_client_acquisition/observability_adapters/base.py` | NotImplementedError | فئة أساس مجرّدة (بالتصميم). |
| `auto_client_acquisition/designops/exporter.py` | NotImplementedError | تصدير PDF/PPTX غير منفَّذ (موثّق). |
| `api/routers/{auth,customer_webhooks,customer_success,pricing}.py` | TODOs إنتاجية | منخفضة الأولوية، موثّقة، ليست محجِّبات. |

> أي stub يُكمَل **فقط** عند حاجة عميل دافع فعلية له (انظر عقيدة مكافحة التضخّم،
> `NORTH_STAR.md §7`). وإلا يبقى موسوماً بوضوح.
