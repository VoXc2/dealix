# Sales Autopilot — Dealix Full Ops

**المرجع الاستراتيجي:** [`../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md`](../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md)  
**الإعدادات:** [`../../dealix/config/lead_scoring.yaml`](../../dealix/config/lead_scoring.yaml) · [`stage_transitions.yaml`](../../dealix/config/stage_transitions.yaml)

## الهدف

أي lead لا يضيع: تسجيل، تسجيل نقاط، مسار، مسودات، موافقة، أدلة.

## الحالات (مرجع)

`new_lead` → `qualified_A` | `qualified_B` → `nurture` | `partner_candidate` → `meeting_booked` → `meeting_done` → `scope_requested` → `scope_sent` → `invoice_sent` → `invoice_paid` → `delivery_started` → `proof_pack_sent` → `sprint_candidate` | `retainer_candidate` → `closed_lost`

## تسجيل النقاط (ملخص)

| إشارة | نقاط تقريبية |
|--------|----------------|
| CEO / Founder / COO / CRO / Head Ops | +4 |
| B2B | +3 |
| CRM / pipeline / revenue workflow | +3 |
| يستخدم أو يخطط لـ AI | +3 |
| Saudi / GCC | +2 |
| عاجل ≤ 30 يوم | +2 |
| ميزانية 5k+ SAR | +2 |
| إمكان شريك/إحالة | +2 |
| بدون شركة / باحث عن وظيفة / فضول AI غامض / لا ألم workflow | سالب |

## التوجيه

- **15+** → Qualified A → دفع اجتماع  
- **10–14** → Qualified B → Proof Pack + nurture  
- **6–9** → تثقيف أو مسار شريك  
- **&lt;6** → أرشفة  

## أتمتة (مسودات فقط + موافقة)

- lead جديد → سجل CRM/ذاكرة إيراد → score → evidence event → عرض مقترح → مسودة رسالة (لا إرسال حي)  
- Qualified A → عنصر موافقة → رسالة حجز  
- اجتماع محجوز → مسار ديمو + أسئلة اكتشاف  
- اجتماع منتهي → نموذج نتيجة → مسودة نطاق أو nurture  
- نطاق معتمد → مسودة فاتورة (لا إرسال بدون موافقة)

## الوكلاء (أسماء مرجعية)

`LeadCaptureAgent` · `ICPScoringAgent` · `PositioningAgent` · `OutreachDraftAgent` · `ReplyClassifierAgent` · `MeetingBriefAgent` · `SalesCoachAgent` · `ScopeBuilderAgent` · `BillingDraftAgent` · `UpsellAgent` · `GovernanceAgent`

## ممنوعات (لا مساومة)

لا إرسال تلقائي خارجي · لا cold WhatsApp · لا أتمتة LinkedIn · لا scraping · لا ادّعاء إيراد قبل دفع · لا ضمان · لا إثبات مزيف — متوافق مع [`../V12_FULL_OPS_ARCHITECTURE.md`](../V12_FULL_OPS_ARCHITECTURE.md).
