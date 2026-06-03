# Contact Confidence Levels — مستويات ثقة التواصل

*كم نثق في أننا نستطيع الوصول للجهة المناسبة عبر قناة عامة.*
*يختلف عن Evidence Levels (التي تخص الألم/الحقائق). هذا يخص **التواصل**.*
*آخر تحديث: 2026-06-03*

---

## المستويات (`contact_confidence`)

| المستوى | المعنى | مثال | نقاط Contact Availability |
|--------|--------|------|--------------------------:|
| **CC0** | لا قناة عامة | لم نجد شيئًا منشورًا | 0 |
| **CC1** | قناة عامة عامّة | info@ / نموذج / خط رئيسي | 10 |
| **CC2** | قناة دور/قسم عامة | sales@ / proposals@ / LinkedIn / Google Business | 15 |
| **CC3** | شخص مُسمّى من مصدر عام | اسم منشور على صفحة فريق عامة | 20 |

> الأغلبية الواقعية تقع في CC1–CC2. CC3 نادر ولا يُفترض إلا بمصدر عام صريح.

---

## الفرق عن Evidence Levels

```txt
Evidence Levels (L0–L4)  →  كم نثق في الألم/الحقائق عن الشركة؟
Contact Confidence (CC0–CC3) → كم نثق في أننا نصل للجهة عبر قناة عامة؟
```

يمكن أن تكون شركة عند **L2** (نعرف ألمها من صفحة وظيفة عامة) لكن **CC1** فقط
(لا نملك سوى info@). والعكس ممكن.

---

## أثرها على القرار

```txt
CC0 → غالبًا hold (لا قناة) → MISSING_CONTACTS_REVIEW
CC1 → مسودة عبر بريد/نموذج عام
CC2 → أولوية أعلى (دور/قسم واضح)
CC3 → الأعلى (شخص عام) — مع احترام الخصوصية
```

تدخل `contact_confidence` مباشرة في مكوّن *Contact availability* من نموذج التقييم
(`ACCOUNT_SCORING_MODEL_AR.md`).

---

## أمثلة من التشغيل الحالي

| Company | contact_confidence | route |
|---------|--------------------|-------|
| TrainMe KSA | CC2 | phone (public WhatsApp + line) |
| Digital Rise Agency | CC1 | email (info@) |
| Growth Labs SA | CC2 | linkedin_public |
| Alpha Consulting Group | CC0 | none_found → hold |
