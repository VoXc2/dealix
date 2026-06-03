# Dealix — Complete Business OS Map
## خريطة نظام تشغيل الأعمال الكامل

> **التاريخ:** 2026-06-03 · **المالك:** المؤسس · **القاعدة:** موافقة المؤسس أولًا، تشغيل تجريبي افتراضيًا، مدفوع بالأدلة.

```
Dealix Complete Business OS =
  Market Production OS          (أساس Agent #1 — لا يُكرَّر)
+ Revenue Execution OS
+ WhatsApp Client OS
+ Secure Client Portal
+ Proposal / Proof / Payment OS
+ Client Delivery OS
+ Renewal OS
+ Customer Success OS
+ Finance OS
+ Founder Control Room
+ Agent Governance OS
+ Trust / Security / Privacy OS
+ Metrics & Learning Loop
```

كل نظام يُعرَّف بـ: المهمة · الوكيل المالك · المدخلات · المخرجات · الإجراءات المسموحة · الإجراءات الممنوعة · التقارير · الإيقاع اليومي · الإيقاع الأسبوعي · قرارات المؤسس.

---

### 1) Market Production OS (أساس Agent #1 — مرجع فقط)
- **المهمة:** إنتاج الاهتمام السوقي (محتملون، تواصل، سوق، إشارات).
- **المالك:** `prospect_research` + المحتوى (Agent #1).
- **المدخلات:** بحث سوق، قطاعات، إشارات. **المخرجات:** `company_os/revenue/prospects.csv`, `outreach_queue.json`, `pipeline.json`.
- **مسموح:** بحث، تسجيل، صياغة تواصل (Draft). **ممنوع:** إرسال بلا موافقة، PII في أدوات عامة.
- **التقارير:** `company_os/war_room/REVENUE_WAR_ROOM_TODAY.md`. **يومي:** قائمة التواصل. **أسبوعي:** CEO Brief.
- **قرارات المؤسس:** أي قطاع، اعتماد التواصل. **(لا نُعدّل هذا النظام — نستقبل مخرجاته فقط.)**

### 2) Revenue Execution OS
- **المهمة:** تحويل الاهتمام إلى عرض/إثبات/دفع جاهز للموافقة.
- **المالك:** revenue execution agent. **المدخلات:** رد إيجابي/تقييم العميل، الكتالوج. **المخرجات:** `data/proposals/*`, `data/proof_packs/*`, `data/payments/*`, `data/revenue/action_cards.jsonl`.
- **مسموح:** توليد عروض/أدلة/تجهيز دفع (Draft/L4). **ممنوع:** سعر نهائي بلا موافقة، إرسال رابط دفع، وعد قانوني.
- **التقارير:** `reports/revenue_execution/{PROPOSAL,PROOF_PACK,PAYMENT_HANDOFF,REVENUE_ACTION}_QUEUE.md`.
- **يومي:** طابور العروض/الدفع. **أسبوعي:** معدل تحويل العروض. **قرارات المؤسس:** اعتماد السعر/الدفع.

### 3) WhatsApp Client OS (بعد الموافقة)
- **المهمة:** تجربة عميل آمنة على واتساب بعد الموافقة عبر بطاقات إجراء.
- **المالك:** whatsapp client agent. **المدخلات:** موافقة (`consent_basis`)، تقييم. **المخرجات:** `data/whatsapp/*`.
- **مسموح:** ترحيب/فحص/توصية/بطاقات (L3/L4 بموافقة). **ممنوع:** واتساب بارد، طلب أسرار، إرسال تلقائي، روابط دفع.
- **التقارير:** `reports/whatsapp/*`. **يومي:** طابور ما بعد الرد + بطاقات الإجراء. **أسبوعي:** تحويل ما بعد الرد.
- **قرارات المؤسس:** اعتماد كل بطاقة إجراء قبل أي إرسال.

### 4) Secure Client Portal
- **المهمة:** المكان الوحيد للأسرار/الملفات/الصلاحيات/المراجعات.
- **المالك:** portal agent + Auth/S3. **المدخلات:** جلسات/رفع/صلاحيات. **المخرجات:** `data/client_portal/*`.
- **مسموح:** رفع آمن، صلاحية قراءة فقط، مراجعة عرض/إثبات، تأكيد دفع (L4/L5). **ممنوع:** أسرار في السجلات، روابط بلا انتهاء، صلاحية واسعة.
- **التقارير:** `reports/client_portal/{CLIENT_PORTAL_HANDOFF_REPORT,CLIENT_PERMISSION_REVIEW}.md`.
- **يومي:** الجلسات النشطة. **أسبوعي:** مراجعة الصلاحيات. **قرارات المؤسس:** منح/إلغاء صلاحيات حساسة.

### 5) Proposal / Proof / Payment OS
- **المهمة:** قوالب وعقود بيانات للعرض والإثبات والدفع. **المالك:** revenue execution agent.
- **المدخلات:** الكتالوج، بيانات العميل. **المخرجات:** سجلات مطابقة لـ `schemas/{proposal,proof_pack,payment_handoff}.schema.json`.
- **مسموح:** توليد ومطابقة بالكتالوج. **ممنوع:** عرض بلا `product_id`، رقم بلا `evidence_level`، عائد مضمون.
- **التقارير:** ضمن Revenue Execution. **قرارات المؤسس:** اعتماد العرض النهائي والدفع.

### 6) Client Delivery OS
- **المهمة:** تحويل كل صفقة مربوحة إلى تسليم قيمة. **المالك:** delivery agent.
- **المدخلات:** صفقة مربوحة. **المخرجات:** `data/delivery/{handoffs,onboarding,weekly_reports,acceptance}.jsonl`.
- **مسموح:** handoff، إعداد، تقارير قيمة، قبول. **ممنوع:** صفقة مربوحة بلا handoff، تسليم بلا قالب تقرير أسبوعي، تضخم نطاق.
- **التقارير:** `reports/delivery/*`. **يومي:** طابور الإعداد. **أسبوعي:** تقرير القيمة + مراجعة المخاطر.
- **قرارات المؤسس:** قبول التسليم، تغييرات النطاق عبر Scope Guard.

### 7) Renewal OS
- **المهمة:** تجديد/توسعة مبنية على قيمة مُسلَّمة. **المالك:** renewal agent.
- **المدخلات:** صحة العميل، تقارير القيمة. **المخرجات:** `data/renewals/{renewals,upsell_opportunities}.jsonl`.
- **مسموح:** مسودات تجديد/ترقية بقيمة مُسلَّمة (L4 بموافقة). **ممنوع:** تجديد بلا قيمة (`evidence_level<client_data`)، ضغط، أكثر من خطوة.
- **التقارير:** `reports/renewal/*`. **أسبوعي:** طابور التجديد/الترقية. **قرارات المؤسس:** اعتماد كل مسودة.

### 8) Customer Success OS
- **المهمة:** صحة العميل ونجاحه أول 30 يوم وما بعدها. **المالك:** customer success agent.
- **المدخلات:** إشارات الإعداد/الوصول/التسليم/التفاعل. **المخرجات:** `data/customer_success/client_health.jsonl`.
- **مسموح:** حساب الصحة، التوصية بمسار التجديد. **ممنوع:** تجاوز قرارات العميل، وعود.
- **التقارير:** `reports/customer_success/CLIENT_HEALTH_REVIEW.md`. **أسبوعي:** مراجعة الصحة. **قرارات المؤسس:** التدخل عند الأحمر.

### 9) Finance OS (أساس قائم — مرجع)
- **المهمة:** المدفوعات، الفواتير، اقتصاديات الوحدة. **المالك:** finance agent (Agent #1).
- **المدخلات:** عروض معتمدة، مدفوعات. **المخرجات:** `company_os/finance/*` + جدول `payments` في DB.
- **مسموح:** حساب المقاييس، تتبع الفواتير (Observe). **ممنوع:** إنشاء فواتير/معالجة مدفوعات آليًا.
- **التقارير:** `company_os/finance/revenue_scorecard.csv`. **قرارات المؤسس:** كل التزام مالي.

### 10) Founder Control Room
- **المهمة:** أمر واحد يومي + مراجعة أسبوعية + سجل قرار. **المالك:** المؤسس.
- **المدخلات:** كل الطوابير. **المخرجات:** `reports/founder/{DAILY_SUPER_COMMAND,WEEKLY_BOARD_REVIEW,DECISION_LOG}.md`.
- **مسموح:** approve/reject/edit/copy/mark-sent/nurture/do-not-contact/handoff. **ممنوع:** زر إرسال خارجي في v1 قبل اكتمال البوابات.
- **يومي:** أمر المؤسس. **أسبوعي:** مراجعة المجلس. **قرارات المؤسس:** قرار حرج واحد يوميًا.

### 11) Agent Governance OS (أساس قائم — يُوسَّع)
- **المهمة:** مستويات الصلاحية، طابور الموافقة، سجل الإجراءات. **المالك:** governance agent.
- **المدخلات:** كل إجراء وكيل. **المخرجات:** `company_os/governance/{approval_queue.json,ai_action_ledger.jsonl}` + `AGENTS.md`.
- **مسموح:** مراجعة/تنبيه (Observe/Advise). **ممنوع:** تجاوز قرار بشري.
- **التقارير:** فحص الحوكمة. **أسبوعي:** مراجعة كل الإجراءات.

### 12) Trust / Security / Privacy OS
- **المهمة:** لا أسرار، PDPL، أقل امتياز، تدقيق. **المالك:** governance + security.
- **المخرجات:** `docs/security/*`, `docs/privacy/*`, `company_os/governance/{pdpl_checklist,data_handling_checklist}.md`.
- **مسموح:** فحص/تنبيه. **ممنوع:** أسرار في أي مخرَج، نقل بيانات خارج السعودية بلا أساس.
- **التقارير:** فحص الأمن. **يومي/أسبوعي:** تنبيهات الخصوصية/الأمن في غرفة القيادة.

### 13) Metrics & Learning Loop
- **المهمة:** قياس وتعلّم عبر كل النظام. **المالك:** كل الوكلاء + المؤسس.
- **المدخلات:** التقارير والطوابير. **المخرجات:** `reports/whatsapp/WHATSAPP_METRICS.md`, مراجعات التحويل، حالات التقييم `data/evals/*`.
- **مسموح:** قياس، تقييم (evals)، اقتراح تحسين. **ممنوع:** تزييف نتائج.
- **أسبوعي:** مراجعة المقاييس + تحديث حالات التقييم.

---

## مصفوفة الإجراءات الافتراضية لكل نظام خارجي

| النظام | dry_run | approval_required | send_enabled (v1) |
|---|:--:|:--:|:--:|
| WhatsApp | ✅ true | ✅ true | ❌ false |
| Portal links | ✅ true | ✅ true | ❌ false |
| Payment handoff | ✅ true | ✅ true | ❌ false |
| Renewal/Upsell | ✅ true | ✅ true | ❌ false |

*المرجع الحاكم: `AGENTS.md`. خريطة التدقيق: `reports/business_os/CLAUDE_CLIENT_REVENUE_DELIVERY_AUDIT.md`.*
