# Account Scoring Model — نموذج تقييم الحسابات (Top 100)

*يحوّل كل باقة إلى نقاط 0–100 لترتيب التشغيل الليلي واختيار مرشحي الإرسال والاتصال.*
*المرجع الآلي: `schemas/account_scoring.schema.json` + دالة `score_pack()` في المدقّق.*
*آخر تحديث: 2026-06-03*

---

## المكوّنات (مجموعها 100)

| المكوّن | الوزن | يقيس |
|--------|------:|------|
| Pain clarity | 25 | وضوح الألم (مدفوع بمستوى الدليل + وجود إشارة شراء) |
| Contact availability | 20 | توفّر قناة تواصل عامة (CC0–CC3) |
| System fit | 20 | قوة ملاءمة النظام المختار |
| Ability-to-pay signal | 15 | إشارة القدرة على الدفع (مخاطرة + نضج الخدمات) |
| Evidence level | 10 | جودة الدليل العام |
| Low risk | 10 | انخفاض المخاطرة |

---

## كيفية الاشتقاق (Deterministic)

النقاط تُشتق آليًا من حقول الباقة (لا اجتهاد يدوي):

```txt
pain_clarity   = {L0:8, L1:14, L2:20, L3:23, L4:25}[evidence] + (2 إن وُجدت buying_signal)   ≤ 25
contact_avail  = {CC0:0, CC1:10, CC2:15, CC3:20}[contact_confidence]  (=0 إن none_found)       ≤ 20
system_fit     = {L0:12, L1:16, L2:18, L3:20, L4:20}[evidence]                                  ≤ 20
ability_to_pay = {low:12, medium:9, high:5}[risk] + (3 إن وُجدت services_detected)              ≤ 15
evidence       = {L0:2, L1:5, L2:8, L3:9, L4:10}[evidence]                                       ≤ 10
low_risk       = {low:10, medium:6, high:2}[risk]                                                ≤ 10
total = مجموع المكوّنات
```

---

## التصنيف (Rank Tiers)

```txt
none_found أو do_not_contact            → hold
total ≥ 78 و contact ≥ 10               → top_20_send
total ≥ 66                              → top_30_call
total ≥ 50                              → top_100
غير ذلك                                  → backlog
```

---

## مثال حقيقي من التشغيل (2026-06-03)

محسوب بـ `python3 scripts/validate_account_intelligence.py` على 10 باقات:

| Company | System | Score | Tier |
|---------|--------|------:|------|
| TrainMe KSA | whatsapp_client_os | 88 | top_20_send |
| BrightSmile Dental Clinic | whatsapp_client_os | 88 | top_20_send |
| TechVenture Partners | executive_command_os | 88 | top_20_send |
| LegalEdge SA | proposal_proof_os | 88 | top_20_send |
| Digital Rise Agency | revenue_os | 83 | top_20_send |
| Growth Labs SA | followup_recovery_os | 68 | top_30_call |
| CloudShift Consulting | proposal_proof_os | 68 | top_30_call |
| Nexus IT Solutions | revenue_os | 63 | top_100 |
| LearnFast Academy | followup_recovery_os | 63 | top_100 |
| Alpha Consulting Group | executive_command_os | 29 | hold |

**التوزيع:** top_20_send=5 · top_30_call=2 · top_100=2 · hold=1.

> لاحظ: Alpha Consulting Group (L0، بلا قناة عامة) سقط تلقائيًا إلى `hold` — وهذا
> المقصود: لا نُرسل لمن لا نملك له قناة عامة، ولا نختلق له تواصلًا.
