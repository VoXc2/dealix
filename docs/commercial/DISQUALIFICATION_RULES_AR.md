# Disqualification Rules — قواعد عدم الأهلية
**Dealix — Agent #3**

> **الغرض:** قائمة واضحة بـ **متى نقول "لا"** — للمحافظة على الوقت، الهامش، السمعة. امتداد لـ `icp_primary.yaml.disqualifiers` لكن أكثر تفصيلاً.

---

## 1. الفلسفة

**"لا" هي خدمة للمؤسس وللعميل في آن واحد:**
- للمؤسس: تحمي وقته، تسليمه، هامشه
- للعميل: لا يدخل في شيء لا يناسبه

**القاعدة الذهبية:** إذا كان هناك شك في الأهلية، ارجع للـ founder.

---

## 2. Hard Disqualifiers (رفض فوري — لا استثناء)

### 2.1 لا Leads Recurring
- **الشرط:** لا leads جديدة على الأقل 5/week
- **لماذا:** لا ROI ممكن
- **الإجراء:** redirect إلى nurture أو partner referral

### 2.2 No Decision Maker Access
- **الشرط:** لا يمكن الوصول لـ CEO/Owner/Head
- **لماذا:** لا يمكن اتخاذ قرار
- **الإجراء:** اطلب access أو nurture

### 2.3 No Budget
- **الشرط:** < 5,000 SAR budget (إلا partner referral)
- **لماذا:** لا هامش
- **الإجراء:** nurture أو partner

### 2.4 Wants Spam / Mass Sending
- **الشرط:** طلب cold email blast، WhatsApp bulk، LinkedIn automation
- **لماذا:** PDPL violation + reputation risk
- **الإجراء:** رفض واضح + redirect لبديل (warm only)

### 2.5 Wants Guaranteed Revenue Claims
- **الشرط:** طلب "ضمان 100% زيادة مبيعات"
- **لماذا:** يخالف `claim_policy.yaml.roi_or_guarantee.allowed: false`
- **الإجراء:** رفض + شرح حدودنا

### 2.6 Refuses Approval Process
- **الشرط:** يرفض workflow الموافقة (auto-send)
- **لماذا:** يكسر نظام SOAEN
- **الإجراء:** لا deal بدون approval

### 2.7 Refuses Data/Privacy Basics
- **الشرط:** لا يوافق على PDPL، DPA، data retention policy
- **لماذا:** compliance risk
- **الإجراء:** لا deal بدون PDPL consent

### 2.8 Asks for Illegal / Suspicious Scraping
- **الشرط:** طلب scrape لـ data بدون consent
- **لماذا:** يخالف `no_scraping` rule + قانون
- **الإجراء:** رفض قاطع

### 2.9 Wants Unpaid Heavy Custom Work
- **الشرط:** POC مجاني كبير، custom build مجاني
- **لماذا:** delivery burden
- **الإجراء:** اعرض diagnostic مدفوع أو POC صغير بـ fee

### 2.10 Delivery Risk Too High
- **الشرط:** scope غير واضح، client unavailable، data فوضوية جداً
- **لماذا:** فشل محتمل = reputation
- **الإجراء:** رفض أو readiness scan أولاً

---

## 3. Soft Disqualifiers (تحذير + founder approval)

### 3.1 Founder-Led with No Backup
- **الشرط:** decision maker = founder but no team
- **مخاطرة:** single point of failure
- **الإجراء:** founder approval

### 3.2 Regulated Industry Without Compliance Review
- **الشرط:** health, finance, education مع sensitive data
- **مخاطرة:** PDPL/health/financial regulations
- **الإجراء:** compliance review قبل proposal

### 3.3 Geographic Distance
- **الشرط:** client في منطقة بعيدة بدون online workflow
- **مخاطرة:** delivery cost
- **الإجراء:** digital-only delivery أو founder approval

### 3.4 Multi-Stakeholder Confusion
- **الشرط:** لا يوجد decision maker واحد واضح
- **مخاطرة:** طول cycle + فشل
- **الإجراء:** اطلب champion واضح أولاً

### 3.5 Public Company / Regulated Entity
- **الشرط:** listed company، حكومي
- **مخاطرة:** procurement, compliance
- **الإجراء:** legal review أولاً

