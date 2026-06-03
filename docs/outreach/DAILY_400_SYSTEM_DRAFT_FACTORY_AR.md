# Dealix — مصنع الـ 400 مسودة اليومية (System Draft Factory)

> كل يوم يُنتج Dealix **400 مسودة مخصصة** (company-specific drafts)، مبنية على تحليل
> الشركة وألمها — وليست رسائل عامة.
>
> **مصدر الحقيقة:** `src/data/draftFactory.ts`، ويتحقق منه `tests/draftFactory.test.ts`.

---

## 1. قاعدة أساسية: المسودات ليست إرسالًا

```txt
400 drafts/day   = مطلوب  (إلزامي)
400 sends/day    = غير مفعّل افتراضيًا
```

الإرسال يتطلب: **موافقة بشرية + unsubscribe + suppression list + جاهزية
SPF/DKIM/DMARC + صحة دومين**. هذه القاعدة منعكسة في الكود:
`SEND_DEFAULT_ENABLED = false`.

يتوافق هذا مع حوكمة الوكلاء: «الذكاء الاصطناعي لا يرسل رسائل خارجية بدون موافقة»
(`company_os/governance/agent_permissions.md`).

---

## 2. توزيع 400 مسودة على الأنظمة

| النظام | عدد Drafts يوميًا |
| --- | ---: |
| Revenue Operating System | 100 |
| Follow-up Recovery OS | 90 |
| Executive Command OS | 70 |
| WhatsApp Client OS | 70 |
| Proposal & Proof OS | 70 |
| **المجموع** | **400** |

---

## 3. ماذا تحتوي كل مسودة؟

ليست رسالة عامة. كل شركة تأخذ بطاقة احتياج (Client Need Card) كاملة:

```txt
company / sector / country / city / website
signal / likely_pain
recommended_system / why_this_system
first_mission / proof_angle / email_angle / cta
risk_level / evidence_level
approval_status / send_readiness
```

التفاصيل الكاملة في: [`SYSTEM_BASED_CLIENT_NEED_CARD_AR.md`](./SYSTEM_BASED_CLIENT_NEED_CARD_AR.md).

---

## 4. Top 100 Approval Queue

لا نراجع 400 يدويًا. النظام يرتّبها ويختار أفضل 100 حسب:

```txt
- ألم واضح
- قطاع مناسب
- إشارة شراء
- قابلية الدفع
- جودة التخصيص
- انخفاض المخاطر
```

ثم نرسل **20–80 فقط** في البداية حسب صحة الدومين.

---

## 5. الإرسال اليومي: لا نخلط Drafts مع Sends

Google توصي بزيادة حجم الإرسال تدريجيًا، وتطلب SPF/DKIM لكل المرسلين إلى Gmail،
و SPF + DKIM + DMARC للمرسلين فوق 5,000 رسالة يوميًا، و spam rate أقل من 0.3%، وتمنع
الممارسات المضللة (مثل Re/Fwd مزيف أو القوائم المشتراة)، وتطلب unsubscribe واضحًا
للرسائل التسويقية.

### خطة الإرسال الآمنة (Send Ramp)

| الفترة | Drafts/day | Sends/day |
| --- | ---: | ---: |
| الأسبوع 1 (أول 7 أيام) | 400 | 20–40 |
| الأسبوع 2 | 400 | 50–100 |
| الأسبوع 3 | 400 | 100–200 |
| الأسبوع 4 | 400 | 200–300 |
| بعد ثبات صحة الدومين | 400–800 | 300–400 |

### لا ترفع الإرسال إلا إذا

```txt
bounce منخفض
spam complaints منخفضة
unsubscribe يعمل
suppression list تعمل
domain health جيد
reply rate مقبول
لا توجد شكاوى
```

---

## 6. ممنوعات صارمة (Hard Rules)

```txt
- لا cold WhatsApp تلقائي
- لا LinkedIn automation
- لا قوائم بريد مشتراة (purchased lists)
- لا Re:/Fwd: مزيفة أو عناوين مضللة
- لا وعود بأرقام إيراد محددة
- لا أسرار أو بيانات شخصية (PII) في المسودات أو السجلات
- لا أسماء وحدات/أنظمة داخلية في نص موجّه للعميل
```

هذه الممنوعات منعكسة في `PROHIBITED_PRACTICES` ضمن `src/data/draftFactory.ts`.

---

## 7. ملخص التشغيل اليومي

```txt
1) إنتاج 400 مسودة مخصصة (إلزامي)
2) ترتيب Top 100 للمراجعة
3) اعتماد بشري لدفعة الإرسال
4) إرسال محدود ضمن خطة الـ ramp
5) قياس الصحة (bounce / spam / replies)
6) تسجيل كل إجراء في ai_action_ledger
```
