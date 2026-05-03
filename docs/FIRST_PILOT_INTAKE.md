# First Pilot Intake — Pilot 499 (Growth Starter)

**الجمهور:** الـ Founder + أول 5 عملاء.
**الاستخدام:** انسخ الـ template، املأه مع العميل في 15 دقيقة، ارفعه في
`/api/v1/operator/service/start` body كـ `inputs`.

---

## القسم 1: Intake Form (انسخ + املأ)

```yaml
# عميل #001 — Pilot 499 / Growth Starter
customer:
  company_name: ""                # شركة العميل
  legal_name: ""                  # الاسم القانوني (لـ invoice)
  cr_number: ""                   # السجل التجاري
  vat_number: ""                  # ضريبة القيمة المضافة (إن وجد)
  contact:
    name: ""                      # اسم الـ founder/decision maker
    role: ""                      # CEO / Co-founder / Sales Manager
    email: ""                     # بريد رسمي
    whatsapp: ""                  # رقم سعودي (للـ inbound فقط)
    linkedin: ""                  # رابط
  city: ""                        # الرياض / جدة / الدمام / ...
  sector: ""                      # tech / consulting / training / real_estate / ...
  size: ""                        # 1-10 / 11-50 / 51-200 / 200+

icp:
  ideal_customer_description: ""  # نص حر — من العميل المثالي؟
  industry: ""                    # القطاع المستهدف
  city_focus: ""                  # المدن المستهدفة
  company_size_range: ""          # 11-50 / 51-200 / ...
  decision_maker_titles: []       # ["CEO", "VP Sales", ...]
  avg_deal_value_sar: 0           # متوسط الصفقة
  sales_cycle_days: 0             # متوسط طول الدورة

current_state:
  current_channels: []            # ["LinkedIn personal", "Email", "Referrals"]
  has_crm: false                  # true / false
  crm_name: ""                    # HubSpot / Salesforce / Sheets / None
  has_existing_list: false
  existing_list_size: 0
  current_pain: ""                # نص حر: ما المشكلة الأكبر الآن؟
  past_outreach: ""               # ما جربوا قبل + النتيجة

pilot_goals:
  primary_goal: ""                # leads / meetings / pilot conversions / brand
  success_metric: ""              # كيف يقيس النجاح بعد 7 أيام؟
  blockers: []                    # ما الذي يمنعهم من نتائج أفضل
  approval_authority: ""          # هل الـ Founder = decision maker؟

policy:
  channels_approved: []           # ["email"]  ← لا "whatsapp" بدون opt-in
  channels_forbidden: []          # ["cold_whatsapp", "scrape_linkedin"]
  consent_status:                 # PDPL
    has_existing_consent: false
    consent_source: ""
  reply_window_hours: 24

billing:
  pilot_price_sar: 499
  invoice_method: "manual_moyasar"  # MOYASAR_ALLOW_LIVE_CHARGE = false
  payment_terms: "due_on_receipt"
  refund_policy: "full_refund_if_no_proof_pack_in_7d"

ops:
  start_date: ""                  # YYYY-MM-DD
  delivery_date: ""               # +7 days
  proof_pack_recipients: []       # CEO + 1-2 آخرين
  weekly_call_slot: ""            # يوم + وقت ثابت للأسبوع
```

---

## القسم 2: Definition of Done (Pilot 499)

عميل لا يتحول إلى "Pilot delivered" إلا بعد كل البنود التالية:

- [ ] 10 opportunities `opportunity_created` events سُجِّلت في Proof Ledger
- [ ] 8+ `draft_created` events لرسائل عربية
- [ ] 6+ `approval_collected` events (drafts معتمدة من العميل)
- [ ] 1+ `meeting_drafted` event (لقاء محتمل)
- [ ] 3+ `risk_blocked` events (إن وجدت — تثبت أن النظام يحمي)
- [ ] 5+ `followup_created` events (متابعات مجدولة لـ 7 أيام)
- [ ] **1 Proof Pack** assembled عبر `GET /api/v1/proof-ledger/customer/{id}/pack`
- [ ] الـ Proof Pack PDF مُرسَل بالبريد للـ recipients
- [ ] `ServiceSession` بـ status=`proof_generated`
- [ ] CEO Brief نهاية الأسبوع مذكور فيه أن `customer:{id}` انتهى Pilot

