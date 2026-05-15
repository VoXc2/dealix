# العربية

# جاهزية الطبقة ١١ — التحويل

**Owner:** قائد التحويل في Dealix (Transformation Lead).

## ١. الغرض ونطاق الطبقة

الطبقة ١١ تضمن أن Dealix لا يضيف الذكاء الاصطناعي فوق العمليات القائمة، بل يعيد تصميم تشغيل الشركة حوله. إشارة الجاهزية: يمكن لـ Dealix دخول أي شركة وإنتاج خريطة تحويل، وربط كل حالة استخدام بفرضية عائد، وتقسيم المشروع إلى مراحل، وبيع التدقيق ثم التجربة ثم التحويل ثم العقد الدوري.

## ٢. قائمة تحقق الجاهزية

- [ ] نموذج النضج جاهز وينتج درجة ٠–١٠٠ (`transformation/maturity_model.md`).
- [ ] نموذج التشغيل يحدّد الأدوار الأربعة وحدود القرار (`transformation/ai_operating_model.md`).
- [ ] إطار إعادة تصميم سير العمل بخطواته الست موثّق.
- [ ] إطار التبنّي يربط الرعاية والأبطال والتدريب والمراجعة.
- [ ] حوكمة الانتشار تربط البوّابات بـ `enterprise_rollout_os/adoption_gates.py`.
- [ ] تحقيق القيمة يربط فرضية العائد بسجل القيمة.
- [ ] خريطة ٣٠–٦٠–٩٠ يوماً تطابق مسار البيع.
- [ ] كل ملف ثنائي اللغة بقسمَي H1 (`# العربية` ثم `# English`).
- [ ] كل المسارات البرمجية المرجعية حقيقية وموجودة.

## ٣. المقاييس

| المقياس | التعريف | الهدف |
|---|---|---|
| زمن خريطة التحويل | أيام من التدقيق إلى الخريطة | ≤ ٣٠ يوماً |
| تغطية فرضية العائد | نسبة حالات الاستخدام المرتبطة بفرضية | ١٠٠٪ |
| اكتمال الأدوار | الأدوار الأربعة مسمّاة قبل المرحلة | ١٠٠٪ |
| اجتياز البوّابات | بوّابات مُجتازة بمعيار موثّق | ١٠٠٪ |
| إيقاع تقرير القيمة | تقرير قيمة شهري مُنتَج | شهري |

## ٤. روابط الملاحظة

- درجة التبنّي ولوحتها: `auto_client_acquisition/adoption_os/adoption_score.py` و`adoption_dashboard.py`.
- لوحة الانتشار وحالة المراحل: `auto_client_acquisition/enterprise_rollout_os/rollout_dashboard.py`.
- سجل القيمة والتقرير الشهري: `auto_client_acquisition/value_os/value_ledger.py` و`monthly_report.py`.
- سجل الاحتكاك: `auto_client_acquisition/adoption_os/friction_log.py`.
- سجل مخاطر الانتشار: `auto_client_acquisition/enterprise_rollout_os/enterprise_risk.py`.

## ٥. قواعد الحوكمة

- لا مرحلة تبدأ قبل تسمية الأدوار الأربعة واجتياز بوّابتها.
- لا تُربط حالة استخدام بعائد مضمون — فقط بفرضية عائد بأدلة.
- الإرسال التلقائي للرسائل الخارجية والكشط والتواصل البارد المؤتمت محظورة.
- لا يُذكر اسم عميل علناً بدون إذن موقّع.
- القيمة لا تُعرض كمؤكَّدة قبل توقيع العميل.

## ٦. إجراء التراجع

إذا أنتجت مرحلة قيمة سلبية أو احتكاكاً عالياً: (١) أوقف الانتقال إلى البوّابة التالية، (٢) أعد الفريق إلى آخر سير عمل مستقر، (٣) سجّل السبب في سجل الاحتكاك وسجل المخاطر، (٤) أعد تشغيل خطوة إعادة التصميم للحالة المتأثرة فقط، (٥) لا تتقدّم قبل اجتياز البوّابة من جديد. التراجع لا يحذف القيمة المُسجَّلة سابقاً.

## ٧. درجة الجاهزية الحالية

