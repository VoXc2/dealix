# Readiness Scoring System — Revenue OS

## طريقة الحساب

الدرجة النهائية من 100 موزعة على 5 محاور:

1. Operational Reliability (25)
2. Governance & Control (25)
3. Tenant & Data Isolation (20)
4. Business Impact (20)
5. Delivery Repeatability (10)

النتيجة النهائية = مجموع المحاور بعد تطبيق بوابات الإيقاف (Hard Stops).

## المحاور بالتفصيل

### 1) Operational Reliability (25)

- Workflow success rate (10)
- Retry recovery success (5)
- Mean time to resolution للحالات الفاشلة (5)
- Rollback drill readiness (5)

### 2) Governance & Control (25)

- Approval enforcement rate (10)
- Policy check coverage (5)
- Audit log completeness (5)
- Action risk classification coverage (5)

### 3) Tenant & Data Isolation (20)

- `tenant_id` propagation coverage (10)
- Permission-aware retrieval compliance (5)
- Cross-tenant leak incidents (5, عكسي: أي حادث = صفر)

### 4) Business Impact (20)

- Lead qualification SLA improvement (5)
- Response-time reduction (5)
- Conversion lift to next sales stage (5)
- ROI evidence quality (5)

### 5) Delivery Repeatability (10)

- Discovery + onboarding completion quality (4)
- QA + monthly review discipline (3)
- Playbook adherence across clients (3)

## Hard Stops (بوابات إيقاف)

إذا تحقق أي بند، تعتبر النتيجة "غير جاهز" مهما كانت الدرجة:

1. Action خارجي عالي المخاطر بدون موافقة.
2. Cross-tenant data exposure.
3. Missing audit trail لخطوة تنفيذ.
4. Failure to produce monthly ROI report.

## تصنيف الجاهزية

- 90-100: Enterprise-Ready Pilot
- 75-89: Controlled Production Pilot
- 60-74: Managed Beta
- أقل من 60: Prototype / Not Operationally Embedded

## دورة التقييم

- يومي: Operational + governance checks.
- أسبوعي: Eval report + incident review.
- شهري: ROI + readiness score + action plan.
