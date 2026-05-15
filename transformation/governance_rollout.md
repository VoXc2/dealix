# العربية

# حوكمة الانتشار — الطبقة ١١

**المالك:** قائد التحويل في Dealix بالاشتراك مع مالك الموافقات لدى العميل.

## الغرض

حوكمة الانتشار تضمن أن كل تحويل يتقدّم بانضباط: لا مرحلة تبدأ قبل اجتياز معاييرها، ولا حالة استخدام تُنشر بدون حدود قرار واضحة. الحوكمة هنا ليست عائقاً بل آلية تجعل التوسّع آمناً وقابلاً للتدقيق.

## بوّابات الانتشار

تُدار البوّابات عبر `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py`، وكل بوّابة تفرض معياراً صريحاً قبل الانتقال:

| البوّابة | المعيار | المصدر |
|---|---|---|
| الراعي | راعٍ تنفيذي مسمّى | `client_roles.py` |
| البيانات | مصادر بيانات معروفة وموحّدة | تدقيق الجاهزية |
| سير العمل | مالك سير عمل + حدود قرار | `workflow_redesign_framework.md` |
| الحوكمة | مالك موافقات + مسار موافقة | `adoption_gates.py` |
| الأدلة | قيمة مُسجَّلة في سجل القيمة | `value_os/value_ledger.py` |
| التبنّي | درجة تبنّي ≥ العتبة | `adoption_os/adoption_score.py` |
| العقد الدوري | اجتياز فحص الجاهزية | `adoption_os/retainer_readiness.py` |

## مراحل الانتشار

تطابق `auto_client_acquisition/enterprise_rollout_os/rollout_stage.py`: الإنزال، الإثبات، التبنّي، التشغيل، التوسّع، التوحيد، الترسيخ المؤسسي. تُتابَع الحالة عبر `auto_client_acquisition/enterprise_rollout_os/rollout_dashboard.py`.

## إدارة المخاطر

تُسجَّل مخاطر الانتشار عبر `auto_client_acquisition/enterprise_rollout_os/enterprise_risk.py`. كل مرحلة تحمل سجلّ مخاطر يُراجَع قبل البوّابة التالية. سحب التوسّع يُقاس عبر `auto_client_acquisition/enterprise_rollout_os/platform_pull.py`.

## قواعد الحوكمة غير القابلة للتفاوض

- لا تُتجاوز بوّابة بدون اكتمال معيارها الموثّق.
- الإرسال التلقائي للرسائل الخارجية محظور؛ كل إجراء خارجي يمرّ بموافقة بشرية صريحة.
- لا كشط ولا تواصل بارد مؤتمت في أي مرحلة.
- لا يُذكر اسم عميل علناً بدون إذن موقّع.
- لا تُربط أي حالة استخدام بعائد مضمون — فقط بفرضية عائد بأدلة.

## ربط الحوكمة بمسار البيع

تُفعَّل الحوكمة من **التدقيق** (تحديد البوّابات) إلى **العقد الدوري** (مراجعة مستمرة). يطابق هذا سُلَّم الخدمات في `docs/COMPANY_SERVICE_LADDER.md`.

القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

# Governance Rollout — Layer 11

**Owner:** Dealix Transformation Lead, jointly with the client Approval Owner.

## Purpose

Governance rollout ensures every transformation advances with discipline: no stage begins before its criteria are met, and no use case ships without clear decision boundaries. Governance here is not an obstacle; it is the mechanism that makes scaling safe and auditable.

## Rollout gates

Gates are run through `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py`, and each gate enforces an explicit criterion before transition:

| Gate | Criterion | Source |
|---|---|---|
| Sponsor | Named executive sponsor | `client_roles.py` |
| Data | Data sources known and unified | Readiness audit |
| Workflow | Workflow owner + decision boundaries | `workflow_redesign_framework.md` |
| Governance | Approval owner + approval path | `adoption_gates.py` |
| Proof | Value recorded in the value ledger | `value_os/value_ledger.py` |
| Adoption | Adoption score >= threshold | `adoption_os/adoption_score.py` |
| Retainer | Readiness check passed | `adoption_os/retainer_readiness.py` |

## Rollout stages

Matches `auto_client_acquisition/enterprise_rollout_os/rollout_stage.py`: land, prove, adopt, operate, expand, standardize, institutionalize. Status is tracked through `auto_client_acquisition/enterprise_rollout_os/rollout_dashboard.py`.

## Risk management

Rollout risks are recorded through `auto_client_acquisition/enterprise_rollout_os/enterprise_risk.py`. Every stage carries a risk register reviewed before the next gate. Expansion pull is measured through `auto_client_acquisition/enterprise_rollout_os/platform_pull.py`.

## Non-negotiable governance rules

- No gate is bypassed without its documented criterion complete.
- Auto-send of external messages is blocked; every external action passes explicit human approval.
- No scraping and no automated cold outreach at any stage.
- No client name is mentioned publicly without signed permission.
- No use case is tied to a guaranteed return — only to an evidence-backed ROI hypothesis.

## Mapping governance to the sales path

Governance activates from the **Audit** (defining the gates) to the **Retainer** (continuous review). This mirrors the service ladder in `docs/COMPANY_SERVICE_LADDER.md`.

Estimated value is not Verified value.
