# Dealix — Governed Revenue & AI Operations (Execution Spine)

## الحكم الأعلى

Dealix تُبنى كطبقة تشغيل محكومة للإيراد والذكاء الاصطناعي، لا كـ AI agency عامة.

```text
Signal → Source → Approval → Action → Evidence → Decision → Value → Asset
```

## نجم الشمال

**Governed Value Decisions Created**

تعريف: قرارات لها مصدر واضح + موافقة + أثر قابل للقياس + دليل محفوظ.

## الاستراتيجية الكبرى

```text
Service-led → Software-assisted → Evidence-first → Retainer-backed → Platform-later
```

## العروض الأساسية الثلاثة

1. Governed Revenue Ops Diagnostic
2. Revenue Intelligence Sprint
3. Governed Ops Retainer

## State Machine (مختصر)

- `prepared_not_sent` = L2
- `sent` = L4
- `replied_interested` = L4
- `meeting_booked` = L4
- `used_in_meeting` = L5
- `scope_requested` = L6
- `invoice_sent` = L7_candidate
- `invoice_paid` = L7_confirmed

## القواعد الصارمة

- لا `sent` بدون `founder_confirmed=true`.
- لا L5 بدون `used_in_meeting`.
- لا L6 بدون `scope_requested` أو `pilot_intro_requested`.
- لا L7_confirmed بدون `invoice_paid`.
- لا Claim Revenue قبل الدفع الفعلي.

## التنفيذ الآن (Now Loop)

1. شغّل `bash scripts/run_ceo_one_session_readiness.sh`.
2. حدّث التموضع في المواد التجارية إلى Governed Revenue & AI Operations.
3. جهّز أول 5 warm contacts كـ `prepared_not_sent`.
4. إرسال يدوي فقط.
5. بعد كل إرسال: سجّل `sent` + timestamp + channel.
6. عند الرد المهتم: احجز اجتماع.
7. عند طلب scope: جهّز Diagnostic scope.
8. عند القبول: أنشئ invoice draft.
9. بعد الدفع: ابدأ Proof Pack.
10. لا بناء جديد قبل تكرار workflow أو طلب مدفوع.

## ما لا نفعله

- لا SaaS-first.
- لا agent autonomy خارجي.
- لا إرسال تلقائي.
- لا cold outreach automation.
- لا case study بدون موافقة.

## مراجع مرتبطة

- `docs/commercial/DEALIX_REVOPS_PACKAGES_AR.md`
- `docs/strategic/ENTERPRISE_OFFER_POSITIONING_AR.md`
- `docs/ops/today_send_queue.md`
- `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md`
