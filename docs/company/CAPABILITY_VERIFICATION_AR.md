# التحقق من القدرة التشغيلية — Dealix كشركة (ليست «أفكار فقط»)

هذا الملف يجيب سؤالين: **كيف أعرف أن Dealix وصلت؟** و**كيف أثبت أنني أقدّم الخدمة بجودة وأمان وتكرار؟**  

**النظام الثماني (Master System):** [`DEALIX_MASTER_SYSTEM_AR.md`](DEALIX_MASTER_SYSTEM_AR.md).

يرتبط بـ: [نموذج التشغيل الاستراتيجي](../strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md)، [مصفوفة التنفيذ](../DEALIX_MASTER_EXECUTION_MATRIX.md)، [جدول الأدلة](../DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md)، [مقاييس North Star](../commercial/NORTH_STAR_METRICS_AR.md)، و[خريطة الكود التجارية ↔ الريبو](../commercial/CODE_MAP_OS_TO_MODULES_AR.md).

---

## 1) السبع «اختبارات» — تعريف قابل للقياس في المستودع

| الاختبار | معنى تشغيلي | مؤشرات / أدوات في الريبو |
|-----------|-------------|---------------------------|
| **السوق** | دفع + تكرار + توسع | حقول CRM يدوية أو لاحقاً دفتر إيراد؛ مرجع المقاييس: [NORTH_STAR_METRICS_AR.md](../commercial/NORTH_STAR_METRICS_AR.md) |
| **المنتج** | كل خدمة لها أصول تسليم | `Service Readiness Score` — [`delivery_os/service_readiness.py`](../../auto_client_acquisition/delivery_os/service_readiness.py) + `GET /api/v1/commercial/service-readiness/{service_id}` |
| **التكرار** | نفس الجودة لعميلين | جلسات خدمة + قوائم تحقق: [`service_sessions`](../../api/routers/service_sessions.py)، [`delivery_os/framework.py`](../../auto_client_acquisition/delivery_os/framework.py) |
| **الأثر** | قياس قبل/بعد | تقارير Sprint JSON: [`commercial_engagements`](../../auto_client_acquisition/commercial_engagements/) |
| **الحوكمة** | مسودات + موافقة + تدقيق | [`governance_os`](../../auto_client_acquisition/governance_os/)، [`GET /api/v1/governance/risk-dashboard`](../../api/routers/governance_risk_dashboard.py) |
| **البيانات** | جاهزية قبل AI | [`data_os`](../../auto_client_acquisition/data_os/)، بوابة `ai` في `POST /api/v1/commercial/readiness-gates/check` |
| **الفريق** | قالب → قائمة → أداة | نفس أصول التسليم + وثائق `docs/commercial/templates/` |

---

## 2) نموذج النضج L0–L5 — ربط بالريبو

| المستوى | تعريف مختصر | علامات في المستودع |
|---------|---------------|---------------------|
| **L0** | فكرة / كلام | لا runners، لا قوالب مربوطة |
| **L1** | خدمات مصنّفة | عروض + وثائق + `delivery_catalog` + Sprint API |
| **L2** | تسليم متكرر | `service_sessions` + JSONL + انتقالات موافقة |
| **L3** | منصة تساعد التسليم | import/جودة، مسودات، لوحات read-only |
| **L4** | آلة ريتينر | تقارير شهرية + لوحة صحة عميل (لاحقاً DB كامل) |
| **L5** | Enterprise AI OS | multi-tenant، RBAC، تكاملات — خارج نطاق MVP الحالي |

---

## 3) نظام التحقق (Verification System) — ثلاث طبقات

### أ) وثائق + أدلة بشرية

- تحديث [EVIDENCE_TABLE](../DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md) عند كل عميل مدفوع (حتى لو صف واحد في الجدول).

### ب) بوابات حتمية (Gates) — قبل البيع أو قبل «تشغيل AI»

- **Delivery gate**: ثمانية أسئلة كحقول boolean في `POST /api/v1/commercial/readiness-gates/check` مع `"gate": "delivery"`.
- **AI gate**: محاور + مصادر بيانات + `lawful_basis` + (اختياري) عينة صفوف لجودة الجدول.
- **Production gate**: قائمة تقنية (اختبارات، logging، audit، schema، …) — تُعبّأ يدوياً أو من CI لاحقاً.

التنفيذ: [`delivery_os/readiness_gates.py`](../../auto_client_acquisition/delivery_os/readiness_gates.py).

### ج) لوحة المؤسس الأسبوعية

- `GET /api/v1/founder/operating-scorecard` — تجميع read-only (مخاطر + جلسات + placeholders مالية).

### د) CI

- `bash scripts/dealix_capability_verify.sh` — يشغّل pytest على بوابات الجاهزية ودرجة الخدمة.

---

## 4) قاعدة البيع

- **لا تُباع رسمياً** أي خدمة بدرجة جاهزية `< 80` حسب `Service Readiness Score` إلا كـ beta مع توثيق المخاطر (قرار مؤسس).

---

## 5) المراجع الخارجية (اتجاه سوق — لا تُنسَخ كأهداف Dealix)

- McKinsey — The State of AI (انتشار مقابل أثر EBIT):  
  https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai  
- PDPL — أسس معالجة قانونية:  
  https://istitlaa.ncc.gov.sa/en/Transportation/NDMO/IMPLEMENTINGPDPL/Pages/Article_003.aspx  
- Gartner — مخاطر بيانات غير جاهزة لمشاريع AI:  
  https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk  
- SPA — حجم السجلات التجارية (سياق سوق):  
  https://www.spa.gov.sa/en/N2484191  
