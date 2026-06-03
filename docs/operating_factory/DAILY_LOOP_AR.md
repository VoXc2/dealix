# Dealix Daily Operating Loop — الحلقة اليومية

> *آخر تحديث: 2026-06-03* — التوقيت: السعودية (AST / UTC+3)
> الملف الأب: `DEALIX_MAXIMUM_REVENUE_FACTORY_AR.md`

الحلقة اليومية تمشي من **اكتشاف الشركات** إلى **الأمر القيادي للمؤسس**. كل خطوة
لها: مُدخل، مخرج، مالك، وبوابة جودة. لا تنتقل خطوة قبل أن تمرّ على بوابتها.

---

## الجدول اليومي

| الساعة | الخطوة | المالك | المُخرج |
|:------:|--------|--------|---------|
| 06:00 | Account Discovery | وكيل البحث | قائمة شركات جديدة (مصادر عامة) |
| 07:00 | Account Intelligence Packs | وكيل البحث | 400 Account Packs |
| 08:00 | Contact Discovery | وكيل البحث | قنوات تواصل + `contact_confidence` |
| 09:00 | Email Draft + Call Brief | وكيل الصياغة | مسودات + Call Briefs |
| 10:00 | Quality Gate + Top 100 | المشغّل | Top 100 Queue |
| 11:00 | Founder / Operator Review | **المؤسس** | موافقات/رفض |
| 12:00 | Send / Call Handoff | **إنسان** | إرسال/اتصال فعلي |
| 14:00 | Reply + Objection Classification | المشغّل | تصنيف الردود |
| 16:00 | Mini Proposal Queue | وكيل العروض | عروض مصغّرة جاهزة للمراجعة |
| 18:00 | Delivery Pipeline Review | وكيل التسليم | حالة التسليم |
| 19:00 | Founder Daily Super Command | **المؤسس** | قرارات الغد |

---

## تفصيل الخطوات

### 06:00 — Account Discovery
- **المُدخل:** قطاعات/مدن مستهدفة + معايير الاكتشاف من حلقة الأمس (Learn).
- **المخرج:** شركات جديدة من **مصادر عامة مشروعة فقط**.
- **البوابة:** لا قوائم مشتراة، لا قواعد مسرّبة، لا جهات مُختلقة.
- **يكتب إلى:** `company_os/revenue/prospects.csv` (مرحلة Target).

### 07:00 — Account Intelligence Packs
- **المُدخل:** الشركات المكتشفة.
- **المخرج:** 400 Account Packs (راجع بنية الـ Pack في الدستور §5).
- **البوابة:** كل Pack يجب أن يحمل `public_signal` حقيقيًا و`recommended_system`.
- **التوزيع:** Revenue 100 / Follow-up 90 / Executive 70 / WhatsApp 70 / Proposal 70.

### 08:00 — Contact Discovery
- **المخرج لكل شركة:**
  ```txt
  contact_page_url · phone_if_public · email_if_public
  public_social_links · contact_form_available
  likely_decision_maker_role · best_contact_route
  contact_confidence (C0–C4) · source · last_checked_at
  ```
- **البوابة:** إذا `C0/C1` → لا إرسال ولا اتصال؛ يُعاد البحث أو نموذج رسمي فقط.
- **مرجع:** `QUALITY_GATES_AR.md` ← Contact Confidence.

### 09:00 — Email Draft + Call Brief Generation
- **المخرج:** مسودة إيميل لكل فرصة مؤهّلة + Call Brief.
- **البوابة:** الإيميل يمرّ على **6 بوابات** (Evidence / Personalization / System Fit /
  Claim Safety / Deliverability / Founder Approval).
- **يكتب إلى:** `company_os/revenue/outreach_queue.json` (مسودة، غير مُرسلة).

### 10:00 — Quality Gate + Top 100 Queue
- **المُدخل:** كل المسودات + Scores.
- **المخرج:** **Top 100** مرتّبة حسب `cash_priority_score` + Email Score.
- **البوابة:** يُرفض ما Email Score < 70؛ ما بين 70–79 يُعاد كتابته.

### 11:00 — Founder / Operator Review
- **المالك:** المؤسس.
- **القرار:** موافقة/رفض كل عنصر في Top 100 (إرسال، اتصال، عرض).
- **يكتب إلى:** `company_os/governance/approval_queue.json` (`approved: true/false`).

### 12:00 — Send / Call Handoff
- **المالك:** **إنسان** (ليس وكيلًا).
- **العمل:** إرسال أفضل 20 إيميل، تجهيز أفضل 30 اتصال.
- **البوابة:** لا يُرسل/يُتصل إلا ما عليه `approved: true`.

### 14:00 — Reply + Objection Classification
- **المخرج:** تصنيف كل ردّ (مهتم / أرسل تفاصيل / سؤال سعر / غير مهتم / لا تتواصل…).
- **يكتب إلى:** `company_os/revenue/objections.json` و`followups.json`.
- نتيجة `do_not_contact` → تُضاف فورًا إلى قائمة الـ Suppression.

### 16:00 — Mini Proposal Queue
- **المُدخل:** الفرص بنتيجة `interested` / `send_more_info`.
- **المخرج:** Mini Proposal صفحة واحدة لكل فرصة (نفس اليوم).
- **البوابة:** Proposal Approval Gate (لا سعر مفقود، لا scope مفتوح، لا ضمان).

### 18:00 — Delivery Pipeline Review
- **المُدخل:** الصفقات بحالة `won`.
- **المخرج:** حالة كل تسليم + العوائق (bottlenecks).
- **يكتب إلى:** `company_os/delivery/` + `company_os/war_room/`.

### 19:00 — Founder Daily Super Command
- **المالك:** المؤسس.
- **المخرج:** قرارات الغد:
  ```txt
  ماذا نرسل غدًا؟ من نتصل؟ أي عرض نقدّم؟ أي تسليم نبدأ؟
  ما تركيز الاكتشاف غدًا؟ (يُغذّي 06:00)
  ```
- **يُلخَّص في:** `reports/operating_factory/DAILY_LOOP_STATUS.md` و
  `company_os/war_room/REVENUE_WAR_ROOM_TODAY.md`.

---

## تغطية التدفّق الكامل

```txt
Discover(06) → Score(07) → Contact(08) → Draft(09) → Gate+Queue(10)
→ Approve(11) → Send/Call(12) → Reply/Classify(14) → Mini Proposal(16)
→ Delivery(18) → Founder Command(19) → (تركيز اكتشاف الغد يعود إلى 06)
```

كل حلقة يومية تُنتج مُدخلًا واحدًا على الأقل لحلقة التعلّم الأسبوعية.

---

*Dealix Daily Operating Loop | Version 1.0 | 2026-06-03*
