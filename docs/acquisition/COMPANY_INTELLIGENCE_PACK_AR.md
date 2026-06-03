# Company Intelligence Pack — دليل التشغيل (AR)

> الملف الأساسي لكل شركة مستهدفة. هو الطبقة التي تجعل الإيميل والـ Call Brief والـ Mini Proposal مخصّصة بعمق بدل أن تكون رسائل عامة.
> مرجع المصطلحات الحرفي: `AGENTS.md`. مرجع الحقول الحرفي: `schemas/company_intelligence_pack.schema.json`.

---

## 1. الغرض (Purpose)

الـ Company Intelligence Pack (نسمّيه اختصارًا "الـ pack") هو نقطة البداية في Acquisition Engine. لكل شركة pack واحد يجمع:

- ما نعرفه عن الشركة من **مصادر عامة فقط** (موقع، صفحة تواصل، حساب عام).
- الإشارة (signal) التي لاحظناها، والألم المحتمل (likely_pain) المبني عليها.
- النظام المناسب من الأنظمة الخمسة، وسبب اختياره.
- المواد الجاهزة للتنفيذ: `email_subject` + `email_draft` + `call_opener` + `call_questions` + `mini_proposal_angle`.

الـ pack ليس وثيقة تسويقية، بل **ورقة عمل تشغيلية** يأخذها Outreach Operator والـ Caller وينفّذان منها مباشرة دون شرح إضافي.

```txt
Company Research → Company Intelligence Pack → Client Need Card → Email Draft → Call Brief → Mini Proposal
```

**قاعدة الأمان الأساسية:** كل ما في الـ pack هو *تحضير*. الإيميل يبقى draft حتى موافقة founder. لا اتصال آلي — الـ call مواد لمتصل بشري. لا claims مضمونة. أي معلومة عند `L0`/`L1` تُصاغ كاحتمال.

---

## 2. الحقول الـ 23 (The 23 Fields)

هذه هي الحقول المطلوبة حرفيًا في الـ schema. الترتيب نفس ترتيب `required` في الملف.

| # | الحقل | الشرح بسطر واحد |
|---|---|---|
| 1 | `company` | اسم الشركة المستهدفة (اسم تركيبي بنمط سعودي في العيّنات). |
| 2 | `website` | الموقع الرسمي العام للشركة — مصدرنا الأول. |
| 3 | `country` | الدولة (عادة Saudi Arabia). |
| 4 | `city` | المدينة (الرياض، جدة، الدمام…). |
| 5 | `sector` | القطاع (Training, Real Estate, Clinics, Agency, Consulting…). |
| 6 | `public_contact_channels` | قنوات تواصل **عامة فقط**: صفحة تواصل، حساب عام. لا أرقام جوال شخصية. |
| 7 | `likely_decision_maker` | من **غالبًا** صاحب القرار (وصف، لا اسم شخص ما لم يكن منشورًا عامًا). |
| 8 | `best_contact_role` | أفضل دور للتواصل — يجب أن يكون ضمن أدوار النظام المسموحة (راجع `CONTACT_TARGETING_RULES_AR.md`). |
| 9 | `signal` | الإشارة العامة التي لاحظناها (برامج متعددة، واتساب ظاهر، صفحات خدمات كثيرة…). |
| 10 | `likely_pain` | الألم المحتمل المبني على الإشارة — **يُصاغ كاحتمال** عند L0/L1. |
| 11 | `recommended_system` | أحد الأنظمة الخمسة: `revenue_os` / `executive_command_os` / `followup_recovery_os` / `whatsapp_client_os` / `proposal_proof_os`. |
| 12 | `why_this_system` | لماذا هذا النظام تحديدًا لهذه الشركة (يربط الإشارة بالقيمة الأسرع). |
| 13 | `first_mission` | أول مهمة عملية صغيرة يبدأ بها الـ Sprint. |
| 14 | `proof_angle` | زاوية الإثبات: أي مخرج ملموس يُظهر القيمة مبكرًا. |
| 15 | `email_subject` | عنوان الإيميل — لا `Re:`/`Fwd:` مزيّف، لا وعد مضمون. |
| 16 | `email_draft` | نص الإيميل **كمسودة** — لا يُرسل قبل موافقة founder. |
| 17 | `call_opener` | جملة افتتاح الاتصال لمتصل بشري. |
| 18 | `call_questions` | أسئلة الاكتشاف (discovery) أثناء الاتصال. |
| 19 | `expected_objections` | الاعتراضات المتوقعة لهذه الشركة/القطاع. |
| 20 | `mini_proposal_angle` | زاوية العرض المصغّر (أي Sprint سنقترح). |
| 21 | `next_action` | الخطوة التالية الواضحة الواحدة. |
| 22 | `risk_level` | `low` / `medium` / `high`. |
| 23 | `evidence_level` | `L0`–`L4` حسب قوة المصدر. |

