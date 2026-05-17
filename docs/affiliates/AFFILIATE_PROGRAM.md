# Affiliate Program — برنامج الشركاء بالعمولة

A governed affiliate program. Affiliates promote Dealix to their audience and
earn a commission when a referred deal is **paid**. Every step is gated.

## How it works

1. **Apply** — an affiliate submits an application (`POST /api/v1/affiliate-os/apply`).
2. **Score** — a pure-function fit score (0–100) assigns a commission tier:
   `standard` (10%), `preferred` (15%), `strategic` (20%).
3. **Approve** — the founder approves or rejects the affiliate.
4. **Asset gate** — any promotional copy the affiliate wants to use is reviewed
   by the governance claim guards. Guaranteed-outcome claims are **blocked**.
   Approved assets carry a mandatory disclosure line.
5. **Link** — an approved affiliate is issued a tracking link (`AFF-XXXXXXXX`)
   with UTM parameters.
6. **Referral → paid invoice** — when a referred deal's invoice has a recorded
   payment confirmation, a commission accrues. **No paid invoice, no commission.**
7. **Payout** — a payout is requested, which opens an approval. A human must
   approve before the payout settles.

## The three hard gates

| Gate | Rule |
|---|---|
| Asset gate | No affiliate copy may promise guaranteed outcomes. |
| Commission gate | A commission accrues only against a payment-confirmation evidence event. |
| Payout gate | A payout settles only after human approval via the Approval Center. |

## Backing module

`auto_client_acquisition/affiliate_os/` — intake, scoring, links, asset
registry, commission engine, payout gate. Config in
`affiliate_os/config/affiliate_rules.yaml`. API under `/api/v1/affiliate-os`.
Acceptance tests in `tests/test_affiliate_os.py`.

## بالعربية

برنامج شركاء محوكم. الشريك يروّج لـDealix لجمهوره ويحصل على عمولة عند **دفع**
الصفقة المُحالة. لا عمولة بدون فاتورة مدفوعة، ولا دفع بدون موافقة بشرية، ولا
نسخة تسويقية تَعِد بنتائج مضمونة.
