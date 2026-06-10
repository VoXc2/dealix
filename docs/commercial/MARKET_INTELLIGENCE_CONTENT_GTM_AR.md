# محتوى وGTM — حزمة استخبارات السوق (12 أسبوعاً)

**قاعدة:** كل منشور = **مسودة → موافقة** · CTA واحد · لا أرقام سوق دقيقة كادعاء  
**آخر تحديث:** 2026-05-18

---

## 1) أعمدة المحتوى (SOAEN + سوق)

| عمود | رسالة | دليل L4+ قبل حملة مدفوعة |
|------|-------|---------------------------|
| AI بلا حوكمة | موافقة قبل إرسال | Proof / policy sample |
| CRM vs Revenue OS | Decision Passport | Sample passport |
| PDPL عملي | لغة آمنة | PDPL_LEGAL ملخص |
| Why Now 2030 | تحول مؤسسي | Business Now لقطة |
| Founder-led | نظام قبل التوظيف | War Room screenshot |
| Proof | قيمة مسلّمة | Sample Proof Pack |
| Build in public | تقدم حقيقي | evidence CSV (بدون أرقام وهمية) |

**حوكمة:** [COMMERCIAL_GOVERNANCE_GATES_AR.md](operations/COMMERCIAL_GOVERNANCE_GATES_AR.md) · `social_content_queue.yaml`

---

## 2) تقويم 12 أسبوع (مسودة)

| أسبوع | موضوع | CTA | قناة |
|-------|-------|-----|------|
| 1 | لماذا Revenue OS وليس CRM | Risk Score | LinkedIn |
| 2 | Decision Passport في 60 ثانية | Sample Proof | LinkedIn |
| 3 | PDPL + outreach — ما المسموح | Diagnostic | LinkedIn + `/learn` |
| 4 | قصة founder-led → نظام | Calendly 10min | LinkedIn |
| 5 | anti-waste: لا تسويق تحت L4 | Proof Pack | LinkedIn |
| 6 | Motion A — وكالات | ABM لمسة يدوية | LinkedIn + warm |
| 7 | إقامة بيانات — شفافية | RFP pack | LinkedIn |
| 8 | Sprint 499 — TTV | `/dealix-diagnostic` | LinkedIn |
| 9 | شريك قناة | `/partners` | LinkedIn |
| 10 | Case structure (بدون أرقام وهمية) | Proof | LinkedIn |
| 11 | RevOps أسبوعي | Business Now | LinkedIn |
| 12 | مراجعة ربع + What we learned | Digest | LinkedIn |

**تنفيذ:** `generate_weekly_content_drafts.py` · `queue_content_drafts_for_approval.py`  
**تقويم آلي:** [`dealix/config/market_intelligence_content_calendar.yaml`](../../dealix/config/market_intelligence_content_calendar.yaml)

---

## 3) قوالب منشور LinkedIn (AR)

### قالب A — Why Now
```
السوق السعودي للـ B2B SaaS ينمو — لكن المشتري اليوم يشتري:
① امتثال (PDPL)
② قرار موثّق (ليس فقط سجل صفقة)
③ AI بموافقة (ليس بوت بارد)

Dealix = Revenue OS عربي أولاً: مسودة → موافقة → Proof.

CTA: [رابط Risk Score أو ديمو 10 دقائق]
```

### قالب B — حوكمة
```
«الذكاء الاصطناعي للمبيعات» بدون حوكمة = مخاطرة سمعة + امتثال.

عندنا: Decision Passport + مستوى أدلة L0–L5 + لا واتساب/لينكد إن بارد.

إذا تبغى تشوف Sample Proof — رد «Proof» بالخاص (warm فقط).
```

### قالب C — إثبات
```
قبل Growth شهري: Proof Pack مسلّم.

سلمنا: [وصف عام بدون أرقام CRM مخترعة] — الأرقام من نظام العميل فقط.

الخطوة التالية للمهتمين: Diagnostic Ops — ليس «اشتراك من اليوم».
```

---

## 4) AEO و`/learn`

| slug مقترح | عنوان | يربط بـ |
|------------|-------|---------|
| `pdpl-outreach-saudi` | outreach وPDPL | PDPL_LEGAL |
| `decision-passport-b2b` | جواز القرار | GOVERNED_AI |
| `founder-led-revops` | RevOps مؤسس | FOUNDER_REVOPS |
| `revenue-os-vs-crm` | Revenue OS | POSITIONING |

**مرجع:** [AEO_CONTENT_CALENDAR_AR.md](operations/AEO_CONTENT_CALENDAR_AR.md)

---

## 5) مسار Lead من المحتوى

```mermaid
flowchart LR
  LI[LinkedIn_draft_approved]
  RS[/risk-score]
  PP[/proof-pack]
  DG[/dealix-diagnostic]
  MTG[Calendly_discovery]
  LI --> RS
  RS --> PP
  PP --> DG
  DG --> MTG
```

---

## 6) ممنوعات المحتوى (سوق + doctrine)

- ادعاء «معتمد SDAIA» أو «100% KSA hosting» بدون ملحق
- أرقام إيراد/عملاء غير موجودة في KPI import
- لقطات CRM حقيقية بدون إذن
- وعود تكامل أحمر في Truth Matrix
- CTA واتساب بارد جماعي

---

## 7) أسبوعي — مراجعة محتوى (15 دقيقة)

| # | سؤال |
|---|------|
| 1 | هل كل منشور الأسبوع مُوافَق عليه؟ |
| 2 | هل CTA واحد فقط per منشور؟ |
| 3 | هل يوجد Proof مرتبط بادعاء L4+؟ |
| 4 | هل SOAEN في digest متسق؟ |
| 5 | تحديث objection → منشور إن تكرر اعتراض |

**مرجع:** [MARKET_INTELLIGENCE_WEEKLY_REVIEW_CHECKLIST_AR.md](MARKET_INTELLIGENCE_WEEKLY_REVIEW_CHECKLIST_AR.md)
