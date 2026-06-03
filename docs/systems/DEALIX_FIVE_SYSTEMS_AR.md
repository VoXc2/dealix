# Dealix — الأنظمة الخمسة الأساسية (Five Launch Systems)

*Single source of truth — تستند إليه باقات الحسابات، التقييم، الاستهداف، العروض، والتسليم.*
*آخر تحديث: 2026-06-03*

كل نظام له **slug ثابت** يُستخدم في البيانات والـ schemas، واسم خارجي للعرض،
وألم، و First Sprint بسعر افتتاحي، ومخرجات، ومدخلات مطلوبة، ودور تواصل مستهدف.

| slug | الاسم الخارجي | First Sprint | السعر الافتتاحي | الحصة الليلية |
|------|----------------|--------------|----------------:|--------------:|
| `revenue_os` | Revenue Operating System | Revenue Leakage Sprint | 4,500 SAR | 100 |
| `executive_command_os` | Executive Command OS | Daily Command Sprint | 5,500 SAR | 70 |
| `followup_recovery_os` | Follow-up Recovery OS | 7-Day Follow-up Recovery Sprint | 3,500 SAR | 90 |
| `whatsapp_client_os` | WhatsApp Client OS | WhatsApp Flow Sprint | 4,500 SAR | 70 |
| `proposal_proof_os` | Proposal & Proof OS | Proposal & Proof Sprint | 3,000 SAR | 70 |

> مجموع الحصص الليلية = **400** (يتحقق آليًا في `scripts/validate_account_intelligence.py`).

---

## 1. Revenue Operating System — `revenue_os`

- **الألم:** الفرص تضيع ولا يوجد next action واضح.
- **First Sprint:** Revenue Leakage Sprint — **4,500 SAR**
- **المخرجات:** Revenue Leakage Map · Opportunity Stage Model · Follow-up Workflow · Draft Templates · Revenue Report
- **المدخلات المطلوبة:** lead sources · current pipeline stages · sample leads · current follow-up process · sales owner
- **الدور المستهدف:** Head of Sales / Founder → (بديل) Marketing Manager / GM
- **سبب الاستهداف:** مسؤول عن الفرص والإيراد.

## 2. Executive Command OS — `executive_command_os`

- **الألم:** الإدارة لا ترى القرار اليومي.
- **First Sprint:** Daily Command Sprint — **5,500 SAR**
- **المخرجات:** KPI Map · Daily Command Report · Risk/Priority Matrix · Decision Log · Executive Action Board
- **المدخلات المطلوبة:** company goals · current KPIs · weekly reports · risk areas · decision owners
- **الدور المستهدف:** Founder / CEO / GM → (بديل) Operations Manager
- **سبب الاستهداف:** يملك قرار الإدارة والتقارير.

## 3. Follow-up Recovery OS — `followup_recovery_os`

- **الألم:** المتابعة تضيع.
- **First Sprint:** 7-Day Follow-up Recovery Sprint — **3,500 SAR**
- **المخرجات:** Follow-up Queue · Lead Status Model · Message Set · Recovery Report · Escalation Rules
- **المدخلات المطلوبة:** lead list · last contact date · lead statuses · message samples · follow-up channel
- **الدور المستهدف:** Sales Manager / Marketing Manager → (بديل) Founder
- **سبب الاستهداف:** يملك المتابعة والحملات.

## 4. WhatsApp Client OS — `whatsapp_client_os`

- **الألم:** واتساب مليء بالمحادثات غير المنظمة.
- **First Sprint:** WhatsApp Flow Sprint — **4,500 SAR**
- **المخرجات:** WhatsApp Flow Map · Readiness Scan · Action Cards · Human Handoff Policy · Secure Portal Handoff
- **المدخلات المطلوبة:** conversation types · FAQs · handoff cases · links/forms · support roles
- **الدور المستهدف:** Operations / Customer Service Manager → (بديل) Founder / Clinic Manager
- **سبب الاستهداف:** يملك تجربة العميل والواتساب.

> ملاحظة منصة: WhatsApp Business Platform / Cloud API مناسبة لخدمة العملاء
> والتجارة الحوارية والتكامل مع الأنظمة، لكنها ليست واجهة جاهزة بذاتها وتحتاج تجربة
> مبنية فوقها. القيود الحديثة تستهدف general-purpose AI chatbots، بينما تبقى
> customer-support / business workflows أكثر ملاءمة. **WhatsApp Client OS ينظّم
> المحادثات الواردة للعميل — ولا يُرسِل رسائل cold إطلاقًا.**

## 5. Proposal & Proof OS — `proposal_proof_os`

- **الألم:** العروض لا تقنع أو تتأخر.
- **First Sprint:** Proposal & Proof Sprint — **3,000 SAR**
- **المخرجات:** Proposal Template · Proof Pack Template · Scope Block · Risk & Assumption Block · Next-step Card
- **المدخلات المطلوبة:** service description · old proposal · pricing range · objections · proof/examples · scope boundaries
- **الدور المستهدف:** Founder / BD / Sales Lead → (بديل) Marketing Manager
- **سبب الاستهداف:** يملك العروض والإقناع.

---

## قاعدة الاختيار (System Selection Rule)

يُختار **نظام واحد فقط** لكل شركة بناءً على الألم الأوضح من الدليل العام:

```txt
الفرص تضيع / لا next action            → revenue_os
الإدارة لا ترى القرار اليومي           → executive_command_os
المتابعة تضيع / ردود متأخرة            → followup_recovery_os
واتساب هو القناة الأساسية للعميل       → whatsapp_client_os
العروض تتأخر / لا تقنع                  → proposal_proof_os
```

عند تساوي الإشارات، يُفضَّل النظام الذي **تتوفر له قناة تواصل عامة أوضح** و**أعلى ملاءمة**.
