# تعبئة أهداف warm — قبل الإطلاق

1. افتح `agency_accounts_seed.csv` واستبدل `REPLACE:` في أعمدة `company` و`contact` بأسماء حقيقية من شبكتك (10–25 صفاً للأسبوع الأول).
2. تحقق: `python scripts/validate_warm_targeting_csv.py` (بدون `--max-replace-top 99` يجب صفر REPLACE في أعلى 10 صفوف نشطة).
3. استيراد War Room: `DEALIX_API_BASE` + `DEALIX_ADMIN_API_KEY` ثم `python scripts/sync_war_room_targets_api.py`.

لا تُخترَع أسماء شركات في الأتمتة — المصدر هو CRM أو مقدمة شخصية فقط.
