# Commercial Decision Rules — قواعد القرار التجاري
**Dealix — Agent #3**

> **الغرض:** كل سؤال تجاري شائع يجب أن يكون له جواب مختصر، ومسار قرار، ومالك، وميّزات قبول/رفض.

---

## 1. How to Use This File

كل قاعدة في هذا الملف تتبع نفس النمط:
- **السؤال** (Question)
- **القاعدة** (Rule)
- **صاحب القرار** (Owner)
- **قبول** (Yes condition)
- **رفض** (No condition)
- **الإحالة** (Reference)

---

## 2. ICP Decisions

### 2.1 هل هذا العميل ضمن ICP؟
| الشرط | المالك | Yes | No |
|-------|-------|-----|-----|
| هل عنده leads متكررة؟ | ICP Agent | ≥10 leads/week | → B-only or nurture |
| هل عنده decision maker معروف؟ | ICP Agent | اسم + دور | → bad fit |
| هل عنده budget ≥ 5,000 SAR؟ | ICP Agent | budget ≥ 5K | → bad fit or partner |
| هل عنده data readiness (CRM/file)? | ICP Agent | structure exists | → readiness scan first |
| هل القطاع مسموح؟ | ICP Agent | B2B in target list | → not for us |

**التفصيل:** `icp_primary.yaml` + `disqualifiers`

### 2.2 أي Motion؟ (A/B/C/D)
| Symptom | Motion |
|---------|--------|
| عميل = وكالة تسويق | A |
| عميل = عيادة/تدريب/عقار/خدمات B2B | B |
| شريك CRM/automation/consultant | C |
| CEO/Governance/AI risk | D |

**التفصيل:** `icp_segments.yaml` + `MASTER_COMMERCIAL_OPERATING_PLAN_AR.md`

---

## 3. Pricing Decisions

### 3.1 هل أعطي سعر؟
| الحالة | الإجراء |
|--------|---------|
| في مكالمة discovery جارية | ✅ نعم، range فقط (مثل "8-18K") |
| في مرحلة negotiation | ✅ نعم، final بعد founder approval |
| قبل discovery | ❌ لا، نحتاج pain + scope |
| في رسالة cold | ❌ لا، PDPL + reputation |

### 3.2 أي tier من Diagnostic؟
| Symptom | Tier | السعر |
|---------|------|-------|
| Agency صغير، urgent | starter | 4,999 SAR |
| B2B متوسط، pain واضح | standard | 9,999 SAR |
| Enterprise سعودي، governance | executive | 15,000 SAR |
| Multi-unit / regulated | enterprise | 25,000 SAR |

**التفصيل:** `pricing.yaml`

### 3.3 Discount؟
| الحالة | الإجراء |
|--------|---------|
| في النطاق (within range) | ✅ founder يوافق (default) |
| < 15% discount | ✅ founder approval |
| > 15% discount | ⚠️ founder + CCO approval + reason logged |
| > 30% discount | ❌ رفض (أو scope reduction) |
| بسبب تردد العميل | ❌ رفض |
| بسبب partner referral | ✅ ممكن (per `partner_rules.yaml`) |
| بسبب case study permission | ✅ ممكن |
| بسبب fast payment | ✅ ممكن |

**التفصيل:** `DISCOUNT_POLICY_AR.md`

### 3.4 Final Price Approval Levels
| Level | الإجراء | Approval |
|-------|---------|----------|
| L1 | في نطاق published | founder auto-approve |
| L2 | < 15% discount | founder |
| L3 | > 15% discount | founder + reason logged |
| L4 | Custom enterprise > 50K | founder + legal review |
| L5 | Legal/sensitive | founder + legal counsel |

---

## 4. Proposal Decisions

### 4.1 هل أرسل Proposal؟
| الشرط | Yes | No |
|-------|-----|-----|
| هل تم discovery؟ | ✅ | ❌ |
| هل pain category معروف؟ | ✅ | ❌ |
| هل يوجد product match؟ | ✅ | ❌ |
| هل success metric محدد؟ | ✅ | ❌ |
| هل scope واضح؟ | ✅ | ❌ |
| هل في budget ≥ tier? | ✅ | ❌ |
| هل founder وافق؟ | ✅ | ❌ |

