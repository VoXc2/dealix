# Target Account Profile (TAP) — ملف الحساب المستهدف

> **Status:** READY (structure) / PARTIAL (numerical scoring weights)
> **Evidence Level:** assumption (design-time template)
> **Owner:** Sales Lead (Primary) · Marketing (Secondary)
> **الاستخدام:** قالب إلزامي لكل حساب يدخل ABM Tier-1 أو Tier-2.

---

## 1. الفرق الجوهري: ICP vs TAP

| | **ICP (Ideal Customer Profile)** | **TAP (Target Account Profile)** |
|---|---|---|
| **النطاق** | قطاع/شريحة سوق بأكملها | حساب واحد (شركة واحدة بالاسم) |
| **الاستخدام** | لتوليد Leads، تسعير، Product strategy | لتخصيص كل خطوة مبيعات لهذا الحساب |
| **التفاصيل** | مرتفعة المستوى (القطاع، الحجم، الألم) | مرتفعة التخصيص (الأحداث الأخيرة، صانعو القرار بالاسم، ضغط الميزانية) |
| **الثبات** | ثابت نسبيًا (ربع سنوي) | متغيّر (يُحدَّث كل شهر) |
| **العدد** | 2–5 ICPs لـ Dealix | 5–20 TAPs نشطة في نفس الوقت |
| **المالك** | Product/Marketing | Sales Lead |

> **القاعدة:** ICP يقول «من يشتري؟»، TAP يقول «كيف نخترق هذا الحساب بالذات؟».

**الربط:** ICP في `docs/commercial/POSITIONING_AND_ICP.md` و `schemas/icp.schema.json`. هذا الـ OS يُترجم ICP إلى TAPs قابلة للتنفيذ.

---

## 2. قالب TAP — 14 حقلًا إلزاميًا

> **ملاحظة:** الحقول أدناه تطابق `schemas/enterprise_account.schema.json`. أي TAP يُسجَّل في `data/enterprise_sales/accounts.jsonl` يجب أن يستوفي كل حقل إلزامي.

### الحقول الأساسية

#### 1) `company.name_placeholder` (Placeholder Name)
- **الوصف:** اسم مستعار مجهول الهوية، يُستخدم في كل وثائق OS.
- **أمثلة:** `شركة_X_صناعية`، `ExampleCo KSA - Healthcare`، `SaudiCo_Retail_RUH`.
- **القاعدة:** لا يُكتب الاسم الحقيقي داخل الـ TAP. يُحفظ في مكان آمن (CRM مغلق).
- **Required:** نعم.

#### 2) `company.sector` (القطاع)
- **القيم:** `industrial | healthcare | retail | financial_services | logistics | real_estate | education | government | telecom | other`.
- **Required:** نعم.

#### 3) `company.sub_sector` (القطاع الفرعي)
- **مثال:** داخل `industrial` → `petrochemicals`، `cement`، `food_processing`.
- **Required:** اختياري.

#### 4) `company.hq_region` (مقرّ الشركة)
- **القيم:** `Riyadh | Jeddah | Dammam | Mecca | Medina | NEOM | Tabuk | Jizan | Abha | multi_region | other`.
- **Required:** نعم.

#### 5) `size.employees_band` (نطاق عدد الموظفين)
- **القيم:** `1-50 | 51-200 | 201-500 | 501-1000 | 1001-5000 | 5001-10000 | 10000+`.
- **Required:** نعم.

#### 6) `size.revenue_band_sar` (نطاق الإيرادات بالريال السعودي)
- **القيم:** `<50M | 50-200M | 200M-1B | 1-5B | 5B+ | undisclosed`.
- **Required:** نعم.

#### 7) `pain.primary_pain` (الألم الأساسي)
- **الوصف:** جملة واحدة تصف الألم الذي يدفع هذا الحساب للتفكير في حل.
- **مثال:** «تسرّب العملاء المحتملون بين الـ Marketing Qualified Lead وفريق المبيعات بسبب عدم وجود متابعة منهجية».
- **Required:** نعم.

#### 8) `pain.severity` (شدّة الألم)
- **القيم:** `low | medium | high | critical`.
- **Required:** نعم.

#### 9) `trigger.trigger_type` (نوع المحفّز)
- **القيم:** `strategic_initiative | regulatory_pressure | competitive_pressure | leadership_change | vendor_dissatisfaction | ma_event | budget_cycle | audit_finding | incident | growth_target | other`.
- **الوصف:** ما الذي حدث **مؤخرًا** جعل هذا الحساب مستعدًا للشراء الآن؟
- **Required:** نعم.

