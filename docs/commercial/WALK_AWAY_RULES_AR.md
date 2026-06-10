# Walk-Away Rules — قواعد الانسحاب
**Dealix — Agent #3**

> **الغرض:** متى نقول "لا" ونمشي. حماية المؤسس، العميل المحتمل، والسمعة.

---

## 1. The Core Rule

**Walk away = professional selectivity, not rejection.**

المشي بكرامة = خدمة للطرفين:
- للمؤسس: يحمي الوقت، الهامش، السمعة
- للعميل: لا يدخل في شيء لا يناسبه

---

## 2. The 10 Hard Walk-Away Conditions

### 2.1 Spam Request
- **Trigger:** طلب cold email blast، WhatsApp bulk، LinkedIn automation
- **Why:** PDPL violation + reputation risk
- **Action:** رفض واضح + redirect لبديل
- **No override**

### 2.2 Guaranteed Revenue Claim
- **Trigger:** طلب ضمان نتائج، ROI مضمون
- **Why:** يخالف `claim_policy.yaml`
- **Action:** رفض + شرح حدودنا
- **No override**

### 2.3 Unpaid Heavy Custom Build
- **Trigger:** طلب POC مجاني كبير، custom build مجاني
- **Why:** delivery burden + margin loss
- **Action:** اعرض diagnostic مدفوع أو POC صغير بـ fee
- **No override**

### 2.4 Refusal of Approval Process
- **Trigger:** يرفض workflow الموافقة (auto-send)
- **Why:** يكسر SOAEN + governance
- **Action:** لا deal بدون approval
- **No override**

### 2.5 Refusal of Privacy Basics
- **Trigger:** لا يوافق على PDPL، DPA، data retention
- **Why:** compliance risk
- **Action:** لا deal بدون PDPL consent
- **No override**

### 2.6 Illegal Scraping Request
- **Trigger:** طلب scrape لـ data بدون consent
- **Why:** يخالف `no_scraping` rule + قانون
- **Action:** رفض قاطع
- **No override**

### 2.7 No Decision Maker Access (after 3 attempts)
- **Trigger:** لا يمكن الوصول لـ CEO/Owner/Head
- **Why:** لا يمكن اتخاذ قرار
- **Action:** archive + nurture if possible
- **Override:** founder في حالات خاصة

### 2.8 No Budget (with no future)
- **Trigger:** < 5,000 SAR budget بدون شريك أو future
- **Why:** لا هامش
- **Action:** nurture أو disqualify
- **Override:** founder مع reason

### 2.9 Bad-Fit Profile
- **Trigger:** 5+ red flags (PHASE 2 disqualification)
- **Why:** founder time wasted
- **Action:** disqualify
- **Override:** founder في strategic cases

### 2.10 Abusive Behavior
- **Trigger:** aggressive، insulting، threatening
- **Why:** team safety
- **Action:** walk away + blacklist
- **No override**

---

## 3. The Soft Walk-Away Conditions (with Founder Override)

### 3.1 Founder-Led with No Backup
- **Trigger:** decision maker = founder but no team
- **Override:** founder approval
- **Mitigation:** milestone-based

### 3.2 Regulated Industry without Compliance Review
- **Trigger:** health, finance, education with sensitive data
- **Override:** founder approval after compliance review
- **Mitigation:** compliance review + DPA

### 3.3 Multi-Stakeholder Confusion
- **Trigger:** لا يوجد decision maker واحد واضح
- **Override:** founder approval if champion واضح
- **Mitigation:** multi-meeting approach

### 3.4 Public Company / Regulated Entity
- **Trigger:** listed company، حكومي
- **Override:** founder + legal review
- **Mitigation:** legal + procurement

### 3.5 Recent Bad Experience
- **Trigger:** tried automation before and failed
- **Override:** founder approval
- **Mitigation:** discovery deeper + reset expectations

### 3.6 Geographic Distance
- **Trigger:** remote area without digital workflow
- **Override:** founder approval
- **Mitigation:** digital-only delivery

---

## 4. The Walk-Away Conversation

### 4.1 Tone
- مهني، لا attack
- مفيد، redirect لبديل
- brief، لا تبرير طويل
- يذكر السبب بوضوح

### 4.2 Template
```
"شكراً لاهتمامك. بعد المراجعة، أرى أن [سبب عدم الأهلية] 
يجعل شراكتنا غير مثالية في الوقت الحالي. أقترح:
1. [بديل 1]
2. [بديل 2]
3. [nurture للوقت المناسب]

بالتوفيق."
```

### 4.3 Forbidden Phrases
- ❌ "لسنا مهتمين" (cold)
- ❌ "لا نعمل معكم" (personal)
- ❌ "غير مؤهلين" (judgmental)
- ❌ "فاشل" / "ضعيف" (insulting)

---

## 5. Walk-Away Documentation

```yaml
- walk_away_id: "wa_001"
- opportunity_id: "opp_001"
- client_name: "Acme"
- reason: "spam_request"
- walk_away_type: "hard" # or "soft"
- conversation_date: "2026-06-03"
- message_sent: "شكراً لاهتمامك..."
- redirect_to: "nurture"
- founder_approved: true
- approved_at: "2026-06-03"
- notes: "Asked for 10K email blast"
```

---

## 6. After Walking Away

### 6.1 Documentation
- Log reason
- Update ICP if pattern
- Update qualification

### 6.2 Communication
- Polite message
- No future outreach (unless they re-engage)
- Mark do_not_contact if appropriate

### 6.3 Internal
- Team learns from pattern
- Update training
- Update objection bank

---

## 7. Walk-Away Metrics

### 7.1 Tracking
- Walk-away rate (target: 20-30% = selective)
- Reasons distribution
- Override rate (target: < 5% of soft)
- Recovery rate (did they come back?)

### 7.2 Healthy
- 20-30% walk away = selective
- < 10% walk away = accepting bad fit
- > 50% walk away = quality issue in pipeline

---

## 8. The Founder Override

### 8.1 When
- Strategic value
- High potential
- Specific situation

### 8.2 Process
- Document reason
- Risk acknowledged
- Special terms
- Close monitoring

### 8.3 Limit
- Max 5% of soft walk-aways
- If higher = re-evaluate qualification

---

## 9. The "Maybe" Category (Not Walk-Away)

### 9.1 When
- Some concerns but not deal-breakers
- Worth more discovery
- Timing issue

### 9.2 Process
- Nurture with quarterly check-in
- Re-evaluate in 6-12 months
- Don't disqualify yet

---

## 10. The Recovery Path

### 10.1 When Client Returns
- Re-qualify
- Don't assume past
- Fresh start

### 10.2 When Pattern Emerges
- ICP issue
- Channel issue
- Founder decision

---

## 11. Companion Files

- Risk: `COMMERCIAL_RISK_REGISTER_AR.md`
- Bad-fit: `BAD_FIT_CLIENT_POLICY_AR.md`
- Disqualification: `DISQUALIFICATION_RULES_AR.md` (PHASE 2)
- Objection: `OBJECTION_BANK_AR.md` (PHASE 8)
- Decision: `COMMERCIAL_DECISION_RULES_AR.md` (PHASE 1)

---

**المشي = selectivity، لا rejection. founder يحمي، العميل المحتمل يربح (مع nudge)، السمعة تبقى.**