عند تحقق هذه البنود → خلال 24 ساعة، احجز Upgrade call.

---

## القسم 3: Workflow Execution (التنفيذ بالـ APIs)

### الخطوة 1 — افتح الـ session
```bash
curl -X POST $BASE_URL/api/v1/delivery/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "service_id": "growth_starter",
    "customer_id": "demo_co_001",
    "owner": "founder@dealix.me",
    "inputs": { "company_name": "...", "ideal_customer": "...", ... }
  }'
```
يُرجع `session_id` + `deadline_at` (after 168 hours).

### الخطوة 2 — كل يوم: أنشئ proof events
لكل فرصة:
```bash
curl -X POST $BASE_URL/api/v1/proof-ledger/events \
  -d '{
    "unit_type": "opportunity_created",
    "customer_id": "demo_co_001",
    "session_id": "svc_xxx",
    "service_id": "growth_starter",
    "actor": "founder",
    "label_ar": "شركة [الاسم] — [القطاع] — fit_score 0.82"
  }'
```

لكل draft:
```bash
curl -X POST $BASE_URL/api/v1/proof-ledger/events \
  -d '{
    "unit_type": "draft_created",
    "customer_id": "demo_co_001",
    "session_id": "svc_xxx",
    "approval_required": true,
    "approved": false,
    "label_ar": "Email draft للمدير التنفيذي [الاسم]"
  }'
```

عند موافقة العميل:
```bash
curl -X POST $BASE_URL/api/v1/proof-ledger/events \
  -d '{
    "unit_type": "approval_collected",
    "customer_id": "demo_co_001",
    "session_id": "svc_xxx",
    "approved": true,
    "actor": "customer"
  }'
```

عند رفض حركة غير آمنة:
```bash
curl -X POST $BASE_URL/api/v1/proof-ledger/events \
  -d '{
    "unit_type": "risk_blocked",
    "customer_id": "demo_co_001",
    "session_id": "svc_xxx",
    "risk_level": "high",
    "label_ar": "محاولة WhatsApp بدون opt-in — مُنعت"
  }' && \
curl -X POST $BASE_URL/api/v1/observability/unsafe/record \
  -d '{
    "pattern": "cold_whatsapp",
    "blocked_reason": "no_opt_in_for_target",
    "customer_id": "demo_co_001"
  }'
```

### الخطوة 3 — يوم 7: ابن Proof Pack
```bash
curl $BASE_URL/api/v1/proof-ledger/customer/demo_co_001/pack
```
يُرجع dict كامل (انظر `proof_pack_builder.py`).

استخدم الـ output لبناء PDF (manual أو via template). أرسله للعميل.

### الخطوة 4 — انقل الـ session إلى delivered
```bash
curl -X POST $BASE_URL/api/v1/delivery/sessions/svc_xxx/transition \
  -d '{
    "to_status": "delivered",
    "actor": "founder",
    "deliverables": [
      {"type": "proof_pack_pdf", "url": "https://..."},
      {"type": "opportunities_csv", "url": "https://..."}
    ]
  }'

# ثم:
curl -X POST $BASE_URL/api/v1/delivery/sessions/svc_xxx/transition \
  -d '{"to_status": "proof_generated", "proof_pack_url": "https://..."}'

# ثم:
curl -X POST $BASE_URL/api/v1/delivery/sessions/svc_xxx/transition \
  -d '{"to_status": "upgrade_pending", "next_step": "schedule_upgrade_call"}'
```

---

## القسم 4: Upgrade Call Script (Pilot → Growth OS)

بعد تسليم Proof Pack بـ 24-48 ساعة، احجز call 30 دقيقة.

