# Cold Email Channel — قناة البريد البارد
**Dealix — Agent #3**

> **الغرض:** قواعد استخدام cold email (warm only) بدون spam، مع احترام DMARC/SPF/DKIM.

---

## 1. The Core Rule

**Cold email = warm, manual, 1:1, founder-approved.**

❌ لا blast
❌ لا automation
❌ لا scraped lists
❌ لا misleading subject
❌ لا unsubscribe مخفي

---

## 2. The 5 Requirements for Cold Email

### 2.1 Deliverability
- SPF ✅ configured
- DKIM ✅ configured
- DMARC ✅ configured (`v=DMARC1; p=quarantine; rua=mailto:...`)
- Domain reputation: maintained
- Warmup: ramp slowly

### 2.2 List Hygiene
- Verified emails only
- Removed bounces immediately
- Honor unsubscribes instantly
- Segment by ICP

### 2.3 Content
- Customized (not template-only)
- Founder voice
- Clear CTA
- One-click unsubscribe
- Sender name = real person

### 2.4 Volume
- Max 50/day per sender
- Max 1 email/contact per 30 days
- Stop if bounce > 5%

### 2.5 Approval
- Each template: founder approved
- Each send batch: founder approved
- Founder manual send (or assistant)

---

## 3. Email Anatomy

### 3.1 Subject Line
- 6-8 words
- Specific (not "Quick question")
- Relevant to recipient
- No spam triggers (FREE, URGENT, !!!)

### 3.2 Body
- Hi [Name],
- 1-line context (why them)
- 1-line pain (hypothesis)
- 1-line value (what we do)
- 1-line CTA (low-friction)
- Sign off (real name, title, contact)

### 3.3 Length
- 50-100 words (cold)
- 100-200 words (warm)
- 200-300 words (deep relationship)

### 3.4 CTA Examples
- "15-min call next week?"
- "Worth a chat?"
- "Should I send a sample?"
- "Interested in [specific value]?"

---

## 4. Email Sequence (3 touches)

### 4.1 Day 0
- Initial outreach
- Customized

### 4.2 Day 3 (if no reply)
- Follow-up #1
- Add value (not just "checking in")
- Different angle

### 4.3 Day 7 (if no reply)
- Final follow-up
- "Closing the loop" tone
- Open to re-engage later

### 4.4 Day 14+
- Move to nurture
- Don't keep emailing

---

## 5. Forbidden Practices

### 5.1 ❌ Don't Do
- ❌ Buy lists
- ❌ Scrape emails
- ❌ Mass blast
- ❌ Misleading subject
- ❌ Hidden unsubscribe
- ❌ Fake sender
- ❌ Attachment in cold
- ❌ HTML heavy (text better)
- ❌ Same template for all
- ❌ Bypass DMARC

### 5.2 ✅ Do
- ✅ Custom subject
- ✅ Personal body
- ✅ Clear value
- ✅ Easy opt-out
- ✅ Real sender
- ✅ Plain text
- ✅ Founder voice
- ✅ One CTA
- ✅ Follow sequence
- ✅ Honor stops

---

## 6. Anti-Spam Indicators

### 6.1 Avoid
- ❌ All caps
- ❌ Multiple !!!
- ❌ Multiple ???
- ❌ "FREE", "URGENT", "ACT NOW"
- ❌ "Click here"
- ❌ Image-only
- ❌ Attachment (cold)
- ❌ Tracking pixels (cold)
- ❌ Link shorteners (cold)

### 6.2 Use
- ✅ Lower case
- ✅ Punctuation normal
- ✅ Specific, not generic
- ✅ Real links
- ✅ Text + image
- ✅ Real attachments (warm)

---

## 7. Metrics

| Metric | Target |
|--------|--------|
| Delivery rate | > 95% |
| Open rate | > 30% |
| Reply rate | > 5% |
| Bounce rate | < 5% |
| Spam complaint | < 0.1% |
| Unsubscribe | < 2% |
| Conversion to discovery | > 10% of reply |

---

## 8. Tools (Approved)

- **Email warmup:** Lemlist, Instantly (with care)
- **Verification:** ZeroBounce, NeverBounce
- **Tracking:** (avoid in cold)
- **Sending:** Gmail (manual), Outlook (manual)
- **List mgmt:** CRM, manual

---

## 9. The Approval Workflow

```
Draft template
   ↓
Founder approves (template once)
   ↓
Build list (verified, segmented)
   ↓
Founder approves (each batch)
   ↓
Send (founder manual)
   ↓
Track (replies, bounces, unsubs)
   ↓
Follow-up (if appropriate)
   ↓
Move to nurture (if no reply)
```

---

## 10. DMARC / SPF / DKIM

### 10.1 Why
- بدون DMARC: emails go to spam
- بدون SPF: spoofed
- بدون DKIM: tampered

### 10.2 Setup
- DNS: SPF record (allowed senders)
- DNS: DKIM (signature)
- DNS: DMARC (policy + reports)
- Monitor reports

### 10.3 Reference
- Wikipedia DMARC: "an email validation system... designed to detect and prevent email spoofing"
- Required by Gmail, Yahoo, etc. for bulk senders
- Required for one-click unsubscribe for marketing

---

## 11. When to Stop

- Spam complaint > 0.1% → stop
- Bounce > 10% → stop
- Domain reputation drop → stop
- Open < 10% → list quality issue
- Reply < 1% → content issue

---

## 12. Companion Files

- Channel: `CHANNEL_STRATEGY_AR.md`
- WhatsApp: `WHATSAPP_AFTER_CONSENT_CHANNEL_AR.md`
- Existing: `dealix/config/outreach_templates.yaml`
- Existing: `data/templates/warm_intro_whatsapp_ar.md`
- Existing: `docs/ops/GMAIL_OAUTH_SETUP_CHECKLIST.md`

---

**Cold email = warm, manual, 1:1. لا blast، لا automation. founder يوقّع، الـ DMARC يحمي، الـ list تنظف.**