### 3.6 Recent Bad Experience
- **الشرط:** tried automation قبل سنة وفشل
- **مخاطرة:** expectations مشوهة
- **الإجراء:** discovery أعمق + reset expectations

---

## 4. Time-Based Disqualifiers (مهلة القرار)

| الحالة | مهلة القرار | بعد المهلة |
|--------|-------------|-----------|
| Discovery not scheduled | 14 يوم | → nurture |
| Discovery not completed | 14 يوم بعد schedule | → reschedule once, then nurture |
| Proposal not responded | 14 يوم | → follow-up once, then closed_lost |
| Payment not received | 7 أيام after approval | → reminder + reschedule |
| Renewal discussion no response | 30 يوم | → escalate to founder |

---

## 5. Red Flag Phrases (عبارات إنذار)

إذا قالها prospect، فكّر في disqualification:

| العبارة | المؤشر | الإجراء |
|---------|--------|---------|
| "Just send 10,000 emails" | spam | hard disqualify |
| "Guaranteed leads" | scam | hard disqualify |
| "We need it by tomorrow" | unrealistic | reschedule |
| "Can you do everything for free first?" | bad fit | disqualify |
| "We don't need any approval" | no governance | disqualify |
| "I want to scrape LinkedIn" | illegal | hard disqualify |
| "We don't care about PDPL" | compliance risk | hard disqualify |
| "Just send WhatsApp to everyone" | spam | hard disqualify |
| "Guarantee 5x revenue" | claim violation | hard disqualify |
| "We don't have a CRM" | maturity issue | readiness scan first |

---

## 6. The "Bad-Fit Client" Profile

العميل السيئ عادةً لديه:
- ❌ لا budget ولا planning
- ❌ يطلب "كل شيء في يومين"
- ❌ يرفض governance
- ❌ pressure + aggression
- ❌ history of vendor conflicts
- ❌ unrealistic timeline
- ❌ focus on discount only
- ❌ wants custom but no clarity
- ❌ no internal owner
- ❌ wechselt decisions often

**القاعدة:** إذا رأيت 3+ من هذه → founder escalation + likely disqualify.

---

## 7. When to Override (متى نتجاهل disqualifier)

**لا تتجاوز أبداً** hard disqualifier (قسم 2).

**Soft disqualifier** يمكن تجاهله إذا:
- ✅ founder يوافق صراحة
- ✅ Risk is acknowledged and mitigated
- ✅ Has upside (high value, strategic, etc.)
- ✅ Price premium justifies risk

**السجل:** أي override يجب أن يُسجّل في `risk_register.yaml` مع reason.

---

## 8. The Disqualification Conversation (الرسالة)

### 8.1 Template
```
شكراً لاهتمامك. بعد المراجعة، أرى أن [سبب عدم الأهلية] يجعل شراكتنا
غير مثالية في الوقت الحالي. أقترح عليك:
1. [بديل 1]
2. [بديل 2]
3. [nurture للوقت المناسب]
```

### 8.2 Tone
- مهني، لا attack
- مفيد، redirect لبديل
- brief، لا تبرير طويل
- يذكر السبب بوضوح

### 8.3 Forbidden
- ❌ "لسنا مهتمين" (cold)
- ❌ "لا نعمل معكم" (personal)
- ❌ "غير مؤهلين" (judgmental)

---

## 9. Disqualification Metrics

تابع شهرياً:
- Disqualification rate (target: 30-50% — يثبت selectivity)
- Reasons distribution (top disqualifier patterns)
- Override rate (target: < 10%)
- Recovery rate (هل disqualifies ترجع في nurture؟)

**مؤشر صحي:** disqualification rate > 30% = we are selective.
مؤشر سيء: < 10% = we accept bad fit.

---

## 10. Companion Files

- ICP: `ICP_MATRIX_AR.md`
- Risk: `COMMERCIAL_RISK_REGISTER_AR.md` (PHASE 13)
- Walk-away: `WALK_AWAY_RULES_AR.md` (PHASE 13)
- Bad-fit policy: `BAD_FIT_CLIENT_POLICY_AR.md` (PHASE 13)

---

**Disqualification = professional selectivity, not rejection. قل "لا" مبكراً لتقول "نعم" بثقة لاحقاً.**
