# مساران GTM — أيهما الآن؟ (ترويج للعملاء vs تشغيل داخلي)

**الغرض:** إنهاء الغموض في «تطبيق الاستراتيجية» vs «ترويج المنتج» — كلاهما صحيح، لكن **أولوية الأسبوع** واحدة فقط.

---

## المساران

| المسار | المعنى | مخرجات ناجحة | أين في الريبو |
|--------|--------|--------------|----------------|
| **A — ترويج للعملاء** | محادثات، عروض، pilots، إيراد مدفوع | `payment_received` · Proof Pack مسلّم | [agency_accounts_seed.csv](targeting/agency_accounts_seed.csv) · War Room · [EVIDENCE_EVENTS_CLOSE_PATH_AR.md](EVIDENCE_EVENTS_CLOSE_PATH_AR.md) |
| **B — تشغيل داخلي (Ops)** | سكربتات، بوابات، KPI، محتوى بموافقة | `DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS` · brief يومي | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) · `run_founder_commercial_day` · `/ops/*` |

---

## شجرة قرار (30 ثانية)

```text
هل لديك ≥ 1 lead warm بلا next_action بتاريخ اليوم؟
  نعم → المسار A (ترويج): War Room أولاً، لا «بناء ميزة» قبل اللمسة.
  لا  → هل بوابة soft/paid launch = FAIL؟
          نعم → المسار B (ops): verify + MASTER §no-build حتى PASS.
          لا  → هل لديك ≥ 3 discovery مجدولة هذا الأسبوع؟
                  نعم → A (إغلاق) + B خفيف (مساء evidence فقط).
                  لا  → A (ملء موجة ABM 1) ثم B (محتوى مسودة للموافقة).
```

---

## قواعد عدم الخلط

1. **لا تعدّ بناء منتج «GTM»** بين 09:00–12:00 إذا قائمة War Room فيها `not_contacted` بأولوية `high`.
2. **لا تعدّ إرسالاً خارجياً** «ترويجاً» — كل لمسة عبر مسودة + موافقة ([GATED_AUTO_SEND_RFC_AR.md](GATED_AUTO_SEND_RFC_AR.md)).
3. **KPI من CRM فقط** — لا أرقام مخترعة في التقارير (`kpi_founder_commercial_import.yaml`).
4. المسار B **يدعم** A (brief، سوشال مسودة، استيراد أهداف)؛ لا يستبدله.

---

## ربط بالخطة الأسبوعية

| يوم | افتراضي |
|-----|---------|
| اثنين–خميس صباحاً | A: 3 لمسات معتمدة + 1 متابعة |
| اثنين–خميس مساءً | A: سطر evidence · B: 5 دقائق scorecard |
| جمعة | B: مراجعة GTM عميقة ([DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](../DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md)) + A: ملخص تعلّم الأسبوع ([FOUNDER_SALES_LOOP_AR.md](FOUNDER_SALES_LOOP_AR.md)) |

**المرجع التالي:** [targeting/ABM_WAVE1_ICP_AR.md](targeting/ABM_WAVE1_ICP_AR.md)
