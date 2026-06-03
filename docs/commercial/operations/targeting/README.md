# استهداف الوكالات — agency_accounts_seed.csv

**موجة ABM 1 (معايير + توزيع):** [ABM_WAVE1_ICP_AR.md](ABM_WAVE1_ICP_AR.md) · config: `dealix/config/gtm_abm_wave1.yaml`

## الاستخدام

1. املأ الصفوف من قائمة **warm** معتمدة فقط — لا scraping.
2. راجع [WARM_LIST_WORKFLOW.md](../../../sales-kit/WARM_LIST_WORKFLOW.md).
3. جفاف: `py -3 scripts/import_war_room_targets.py --dry-run`
4. تطبيق محلي: `py -3 scripts/import_war_room_targets.py --apply`
5. أو من UI: `/ops/war-room` → «استيراد من CSV» (مفتاح Admin).

## الحقول

`company`, `contact`, `segment`, `pain_hypothesis`, `channel`, `motion`, `offer_id`, `status`, `next_action`, `next_action_date`, `priority`, `notes`

## الهدف

≥ **50** صف فعّال للتدشين الاستراتيجي (Motion A agency wedge أولاً).  
**توسيع تلقائي:** `py -3 scripts/expand_agency_targets_seed.py` (افتراضي 120) · `--wave2` · أو `powershell -File scripts/founder_commercial_expand.ps1 -Wave2`