#### 10) `recent_events` (الأحداث الأخيرة)
- **الوصف:** قائمة بأهم 3–5 أحداث في آخر 12 شهرًا (مثال: تعيين CTO جديد، إطلاق استراتيجية AI، غرامة PDPL، استحواذ، توسّع في 3 مدن).
- **مصدر الدليل:** `assumption` افتراضيًا حتى يُؤكَّد من قِبل Sales Lead.
- **Required:** اختياري (لكن موصى به).

#### 11) `current_stack` (المكدس التقني الحالي)
- **الوصف:** الأدوات التي يستخدمها الحساب اليوم (CRM, ERP, Data Warehouse, BI tools).
- **مثال:** `Salesforce + SAP S/4HANA + Snowflake + Power BI + custom ETL`.
- **Required:** اختياري.

#### 12) `decision_makers_hint` (تلميح عن صانعي القرار)
- **الوصف:** وصف لمستويات اتخاذ القرار المتوقّعة.
- **مثال:** «CFO + Chief Revenue Officer + IT Director → توصية → Board approval للمبالغ > نطاق معين».
- **Required:** اختياري.

#### 13) `fiscal_year` (السنة المالية)
- **الوصف:** شهر بداية السنة المالية (`fiscal_year_start_month`)، يُستخدم لتوقيت التجديد.
- **مثال:** `1` (يناير) للشركات السعودية، بعض الشركات تبدأ في أبريل.
- **Required:** اختياري.

#### 14) `regulatory_pressure` (الضغط النظامي)
- **الوصف:** الأنظمة/اللوائح التي تضغط على الحساب.
- **أمثلة:** PDPL، NDMO، NCA ECC، SAMA Cybersecurity Framework، CITC.
- **Required:** اختياري.

#### 15) `strategic_initiative` (المبادرة الاستراتيجية)
- **الوصف:** ربط الحساب بمبادرة استراتيجية معلنة (Vision 2030 sector، مثلًا: «هيئة الحكومة الرقمية»، «برنامج تطوير الصناعة»).
- **Required:** اختياري.

#### 16) `competitive_pressure` (الضغط التنافسي)
- **الوصف:** المنافسون أو التهديدات التي تدفع الحساب للتسريع.
- **مثال:** «منافس رئيسي أعلن عن أتمتة المبيعات قبل 6 أشهر».
- **Required:** اختياري.

#### 17) `urgency` (الإلحاح)
- **القيم:** `low | medium | high | critical`.
- **Required:** اختياري (يُستنتج من trigger و recent_events).

#### 18) `budget_posture` (وضع الميزانية)
- **القيم:** `unknown | not_approved | approved_for_pilot | approved_for_full | frozen | expanding`.
- **Required:** اختياري.

---

## 3. حقول إضافية مُوصى بها (Outside Required Schema)

- `last_known_champion_name_hint` — placeholder للشخص الذي قد يكون البطل.
- `tier` — `tier_1 | tier_2 | tier_3` (للربط مع ABM).
- `stage` — `prospect | discovery | … | closed_won | closed_lost | stalled` (للربط مع Pipeline).
- `next_action` — الإجراء التالي بالـ owner و due_window.
- `evidence_level` — افتراضي `assumption` للحسابات الجديدة.

---

## 4. Worked Example (TAP مجهول الهوية)

> **Evidence Level:** assumption (تصميميّ بالكامل، لا توجد بيانات حقيقية).