> حقول إضافية اختيارية في الـ schema (ليست ضمن الـ 23 المطلوبة): `id` (نمط `CIP-###`)، `status`، `draft_quality`، `owner`، `created_at`.

---

## 3. كيف يُغذّي الـ pack الإيميل + الـ Call Brief + الـ Mini Proposal

الـ pack هو المصدر، والمخرجات الثلاثة مشتقّة منه. هذا الجدول يوضح أي حقل يذهب إلى أين:

| المخرج | يأخذ من الـ pack |
|---|---|
| **Client Need Card** | `signal`, `likely_pain`, `recommended_system`, `why_this_system`, `first_mission`, `proof_angle` + يضيف `email_angle` و`CTA`. |
| **Email Draft** | `email_subject` + `email_draft` (المبنيان على `likely_pain` + `recommended_system` + angle). |
| **Call Brief** | `best_contact_role` → `contact_role`، `likely_pain`، `call_opener` → `opening_line`، `call_questions` → `discovery_questions`، `expected_objections` → `expected_objection`. |
| **Mini Proposal** | `mini_proposal_angle` → `title`/`first_sprint`، `why_this_system`، `proof_angle` → `expected_first_proof`. |

تسلسل التغذية:

```txt
pack.signal + pack.likely_pain
        │
        ▼
recommended_system  ──►  email_draft (draft)  ──►  [founder approval]  ──►  sent
        │                                                                     │
        ▼                                                                     ▼
mini_proposal_angle                                              follow_up_due + call_brief
```

**ملاحظة حوكمة:** الـ pack يُولَّد آليًا (بحث + تحليل + صياغة)، لكن الإرسال والتسعير النهائي والـ Mini Proposal تحتاج موافقة founder. الذكاء يحلّل ويكتب ويرتّب — لا يرسل ولا يسعّر ولا ينفّذ.

---

## 4. مثال عملي كامل (Full Worked Example)

شركة تركيبية في قطاع التدريب. لاحظ كيف تُملأ الحقول الـ 23 كلها، وكيف صيغ الألم كاحتمال (لأن الإشارة عامة من الموقع).

