# Dealix — ما لا نُبنى

## المبدأ الأساسي

**Strategic "No" هو قوة.**

كل "لا" هي:
- حماية للموارد
- تركيز على القيمة
- تقليل المخاطر
- بناء منتج متماسك

---

## категории لا نُبنى

### 1. Cold Outreach Automation

| لا نُبنى | السبب | البديل |
|----------|-------|--------|
| Cold email automation بدون موافقة | Spam risk, compliance | Warm intro first |
| Cold WhatsApp | Consent required | Opt-in flow |
| LinkedIn automation | Platform TOS violation | Manual outreach |
| Mass cold DM | Risk to reputation | Targeted warm |

### 2. Scraping & Data Collection

| لا نُبنى | السبب | البديل |
|----------|-------|--------|
| Broad scraping | Legal risk, quality | Manual research |
| Automated data collection | Compliance | Curated lists |
| LinkedIn profile scraping | TOS violation | Public data only |

### 3. General AI Chatbots

| لا نُبنى | السبب | البديل |
|----------|-------|--------|
| General purpose chatbot | Not our focus | Domain-specific bots |
| Open-ended AI assistant | Unpredictable | Templated flows |
| Autonomous AI agent | Risk without oversight | Human-in-loop |

### 4. Production Deploy Automation

| لا نُبنى | السبب | البديل |
|----------|-------|--------|
| Auto-deploy to production | Risk | Manual approval gates |
| Auto-rollback | Complex | Manual rollback plan |
| Auto-scaling بدون limits | Cost risk | Measured scaling |

### 5. Custom Enterprise Features

| لا نُبنى | السبب | البديل |
|----------|-------|--------|
| Enterprise SSO قبل MVP | Not repeatable | Basic auth |
| Custom integrations | One-off work | API-first |
| Bespoke workflows | Devours resources | Standard playbooks |

### 6. Complex Agent Frameworks

| لا نُبنى | السبب | البديل |
|----------|-------|--------|
| Multi-agent orchestration | Premature | Single-purpose agents |
| Autonomous decision making | Risk | Human approval |
| Self-improving agents | Unpredictable | Measured improvements |

---

## Anti-Patterns

| Anti-Pattern | السبب |
|--------------|-------|
| "Everyone asks for it" | لا يعني قيمة حقيقية |
| "Competitor has it" | لا يعني يناسبنا |
| "It would be cool" | ليس كافي |
| "We could easily add it" | ليس أولوية |

---

## Decision Framework

### اسأل دائماً:

1. **هل هناك إشارة عميل واضحة؟**
   - لا إشارة = لا بناء

2. **هل يوافق على ICP؟**
   - لا = لا بناء

3. **هل يُحقق إيراد أو يُقلل تكلفة؟**
   - لا = لا بناء

4. **هل المخاطرة مقبولة؟**
   - Risk > 7 = لا بناء

5. **هل يُبنى بسرعة؟**
   - Effort > 3 months = تأجيل

6. **هل يُكرر our core value?**
   - لا = لا بناء

---

##灰色的区域 (Gray Areas)

### Might Build Later

| Feature | Condition |
|---------|-----------|
| LinkedIn automation | إذا توفر consent + legal clarity |
| Advanced AI | بعد إثبات القيمة الأساسية |
| Enterprise features | بعد 10 عملاء متكررين |

### Never Build

| Feature | Reason |
|---------|--------|
| Spam tools | Reputation risk |
| Fake engagement | Ethical violation |
| Data theft | Legal risk |
| Deceptive practices | Trust risk |

---

## Execution

### عند طلب feature "لا نُبنى":

1. **استمع**: فهم الحاجة
2. **اشرح**: لماذا لا الآن
3. **اقترح**: بديل أو حل مؤجل
4. **سجل**: في feedback log
5. **تابع**: إذا تغيرت الظروف

---

## _links

- Strategy: `PRODUCT_STRATEGY_AR.md`
- Principles: `PRODUCT_PRINCIPLES_AR.md`
- MVP Scope: `MVP_SCOPE_AR.md`
- Feature Prioritization: `FEATURE_PRIORITIZATION_AR.md`
