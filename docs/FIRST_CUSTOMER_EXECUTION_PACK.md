# First Customer Execution Pack

> Use this pack only AFTER `docs/OUTREACH_GO_NO_GO.md` returns GO.

## 1. Warm LinkedIn message (Arabic)

```
السلام عليكم [الاسم]،
أطلقت Dealix كـ Beta محدودة للشركات والوكالات السعودية.

الفكرة:
نساعدكم ترتبون النمو بشكل عملي:
فرص مناسبة، رسائل عربية، متابعة، وقنوات آمنة — وكل شيء يمر بموافقتكم.

أقدر أجهز لكم Mini Diagnostic مجاني:
3 فرص + رسالة عربية + توصية قناة + مخاطرة لازم تتجنبونها.

أرسله لك؟
```

Use only with **1st-degree LinkedIn contacts**. No automation. No
purchased lists. No bulk send.

## 2. Warm LinkedIn message (English)

```
Hi [Name],
I'm launching Dealix in private beta for Saudi/GCC B2B companies and agencies.

It helps turn growth into an operating system:
qualified opportunities, safe outreach drafts, follow-up decisions, and proof packs.

I can prepare a free Mini Diagnostic:
3 opportunities + one message draft + recommended channel + risk note.

Would you like me to send one?
```

## 3. Mini Diagnostic intake questions

Ask in this order. Don't skip. Don't paraphrase.

1. اسم الشركة + الموقع الإلكتروني
2. القطاع (saas / clinics / real-estate / agency / training / logistics / other)
3. المدينة الرئيسية للعمليات
4. العرض في جملة واحدة (offer)
5. العميل المثالي (ICP) — قطاع/حجم/منطقة
6. هدف الأشهر الـ 3 القادمة (e.g. 10 demos / 5 paying customers / partner network)
7. القنوات الحالية (إيميل / LinkedIn / inbound / referrals / other)
8. هل عندك قائمة عملاء سابقين عندهم موافقة تواصل؟ (نعم/لا — مع التاريخ والمصدر)
9. متوسط قيمة الصفقة (SAR)
10. أكبر اعتراض تسمعه من العملاء

## 4. Mini Diagnostic output (deliver within 24h)

Single Arabic doc, ≤ 1 page:

```
1. أفضل شريحة بداية — [القطاع/المنطقة] — لأن [سبب من بياناتك]
2. 3 فرص محددة (إذا أمكن بالأسماء، وإلا بالمعايير):
   - الفرصة #1: [وصف]
   - الفرصة #2: [وصف]
   - الفرصة #3: [وصف]
3. رسالة عربية جاهزة للإرسال اليدوي (LinkedIn أو إيميل):
   "[نص الرسالة]"
4. القناة الآمنة الموصى بها: [LinkedIn manual / inbound wa.me / opt-in form / email draft with approval]
5. مخاطرة لازم تتجنبها: [مثلاً: لا cold WhatsApp على أرقام بدون موافقة]
6. الخطوة التالية: 7-Day Growth Proof Sprint بـ 499 ريال — يبدأ متى ما ترتاح
```

Send manually via WhatsApp/email. Dealix does NOT auto-send the
diagnostic. NEVER include "نضمن لك" or "guaranteed".

## 5. Pilot 499 SAR pitch

```
الـ Pilot هو 7-Day Growth Proof Sprint:
- 10 فرص محددة
- 6 رسائل عربية مسودّات
- 3 خطط متابعة
- ملاحظات مخاطر (compliance + spam)
- Proof Pack في اليوم السابع

السعر: 499 ريال — رسوم تفعيل واحدة، لا اشتراك.
الدفع: تحويل بنكي / STC Pay (نرسل التفاصيل)، أو رابط Moyasar إذا تفضل.
لا خصم بطاقة مباشر — أنت تدفع طوعاً بعد ما توافق.

لو راضي، رد بـ "موافق" وأرسل لك تفاصيل الدفع خلال ساعة.
```