### 4.2 ما الذي يجب أن يكون في Proposal؟
- Client + sector
- Problem (with pain category)
- Why now
- Product/offer
- Scope (in / out)
- Deliverables
- Timeline
- Price range
- Payment terms
- Assumptions
- Risks
- Evidence level
- Next step
- Approval status

**التفصيل:** `PROPOSAL_STRATEGY_AR.md`

### 4.3 متى أرفض Proposal؟
- ❌ لا discovery بعد
- ❌ Pain غير واضح
- ❌ Budget < 5K بدون partner
- ❌ Spam/guarantee request
- ❌ No decision maker access
- ❌ Delivery risk too high
- ❌ Legal/compliance blocker

---

## 5. Pipeline Decisions

### 5.1 هل أنقل lead من stage X إلى Y؟
استخدم `stage_transitions.yaml` — المرجع الرسمي. لا انتقالات عشوائية.

### 5.2 متى أغلق opportunity (closed_lost)؟
- 3 محاولات اتصال فاشلة
- لا رد بعد 30 يوم من last touch
- Bad fit اكتُشف بعد qualification
- Prospect طلب عدم المتابعة
- Budget/authority/timing غير متاح بعد 60 يوم

### 5.3 متى أحول إلى nurture؟
- Discovery لم تكتمل بعد 14 يوم
- Pain موجود لكن timing غير مناسب
- No budget الآن لكن قد يعود

---

## 6. Channel Decisions

### 6.1 هل أرسل cold email؟
| الشرط | Yes | No |
|-------|-----|-----|
| هل على قائمة opted-in؟ | ✅ | ❌ |
| هل في daily cap (50/يوم max)؟ | ✅ | ❌ |
| هل الرسالة customized؟ | ✅ | ❌ |
| هل unsubscribe link موجود؟ | ✅ | ❌ |
| هل SPF/DKIM/DMARC configured؟ | ✅ | ❌ |
| هل founder وافق على النسخة؟ | ✅ | ❌ |

**التفصيل:** `COLD_EMAIL_CHANNEL_AR.md`

### 6.2 هل أرسل WhatsApp؟
| الشرط | Yes | No |
|-------|-----|-----|
| هل العميل أعطى consent صريح؟ | ✅ | ❌ |
| هل الرسالة service-related (post-purchase)؟ | ✅ | ❌ |
| هل template approved + on allowlist؟ | ✅ | ❌ |
| هل 24h window محترم؟ | ✅ | ❌ |

**التفصيل:** `WHATSAPP_AFTER_CONSENT_CHANNEL_AR.md`

### 6.3 هل أكتب LinkedIn message؟
| الشرط | Yes | No |
|-------|-----|-----|
| هل يدوي 1:1؟ | ✅ | ❌ |
| هل بعد engagement سابق (like/comment)؟ | ✅ | ❌ |
| هل في founder's voice؟ | ✅ | ❌ |

---

## 7. Customer Success Decisions

### 7.1 متى أصنّف العميل كـ risk؟
- لا رد لـ 2 weekly reports متتالية
- Usage < 50% من المتوقع
- Unresolved blocker > 7 أيام
- Renewal discussion refused

### 7.2 متى أقترح expansion؟
- نجاح metric محقق
- Adoption > 70%
- New pain surfaced
- Renewal approaching
- Budget available

### 7.3 متى أقترح renewal؟
- 30 يوم قبل انتهاء العقد
- Health score ≥ yellow
- Usage data إيجابي
- Testimonial/case study provided (optional)

---

## 8. Partner Decisions

### 8.1 هل أوافق على partner؟
| الشرط | Yes | No |
|-------|-----|-----|
| هل عنده access to clients؟ | ✅ | ❌ |
| هل يفهم B2B services؟ | ✅ | ❌ |
| هل يقبل approval-first policy؟ | ✅ | ❌ |
| هل يبيع spam/guarantees؟ | ❌ | ✅ disqualify |
| هل legal entity موجود؟ | ✅ | ❌ |
| هل في 3 paid pilots (white-label)؟ | ✅ | ❌ |

**التفصيل:** `PARTNER_QUALIFICATION_AR.md`