```txt
id:                       CIP-101
company:                  شركة تدريب في الرياض
website:                  https://example-training.sa
country:                  Saudi Arabia
city:                     الرياض
sector:                   Training
public_contact_channels:  ["صفحة تواصل في الموقع", "حساب عام على منصة تواصل"]
likely_decision_maker:    غالبًا مسؤول التسويق أو المؤسس (شركة تدريب متوسطة)
best_contact_role:        Marketing Manager
signal:                   برامج تدريبية متعددة معروضة + رقم/زر واتساب ظاهر للتسجيل
likely_pain:              استفسارات التسجيل غالبًا تضيع أو لا تُتابع بنفس الجودة عبر القنوات
recommended_system:       followup_recovery_os
why_this_system:          أسرع قيمة تظهر في ترتيب المتابعة وتجهيز رسائل التسجيل حسب حالة المسجّل
first_mission:            بناء follow-up queue للمسجّلين المحتملين + رسائل متابعة جاهزة
proof_angle:              Weekly Recovery Report يوضح كم استفسارًا أعيد تفعيله بمتابعة منظمة
email_subject:            آخر متابعة لم تحدث قد تكون أغلى فرصة
email_draft: |
  السلام عليكم [الاسم]،
  لاحظنا أن لديكم برامج تدريبية متعددة وقناة واتساب ظاهرة للتسجيل.
  في هذا النوع من شركات التدريب، غالبًا يضيع جزء من الاستفسارات لأن المتابعة
  بعد أول تواصل غير منظمة. الفكرة ليست بيع أداة، بل Sprint صغير (followup_recovery_os)
  نبني فيه follow-up queue ونجهّز رسائل متابعة حسب حالة المسجّل، ونطلع بتقرير
  أسبوعي يوضح أين تتعطل المتابعة. هل يناسب أرسل لكم نموذجًا مختصرًا من صفحة واحدة؟
  (هذه رسالة مختصرة، ويمكنكم إيقاف المراسلة في أي وقت.)
call_opener:              تواصلنا لأن شركات التدريب غالبًا تخسر جزءًا من التسجيل بسبب متابعة غير منظمة
call_questions:
  - هل عندكم متابعة موحّدة بعد أول تواصل مع المسجّل المحتمل؟
  - هل الرسائل جاهزة حسب حالة العميل (استفسر / سجّل مبدئيًا / لم يكمل)؟
  - من يتابع الاستفسارات حاليًا، وعبر أي قناة؟
expected_objections:
  - "ما عندنا وقت"
  - "عندنا فريق يتابع"
  - "أرسل معلومات أكثر"
mini_proposal_angle:      7-day Follow-up Recovery Sprint — follow-up queue + رسائل تسجيل + تقرير أسبوعي
next_action:              إرسال الإيميل (بعد موافقة founder) ثم تجهيز Call Brief للمتابعة
risk_level:               low
evidence_level:           L1
```

**لماذا `evidence_level = L1`؟** كل ما لدينا مصدره موقع الشركة (برامج + واتساب ظاهر). لم نتحقق من سير العمل الداخلي. لذلك `likely_pain` صيغ بـ "غالبًا" و"في هذا النوع من الشركات" — لا كحقيقة مؤكدة.

**لماذا `best_contact_role = Marketing Manager`؟** للنظام `followup_recovery_os` الأدوار المسموحة هي: Sales Manager, Marketing Manager, Founder. في شركة تدريب، التسجيل غالبًا تحت التسويق، فاخترنا Marketing Manager، والبدائل Sales Manager ثم Founder.

---

## 5. قاعدة مستوى الدليل (Evidence-Level Rule)

| level | المعنى | كيف نصوغ المعلومة |
|---|---|---|
| `L0` | تخمين قطاعي | احتمال صريح: "في هذا النوع من الشركات غالبًا…" |
| `L1` | موقع الشركة | احتمال: "غالبًا"، "قد يكون"، بناءً على ما يظهر في الموقع. |
| `L2` | صفحة خدمة/وظيفة/خبر عام | يمكن الإسناد لمصدر محدد عام مع بقاء `likely_*` احتمالية. |
| `L3` | عدة مصادر عامة متوافقة | ثقة أعلى، لكن بلا ادعاء يقين مطلق. |
| `L4` | بيانات مقدّمة من الشركة | حقائق مؤكدة من العميل نفسه. |

**القاعدة الصارمة:** أي معلومة عند `L0` أو `L1` تُصاغ كاحتمال (`غالبًا` / `قد يكون` / `في هذا النوع من الشركات`) ولا تُصاغ كحقيقة مؤكدة. الحقول التي تبدأ بـ `likely_` احتمالية بطبيعتها.

---

## 6. أين تعيش البيانات والتحقق

- البيانات: `data/acquisition/company_intelligence_packs.jsonl` — **عيّنات تركيبية (synthetic)** بأسماء وهمية، بلا أرقام جوال حقيقية ولا PII.
- التحقق من الصحة: `schemas/company_intelligence_pack.schema.json`.
- الفاحص: `scripts/acquisition_delivery_check.py` (يتحقق من الـ schema + الفحوصات الصارمة). تشغيل: `python3 scripts/acquisition_delivery_check.py` أو `npm run os:check`.

> لا أسرار ولا PII في الـ packs: لا مفاتيح API، لا أرقام جوال سعودية بنمط 05XXXXXXXX، لا هويات وطنية. المصادر عامة فقط.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
