# Moyasar Sandbox → Live Cutover — الانتقال من اختبار إلى إنتاج

> Bilingual operations runbook for flipping Dealix payments from Moyasar test mode to live, verifying the webhook chain end-to-end, exercising the manual confirmation flow, and rotating ZATCA from sandbox to production. No code changes are required for the cutover itself; the flip is environment-driven.
>
> Cross-link: [BILLING_MOYASAR_RUNBOOK.md](./BILLING_MOYASAR_RUNBOOK.md), [MOYASAR_E2E_GUIDE.md](./MOYASAR_E2E_GUIDE.md), [INVOICING_ZATCA_READINESS.md](./INVOICING_ZATCA_READINESS.md), [ops/MANUAL_PAYMENT_SOP.md](./ops/MANUAL_PAYMENT_SOP.md).

---

## 1. Environment variable sequence — تسلسل المتغيرات

The cutover is gated by three environment variables only. Flip them in this exact order on the production secret store (Railway / Render / Docker secrets — never in `.env` committed to git, never in the browser bundle).

| Variable | Test value | Live value | Notes |
|---|---|---|---|
| `MOYASAR_PUBLISHABLE_KEY` | `pk_test_...` | `pk_live_...` | Published to the checkout page. |
| `MOYASAR_SECRET_KEY` | `sk_test_...` | `sk_live_...` | Server-side only. Never log. |
| `MOYASAR_WEBHOOK_SECRET` | sandbox secret | live secret | Recomputed from the live dashboard. |
| `DEALIX_MOYASAR_MODE` | `test` | `live` | The application-level switch read on boot. |

`DEALIX_MOYASAR_MODE` defaults to `test`. The application refuses to charge a card in `test` mode unless the keys are `pk_test_*` / `sk_test_*`, and refuses to charge in `live` mode unless the keys are `pk_live_*` / `sk_live_*`. The mismatch refusal is intentional and is treated as a deploy-time error, not a runtime warning.

التسلسل السعودي بالترتيب: أوقف الحركة، استبدل المفاتيح، فعّل `DEALIX_MOYASAR_MODE=live`، أعد تشغيل الخدمة، ثم نفّذ قائمة "أوّل ريال" أدناه.

---

## 2. First-SAR-collected checklist — قائمة أوّل ريال مُحصَّل

Run this checklist after each live cutover, on the production environment, with a real card you own. Do not skip.

1. **Health gate / بوابة الجاهزية.** `GET /api/v1/health/payments` returns `{ "mode": "live", "moyasar_reachable": true, "webhook_secret_loaded": true }`. If any field is false, abort and roll back to `test`.
2. **One-SAR test charge / دفعة ريال واحد.** Create an invoice of `amount=100` (halalas = 1 SAR), description `"live cutover smoke — do not refund automatically"`, with your real card. Confirm the redirect returns and the payment status is `paid`.
3. **Webhook arrival / استقبال الـ webhook.** Inside 30 seconds, the application receives a `payment_paid` webhook. Check the audit log: it must contain the `payment_id`, `mode=live`, and the HMAC signature verified.
4. **Idempotency / عدم التكرار.** Replay the same webhook payload via the Moyasar dashboard "redeliver" button. The application returns `200` but creates no duplicate ledger entry. Confirm by counting rows in `payment_ledger` before and after the replay — the count must be identical.
5. **Receipt / الإيصال.** A bilingual receipt is generated and visible in the customer workspace. ZATCA UUID is attached (sandbox UUID is acceptable during the staged cutover; production UUID required once Section 5 is complete).
6. **Refund / الاسترجاع.** Issue a full refund on the 1-SAR charge from the Moyasar dashboard. Confirm a `payment_refunded` webhook arrives, the ledger shows the reversal, and the customer-visible status flips to `refunded`.
7. **Reconciliation / المطابقة.** `GET /api/v1/payment-ops/reconcile?date=today` returns zero discrepancies. The Moyasar dashboard balance, the application ledger, and the bank settlement projection for the day must agree on the same total.

If steps 1 through 7 pass in a single session, the live cutover is signed off by the founder in the proof_ledger (`event=moyasar_live_signoff`).

---

## 3. Webhook dashboard verification — التحقق من لوحة الـ Webhook

Inside the Moyasar live dashboard, under "Webhooks":

