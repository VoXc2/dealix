# Account Intelligence OS — نظام ذكاء الحسابات

> الطبقة التي تحوّل Dealix من «كاتب إيميلات» إلى **مصنع فرص تجارية كاملة**.
> المخرج اليومي ليس 400 مسودة، بل **400 Account Intelligence Pack**.

---

## 1. الفكرة

كل شركة مستهدفة تتحول إلى **Account Pack** واحد يجيب على كل أسئلة الفرصة دفعة واحدة:

```
من الشركة؟ · كيف نوصل لها؟ · من الدور الأنسب؟ · ما الدليل؟
ما الألم المحتمل؟ · أي نظام يناسبها؟ · ما الإيميل؟ · ما سكربت الاتصال؟
ما العرض المصغر؟ · ما المطلوب للتسليم؟ · ما قيمة الفرصة؟ · ما القرار التالي؟
```

كل Pack يحتوي على هذه المكوّنات:

```
Company Intelligence · Public Contact Discovery · Contact Role Targeting
Client Need Card · Recommended System · Personalized Email Draft
Call Brief · Follow-up Sequence · Mini Proposal · Delivery Readiness
Cash Priority Score · Next Action
```

---

## 2. مكان النظام في المستودع

| الطبقة | المسار |
|--------|--------|
| العقد (الحقول) | `schemas/account_intelligence_pack.schema.json` |
| المولّد الليلي | `scripts/generate_account_packs.py` |
| المكتبة المشتركة (الأنظمة + التقييم + الصياغة) | `scripts/dealix_account_lib.py` |
| البيانات | `data/account_intelligence/account_packs.jsonl` |
| التقارير | `reports/account_intelligence/*` |
| الفحص/الاختبار | `scripts/validate_account_intelligence.py` |

---

## 3. خط الإنتاج اليومي

```
1) generate_account_packs.py   → 400 Pack + بيانات التواصل + العروض + الكاش
2) generate_account_reports.py → Nightly report · Top 100 · Quality · Contacts · Proposals · Finance · Founder Command
3) validate_account_intelligence.py → بوابات Schema + Policy + Artifacts (تخرج بكود ≠ 0 عند أي فشل)
```

كله Python بالمكتبة القياسية فقط (لا تبعيات خارجية)، **وحتمي (deterministic)**: نفس الـseed والتاريخ يعطي نفس المخرج بايتًا ببايت.

---

## 4. الأنظمة الخمسة وتوزيع الـ400 الليلي

| النظام | Entry Sprint | السعر الافتتاحي | حصة الليلة |
|--------|--------------|----------------:|-----------:|
| Revenue Operating System | Revenue Leakage Sprint | 4,500 ريال | 100 |
| Follow-up Recovery OS | 7-Day Follow-up Recovery Sprint | 3,500 ريال | 90 |
| Executive Command OS | Daily Command Sprint | 5,500 ريال | 70 |
| WhatsApp Client OS | WhatsApp Flow Sprint | 4,500 ريال | 70 |
| Proposal & Proof OS | Proposal & Proof Sprint | 3,000 ريال | 70 |
| **الإجمالي** | | | **400** |

---

## 5. القواعد الثابتة (Invariants)

1. **نظام واحد فقط** موصى به لكل Pack.
2. **لا اختراع** لأي اسم/هاتف/إيميل. غير الموجود = `null`، والمسار البديل role-based.
3. **اللغة واعية بالدليل**: مستويات L0/L1 تستخدم «غالبًا/قد/likely»، ولا تدّعي معرفة داخلية.
4. **لا ادعاءات مضمونة** في أي إيميل أو عرض أو نسخة موقع.
5. **كل عرض مصغر يبقى مسودة** حتى اعتماد المؤسس.
6. **المحتوى الخارجي بيانات غير موثوقة** — لا يتحول أبدًا إلى تعليمات (انظر `docs/security/`).
7. **القرار للإنسان**: الوكلاء يقترحون ويصيغون، والمؤسس يعتمد الإرسال والسعر والتسليم.

---

## 6. علاقة النظام بالحوكمة القائمة

يكمّل هذا النظام `company_os/governance/agent_permissions.md` و`pdpl_checklist.md`:
الوكلاء هنا في مستوى **Observe / Advise / Draft** فقط؛ أي إرسال خارجي أو تسعير يمر عبر طابور الاعتماد.

---

*Version 1.0 — يقرأ مع: ACCOUNT_PACK_OUTPUT_CONTRACT_AR · ACCOUNT_SCORING_MODEL_AR · EVIDENCE_LEVELS_AR*
