# MVP Build Order — ترتيب البناء دون تشتيت

لا تبني كل شيء دفعة واحدة. الترتيب أدناه يوازن بين **القيمة التجارية** و**العمود الفقري الحوكمي**.

## المراحل (1 → 10)

1. **core_os — الأحداث والكيانات** — `revenue_memory/`، عقود الأحداث، هوية مشروع/عميل.
2. **data_os — Source Passport + معاينة استيراد** — `data_os/`، `sovereignty_os` / `institutional_control_os`، `standards_os/source_passport_standard.py`.
3. **governance_os — قرار تشغيلي** — `governance_os/`، `revenue_os/anti_waste.py`.
4. **revenue_os — تسجيل حسابات + حزمة مسودات** — `revenue_os/` (بدون scraping ولا أتمتة واتساب باردة).
5. **proof_os — Proof Pack + Proof Score** — `proof_architecture_os/`.
6. **value_os — سجل القيمة** — `proof_architecture_os/value_ledger.py`، `value_capture_os/`.
7. **capital_os — دفتر رأس المال التشغيلي** — `operating_finance_os/`، ربط مع `board_decision_os/`.
8. **command_os — لوحة CEO بسيطة** — `board_decision_os/ceo_command_center.py` ووثائق القرار.
9. **client_os — مساحة عمل دنيا** — `client_os/` + واجهة العميل في `frontend/`.
10. **trust_os — حزمة ثقة** — `compliance_trust_os/` (تقارير، تصدير، جواز).

## ما لا تبدأ به في الـ MVP

- سوق (marketplace) عام
- بوابة أكاديمية كاملة
- white-label عميق
- وكلاء مستقلون بالكامل عن الموافقة
- RBAC معقد قبل استقرار الأحداث والموافقات

## مرجع

خريطة أوسع: [SYSTEM_MAP.md](SYSTEM_MAP.md).
