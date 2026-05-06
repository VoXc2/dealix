# Day 1 Launch Kit — جاهز للنسخ واللصق

> **المؤسس:** افتح هذا الملف صباح الإثنين القادم. كل شيء في الأسفل
> جاهز للنسخ. الوقت الكلي: 60 دقيقة. النتيجة: 5 رسائل warm-intro
> أُرسلت يدوياً + 1 تشخيص جاهز للتسليم.

---

## ⏰ 08:30 — Production health check (5 دقائق)

```bash
# 1. تأكد أن الإنتاج على آخر commit
curl -s https://api.dealix.me/health
# يجب أن يرجع: {"git_sha":"6637270"} أو أحدث (ليس 8099b00 القديم)

# 2. تأكد أن جميع الـ 9 OSes تستجيب
for ep in full-ops support-os growth-os sales-os customer-success-os \
          delivery-os executive-os self-improvement-os partnership-os \
          revenue-pipeline; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://api.dealix.me/api/v1/$ep/status")
  echo "$ep: $code"
done

# 3. لو حصل أي 500/404 من الـ 10 → توقف، أبلغني، لا تكمل
```

**Go/No-Go:** إذا كل الـ 10 رجعوا 200 → كمل. لو حتى واحد فشل → توقف.

---

## ⏰ 08:35 — Generate first-10 board (دقيقتين)

```bash
cd ~/dealix  # أو مسار الـ repo عندك
python scripts/dealix_first10_warm_intros.py
# يُنشئ: docs/phase-e/live/FIRST_10_CUSTOMER_BOARD.{md,json}
# (gitignored — ما يُرفع للـ repo)
```

افتح `docs/phase-e/live/FIRST_10_CUSTOMER_BOARD.md` في محرر النصوص.

---

## ⏰ 08:40 — اختر 5 أسماء حقيقية (15 دقيقة)

افتح ملاحظاتك الخاصّة (Notion / Apple Notes / WhatsApp). اختر **5 أسماء** من شبكتك الشخصية تنطبق عليها هذه الشروط:

✅ **شروط القبول:**
- تعرفهم شخصياً (أو معرفة قوية مشتركة)
- يديرون شركة في أحد القطاعات الـ 3 الأولوية:
  - **Tier 1A:** وكالة تسويق (5-30 موظف، تخدم SMEs سعوديّة)
  - **Tier 1B:** خدمات B2B (محاماة/محاسبة/استشارات IT، فريق مبيعات < 5)
  - **Tier 1C:** استشارات أو تدريب (مستقل أو شركة صغيرة)
- يعانون من مشكلة واضحة من هذه الـ 4: leads، follow-up ضعيف، proof للعملاء، support تذاكر
- يُتوقع أنهم سيردّون عليك خلال 48 ساعة (لأنهم يعرفونك)

❌ **استبعد:**
- معرفة سطحية (أضفته على LinkedIn ولم تتحدثا)
- شركة كبيرة (>200 موظف — قرارهم بطيء)
- قطاع الصحة / المالية الحساس (Tier 3 — انتظر بعد 3 paid pilots)
- أي شخص اشتكى منك / اختلفت معه

اكتبهم في ملاحظاتك الخاصّة بهذا الشكل (ليس في الـ repo):

```
Slot-A: [اسم] | [قطاع 1A/1B/1C] | [قناة: WhatsApp/LinkedIn/Email] | [pain hypothesis]
Slot-B: ...
Slot-C: ...
Slot-D: ...
Slot-E: ...
```

---

## ⏰ 08:55 — انسخ + خصّص الرسالة (10 دقائق لكل شخص = 50 دقيقة)

اختر القالب المناسب لقطاع كل slot:

### قالب 1 — وكالات تسويق (Tier 1A)

```
السلام عليكم [الاسم]،

أطلقت بيتا محدودة لـ Dealix — نظام تشغيل سعودي يساعد وكالات
التسويق تطلع Proof Pack أسبوعي لعملائها (وش تم فعلياً، بدون أرقام
مختلقة).

الفكرة بسيطة: العميل يشوف قيمتك أوضح، فيظل معك أطول.

ودّي أجرّبه مع 3 وكالات سعوديّة فقط كـ Mini Diagnostic مجاني
هذا الأسبوع. لو ناسبك، نفتح Pilot 7 أيّام بـ 499 ريال.

ما فيه scraping ولا واتساب بارد ولا أي وعد بأرقام مبيعات. كل خطوة
خارجيّة بموافقتك.

تحب أرسل لك نموذج التشخيص؟
```

### قالب 2 — خدمات B2B (Tier 1B)

```
السلام عليكم [الاسم]،

سؤال سريع: كم lead دخلكم الشهر الماضي ولم يُتابع خلال 7 أيام؟

أطلقت Dealix كنظام يساعد شركات الخدمات B2B السعوديّة تنظّم
متابعة العملاء + تجهّز ردود اعتراضات + تطلع Proof Pack أسبوعي.

أبي أجرّبه مع 3 شركات فقط كـ Mini Diagnostic مجاني. لو شفته
يستحق، نفتح Pilot 7 أيّام بـ 499 ريال.

كل رسالة خارجيّة بموافقتك يدويّاً. لا automation، لا cold WhatsApp،
لا scraping.

أرسل لك نموذج التشخيص؟
```

### قالب 3 — استشارات/تدريب (Tier 1C)