**الدرجة: ٧٠ / ١٠٠ — بيتا داخلية.**

سُلَّم النطاقات الخمسة:

- ٠–٥٩: نموذج أولي
- ٦٠–٧٤: بيتا داخلية
- ٧٥–٨٤: تجربة عميل
- ٨٥–٩٤: جاهز للمؤسسات
- ٩٥+: حرج المهمة

المبرّر: أُطر الطبقة ١١ السبعة موثّقة ومرتبطة بمسار البيع ومسارات برمجية حقيقية. الرفع إلى تجربة عميل يحتاج تشغيل الخريطة على عميل حقيقي وإنتاج أول تقرير قيمة مؤكَّد.

## ٨. ملاحظة الصدق

كل درجة وخريطة في هذه الطبقة فرضية مبنية على إشارات العميل. لا فرضية مرتبطة بنتيجة مضمونة.

القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

# Layer 11 Readiness — Transformation

**Owner:** Dealix Transformation Lead.

## 1. Purpose and layer scope

Layer 11 ensures Dealix does not bolt AI onto existing operations but redesigns how the company runs around it. Readiness signal: Dealix can enter any company and produce a transformation map, tie every use case to an ROI hypothesis, split the project into phases, and sell Audit, then Pilot, then Transformation, then Retainer.

## 2. Readiness checklist

- [ ] Maturity model ready and produces a 0-100 score (`transformation/maturity_model.md`).
- [ ] Operating model defines the four roles and decision boundaries (`transformation/ai_operating_model.md`).
- [ ] Workflow redesign framework documented with its six steps.
- [ ] Adoption framework links sponsorship, champions, training, and review.
- [ ] Governance rollout ties gates to `enterprise_rollout_os/adoption_gates.py`.
- [ ] Value realization ties the ROI hypothesis to the value ledger.
- [ ] 30-60-90 day roadmap mirrors the sales path.
- [ ] Every file is bilingual with two H1 sections (`# العربية` then `# English`).
- [ ] All referenced code paths are real and exist.

## 3. Metrics

| Metric | Definition | Target |
|---|---|---|
| Transformation map time | Days from Audit to map | <= 30 days |
| ROI hypothesis coverage | Share of use cases tied to a hypothesis | 100% |
| Role completeness | Four roles named before the stage | 100% |
| Gate pass rate | Gates passed with a documented criterion | 100% |
| Value report cadence | Monthly value report produced | Monthly |

## 4. Observability hooks

- Adoption score and dashboard: `auto_client_acquisition/adoption_os/adoption_score.py` and `adoption_dashboard.py`.
- Rollout dashboard and stage status: `auto_client_acquisition/enterprise_rollout_os/rollout_dashboard.py`.
- Value ledger and monthly report: `auto_client_acquisition/value_os/value_ledger.py` and `monthly_report.py`.
- Friction log: `auto_client_acquisition/adoption_os/friction_log.py`.
- Rollout risk register: `auto_client_acquisition/enterprise_rollout_os/enterprise_risk.py`.

## 5. Governance rules

- No stage begins before the four roles are named and its gate is passed.
- No use case is tied to a guaranteed return — only to an evidence-backed ROI hypothesis.
- Auto-send of external messages, scraping, and automated cold outreach are blocked.
- No client name is mentioned publicly without signed permission.
- Value is never presented as confirmed before the client signs.

## 6. Rollback procedure

If a stage produces negative value or high friction: (1) halt the transition to the next gate, (2) return the team to the last stable workflow, (3) record the cause in the friction log and the risk register, (4) re-run the redesign step for the affected use case only, (5) do not advance before the gate is passed again. Rollback does not delete previously recorded value.

## 7. Current readiness score

**Score: 70 / 100 — Internal beta.**

The five-band scale:

- 0-59: prototype
- 60-74: internal beta
- 75-84: client pilot
- 85-94: enterprise-ready
- 95+: mission-critical

Rationale: The seven Layer 11 frameworks are documented and linked to the sales path and to real code paths. Moving to client pilot requires running the map on a real client and producing the first client-confirmed value report.

## 8. Honesty note

Every score and map in this layer is a hypothesis built on client signals. No hypothesis is tied to a guaranteed outcome.

Estimated value is not Verified value.
