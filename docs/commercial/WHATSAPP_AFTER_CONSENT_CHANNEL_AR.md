# WhatsApp After-Consent Channel — قناة واتساب بعد الموافقة
**Dealix — Agent #3**

> **الغرض:** استخدام WhatsApp Business Platform بطريقة أخلاقية، بعد موافقة العميل، بدون spam.

---

## 1. The Core Rule

**WhatsApp = service channel، لا marketing channel.**

**الاستخدام المسموح:**
- ✅ بعد موافقة صريحة
- ✅ service messages (existing customers)
- ✅ رد على inquiry
- ✅ utility templates (approved)

**الاستخدام الممنوع:**
- ❌ cold WhatsApp (no consent)
- ❌ bulk messages
- ❌ marketing without consent
- ❌ group spam
- ❌ catalog spam

---

## 2. WhatsApp Business Platform Rules

### 2.1 What's Allowed (per Meta)
- Customer service (existing relationship)
- Transactional notifications (orders, appointments)
- Utility messages (approved templates)
- Authentication (one-time passwords)
- Marketing (only with explicit opt-in)

### 2.2 What's Not Allowed
- General-purpose AI chatbots (per Meta policy shifts)
- Cold outreach
- Bulk messaging
- Spam-like behavior
- Template violations

### 2.3 Reference
- WhatsApp Business Platform ≠ general chatbot
- Meta's policy shifts toward "business workflow assistant" after consent
- We position Dealix as workflow assistant, not open chatbot

---

## 3. Consent Capture

### 3.1 When to Capture
- On website (chat widget)
- After inquiry (via email/website form)
- After purchase (in onboarding)
- Explicit opt-in

### 3.2 Consent Format
- "أوافق على التواصل عبر WhatsApp للخدمة"
- Clear: what, when, opt-out
- Documented
- Revocable

### 3.3 Without Consent
- Don't message on WhatsApp
- Use email or website
- Or wait for them to message you first

---

## 4. The 24-Hour Window

### 4.1 Rule
- Once user messages you, you have 24h to reply freely
- After 24h: must use pre-approved template
- Templates must be utility/transactional

### 4.2 Templates
- Pre-approved by Meta
- 24h+ use only
- Must be specific (not generic)
- Variables allowed (e.g., order number)

### 4.3 Example Templates
- Appointment reminder: "Hi [Name], your appointment is on [date]"
- Order update: "Hi [Name], your order [X] has shipped"
- Support reply: "Hi [Name], we're looking into your issue [Y]"

---

## 5. Use Cases for Dealix

### 5.1 Service Messages (post-purchase)
- Onboarding welcome
- Weekly check-in (with consent)
- Renewal reminder
- Support follow-up
- Delivery update

### 5.2 Inquiry Response
- Reply to inbound WhatsApp inquiry
- Within 24h
- Service-oriented, not marketing

### 5.3 Appointment/Booking
- Confirmation
- Reminder
- Reschedule
- (with consent)

### 5.4 NOT Allowed
- ❌ Cold outreach
- ❌ "Did you see our offer?"
- ❌ Bulk marketing
- ❌ Group invites

---

## 6. The Approval Workflow

```
Consent captured
   ↓
[If inquiry] Reply within 24h (free)
   ↓
[If 24h+] Use approved template
   ↓
Founder approves message (if marketing)
   ↓
Send via approved tool (Moyasar / 360dialog)
   ↓
Track (delivery, read, reply)
   ↓
Update CRM
   ↓
Respect opt-out (immediate)
```

---

## 7. Templates We Use

### 7.1 Welcome (post-purchase)
```
"مرحباً [Name]،

شكراً لاختيارك Dealix. أنا [founder name]، 
سأتابع معك خلال [X] يوم.

أول خطوة: [specific].

أي سؤال، أنا هنا.
Dealix"
```

### 7.2 Appointment Reminder
```
"مرحباً [Name]،

تذكير: موعدك يوم [date] في [time].

إذا تحتاج تعدل، أخبرني.
Dealix"
```

### 7.3 Weekly Check-in (retainer)
```
"مرحباً [Name]،

إليك تحديث أسبوعي:
- [progress 1]
- [progress 2]
- [next step]

أي سؤال، تواصل معي.
Dealix"
```

### 7.4 Renewal Reminder
```
"مرحباً [Name]،

عقدك ينتهي في [X] يوم. 
هل نحتاج نجدد؟

Dealix"
```

---

## 8. Anti-Patterns

### 8.1 ❌ Don't Do
- ❌ Cold WhatsApp
- ❌ Bulk messages
- ❌ Marketing without consent
- ❌ "Just checking in" (vague)
- ❌ Late night messages
- ❌ Multiple messages same day
- ❌ Group spam
- ❌ Auto-replies that look human

### 8.2 ✅ Do
- ✅ Wait for consent
- ✅ Service-oriented
- ✅ Specific value
- ✅ Respect time
- ✅ One message per topic
- ✅ Easy opt-out
- ✅ Real human (when needed)

---

## 9. Metrics

| Metric | Target |
|--------|--------|
| Delivery rate | > 95% |
| Read rate | > 60% |
| Reply rate | > 30% |
| Opt-out rate | < 2% |
| Spam report | < 0.1% |
| Conversion (lead to customer) | > 20% |

---

## 10. Tools

- **WhatsApp Business Platform** (Cloud API or on-prem)
- **Provider:** Twilio, 360dialog, MessageBird (with approval)
- **Templates:** approved by Meta
- **Tracking:** built-in
- **CRM integration:** manual or via Zapier

---

## 11. Positioning as Business Workflow Assistant

### 11.1 Why
- Meta's policy shifts away from "general-purpose AI chatbots"
- WhatsApp Business Platform ≠ open chatbot interface
- Better: position as "business workflow assistant" after consent/interest

### 11.2 What This Means
- We use WhatsApp for service, not open chat
- Customer reaches out (or has consented)
- We reply with structured workflow
- Not a free-form AI chatbot
- Aligns with Meta policy

---

## 12. Companion Files

- Channel: `CHANNEL_STRATEGY_AR.md`
- Cold Email: `COLD_EMAIL_CHANNEL_AR.md`
- Existing: `data/templates/whatsapp_templates_collection.md`
- Existing: `data/templates/warm_intro_whatsapp_ar.md`
- Existing: `dealix/config/outreach_templates.yaml`

---

**WhatsApp = service، لا marketing. بعد موافقة، خدمة، احترام. founder يقرّر، النظام يحمي، Meta يوافق.**
