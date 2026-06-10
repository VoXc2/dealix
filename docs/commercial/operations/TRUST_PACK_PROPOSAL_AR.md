# Trust Pack — مرفق Proposal (Motion A / Diagnostic)

**الغرض:** حPack ثقة PDPL + حوكمة — **ليس** شهادة امتثال قانونية.  
**أرفق مع:** كل Diagnostic proposal · Sprint scope · Data Pack SOW.

---

## 1) ملخص PDPL (للعميل)

- Dealix يعالج بيانات الأفراد **بموافقة وغرض محدد** فقط.
- **لا** إرسال خارجي (WhatsApp/LinkedIn/Gmail) بدون موافقة صريحة.
- حقوق أصحاب البيانات: وصول · تصحيح · حذف — مسار DSAR موثّق.
- الاحتفاظ: حسب العقد + سياسة الخصوصية المنشورة.

**مرجع:** [privacy_pdpl_ar_en.md](../../knowledge-base/privacy_pdpl_ar_en.md)

---

## 2) DPA (معالجة البيانات)

- قالب DPA متاح عند الطلب — يغطي: المعالج · الغرض · مدة الاحتفاظ · الباطنون.
- الباطنون المعروفون: Railway (hosting) · HubSpot (CRM إن فُعّل) · Moyasar (دفع).

**مرجع:** [SECURITY_PDPL_CHECKLIST.md](../../SECURITY_PDPL_CHECKLIST.md)

---

## 3) Approval-First Architecture

```text
مسودة → مراجعة → موافقة → إرسال يدوي (إن وُجد)
```

- كل إجراء AI له `Decision Passport` + مستوى دليل L0–L5.
- **anti-waste:** لا upsell بدون Proof · لا تسويق عام تحت L4.

---

## 4) Data Residency Note

- البنية الحالية: cloud (Railway) — يُوثّق أساس النقل والاحتفاظ في DPA.
- لا ادعاء «استضافة 100% داخل المملكة» ما لم يُنفّذ contractually.

---

## 5) ما لا نعد به (No Overclaim)

- لا ضمان إيراد · لا cold outreach · لا scraping.
- لا «امتثال PDPL كامل» — **عمليات امتثال قابلة للتدقيق**.

**سجل:** [no_overclaim.yaml](../../../dealix/registers/no_overclaim.yaml)

---

## 6) إرفاق في Proposal

```markdown
[Trust Pack — Dealix Revenue OS]
- PDPL summary + DPA on request
- Approval-first · no auto-send
- Evidence levels L0–L5 on every delivery
```

**تحقق:** `python scripts/run_ceo_master_plan_status.py` → `p1_trust_pack`
