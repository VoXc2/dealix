# مقارنة GTM خارجية — مرجع للمؤسس

**الغرض:** وضع Dealix في سياق أنظمة GTM الحديثة **بدون ادعاءات أداء** لـ Dealix.

---

## ما تفعله المنصات الخارجية (نمط 2025–2026)

| مصدر | التركيز | ما يُؤتمت عادة |
|------|---------|----------------|
| [ACT Playbook](https://www.actplaybook.com/) | ICP، personas، value architecture، قوالب صفقات | Playbooks + AI من صفقات سابقة |
| [RVNU](http://rvnu.co/) | إطار 16 مرحلة، GTM debt، benchmarks | تقييم وتوجيه مؤسس |
| [Closing Foundry](https://www.closingfoundry.com/playbooks) | Playbooks مضمّنة في workflow، stage-gating | Qualification + messaging في التدفق |
| Deal OS / Sales Playbook Builder | Audit → Align → Assemble → Accelerate | AI على playbooks مخصّصة |

**النمط المشترك:** ICP واضح · مسار صفقة مكرر · scorecards · تعلّم من النتائج — **ليس** إرسال بارد بلا حوكمة.

---

## ما تفعله Dealix (تمييز)

| بعد | Dealix |
|-----|--------|
| الفئة | **Post-Lead Revenue Operations** — بعد الـ lead وليس «أداة AI عامة» |
| المعيار | **SOAEN** (مصدر، مالك، موافقة، دليل، خطوة تالية) |
| المنتج الأول | **Proof Pack** — ليس dashboard فقط |
| الوتد | **Agency Wedge** — وكالات + proof لعملائهم |
| الثقة | **Trust Layer** — لا cold WhatsApp، لا fake proof، موافقة بشرية |
| التشغيل اليومي | `run_founder_revenue_day` + War Room + evidence events |

---

## متى تقتبس من الخارج

- **من ACT/Closing Foundry:** قوالب Discovery واعتراضات → [objection_engine_registry.yaml](objection_engine_registry.yaml)
- **من RVNU:** سؤال «GTM debt» أسبوعياً في Control Tower
- **لا تقتبس:** إرسال جماعي بارد · ضمان ROI · أتمتة خارجية بلا approval

---

## سياق خارجي 2025–2026 (اتجاهات — تحقق من مصادرك)

| موضوع | مرجع | ملاحظة لـ Dealix |
|-------|------|------------------|
| GTM حسب ACV (PLG vs SLG vs Hybrid) | [ProductQuant GTM Guide](https://productquant.dev/blog/complete-gtm-strategy-guide/) | Diagnostic + Proof = SLG/ثقة عالية |
| Playbook مؤسس B2B | [Design Revision GTM](https://designrevision.com/blog/b2b-saas-go-to-market-strategy) | قناتان، ICP حاد، أول عملاء يدوياً |
| SaaS + AI + مقاييس | [MakeToCreate B2B SaaS 2026](https://maketocreate.com/b2b-saas-2026-complete-guide-to-metrics-gtm-ai/) | NRR/CAC اتجاهات فقط — KPI من CRM عندك |
| اعتماد SaaS في الخليج | [Gulf SaaS Review 2026](https://gulfsaasreview.com/article/saas-adoption-gcc-2026-landscape-report) | CRM/تعاون/أمن — يدعم Risk Score + Ops |
| مبيعات GCC | [Al-Bahr GCC Sales 2026](https://al-bahr-growth-advisory.com/en/blog/sales-strategy-gcc-2026/) | لجان شراء، موسمية، شركاء |

**خريطة موحّدة (داخلية + خارجي):** [COMMERCIAL_VALUE_MAP_AR.md](../COMMERCIAL_VALUE_MAP_AR.md)

---

## مقاييس B2B SaaS (خارجي — للمقارنة فقط)

> لا تُدخل هذه الأرقام في Dealix تلقائياً. صدّقها من مصدرك أو من CRM.

| المقياس | اتجاه شائع (مصادر عامة 2025–2026) | ماذا تراقب في Dealix |
|---------|-----------------------------------|----------------------|
| LTV:CAC | هدف ~3:1+ للنضج | بعد أول 3 عملاء مدفوعين — من CRM |
| CAC payback | أشهر أقل للـ PLG؛ أطول للـ enterprise | Diagnostic = payback أطول · قلّل هدر القنوات |
| NRR | ~106% وسط · 115%+ top quartile | Growth فقط بعد Proof |
| Pipeline forecast | تتبع أسبوعي يحسّن الدقة | `founder_weekly_scorecard` + evidence CSV |
| Time to first value | حرج في GCC (ثقة) | `time_to_proof_days` في KPI registry |

**سؤال RVNU أسبوعياً (GTM debt):** هل تبني قنوات قبل ICP؟ هل تبيع قبل Proof repeatable؟ هل الأتمتة تسبق الموافقة؟

---

## مصفوفة: متى تستخدم أداة خارجية vs Dealix

| الحاجة | خارجي (مثال) | Dealix |
|--------|--------------|--------|
| Playbook صفقة | ACT · Closing Foundry | objection registry + Close Engine |
| تقييم GTM debt | RVNU | Control Tower + scorecard |
| إرسال بارد | — | **ممنوع** — مسودة + موافقة |
| إثبات للعميل | — | Proof Pack + evidence events |
| تسعير وحزم | مرجع سوق | DEALIX_REVOPS_PACKAGES (SoT) |

## روابط داخلية

- [GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md](../GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md) — تطبيق بحث الويب (ABM، لوب، أدلة)
- [DEALIX_UNIFIED_REVENUE_ATLAS_AR.md](../DEALIX_UNIFIED_REVENUE_ATLAS_AR.md)
- [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](../DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md)
- [FOUNDER_REVENUE_DAY_ONE_AR.md](../../ops/FOUNDER_REVENUE_DAY_ONE_AR.md)
