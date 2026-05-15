# العربية

**Owner:** المالك التجاري (Commercial Owner) — بالتنسيق مع مالك طبقة الحوكمة.

## قواعد الموافقة — المبيعات

تحدّد هذه الوثيقة من يوافق على إجراءات المبيعات وكيف. تُطبَّق عبر `auto_client_acquisition/approval_center/approval_policy.py` ومصفوفة `auto_client_acquisition/governance_os/approval_matrix.py`.

### القاعدة الحاكمة

كل إجراء مبيعات مواجِه للعميل يُعرض كمسوّدة فقط ولا يُنفَّذ دون موافقة موثَّقة. الوكيل يقترح، والمراجع يبتّ.

### جدول القواعد

| الإجراء | التصنيف | المُوافِق |
|---|---|---|
| تصنيف فرصة داخلياً | A0 | لا موافقة |
| صياغة مسوّدة عرض | A0 | لا موافقة (مسوّدة فقط) |
| إرسال عرض لعميل | A2 | مدير المبيعات |
| تعديل سعر معروض | A2 | مدير المبيعات |
| إطلاق حملة تواصل | A3 | المالك التجاري + مالك الحوكمة |
| منح خصم تجاري خارج النطاق | A3 | المالك التجاري + المالية |

### قيود غير قابلة للتفاوض

- لا وعد مبيعات أو معدلات تحويل مضمونة؛ تُستخدم "فرص مُثبتة بأدلة".
- لا ادعاء أرقام بلا مصدر موثَّق.
- لا تواصل بقنوات باردة (واتساب بارد، أتمتة LinkedIn).
- لا إرسال نيابة عن العميل دون موافقته الصريحة.

### الآلية

1. يصوغ الوكيل الإجراء كمسوّدة.
2. يُقيّمه محرّك السياسات؛ المخالفات تُحجب.
3. يُرفع للمُوافِق وفق الجدول؛ A3 يتطلب موافقة مزدوجة.
4. عند الموافقة فقط يُنفَّذ؛ كل خطوة قيد تدقيق.

### قائمة الجاهزية

- [x] كل إجراء مبيعات خارجي يتطلب موافقة موثَّقة.
- [x] الحملات تتطلب موافقة مزدوجة وتقييم مخاطر.
- [ ] إشعار فوري للمُوافِق عند رفع طلب A3 (مُخطَّط).

### الحوكمة والتراجع

- لا تفويض ذاتي؛ المراجع لا يوافق على إجراء اقترحه.
- تعديل الجدول يتطلب موافقة المالك التجاري ومالك الحوكمة وقيد تدقيق.

انظر أيضاً: `governance/policies/customer_communication_policy.md`، `governance/risk_models/action_risk_matrix.md`.

---

# English

**Owner:** Commercial Owner — in coordination with the Governance Platform Lead.

## Approval Rules — Sales

This document defines who approves sales actions and how. Enforced via `auto_client_acquisition/approval_center/approval_policy.py` and the matrix `auto_client_acquisition/governance_os/approval_matrix.py`.

### Governing rule

Every customer-facing sales action is presented draft-only and does not execute without a documented approval. The agent proposes, the reviewer decides.

### Rule table

| Action | Classification | Approver |
|---|---|---|
| Classify an opportunity internally | A0 | No approval |
| Draft a proposal | A0 | No approval (draft-only) |
| Send a proposal to a customer | A2 | Sales manager |
| Change a quoted price | A2 | Sales manager |
| Launch an outreach campaign | A3 | Commercial owner + governance owner |
| Grant an out-of-band commercial discount | A3 | Commercial owner + finance |

### Non-negotiable constraints

- No promise of guaranteed sales or conversion rates; "evidenced opportunities" is used.
- No claiming numbers without a documented source.
- No cold-channel outreach (cold WhatsApp, LinkedIn automation).
- No sending on a customer's behalf without their explicit approval.

### Mechanism

1. The agent drafts the action.
2. The Policy Engine evaluates it; breaches are blocked.
3. It is raised to the approver per the table; A3 requires dual approval.
4. Only on approval does it execute; every step is an audit entry.

### Readiness checklist

- [x] Every external sales action requires a documented approval.
- [x] Campaigns require dual approval and risk scoring.
- [ ] Instant approver notification on an A3 request (planned).

### Governance and rollback

- No self-approval; a reviewer does not approve an action they proposed.
- Changing the table requires the commercial owner's and governance owner's approval and an audit entry.

See also: `governance/policies/customer_communication_policy.md`, `governance/risk_models/action_risk_matrix.md`.
