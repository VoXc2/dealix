# العربية

# خريطة التحويل ٣٠–٦٠–٩٠ يوماً — الطبقة ١١

**المالك:** قائد التحويل في Dealix بالاشتراك مع راعي العميل التنفيذي.

## الغرض

هذه الخريطة تقسّم التحويل إلى مراحل قابلة للبيع والتنفيذ. تطابق مسار البيع: التدقيق ثم التجربة ثم التحويل ثم العقد الدوري، وتتوافق مع `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` و`dealix/registers/90_day_execution.yaml`. كل الأرقام أهداف وفرضيات، لا ضمانات.

## الأيام ٠–٣٠ — التدقيق وخريطة التحويل

**الهدف:** إنتاج خريطة تحويل قابلة للتنفيذ ودرجة نضج.

- تشغيل نموذج النضج (`transformation/maturity_model.md`) وإنتاج درجة ٠–١٠٠.
- تسمية الأدوار الأربعة عبر `auto_client_acquisition/adoption_os/client_roles.py`.
- رسم خريطة الحالة الراهنة وتسجيل الاحتكاك عبر `auto_client_acquisition/adoption_os/friction_log.py`.
- تحديد ٣–٥ حالات استخدام وربط كل منها بفرضية عائد.
- تسليم حالة عمل أولية ومستند موافقة تنفيذية.

**بوّابة الخروج:** راعٍ مسمّى + خريطة تحويل + درجة نضج. يطابق رتبة التدقيق في `docs/COMPANY_SERVICE_LADDER.md`.

## الأيام ٣١–٦٠ — التجربة وإثبات حالة استخدام

**الهدف:** إثبات حالة استخدام واحدة بأدلة.

- اختيار حالة الاستخدام الأعلى أولوية من الخريطة.
- إعادة تصميم سير عملها عبر `transformation/workflow_redesign_framework.md`.
- تشغيل أول جلسة تبنّي عبر `auto_client_acquisition/adoption_os/training_products.py`.
- تسجيل القيمة المُلاحَظة في `auto_client_acquisition/value_os/value_ledger.py`.
- إنتاج أول تقرير قيمة عبر `auto_client_acquisition/value_os/monthly_report.py`.

**بوّابة الخروج:** قيمة مُلاحَظة + درجة تبنّي أولية. يطابق رتبة التجربة في سُلَّم الخدمات.

## الأيام ٦١–٩٠ — التحويل وتوسيع الانتشار

**الهدف:** نشر سير العمل المُعاد تصميمه عبر فرق متعددة.

- إعادة تصميم بقية حالات الاستخدام ذات الأولوية.
- التقدّم عبر مراحل الانتشار في `auto_client_acquisition/enterprise_rollout_os/rollout_stage.py`.
- اجتياز بوّابات الانتقال في `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py`.
- مراجعة درجة التبنّي عبر `auto_client_acquisition/adoption_os/adoption_score.py`.
- تقييم الجاهزية للعقد الدوري عبر `auto_client_acquisition/adoption_os/retainer_readiness.py`.

**بوّابة الخروج:** قيمة مُتحقَّقة + اجتياز فحص جاهزية العقد الدوري. يفتح رتبة العقد الدوري.

## ما بعد اليوم ٩٠ — العقد الدوري

طبقة تشغيل شهرية: مراجعة تبنّي، تقرير قيمة مؤكَّد، وتدريب المستخدمين الجدد بإيقاع متكرر.

## القاعدة غير القابلة للتفاوض

كل أهداف الخريطة فرضيات مبنية على إشارات العميل. لا تُربط أي مرحلة بعائد مضمون أو رقم مبيعات.

القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

# 30-60-90 Day Transformation Roadmap — Layer 11

**Owner:** Dealix Transformation Lead, jointly with the client Executive Sponsor.

## Purpose

This roadmap splits the transformation into sellable, executable phases. It maps to the sales path — Audit, then Pilot, then Transformation, then Retainer — and aligns with `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` and `dealix/registers/90_day_execution.yaml`. All numbers are goals and hypotheses, not guarantees.

## Days 0-30 — Audit and transformation map

**Goal:** Produce an executable transformation map and a maturity score.

- Run the maturity model (`transformation/maturity_model.md`) and produce a 0-100 score.
- Name the four roles through `auto_client_acquisition/adoption_os/client_roles.py`.
- Map the current state and log friction through `auto_client_acquisition/adoption_os/friction_log.py`.
- Identify 3-5 use cases and tie each to an ROI hypothesis.
- Deliver an initial business case and an executive buy-in document.

**Exit gate:** Named sponsor + transformation map + maturity score. Matches the Audit rung in `docs/COMPANY_SERVICE_LADDER.md`.

## Days 31-60 — Pilot and prove one use case

**Goal:** Prove a single use case with evidence.

- Select the highest-priority use case from the map.
- Redesign its workflow through `transformation/workflow_redesign_framework.md`.
- Run the first adoption session through `auto_client_acquisition/adoption_os/training_products.py`.
- Record observed value in `auto_client_acquisition/value_os/value_ledger.py`.
- Produce the first value report through `auto_client_acquisition/value_os/monthly_report.py`.

**Exit gate:** Observed value + initial adoption score. Matches the Pilot rung in the service ladder.

## Days 61-90 — Transformation and rollout expansion

**Goal:** Roll out the redesigned workflow across multiple teams.

- Redesign the remaining priority use cases.
- Advance through the rollout stages in `auto_client_acquisition/enterprise_rollout_os/rollout_stage.py`.
- Pass the transition gates in `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py`.
- Review the adoption score through `auto_client_acquisition/adoption_os/adoption_score.py`.
- Assess retainer readiness through `auto_client_acquisition/adoption_os/retainer_readiness.py`.

**Exit gate:** Verified value + retainer readiness check passed. Opens the Retainer rung.

## After Day 90 — Retainer

A monthly operating layer: adoption review, a client-confirmed value report, and new-user training on a repeating cadence.

## Non-negotiable

Every roadmap goal is a hypothesis built on client signals. No phase is tied to a guaranteed return or a sales number.

Estimated value is not Verified value.
