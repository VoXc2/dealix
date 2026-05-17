# سير عمل مراجعة الأفلييت / Affiliate Review Workflow
<!-- COMMERCIAL EMPIRE | Owner: Founder | Date: 2026-05-17 -->

## 1. المبدأ / Principle

**العربية:** شبكة الأفلييت في ديالكس **مغلقة ومحكومة** — ليست مفتوحة للجميع. الهدف ليس حجم المُسوّقين، بل جودة كل إحالة. نبدأ بـ5–10 شركاء موثوقين فقط، بموافقة يدوية، ونصوص معتمدة فقط، وإفصاح إلزامي. لا تُدفع أي عمولة إلا بعد `invoice_paid`. كل رقم يحمل تصنيف حقيقة: تقدير / ملحوظ / مؤكَّد من العميل / مؤكَّد بالدفع.

**English:** The Dealix affiliate network is **closed and governed** — not open to anyone. The goal is not the number of marketers, but the quality of each referral. We start with only 5–10 trusted affiliates, with manual approval, approved scripts only, and mandatory disclosure. No commission is paid until `invoice_paid`. Every metric carries a truth label: Estimate / Observed / Client-confirmed / Payment-confirmed.

## 2. لماذا الإفصاح إلزامي / Why Disclosure Is Mandatory

**العربية:** سجلّ محتوى الأفلييت في السوق ضعيف تاريخيًا — معظم المحتوى الترويجي لا يحمل أي إفصاح بأن الكاتب يتقاضى عمولة. هذا يخلق ادعاءات مضلِّلة ومخاطر ثقة. لذلك الإفصاح عندنا **إلزامي ومُراجَع**: كل قطعة محتوى أفلييت تذكر بوضوح أن هناك علاقة عمولة. غياب الإفصاح يعني رفض المحتوى — لا استثناءات.

**English:** Affiliate content in the market has a historically weak record — most promotional content carries no disclosure that the author earns a commission. This produces misleading claims and trust risk. So at Dealix disclosure is **mandatory and reviewed**: every affiliate content piece clearly states that a commission relationship exists. Missing disclosure means the content is rejected — no exceptions.

## 3. مراحل البرنامج / Program Phases

**العربية:** المرحلة 1 — شبكة مصغّرة: 5–10 شركاء موثوقين، موافقة يدوية على كل شخص، نصوص معتمدة فقط، إفصاح إلزامي، عمولة بعد الدفع فقط. لا توسيع للمرحلة 2 قبل أن تثبت المرحلة 1 امتثالًا نظيفًا عبر 10 إحالات على الأقل.

**English:** Phase 1 — a minimal network: 5–10 trusted affiliates, manual approval of each person, approved scripts only, mandatory disclosure, commission after payment only. No expansion to Phase 2 before Phase 1 proves clean compliance across at least 10 referrals.

## 4. سير العمل / The Workflow

```text
affiliate_submits_copy        ← الأفلييت يقدّم نص الترويج
        |
        v
compliance_review             ← مراجعة الامتثال (بشرية)
        |
   +----+----+----+
   |         |    |
approved  edit_   blocked     ← معتمد / يحتاج تعديل / محظور
   |      required
   |         |
   |     (resubmit)
   v
tracking_link_issued          ← يُصدر رابط تتبّع فريد
        |
        v
lead_submitted                ← وصول عميل محتمل عبر الرابط
        |
        v
qualified                     ← تأهيل عبر sales_os
        |
        v
invoice_paid                  ← فاتورة مدفوعة فعليًا
        |
        v
commission_eligible           ← العمولة تصبح مستحقة
```

**العربية:** لا قفزة بين مراحل السير. المحتوى لا يخرج قبل `approved`. الرابط لا يُصدَر قبل المحتوى المعتمد. العمولة لا تُحسب قبل `invoice_paid`.

**English:** No skipping stages. Content does not go out before `approved`. The link is not issued before approved content. Commission is not counted before `invoice_paid`.

## 5. شروط صرف العمولة / Payout Preconditions

