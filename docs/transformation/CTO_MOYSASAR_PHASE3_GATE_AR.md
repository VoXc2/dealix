# بوابة Phase 3 — Moyasar + DPA

لا تفعّل مفاتيح **live** قبل إكمال هذه القائمة.

## مراجع

- [`docs/BILLING_MOYASAR_RUNBOOK.md`](../BILLING_MOYASAR_RUNBOOK.md)
- [`docs/MOYASAR_LIVE_CUTOVER.md`](../MOYASAR_LIVE_CUTOVER.md)
- [`docs/DPA_PILOT_TEMPLATE.md`](../DPA_PILOT_TEMPLATE.md)
- [`docs/BILLING_RUNBOOK.md`](../BILLING_RUNBOOK.md)

## قائمة

- [ ] Moyasar **test** webhook verified on staging
- [ ] DPA مخصّصة لأول عميل مدفوع
- [ ] `ENVIRONMENT=production` فقط على بيئة الدفع
- [ ] لا فواتير تلقائية خارج مسار موافقة المؤسس
- [ ] `run_compliance_gtm_gate_bundle.sh` PASS بعد تغيير billing

## بعد Live

- سجّل `external_signal: invoice_sent` في أي PR يغيّر `MOYASAR_*` production vars