```markdown
account_id: ACC-ENT-001
company.name_placeholder: شركة_X_صناعية
company.sector: industrial
company.sub_sector: petrochemicals
company.hq_region: Dammam
company.public_or_private: public_listed
size.employees_band: 5001-10000
size.revenue_band_sar: 1-5B
pain.primary_pain: "تسرّب في خط المبيعات بسبب عدم وجود نظام متابعة منهجي بين الـ SDRs وفريق الحسابات الكبيرة؛ الفجوة تتسبب في ضياع 12-18% من الفرص المؤهلة شهريًا (افتراض)."
pain.severity: high
trigger.trigger_type: competitive_pressure
trigger.description: "منافس رئيسي (مجهول) أطلق مبادرة AI للمبيعات قبل 8 أشهر؛ العميل يرى نفسه متأخرًا في السوق."
trigger.urgency: high
recent_events:
  - تعيين Chief Revenue Officer جديد (قبل 4 أشهر)
  - إطلاق مبادرة "Digital Sales 2027" المعلنة
  - توسّع في 3 أسواق إقليمية
current_stack: "Salesforce + custom ETL + Power BI + WhatsApp Business"
decision_makers_hint: "CRO + CFO + IT Director → Board approval مطلوب للمبالغ > نطاق معين"
fiscal_year_start_month: 1
regulatory_pressure: ["PDPL", "NCA ECC"]
strategic_initiative: ["Vision 2030 - تطوير الصناعة الوطنية"]
competitive_pressure: "منافس سعودي مشابه يروّج لـ AI Sales OS منذ 9 أشهر"
urgency: high
budget_posture: not_approved
champion_hypothesis: "CRO الجديد (مجهول) — مصلحة شخصية: تنفيذ مبادرته بنجاح"
economic_buyer_hypothesis: "CFO + Board → قرار على مستوى المجموعة"
technical_reviewer: "IT Director + Data Engineering Lead"
legal_procurement_reviewer: "Procurement Manager + Legal Counsel (مجهول)"
first_offer.offer_type: "pilot"
first_offer.price_band_placeholder: "founder-confirmed range — Tier-1 pilot"
pilot_scope.team_in_scope: "فريق الحسابات الكبيرة — المنطقة الشرقية"
pilot_scope.channel_in_scope: "Inbound + Outbound لحسابات Enterprise"
pilot_scope.duration_weeks: 8
pilot_scope.success_metrics:
  - "تقليل دورة Lead-to-Opportunity بنسبة X%"
  - "زيادة conversion rate من MQL→SQL بنسبة Y%"
  - "إنشاء pipeline مغطّى بـ 3× Pilot ACV خلال فترة التجربة"
pilot_scope.exit_criteria:
  - "العميل يوافق على Expansion Path"
  - "مؤشرات Pilot في النطاق المتوقع"
  - "العميل يوقّع MSA بعد نجاح Pilot"
expansion_path:
  - stage: "Channel Expansion"
    description: "إضافة Outbound لحسابات Mid-Market"
  - stage: "Team Expansion"
    description: "توسعة لـ 3 فرق إضافية"
  - stage: "Multi-department"
    description: "تعميم الحل على Customer Success"
proof_needed:
  - "DPA مكتمل وموقّع"
  - "Security questionnaire مكتمل"
  - "مرجع واحد في قطاع مشابه (anonymized)"
  - "Pilot SOW بنطاق محدود"
risks:
  - category: "champion"
    description: "CRO جديد لم يستقر بعد في منصبه"
    severity: medium
  - category: "competitive"
    description: "منافس سبقنا في 3 عروض مشابهة"
    severity: high
next_action.action: "إرسال رسالة تعريفية مخصّصة عبر LinkedIn لـ CRO"
next_action.owner: "Sales Lead"
next_action.due_window: "هذا الأسبوع"
tier: "tier_1"
stage: "prospect"
evidence_level: "assumption"
```

---

## 5. كيف يُحدَّث TAP؟

| المحفّز | التحديث المطلوب |
|---------|----------------|
| اجتماع Executive جديد | إضافة stakeholder، تحديث `engagement_status` |
| تغيير في CRO/CTO/CFO | تحديث `champion_hypothesis` و `economic_buyer_hypothesis` |
| تأخّر في الردود | إضافة `deal_risks.jsonl` entry |
| تغيير في Stack التقني | تحديث `current_stack` |
| تقدّم في MAP | تحديث `stage` |
| ميزانية جديدة معتمدة | تحديث `budget_posture` |
| ضبط سعر | تحديث `first_offer.price_band_placeholder` فقط بعد Founder approval |

> **التكرار:** TAP يُراجَع كل أسبوع للحسابات النشطة، وكل شهر للحسابات في `stalled`.

---

## 6. الجودة (Quality Bar)

كل TAP يجب أن يستوفي:

- [ ] جميع الحقول الـ 18 `Required` مكتملة.
- [ ] `evidence_level` محدد لكل قسم رئيسي.
- [ ] لا أرقام وهمية (مثال: «نسبة 47% من الفرص ضاعت»). النسب placeholder.
- [ ] لا اسم عميل حقيقي في الـ TAP. الاسم في CRM فقط.
- [ ] يحتوي على `next_action` واضح بـ owner و due_window.
- [ ] مربوط بـ `account_id` و `stakeholder_map` (≥ 4 stakeholders).

---

## 7. Anti-Patterns (ما لا يجب أن يكون في TAP)

- ❌ «هذه الشركة كبيرة، يجب أن نشتريها» بدون trigger واضح.
- ❌ «كل الصناعيين في السعودية يحتاجون» — هذا ICP، ليس TAP.
- ❌ «CFO سيحب العرض» — هذا تخمين. أضف `proof_needed` و `evidence_level: assumption`.
- ❌ الأرقام المطلقة بدون source.
- ❌ نسخ ولصق من TAP آخر.

---

> **آخر تحديث:** 2026-06-03 · v0.1