```
السلام عليكم [الاسم]،

شفت عرضك في [مرجع — لقاء/منشور/إحالة]. عندي سؤال محدّد:

كم مستفسر تواصل معك الشهر الماضي ولم يحجز جلسة استشارة؟
لو الرقم >5، عندي شي يفيدك.

أطلقت Dealix كنظام يساعد المستشارين السعوديّين يحوّلون
المستفسرين إلى عملاء عبر متابعة منظّمة + ردود اعتراضات + Proof Pack.

ودّي أجرّبه معك مجاناً (Mini Diagnostic — 30 دقيقة قراءة). لو
مفيد، Pilot 7 أيّام بـ 499 ريال.

كل خطوة خارجيّة بموافقتك. لا cold outreach، لا وعود مبالغ فيها.

أرسل لك التشخيص؟
```

**القاعدة:** اكتب رسالة واحدة لكل slot، انسخها في WhatsApp/LinkedIn/Email وأرسلها **يدويّاً**. **لا تستخدم BCC، لا تجمعهم في group**.

---

## ⏰ 09:55 — سجّل + اقفل اليوم (5 دقائق)

افتح `docs/phase-e/live/FIRST_10_CUSTOMER_BOARD.md` (لو احتجت — ما يدخل repo) وحدّث:

```
| Slot | first_message_status | last_touch_date    |
|------|----------------------|--------------------|
| A    | sent_manually        | 2026-MM-DD         |
| B    | sent_manually        | 2026-MM-DD         |
| C    | sent_manually        | 2026-MM-DD         |
| D    | sent_manually        | 2026-MM-DD         |
| E    | sent_manually        | 2026-MM-DD         |
```

ثم سجّل proof event صادق (هذا أوّل event حقيقي في النظام):

```bash
mkdir -p docs/proof-events
cat > docs/proof-events/day1_first5_warm_intros_$(date +%Y-%m-%d).json <<'EOF'
{
  "proof_event_id": "day1_first5_$(date +%Y%m%d)",
  "date": "$(date +%Y-%m-%d)",
  "action_taken": "5 warm intro messages sent manually",
  "input_received": "5 contacts picked from founder's private network",
  "output_delivered": "5 personalized Arabic messages via WhatsApp/LinkedIn/Email",
  "customer_approved": "n/a — outreach is unilateral",
  "measurable_result": "messages_sent=5, replies=0 (waiting)",
  "unknowns": ["reply rate", "diagnostic conversion rate"],
  "no_fake_claims": true,
  "internal_only": true,
  "audience": "internal_only"
}
EOF
# ملاحظة: الـ JSON heredoc أعلاه يحتاج تنفيذ يدوي — افتح المحرر
# واكتب بالقيم الصحيحة (التاريخ + جزئية الـ ID)
```

ثم تحقّق أن النظام يعرف بأول proof event:

```bash
curl -s https://api.dealix.me/api/v1/revenue-pipeline/summary | jq .
# يجب أن يرجع revenue_truth.proof_event_files_count >= 1
# و v12_1_unlocked = true (لأن proof event الآن موجود)
```

🎉 **مبروك — V12.1 صار unlocked رسميّاً.**

---

## ⏰ يوم 2 — ماذا تتوقّع

في اليوم التالي:
- لو أحدهم ردّ → أرسل له `python scripts/dealix_diagnostic.py --company "Slot-A" --sector b2b_services --region riyadh --pipeline-state "[ما قاله بالضبط]"`
- لو لم يردّ أحد بعد 48 ساعة → تابع `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md` Day 2
- لو ردّ سلبي → ما تتأذّى. واحد من 5 رفض = طبيعي تماماً

---

## ❌ ما لا تفعله اليوم (مهم)

- ❌ لا تطلب من Claude بناء V14 / V15 / V12.5 / Growth Beast / أي OS جديد
- ❌ لا تفتح PR جديد لميزات جديدة
- ❌ لا تُرسل **نفس الرسالة** لـ 5 أشخاص (يكشف نفسه فوراً — كل رسالة تخصيص)
- ❌ لا تُرسل لشخص لم يردّ على آخر رسالة قبل ≥ 6 شهور
- ❌ لا تذكر أرقام إيرادات لم تتحقّق
- ❌ لا تقل "Dealix يضمن لك X%" لأي شخص — حتى wamily

## ✅ ما تفعله

- ✅ ترسل 5 رسائل يدويّاً
- ✅ تنتظر 24 ساعة
- ✅ تسجّل proof event صادق
- ✅ تشرب قهوة
- ✅ تتذكّر: 1 paid pilot في 14 يوم = نجاح. 0 = إعادة استهداف، ليس فشل تقني.

---

## الـ Day 1 verdict block

بعد إنجاز Day 1 الكامل، نسخة الـ verdict:

```
DAY_1_LAUNCH=COMPLETE
PROD_SHA=6637270 (or newer)
WARM_INTROS_SENT=5
SLOTS_FILLED=5/10
PROOF_EVENTS_LOGGED=1 (first ever real one)
V12_1_TRIGGER=unlocked
NEXT_FOUNDER_ACTION=wait 48h, then follow Day 2 of 14_DAY_FIRST_REVENUE_PLAYBOOK
```

---

## السبب الذي يجعل هذا أهم من Growth Beast

Growth Beast فيه 30 module افتراضي يحاول يحلّ مشاكل ما عندك بيانات
عنها. Day 1 Launch Kit هذا يولّد أوّل بيانات حقيقيّة في النظام
(5 messages_sent, 1 proof event, 5 sector hypotheses لتختبرها). من هذه الـ 5 رسائل
ترجع بإجابات صحيحة لأسئلة كان Growth Beast يحاول يخمّنها:

- أي قطاع من الـ 3 يردّ أسرع؟
- أي قالب من الـ 3 ينتج conversation؟
- ما الاعتراض الأوّل؟ (وقتها نبني `objection_handler` مبني على شيء حقيقي)
- ما القناة الأفضل (WhatsApp / LinkedIn / Email)؟

**Day 1 = البيانات الخام لـ Growth Beast لاحقاً.** لذلك Day 1 ≠ تأجيل — هو شرط مسبق.
