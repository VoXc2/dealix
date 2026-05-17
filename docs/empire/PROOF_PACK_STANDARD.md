<!-- LAYER: empire/doctrine | Owner: Founder | Bilingual AR+EN | draft_only -->
<!-- Part of the Dealix Operating Standard — see INDEX.md -->

# معيار Proof Pack — Proof Pack Standard (doctrine)

> **AR:** المعيار الملزم للبنية والتوقيع والموافقة هو [`../PROOF_PACK_V6_STANDARD.md`](../PROOF_PACK_V6_STANDARD.md). هذا الملف يثبّت **عقيدة** الـProof Pack كأصل شركة.
> **EN:** The binding spec (sections, signing, consent) is `PROOF_PACK_V6_STANDARD.md`. This file codifies the *doctrine* of the Proof Pack as a company asset.

---

## القاعدة / The Rule

> كل مشروع لا يجب أن يُنتج مالاً فقط — يجب أن يُنتج **أصلاً**.
> **EN:** Every project must produce not just revenue but a *reusable asset*.

كل Proof Pack يتحول إلى واحد أو أكثر من: Sprint proposal · Retainer candidate ·
Referral ask · Partner intro · Anonymous case insight · Benchmark data point ·
Product learning.

---

## بنية Proof Pack / Proof Pack Structure (doctrine view)

1. Context — السياق
2. Inputs reviewed — المدخلات المُراجعة
3. Lead / workflow status — حالة الـlead / الـworkflow
4. Source quality — جودة المصدر
5. Owner gaps — فجوات الملكية
6. Approval risks — مخاطر الاعتماد
7. Follow-up gaps — فجوات المتابعة
8. Draft messages — مسودات الرسائل
9. Recommended next actions — الخطوات التالية
10. Truth labels — تسميات الحقيقة
11. Upgrade path — مسار الترقية

> البنية المُلزمة الكاملة (14 قسماً + scoring + توقيع HMAC + بوابة الموافقة) في
> [`../PROOF_PACK_V6_STANDARD.md`](../PROOF_PACK_V6_STANDARD.md).

---

## تسميات الحقيقة / Truth Labels

كل رقم يجب أن يُوسَم — لا يُباع التقدير كحقيقة:

| التسمية / Label | المعنى / Meaning |
|-----------------|------------------|
| Estimate | تقدير — للاستخدام الداخلي فقط |
| Observed | مرصود داخل workflow Dealix |
| Client-confirmed | مؤكَّد من العميل |
| Payment-confirmed | إيراد مؤكَّد بالدفع فقط |
| Repeated workflow | workflow تكرّر |
| Retainer-ready | جاهز للـretainer |

مثال آمن:

```text
Follow-up gap: Observed
Potential value:  Estimate
Client pain:      Client-confirmed
Revenue:          Payment-confirmed only
```

أي score تجريبي يُوسَم `is_estimate` ولا يُعرض كحقيقة.

---

## روابط / Cross-links

- [`../PROOF_PACK_V6_STANDARD.md`](../PROOF_PACK_V6_STANDARD.md) — المعيار الملزم / binding spec
- [`../../auto_client_acquisition/proof_os/`](../../auto_client_acquisition/proof_os/) — كود تجميع Proof Pack / assembly module
- [`../../auto_client_acquisition/value_os/`](../../auto_client_acquisition/value_os/) — سجل القيمة وطبقات الحقيقة / value ledger tiers
- [`AUTHORITY_ENGINE.md`](AUTHORITY_ENGINE.md) — تحويل Proof إلى محتوى / proof → content
- [`BENCHMARK_ENGINE.md`](BENCHMARK_ENGINE.md) — تحويل Proof إلى مرجع / proof → benchmark

---

> **تنبيه:** النتائج التقديرية ليست نتائج مضمونة.
> **Note:** Estimated outcomes are not guaranteed outcomes.
