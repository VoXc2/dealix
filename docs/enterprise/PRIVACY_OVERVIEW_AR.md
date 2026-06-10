# Privacy Overview — Dealix (AR)

> **Companion to:** `docs/governance/PDPL_DATA_RULES.md`, `docs/governance/PII_REDACTION_POLICY.md`.

---

## 1. Commitment

تلتزم Dealix بـ:
- **PDPL السعودي** (نظام حماية البيانات الشخصية)
- مبادئ **Privacy by Design** و **Privacy by Default**
- **Data minimization** — نجمع فقط ما نحتاج
- **Purpose limitation** — لا نستخدم البيانات لغرض غير المعلن
- **Storage limitation** — نحدد retention صريح لكل class
- **Transparency** — نوضح ماذا نجمع ولماذا

## 2. Roles

| Role | Dealix؟ |
|------|---------|
| Controller | ❌ لا، العميل هو Controller للبيانات التي يقدمها |
| Processor | ✅ نعم، لـ client data المُعالج لصالح العميل |
| Sub-processor | ✅ نعم (مثل: LLM provider, email provider) — قائمة في DPA |

## 3. البيانات التي نعالجها (الفئات)

| الفئة | Source | Purpose | Legal basis |
|-------|--------|---------|-------------|
| Client account info | Signup | Service delivery | Contract |
| Lead/contact info | Client upload, public sources | Service delivery | Contract + legitimate interest |
| Communications drafts | Client use | Approval workflow | Contract |
| Usage logs | Auto | Service improvement + security | Legitimate interest |
| Payment info | Payment provider (Moyasar) | Billing | Contract |

**ما لا نجمعه:**
- ❌ بيانات أعمى (sensitive PII) ما لم يقدّمها العميل لغرض محدد وموثّق
- ❌ بيانات الأطفال (أقل من 18)
- ❌ بيانات biometric أو صحية

## 4. Cross-Border Transfers

- **Default region:** Saudi Arabia (provider availability variable)
- **Sub-processors خارج السعودية:** LLM providers (US/EU) — مع **SCCs / DPA addendums** + redaction
- **Adequacy decisions:** نحترم تقييم NDMO
- **Data residency commitment:** يُحدّد في DPA لكل عميل

## 5. Rights of Data Subjects (تُنفّذ عبر الـ Controller = العميل)

- Right of access → العميل يستطيع تصدير بياناته عبر portal
- Right of rectification → تحديث عبر portal
- Right of erasure → deletion workflow مع audit trail
- Right of restriction → opt-out workflow
- Right of portability → JSON export
- Right to object → suppression list
- Right to withdraw consent → opt-out

**SLA للاستجابة:** خلال 30 يوم كحد أقصى (PDPL).

## 6. Data Subject Request Workflow

```
[Request from client] → [Ticket opened] → [Identity verification] → [Action: export/rectify/erase/restrict] → [Audit log] → [Confirmation to client]
```

## 7. Breach Notification

- **Internal escalation:** فوري عند الـ detection
- **Customer notification:** خلال 72 ساعة من التأكد
- **NDMO notification:** خلال 72 ساعة (متطلب PDPL) — يتم عبر العميل كـ Controller، بمساعدتنا
- **Public disclosure:** يعتمد على severity

## 8. Children & Sensitive Data

- لا خدمة لمن هم أقل من 18
- Sensitive PII = D4+ class — لا يُقبل إلا في **sandboxed client-scoped** workflows مع DPA واضح

## 9. Sub-Processor List (يعتمد على إعدادات الـ Agent)

| Sub-processor | Purpose | Region | DPA |
|---------------|---------|--------|-----|
| LLM providers (varies per agent routing) | Text generation | US/EU | ✅ |
| Moyasar | Payment | SA | ✅ |
| Railway | Hosting | varies | ✅ |
| HubSpot (optional) | CRM | varies | ✅ |
| Twilio (optional) | WhatsApp | varies | ✅ |
| Resend (optional) | Email | US | ✅ |

> **كل sub-processor جديد** → review security + DPA، يُضاف للقائمة، يُخطر العملاء.

## 10. Audits & Certifications (Roadmap)

| Stage | Target |
|-------|--------|
| E3 | Internal privacy audit + DPA template جاهز |
| E4 | External privacy review + pen-test |
| E5 | SOC2 Type II مُخطط + ISO 27001 مُخطط |

---

> **Owner:** Founder + (يُعيَّن) Privacy Officer · **Review:** كل 90 يوم