### 8.2 أي partner model؟
| Symptom | Model |
|---------|-------|
| Lead فقط | referral |
| Co-deliver | co-sell |
| Full implementation | implementation_partner |
| Brand as theirs | white-label (3+ pilots first) |

---

## 9. Risk Decisions

### 9.1 متى أمشي (walk away)؟
- Spam/guarantee request
- Unpaid heavy custom build
- Refusal of approval process
- Refusal of privacy basics
- Illegal scraping request
- Demands final price without discovery
- Abusive behavior
- Delivery impossible at price
- No client-side owner

**التفصيل:** `WALK_AWAY_RULES_AR.md`

### 9.2 متى أرفع escalation؟
- Discount > 30%
- Custom enterprise > 50K
- Legal/regulatory claim
- Refund request
- Partner white-label
- Public case study with name

---

## 10. Finance Decisions

### 10.1 هل أوقف channel؟
| المؤشر | Yes (stop) | No (continue) |
|--------|------------|---------------|
| Cost per lead | > 500 SAR | < 200 SAR |
| Cost per reply | > 200 SAR | < 100 SAR |
| Cost per meeting | > 1,000 SAR | < 500 SAR |
| Close rate | < 5% | > 15% |
| ROI | < 1x | > 3x |

### 10.2 هل أرفع السعر؟
- Delivery burden > 70% من السعر → ارفع أو قلل scope
- Founder time > 40% على delivery → hire
- Margin < 25% → ارفع أو غيّر offer

### 10.3 متى أوقف عرض؟
- 0 wins بعد 6 شهور
- Churn > 30%
- CAC > LTV
- Negative margin

---

## 11. Communication Tone Decisions

### 11.1 ما اللغة؟
| المستلم | اللغة |
|---------|--------|
| Saudi B2B (decision maker) | Arabic first |
| English-only prospect | English |
| Government/regulated | Arabic + formal |
| Tech-savvy founder | bilingual OK |

### 11.2 ما النبرة؟
| السياق | النبرة |
|--------|--------|
| Discovery call | consultative, curious |
| Proposal | professional, clear, specific |
| Proof pack | factual, evidence-based |
| WhatsApp (post-purchase) | friendly, service-oriented |
| LinkedIn | personal, founder voice |
| Email cold | professional, brief, no spam signals |

### 11.3 ما الذي لا نقوله أبدًا؟
- ❌ "ضمان 100%"
- ❌ "نتائج مضمونة"
- ❌ "عائد مضمون"
- ❌ "هذا ChatGPT بديل"
- ❌ "سيحل محل فريقك"
- ❌ "مجانًا" (إلا في readiness scan opt-in)
- ❌ "ضمان استرداد كامل" (إلا بسياسة refund_policy)

---

## 12. Escalation Chain (سلسلة التصعيد)

| المستوى | صاحب القرار | النوع |
|---------|--------------|-------|
| L0 | Agent (auto) | internal data |
| L1 | Founder (1 click) | daily decisions |
| L2 | Founder + reason | pricing, scope changes |
| L3 | Founder + CCO | discount > 15% |
| L4 | Founder + Legal | legal/regulated |
| L5 | Founder + Board | > 100K SAR or reputation risk |

---

## 13. Time-to-Decision Standards

| القرار | المهلة |
|--------|--------|
| Discovery reply | < 24 ساعة عمل |
| Proposal draft | < 3 أيام |
| Proposal final | < 5 أيام |
| Payment handoff | same day as approval |
| Inbound demo request | < 1 ساعة |
| Cold reply (qualified) | < 1 يوم عمل |
| Cold reply (cold) | لا نرد (blackhole) |
| Customer support | < 4 ساعات |

---

## 14. Stop Conditions (متى نتوقف فوراً)

- 🚨 Spam complaint rate > 0.1%
- 🚨 PDPL breach detected
- 🚨 Margin drops to 0
- 🚨 Founder burnout signals
- 🚨 3 consecutive deals in dispute
- 🚨 Legal letter received
- 🚨 Test failure > 5%
- 🚨 Production incident > 30 min
- 🚨 Unrecoverable delivery failure

---

**كل قرار يومي في Dealix يجب أن يجد قاعدته في هذا الملف. إذا لم يجد، ارفع للـ founder.**
