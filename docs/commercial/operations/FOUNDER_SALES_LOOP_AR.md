# لوب مبيعات المؤسس — تعلّم من كل مكالمة + time-to-value

**الغرض:** تحويل كل discovery/demo إلى **قرار واحد** ومقياس TTV — متوافق مع بحث founder-led sales ومع مسار الأدلة في Dealix.

**قالب بعد الاجتماع:** [founder_meeting_debrief_template.yaml](founder_meeting_debrief_template.yaml)  
**تتبع:** [soft_launch_meetings_tracker.yaml](soft_launch_meetings_tracker.yaml) · [evidence_events_tracker.csv](evidence_events_tracker.csv)

---

## اللوب (قبل · أثناء · بعد)

```mermaid
flowchart LR
  prep[Prep_Proof_Stack]
  call[Discovery_7Q]
  debrief[Debrief_1_decision]
  evidence[CSV_evidence_event]
  prep --> call --> debrief --> evidence
```

### 1 — قبل (10 دقائق)

- [ ] طبقة الأدلة جاهزة حسب [PROOF_STACK_ORDER_AR.md](PROOF_STACK_ORDER_AR.md) (لا ديمو 30 دقيقة بدونها)
- [ ] `client_pack` إن وُجد: `py -3 scripts/generate_client_pack.py` (انظر [CLIENT_PACK_SOP_AR.md](CLIENT_PACK_SOP_AR.md))
- [ ] فرضية ألم + `offer_id` في War Room
- [ ] 7 أسئلة Discovery من [DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md](../DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md) §7

### 2 — أثناء

| # | سؤال | لماذا |
|---|------|-------|
| 1 | ماذا يحدث للـ lead بعد الحملة/النموذج؟ | ألم Motion A |
| 2 | من المالك اليوم؟ | SOAEN Owner |
| 3 | أين الدليل عند سؤال العميل؟ | Proof gap |
| 4 | ما أكبر مخاطرة تنظيمية/امتثال؟ | تموضع ثقة |
| 5 | ما الميزانية والجدول؟ | تأهيل |
| 6 | من يوقع ومن يعتمد؟ | Champion |
| 7 | ما الخطوة التالية إن وافقنا؟ | Next action |

### 3 — بعد (5 دقائق — إلزامي)

املأ [founder_meeting_debrief_template.yaml](founder_meeting_debrief_template.yaml) أو الجدول:

| حقل | قاعدة |
|-----|-------|
| `one_decision` | رسالة **أو** سعر **أو** خطوة تالية — واحد فقط |
| `message_winner` | جملة عربية فازت في الرد |
| `objection_primary` | اعتراض رئيسي → [objection_engine_registry.yaml](objection_engine_registry.yaml) |
| `evidence_sent` | ما أُرسل من طبقة الأدلة |
| `next_action` + تاريخ | لا صف بلا تاريخ |

```powershell
powershell -File scripts/founder_evening.ps1 -Append -Company "اسم الشركة" -EventType discovery_completed
```

---

## مقاييس time-to-value (TTV) — founder commercial

**لا vanity:** impressions ولا عدد مسودات بدون رد.

| مقياس | تعريف | هدف مرحلة soft launch | مصدر |
|--------|--------|-------------------------|------|
| **TTV_discovery** | أيام من `lead_identified` → `discovery_completed` | ≤ 14 | evidence CSV |
| **TTV_demo** | أيام من `discovery_completed` → `demo_held` | ≤ 7 | evidence CSV |
| **TTV_paid** | أيام من `demo_held` → `payment_received` | تتبع فقط — لا هدف مُعلن للعميل | evidence CSV |
| **activation** | عميل أكمل خطوة أولى في العرض (تشخيص/سبرنت) | 1/أسبوع هدف داخلي | DoD · engagements API |
| **retained_revenue** | إيراد بعد 30 يوم من أول دفع | قياس شهري | KPI import |

### مراجعة أسبوعية (جمعة — 15 دقيقة)

1. كم `discovery_completed` هذا الأسبوع؟ (هدف soft: 3–5 قبل إعلان paid)
2. أي `message_winner` تكررت ≥ 2 مرات؟ → حدّث [POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md](../POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md)
3. أي اعتراض تكرر؟ → سطر في objection registry
4. هل TTV_discovery &gt; 14؟ → قلّل قائمة ABM إلى `high` فقط
5. قرار: توسيع موجة 2 · تعديل ICP · **no-build** — [COMMERCIAL_WEEKLY_SCORECARD_AR.md](COMMERCIAL_WEEKLY_SCORECARD_AR.md)

---

## متى تنتقل من «مؤسس فقط» لفريق مبيعات

انتقل عندما **كل** التالي صحيح لمدة 4 أسابيع:

- [ ] نفس `message_winner` في ≥ 3 صفقات متتالية
- [ ] `offer_id` الافتراضي لا يتغير أسبوعياً
- [ ] playbook اعتراضات يغطي 80% الردود
- [ ] TTV_discovery متوسط ≤ 14 يوماً

حتى ذلك الحين: المؤسس يملك اللوب — الوكلاء **مسودات فقط** ([FOUNDER_AGENT_PLAYBOOK_AR.md](../../ops/FOUNDER_AGENT_PLAYBOOK_AR.md)).

---

## روابط

- [GTM_DUAL_TRACK_CLARIFICATION_AR.md](GTM_DUAL_TRACK_CLARIFICATION_AR.md)
- [ABM_WAVE1_ICP_AR.md](targeting/ABM_WAVE1_ICP_AR.md)
- [PROOF_STACK_ORDER_AR.md](PROOF_STACK_ORDER_AR.md)
