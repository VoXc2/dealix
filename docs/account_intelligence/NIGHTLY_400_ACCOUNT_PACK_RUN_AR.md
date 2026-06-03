# Nightly 400 Account Pack Run — التشغيل الليلي

كيف يُنتج المصنع 400 Account Pack كل ليلة، وما الذي يضمن الجودة.

---

## 1. الأمر

```bash
# 1) توليد البيانات (حتمي)
python3 scripts/generate_account_packs.py --seed 20260603 --date 2026-06-03

# 2) توليد التقارير + Founder Daily Command
python3 scripts/generate_account_reports.py

# 3) التحقق (بوابة قبل أي استخدام)
python3 scripts/validate_account_intelligence.py
```

أو عبر npm (اختياري):

```bash
npm run account:build      # توليد + تقارير
npm run account:validate   # تحقق
npm run account:all        # الثلاثة
```

---

## 2. المخرجات

| الملف | المحتوى |
|-------|---------|
| `data/account_intelligence/account_packs.jsonl` | 400 Pack كامل |
| `data/account_intelligence/account_scoring.jsonl` | تقييم Top-100 + أسباب الاستبعاد |
| `data/contacts/contact_discovery.jsonl` | نتيجة اكتشاف التواصل العام |
| `data/contacts/contact_channels.jsonl` | القنوات (قيمتها null في الـseed) |
| `data/proposals/mini_proposals.jsonl` | 400 عرض مصغر (مسودات) |
| `data/finance/cash_priority_scores.jsonl` | أولوية الكاش لكل فرصة |
| `reports/account_intelligence/NIGHTLY_400_ACCOUNT_PACKS_REPORT.md` | ملخص الليلة |
| `reports/account_intelligence/TOP_100_ACCOUNT_QUEUE.md` | أفضل 100 |
| `reports/account_intelligence/ACCOUNT_PACK_QUALITY_REVIEW.md` | فحص الجودة |
| `reports/contacts/*` | اكتشاف التواصل + الناقص |
| `reports/proposals/*` | طابور العروض + طابور الاعتماد |
| `reports/finance/DAILY_REVENUE_OPPORTUNITY_REPORT.md` | فرص الكاش |
| `reports/founder/DAILY_SUPER_COMMAND.md` | لوحة قرار المؤسس |

---

## 3. التوزيع الليلي

```
Revenue Operating System : 100
Follow-up Recovery OS    : 90
Executive Command OS     : 70
WhatsApp Client OS       : 70
Proposal & Proof OS      : 70
-------------------------------
الإجمالي                 : 400
```

يتحقق المولّد والمدقّق معًا من أن التوزيع يطابق الهدف بالضبط.

---

## 4. ما الذي يجعل الـ«400» حقيقيًا لا مزيّفًا؟

- البيانات **مولَّدة بكود حتمي**، وليست مكتوبة يدويًا.
- بيانات الـseed **تركيبية بوضوح** (شركات خيالية) — ولا تخترع أي هاتف/إيميل.
- كل Pack يمر على **بوابة تحقق** (Schema + Policy) قبل أن يُحتسب.
- عند توفر بيانات عامة حقيقية أو بيانات من المؤسس، ترتفع مستويات الدليل/الثقة (L2→L4، C2→C4) **دون تغيير العقد**.

---

## 5. الجدولة (مقترح)

شغّل الخطوات الثلاث ليلًا (cron/Action) ثم راجع `DAILY_SUPER_COMMAND.md` صباحًا.
أي فشل في خطوة 3 يوقف الاعتماد على مخرجات تلك الليلة.

---

*Version 1.0*