- The URL points to `https://<production-host>/api/v1/payments/webhook` (HTTPS only; no IP literal; no path with a port).
- The events `payment_paid`, `payment_failed`, `payment_refunded`, and `payment_captured` are subscribed.
- The signing secret matches `MOYASAR_WEBHOOK_SECRET` byte-for-byte (recopy if in doubt).
- "Test delivery" returns `200 OK` from the application within 5 seconds. A non-200 response, a timeout, or a `403 signature mismatch` blocks the cutover.

Retry policy: the application acknowledges receipt before doing work, and any post-acknowledgement failure is handled by the DLQ described in [ops/WEBHOOK_RETRY_DLQ.md](./ops/WEBHOOK_RETRY_DLQ.md). Do not configure Moyasar-side retries beyond defaults.

---

## 4. Manual confirmation flow — مسار التأكيد اليدوي

When a customer pays by bank transfer (always-on alternative) or when Moyasar webhook delivery is delayed past the customer-success patience window, the founder records the receipt manually.

```
POST /api/v1/payment-ops/manual-evidence
{
  "engagement_id": "<eng_id>",
  "amount_sar": 499,
  "method": "bank_transfer | moyasar_dashboard_recovery",
  "evidence_type": "bank_statement_pdf | dashboard_screenshot | receipt_pdf",
  "evidence_uri": "s3://dealix-payment-evidence/<file>",
  "received_at": "<ISO8601>"
}
```

`manual-evidence` only records the evidence; it does not flip the engagement to `paid`. The confirmation step is separate so a second human eye can review.

```
POST /api/v1/payment-ops/confirm
{
  "engagement_id": "<eng_id>",
  "evidence_id": "<evidence_id_from_step_above>",
  "founder_signature": "<initials>",
  "decision": "confirm | reject_evidence"
}
```

`confirm` writes to the `payment_ledger`, emits a ZATCA invoice request, and unlocks delivery. `reject_evidence` writes a `friction_log` entry with the reason and notifies the customer.

ملاحظة سعودية: الإيصال البنكي يجب أن يحمل اسم الشركة (Dealix أو ما يقابلها قانونياً)، وتاريخ التحويل ضمن نافذة 24 ساعة، ومبلغاً مطابقاً أو زائداً.

---

## 5. ZATCA sandbox → production — تفعيل الفوترة

ZATCA Phase 2 ships in sandbox by default. Production cutover is a separate flip and must follow Moyasar live signoff, not precede it.

1. Confirm `ZATCA_SANDBOX=true` while running the Moyasar live smoke. Sandbox UUIDs are stamped on the smoke receipt; this is acceptable.
2. Obtain production CSID and secret from the ZATCA portal. Store as `ZATCA_CSID` and `ZATCA_SECRET` on the production secret store.
3. Set `ZATCA_SANDBOX=false`. Redeploy.
4. Run a 1-SAR live charge again (full step 2 list). The receipt now carries a production UUID. Verify the QR code resolves to a valid invoice on the ZATCA verifier portal.
5. The first production-stamped receipt is archived in `capital_ledger` as a reusable asset (`asset_type=invoice_template_live`).

If the ZATCA production flip fails, revert to `ZATCA_SANDBOX=true` and continue accepting payments; the invoice rebuild is a background task and does not block revenue.

---

## 6. Rollback — التراجع

Rollback is the inverse, executed in the same order:

1. Set `DEALIX_MOYASAR_MODE=test`.
2. Restore `pk_test_*` / `sk_test_*` keys.
3. Restore the sandbox webhook secret.
4. Redeploy. Confirm `GET /api/v1/health/payments` reports `mode=test`.
5. Communicate the rollback to any customer with an in-flight invoice via the standard manual confirmation path.

A rollback is not a failure event by itself. A rollback that is hidden from the proof_ledger is a failure event.

---

## 7. Escalation contacts — جهات التصعيد

Fill these placeholders on the operating environment, never in this document committed to git.

- **Founder on-call / المؤسس المناوب:** `<phone>` — answers within 30 min, 06:00–24:00 Riyadh time.
- **Moyasar support / دعم ميسر:** `<account_manager_email>` / `<support_ticket_portal>`.
- **ZATCA technical / الدعم الفني للفوترة:** `<zatca_support_channel>`.
- **Banking partner / الشريك البنكي:** `<relationship_manager>` for settlement disputes.
- **Legal / المستشار القانوني:** `<advisor_contact>` for any PDPL or consumer-protection escalation.

Every escalation, even one resolved in 10 minutes, is logged in `friction_log` with the start time, the resolution, and the contact used. The friction_log becomes the source of truth for capital improvements at the monthly review.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
