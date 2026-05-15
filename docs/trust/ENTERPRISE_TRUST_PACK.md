# Dealix Enterprise Trust Pack (v3 outline)

مستند موحّد للمبيعات Enterprise والشركاء وجولات استثمار — **ليس وعدًا قانونيًا** دون مراجعة counsel.

**مرجع Board v3:** [`../board_ready/ENTERPRISE_TRUST_PACK_V3.md`](../board_ready/ENTERPRISE_TRUST_PACK_V3.md)

---

## 1. What Dealix Does

**Governed AI operations** لبناء **قدرات أعمال** قابلة للقياس والإثبات (وليس «chatbot عام»).

## 2. What Dealix Refuses to Build

- no scraping systems  
- no cold WhatsApp automation  
- no LinkedIn automation  
- no fake proof  
- no guaranteed sales / outcome claims  
- no PII in logs  
- no source-less knowledge answers  
- no external action without explicit approval (where applicable)  

## 3. Data Handling Model

- تصنيف المصدر والعلاقة · allowed use  
- PII detection & sensitivity  
- retention policy (انظر §14)  
- audit events · سجلات تشغيل  
- حدود أمنية للبيانات (انظر §15)  

## 4. Source Passport Standard

**No Source Passport = no AI use** — تفصيل: [`../sovereignty/SOURCE_PASSPORT_STANDARD.md`](../sovereignty/SOURCE_PASSPORT_STANDARD.md) · [`../institutional_control/SOURCE_PASSPORT_STANDARD.md`](../institutional_control/SOURCE_PASSPORT_STANDARD.md)

## 5. AI Run Ledger

تتبع تشغيل النماذج والقرارات الحوكمة المرتبطة — [`../product/AI_RUN_PROVENANCE.md`](../product/AI_RUN_PROVENANCE.md)

## 6. Governance Runtime

قرارات وقت التشغيل والسياسات — [`../institutional_control/RUNTIME_GOVERNANCE.md`](../institutional_control/RUNTIME_GOVERNANCE.md) · [`../governance/GOVERNANCE_RUNTIME.md`](../governance/GOVERNANCE_RUNTIME.md)

## 7. Agent Control Plane

بطاقة الوكيل · مستويات الاستقلالية · MVP 0–3 — [`../institutional_control/AGENT_CONTROL_PLANE.md`](../institutional_control/AGENT_CONTROL_PLANE.md) · [`AI_CONTROL_PLANE.md`](AI_CONTROL_PLANE.md)

## 8. Human Oversight Model

**AI prepares. Human approves. System logs. Proof validates.**

تفصيل: [`HUMAN_OVERSIGHT_MODEL.md`](HUMAN_OVERSIGHT_MODEL.md)

## 9. Approval Workflows

مسارات الموافقة للمخرجات الحساسة والإجراءات الخارجية — [`../governance/APPROVAL_MATRIX.md`](../governance/APPROVAL_MATRIX.md) · [`../enterprise/ENTERPRISE_CONTROL_PLANE.md`](../enterprise/ENTERPRISE_CONTROL_PLANE.md)

## 10. Audit Trail

معيار الأحداث والربط بالمخرجات — [`../institutional_control/AUDIT_TRAIL_STANDARD.md`](../institutional_control/AUDIT_TRAIL_STANDARD.md)

## 11. Proof Pack Standard

هيكل الإثبات والقيود — [`../standards/PROOF_PACK_STANDARD.md`](../standards/PROOF_PACK_STANDARD.md) · **v2 (قيمة ومبيعات):** [`../proof_architecture/PROOF_PACK_V2.md`](../proof_architecture/PROOF_PACK_V2.md) · [`../proof_architecture/PROOF_SCORE.md`](../proof_architecture/PROOF_SCORE.md)

## 12. Incident Response

استجابة الحوادث وإغلاق الحلقة بقواعد/اختبارات — [`../institutional_control/INCIDENT_RESPONSE.md`](../institutional_control/INCIDENT_RESPONSE.md)

## 13. Client Responsibilities

- دقة البيانات المقدّمة من العميل  
- تصاريح الاستخدام حيث تنطبق  
- مراجعة مسودات المخرجات قبل الإطلاق الحساس  
- الامتثال لسياساته الداخلية بالتنسيق مع Dealix  

## 14. Data Retention

سياسات الاحتفاظ حسب نوع المصدر والعقد (مدة المشروع، حذف عند الطلب، إلخ) — يُفصَّل في عقود العمل وسجلات الحوكمة؛ لا PII زائدة في السجلات الدائمة.

## 15. Security Boundaries

- فصل بيئات dev/stage/prod حيث ينطبق  
- عدم تخزين أسرار في الريبو  
- وصول الأدوات والوكلاء بحد أدنى ضروري  
- مراجعة دورية لصلاحيات الوكلاء والتكاملات  

---

**بيانات وثقة:** [`DATA_TRUST_ARCHITECTURE.md`](DATA_TRUST_ARCHITECTURE.md) · **Control plane:** [`AI_CONTROL_PLANE.md`](AI_CONTROL_PLANE.md)

## Institutional & scaling depth

- طبقة الحوكمة المؤسسية: [`../institutional_control/INSTITUTIONAL_GOVERNANCE.md`](../institutional_control/INSTITUTIONAL_GOVERNANCE.md)  
- عقيدة التوسع: [`../institutional_scaling/INSTITUTIONAL_SCALING_DOCTRINE.md`](../institutional_scaling/INSTITUTIONAL_SCALING_DOCTRINE.md)  
- جاهزية المجلس: [`../board_ready/BOARD_LEVEL_THESIS.md`](../board_ready/BOARD_LEVEL_THESIS.md)  

## إشارات بحثية عامة (ليست استشارة قانونية)

- مخاوف السوق (أمن/خصوصية/امتثال): [TechRadar — KPMG](https://www.techradar.com/pro/ai-is-no-longer-a-future-concept-but-an-operational-reality-new-kpmg-report-claims-firms-are-racing-to-deploy-ai-but-need-to-ensure-they-have-the-right-security-protections)
- AudAgent — تدقيق امتثال سياسات الخصوصية للوكلاء: [arXiv:2511.07441](https://arxiv.org/abs/2511.07441)
- بيئة تنفيذ وكلاء لحماية بيانات المستخدم: [arXiv:2604.19657](https://arxiv.org/abs/2604.19657)
- بعد سنة على PDPL — عينة تجارة إلكترونية سعودية: [arXiv:2602.18616](https://arxiv.org/abs/2602.18616)
- GenAI في السعودية — تبنٍ ومخاوف: [arXiv:2601.18234](https://arxiv.org/abs/2601.18234)
- إطار حوكمة بيانات/ذكاء اصطناعي (SDAIA / NDMO) — مرجع عام: [Wikipedia — SDAIA](https://en.wikipedia.org/wiki/Saudi_Authority_for_Data_and_Artificial_Intelligence)

**صعود:** [`../investment/INVESTMENT_THESIS.md`](../investment/INVESTMENT_THESIS.md)
