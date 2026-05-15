# العربية

Owner: قائد التحول (Transformation Lead)

## درجة الطبقة

طبقة التحول (Layer 11): **70 من 100 — نطاق تجربة داخلية**.

## قائمة التحقق المكوّنة من ثمانية أجزاء

| الجزء | الحالة | الدليل (كود حقيقي) |
|---|---|---|
| معمارية | متوفر | `auto_client_acquisition/enterprise_rollout_os/`، `auto_client_acquisition/vertical_os/` |
| جاهزية | متوفر | هذه الوثيقة |
| اختبارات | متوفر | `readiness/transformation/tests.md` |
| مراقبة | متوفر | `auto_client_acquisition/enterprise_rollout_os/rollout_dashboard.py` |
| حوكمة | متوفر | `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py`، `enterprise_risk.py` |
| تراجع | جزئي | `auto_client_acquisition/enterprise_rollout_os/rollout_stage.py` (مراحل الطرح؛ تمرين التراجع غير موثَّق دورياً) |
| مقاييس | متوفر | `readiness/transformation/scorecard.yaml` |
| مالك | متوفر | قائد التحول |

## الفجوات المحددة

- **النطاق الأدنى بين الطبقات (70):** الطبقة في نطاق تجربة داخلية لأن بوابات التبني في `adoption_gates.py` مُحدَّدة لكن لم تُختبَر على وتيرة متحقَّقة عبر طرح حقيقي.
- **تمرين تراجع الطرح:** مراحل الطرح قائمة في `rollout_stage.py`، لكن تمريناً متحقَّقاً يثبت العودة إلى مرحلة سابقة غير مُسجَّل.
- **نموذج النضج:** خرائط الأدوار في `role_map.py` تحتاج ربطاً بأدلة تبني مُسجَّلة، لا تقديرات.

## روابط ذات صلة

- `readiness/transformation/tests.md`
- `readiness/transformation/scorecard.yaml`
- `readiness/cross_layer/rollback_drill.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Transformation Lead

## Layer score

Transformation layer (Layer 11): **70 out of 100 — internal beta band**.

## The 8-part checklist

| Part | Status | Evidence (real code) |
|---|---|---|
| architecture | present | `auto_client_acquisition/enterprise_rollout_os/`, `auto_client_acquisition/vertical_os/` |
| readiness | present | this document |
| tests | present | `readiness/transformation/tests.md` |
| observability | present | `auto_client_acquisition/enterprise_rollout_os/rollout_dashboard.py` |
| governance | present | `auto_client_acquisition/enterprise_rollout_os/adoption_gates.py`, `enterprise_risk.py` |
| rollback | partial | `auto_client_acquisition/enterprise_rollout_os/rollout_stage.py` (rollout stages; the rollback drill is not documented periodically) |
| metrics | present | `readiness/transformation/scorecard.yaml` |
| owner | present | Transformation Lead |

## Specific gaps

- **Lowest band across layers (70):** the layer sits in the internal-beta band because the adoption gates in `adoption_gates.py` are specified but not tested on a verified cadence across a real rollout.
- **Rollout rollback drill:** rollout stages exist in `rollout_stage.py`, but a verified drill proving a return to a prior stage is not recorded.
- **Maturity model:** the role maps in `role_map.py` need to be linked to recorded adoption evidence, not estimates.

## Related links

- `readiness/transformation/tests.md`
- `readiness/transformation/scorecard.yaml`
- `readiness/cross_layer/rollback_drill.md`

Estimated value is not Verified value.