### Opening (5 دقائق)
```
شكراً وقتك. باختصار شو حصل في الـ Pilot:
- X فرصة جديدة سُجِّلت
- Y رسالة approved من فريقكم
- Z مخاطر منعها النظام
- ~W ريال أثر إيرادي مُقدّر
- 1 Proof Pack مُسلَّم

السؤال: تستمر معنا شهرياً أو نوقف؟
```

### Discovery (10 دقائق — استمع)
- ما الذي أعجبكم؟
- ما الذي أزعجكم؟
- ما الذي تريدون أن يتحسن؟
- هل تستطيعون شخصياً اعتماد القرار؟

### Pitch (10 دقائق)
```
Executive Growth OS = 2,999 ريال شهرياً.
يشمل:
- CEO Daily Brief (3 قرارات يومياً)
- Sales / Growth / Service cards حسب أدوارك
- Approval queue يومي (نفس الـ approval-first)
- Weekly Proof Pack (نفس مستوى الـ Pilot)
- Quarterly Business Review
- كل القنوات تبقى approval-first — صفر cold WhatsApp / scraping

الفرق الأكبر عن Pilot:
- يومي بدلاً من أسبوعي
- متعدد الأدوار بدلاً من واحد
- توقعات MRR + خطة ربعية
```

### Close (5 دقائق)
| الـ Reply | الرد |
|---|---|
| "نعم" | جهّز invoice manual، يبدأ شهر مايو |
| "أحتاج أراجع مع الفريق" | سامبل meeting brief للفريق + متابعة بعد 48 ساعة |
| "السعر مرتفع" | "Pilot 499 أثبت Y ريال أثر — Growth OS يستهدف 10x ذلك" |
| "ليس الآن" | "أوقف الـ session بـ proof محفوظ. عُد بعد شهر بـ Pilot ثاني" |

---

## القسم 5: المُسلَّمات (Deliverables)

كل عميل Pilot يستلم:
1. **Proof Pack PDF** (1-page summary + 3-pages detail)
2. **Opportunities CSV** (10 rows: company / contact / why_now / channel / risk)
3. **Drafts folder** (8 رسائل عربية في Markdown أو DOC)
4. **Risk Notes Memo** (1 page — ما الذي رفضناه ولماذا)
5. **7-Day Followup Plan** (calendar export ICS)
6. **Upgrade Recommendation** (1 page — Growth OS أو لا، مع المبررات)

كل ذلك يُحفظ في:
- `/customers/{customer_id}/pilot_001/` على Drive (أو S3)
- مُعلَّم في `ServiceSessionRecord.deliverables_json`
- مُعلَّم في `ProofEventRecord` (`proof_generated`)

---

## القسم 6: ما لا تفعله أثناء Pilot

- ❌ لا توعد بأرقام محددة أبعد من Proof Pack
- ❌ لا ترسل draft بدون موافقة العميل (حتى لو "بدا لطيف")
- ❌ لا تطلب payment تلقائي — كل invoice manual
- ❌ لا تستخدم بياناتهم لـ "case study" بدون موافقة كتابية
- ❌ لا تستخدم WhatsApp business لإرسال drafts — استخدم email فقط
- ❌ لا تقدّم خصم > 0 — Pilot 499 ثابت

---

## القسم 7: المؤشرات (لكل Pilot)

| المؤشر | الهدف |
|---|---|
| Time-to-first-proof | < 168 ساعة |
| Drafts created | ≥ 8 |
| Drafts approved by customer | ≥ 6 (75%+ acceptance) |
| Risks blocked | ≥ 1 (يثبت قيمة السلامة) |
| Customer satisfaction (post-call) | ≥ 4/5 |
| Upgrade conversion (Pilot → Growth OS) | ≥ 30% |

---

**الخلاصة:** Pilot 499 ليس "تجربة"؛ هو contract موقَّع من قبل النظام
بأن العميل سيستلم Proof Pack حقيقي خلال 7 أيام. كل إنجاز مسجَّل في
الـ ledger. لا يوجد "trust me bro" — كل شيء بـ proof.
