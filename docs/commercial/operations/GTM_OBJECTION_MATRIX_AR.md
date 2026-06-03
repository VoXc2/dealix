# مصفوفة اعتراضات GTM — مكالمات حية

**مصدر آلي:** [objection_engine_registry.yaml](objection_engine_registry.yaml)  
**تفصيل PDPL:** [MARKET_INTELLIGENCE_OBJECTIONS_PDPL_AR.md](../MARKET_INTELLIGENCE_OBJECTIONS_PDPL_AR.md)

---

## جدول سريع (رد ≤ 30 ثانية)

| الاعتراض | التصنيف | الرد الجوهر (عربي) | أصل |
|----------|---------|-------------------|-----|
| عندنا CRM | positioning | CRM يخزّن؛ من يملك follow-up وevidence؟ | `crm_exists` |
| عندنا وكالة | wedge | الوكالة تجيب الاهتمام؛ نثبت ما بعده | `have_agency` |
| السعر عالي | pricing | 10 leads · 7 أيام · Proof ثم قرار | `price_high` |
| AI خطر / PDPL | compliance | موافقة بشرية · لا إرسال بارد · DPA | `pdpl_ai_risk` |
| نريد demo طويل | process | Discovery 7 أسئلة · 10 دقائق ثم Proof | `long_demo` |
| نبني داخلياً | build_vs_buy | Revenue Memory + حوكمة جاهزة أسرع من CRM+سكربتات | `build_inhouse` |

---

## بعد كل اعتراض

1. سجّل `objection_primary` في [founder_meeting_debrief_template.yaml](founder_meeting_debrief_template.yaml)
2. إن تكرر ≥ 2 مرات/أسبوع → حدّث registry + مسودة AEO
3. لا تعدّ وعود امتثال خارج [MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md](../MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md)