**العربية:** العمولة لا تُصرف إلا إذا تحققت **كل** الشروط التالية معًا:

**English:** Commission is paid only if **all** of the following hold together:

| الشرط / Precondition | الوصف / Description | تصنيف الحقيقة / Truth Label |
|---|---|---|
| `invoice_paid` | الفاتورة مدفوعة فعليًا / invoice actually paid | Payment-confirmed |
| `no_refund_issue` | لا نزاع استرداد على الدفعة / no refund dispute on the payment | Payment-confirmed |
| `lead_not_duplicate` | العميل ليس مكررًا من مصدر آخر / lead not a duplicate from another source | Observed |
| `copy_compliant` | النص اجتاز مراجعة الامتثال / copy passed compliance review | Observed |
| `disclosure_present` | الإفصاح موجود وظاهر في المحتوى / disclosure present and visible | Observed |

**العربية:** إذا سقط أي شرط، تُجمَّد العمولة حتى تُحَل الحالة، أو تُلغى إن استحال حلها.

**English:** If any precondition fails, the commission is frozen until the case is resolved, or cancelled if resolution is impossible.

## 6. قائمة مراجعة الامتثال / Compliance Review Checklist

```text
[ ] الإفصاح عن علاقة العمولة موجود وواضح / commission disclosure present and clear
[ ] لا وعد بعائد مضمون أو نسبة تحويل / no guaranteed ROI or conversion rate
[ ] لا ذكر لكشط بيانات أو واتساب بارد / no scraping or cold WhatsApp mentioned
[ ] لا إثبات مُختلَق أو اسم عميل بلا موافقة / no fabricated proof or client name without consent
[ ] الأرقام تحمل تصنيف حقيقة / numbers carry a truth label
[ ] العرض المذكور من السجل الرسمي فقط / offer named only from the canonical registry
[ ] لا ادعاء بأن ديالكس يرسل رسائل خارجية بلا موافقة / no claim Dealix sends external messages without approval
[ ] اللهجة تطابق صوت ديالكس — لا مبالغة تسويقية / tone matches Dealix voice — no marketing hype
```

## 7. الادعاءات الممنوعة / Forbidden Claims

**العربية:** يُحظر على أي أفلييت: وعد بعائد مضمون، نسبة تحويل كحقيقة، تواصل بارد أو واتساب بارد، كشط بيانات، إثبات مُختلَق، استخدام اسم عميل دون موافقة مكتوبة، أو الإيحاء بأن ديالكس يرسل رسائل نيابة عن العميل دون موافقة صريحة.

**English:** Forbidden for any affiliate: guaranteed ROI promises, a conversion rate stated as fact, cold outreach or cold WhatsApp, scraping, fabricated proof, using a client name without written consent, or implying Dealix sends messages on a customer's behalf without explicit approval.

## 8. النصوص المعتمدة / Approved Scripts

```text
ALLOWED (affiliate post opener):
"أعمل ضمن برنامج شركاء ديالكس (أتقاضى عمولة عند الإحالة الناجحة).
 ديالكس يدقّق ما يحدث بعد وصول العميل المحتمل ويبدأ بتشخيص مجاني."
"I am part of the Dealix partner program (I earn a commission on a
 successful referral). Dealix audits what happens after a lead arrives
 and starts with a free diagnostic."

FORBIDDEN: any version that drops the disclosure line, promises a return,
or uses a scraped or cold contact list.
```

## 9. حلقة التصحيح / Correction Loop

**العربية:** عند `edit_required`، يستلم الأفلييت ملاحظات محددة بالسطر، ويعيد التقديم. ثلاث محاولات `edit_required` متتالية على نفس النص تنقل الحالة إلى `blocked` ومراجعة المؤسس. `blocked` المتكرر يعني إنهاء الشراكة.

**English:** On `edit_required`, the affiliate receives line-specific notes and resubmits. Three consecutive `edit_required` rounds on the same copy move the case to `blocked` and founder review. Repeated `blocked` means ending the partnership.

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
