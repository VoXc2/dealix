# Dealix Living Fleet Runbook — الطاقم الحي
**STATUS: CANONICAL · v1 2026-08-25**

## الفكرة
طاقم واحد حي فوق الأنظمة الموجودة. لا أطر عمل جديدة، لا مؤقتات جديدة، لا وكلاء شكليون.
**المُوجِّه الوحيد:** `scripts/ops/living_fleet_dispatch.sh <EVENT>`
- يوقّع الأدوار المالكة للحدث فقط.
- `SKIP_UNCHANGED` عبر بصمة مدخلات كل دور (صفر تكلفة عند ثبات الحالة).
- حارس موارد: أدوار LLM ترفض العمل تحت ضغط الذاكرة (<3500MB).
- حالة التشغيل **خارج Git**: `/opt/dealix/control/state/living_fleet/<ROLE>.state.json`
- ممنوع بنيويًا: send/publish/merge/deploy/DNS/pay من داخل المُوجِّه (مثبت باختبارات).

## سجل الأدوار (المالك = نظام قائم)
| ROLE | المالك الفعلي | يستيقظ على | النوع |
|---|---|---|---|
| EXEC_PM | Company Autopilot (morning/midday/evening) + OpenCode integration | morning/midday/evening/strategic | det |
| REVENUE_INTEL | Autopilot commercial logs + connector handoff | gmail_reply/tender_change/morning/midday | llm |
| SALES_NEGOTIATION | Negotiation Desk (board) + OpenCode drafts | gmail_reply | llm |
| MARKET_INTEL | MARKET_SIGNALS artifacts + Hermes research | market_signal/tender_change | llm |
| LEAD_INTEL | Opportunity store ranking | morning | det |
| CUSTOMER_ACQ | outreach_review_queue pipeline | opportunity_signal | llm |
| DIAGNOSTIC | MINI_DIAGNOSTICS templates | opportunity_signal | llm |
| DELIVERY | evidence_events_tracker + evening mode | evening/delivery_evidence | det |
| ENGINEERING | OpenCode + repo_watch/ci_failure events | repo_watch/ci_failure | det |
| GOVERNANCE | APPROVAL_FINGERPRINT_CONTRACT + nightly mode | nightly/approval_changed | det |
| DATA_BRAIN | company_brain_v6 + business_now_cache refresh | nightly/strategic | det |
| CONTENT | Proof Log → drafts (approval-gated) | proof_event | llm |

## التوصيل بالجدولة القائمة
لا مؤقتات جديدة. أوضاع Autopilot الحالية تستدعي المُوجِّه في نهاية دورتها:
`living_fleet_dispatch.sh <mode-as-event>` (heartbeat = حساسات فقط، no-op).
الربط الفعلي داخل سكربت الأوتوبايلوت = PR مستقبلي مركّز بعد استقرار #1247.

## حدود المؤسس الخاص (معزول تمامًا)
- مسارات CAREER / PERSONAL_ADMIN / PERSONAL_MONEY / LEARNING / NETWORK تعمل على حالة محلية خاصة: `/opt/dealix/control/state/founder_personal/` فقط.
- **لا شيء شخصي يدخل مستودع Dealix إطلاقًا.** لا تشخيص طبي، لا قرارات قانونية نهائية، لا أسرار.
- أي التزام خارجي شخصي = موافقة بصمة مثل الشركة.

## مراجعة ROI الأسبوعية
لكل دور: invocations · skips · useful_outputs · timeouts · founder_minutes_saved.
قاعدة القرار: GROW / KEEP / OPTIMIZE / MAKE_DETERMINISTIC / RETIRE_CANDIDATE.
دور بلا مخرج مفيد خلال أسبوعين = RETIRE_CANDIDATE تلقائيًا.

## الدائرة الكهربية (Circuit breakers)
نفس المدخل+نفس الفشل مرتين → توقف، سجّل BLOCKER، انتقل لمسار آخر. المهلة الزمنية تحفظ الأدلة الجزئية وتخرج DEGRADED صادقًا.