## 6. Manual payment fallback

When the customer says "موافق":

```bash
# 1. Record the lead
curl -X POST https://api.dealix.me/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"name":"<contact>","email":"<email>","company":"<co>","phone":"<+966...>","source":"linkedin","sector":"<sector>"}'

# 2. Create deal at pilot_offered
curl -X POST https://api.dealix.me/api/v1/deals \
  -H "Content-Type: application/json" \
  -d '{"lead_id":"<lead_id>","value_sar":499,"stage":"pilot_offered"}'

# 3. Manual invoice — bank transfer instructions returned
curl -X POST https://api.dealix.me/api/v1/payments/manual-request \
  -H "Content-Type: application/json" \
  -d '{"deal_id":"<deal_id>","amount_sar":499}'

# 4. Send the customer the bank IBAN / STC Pay number via WhatsApp/email manually
# 5. When the transfer arrives:
curl -X POST https://api.dealix.me/api/v1/payments/mark-paid \
  -H "Content-Type: application/json" \
  -d '{"deal_id":"<deal_id>","reference":"<bank-ref>"}'
```

If `MOYASAR_SECRET_KEY` is configured (sandbox or live), the same
endpoint can be wired to call Moyasar's hosted invoice API. Amount in
halalah: **499 SAR = 49,900**.

Live card capture remains OFF.

## 7. Proof Pack delivery message (day 7)

```
[الاسم] — هذا Proof Pack لأول 7 أيام معك في Dealix:

ما تم إنجازه:
- 10 فرص محددة (مرفقة)
- 6 رسائل عربية تمت مراجعتها معك
- 3 خطط متابعة جاهزة

ما تمت حمايته:
- تم منع X رسالة على قنوات غير آمنة (تفاصيل في التقرير)
- لا cold WhatsApp، لا قوائم مشتراة

تقدير الأثر:
- pipeline متوقع: [X] ريال (تقدير، ليس ضمان)
- اجتماعات محتملة: [X]

الخطوة التالية:
- نكمل بـ Executive Growth OS (2,999 ريال/شهر) لو ترتاح للنتائج
- أو نكمل Pilot ثاني بقطاع آخر

Proof Pack الكامل مرفق. شكراً على ثقتك.
```

## 8. Follow-up cadence (max 3 touches)

- T+0: Proof Pack
- T+3 days: short check-in ("أي ملاحظة على Proof Pack؟")
- T+7 days: final follow-up ("هل نكمل أم نوقف هنا؟")

If no answer after T+7 → STOP. Do NOT escalate frequency. Do NOT add
to a future drip.

## 9. Upsell to Executive Growth OS (only after Proof Pack signed)

Conditions to upsell:
- Customer signed off on the Proof Pack in writing (WhatsApp / email).
- Proof Pack grade ≥ B (or customer explicitly happy).
- Customer has 2+ users at company.

If yes:

```
بناءً على نتائج Pilot، Executive Growth OS يكمل اللي بدأناه:
- Daily role briefs (CEO / Sales / Growth / RevOps)
- Weekly Proof Pack
- Pipeline hygiene + experiments
- 2,999 ريال/شهر، ابدأ ووقف متى ما تبي

نبدأ بـ شهر تجريبي؟
```

## 10. Safety rules (non-negotiable)

| Rule | Enforcement |
| --- | --- |
| No cold WhatsApp ever | classifier blocks 12+ phrasings; channel gate blocks |
| No purchased lists | compliance/check-outreach blocks |
| No "نضمن" / "guaranteed" | static-text sweep test |
| No automation tools (Linkedin, etc.) | no automation route exists |
| No live charge | manual fallback only |
| No Gmail live send | not configured |
| Consent before any direct outbound | required at intake step 8 |
| Opt-out respected | SuppressionRecord enforced |
| Stop after 3 follow-ups | manual discipline |

If a prospect ever asks "هل تستخدم cold WhatsApp؟" the answer is **NO**
and you point them to `landing/trust-center.html`.
