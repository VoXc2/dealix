# Partner Claims & Disclosure Policy — AR/EN

## Mandatory disclosure
Every partner-controlled promotional asset must make the commercial relationship understandable. Approved concise wording:

AR: `قد أحصل على عمولة إذا نتج عن هذه الإحالة عميل مدفوع مؤهل وفق شروط برنامج شركاء Dealix.`
EN: `I may earn a commission if this referral results in a qualifying paid Dealix customer under the Dealix Partner Program terms.`

## Prohibited claims
- دخل/ربح/عائد مضمون أو guaranteed income/revenue/ROI.
- “Dealix تضمن زيادة المبيعات” أو equivalent absolute outcomes.
- ادعاء اعتماد حكومي أو نفوذ أو وصول خاص غير موثق.
- استخدام أسماء عملاء أو شعارات أو نتائج دون proof/public-use approval.
- سعر عميل ثابت أو خصم غير معتمد.
- ادعاء أن التسجيل كشريك يعني قبولًا، أو أن الإحالة تعني استحقاق عمولة.

## Required claim evidence
Each material claim must map to a `claims_registry` record with source, scope, date, reviewer, allowed channels and expiry/review date.

## Channel rules
- WhatsApp: inbound/opt-in only.
- Email/direct marketing: consent evidence, sender identity and easy opt-out.
- Public social: approved copy, partner disclosure and evidence-backed claims.
- Paid advertising: only approved campaign assets and landing pages.
- B2G/public sector: compliance review before any opportunity-linked economics.
## Automated lint decision
Before an asset is eligible for external review/publishing, Company Machine should evaluate:
- `approved_asset == true`
- `partner_disclosure_present == true`
- `consent_proven == true` for direct marketing
- no guaranteed-income/ROI phrase
- no unverified government-access/influence claim
- no unapproved pricing
- proof/public-use authority exists for customer claims

Any failure → `CLAIMS_OR_CONSENT_HOLD` with a receipt; no automatic send/publish.

## Truth ladder
Draft copy != approved asset != published asset != consented direct message != qualified opportunity != collected cash.

This policy controls partner messaging; it does not replace Saudi legal advice or Dealix's final public-claims approval.