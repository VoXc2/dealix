# Dealix Slack Founder Room V1

## الدور

Slack هو **واجهة Founder Command / Decision / Proof Mirror** فقط. ليس مصدر الحقيقة التجاري أو المالي أو البرمجي.

مصادر الحقيقة الحاكمة تبقى:

- GitHub
- Dealix Company OS
- Commercial State
- Proof Ledger
- verified external evidence

## Workspace

- Workspace: `Dealix`
- Team ID: `T0AV61YPQ9X`
- Domain: `dealixworkspace.slack.com`

## القنوات

### `#dealix-command`

Channel ID المثبت: `C0BTMAWR3NY`

الاستخدام:
- أوامر المؤسس
- President briefs
- طلبات التنفيذ الداخلي L0-L4
- Daily/weekly command

### `#dealix-decisions`

يعرض فقط:
- CASH
- DECISIONS
- RISKS
- APPROVALS
- NEXT ACTION

### `#dealix-proof-log`

مرآة:
- receipts
- verification
- proof evidence

### `#dealix-revenue`

مرآة Revenue OS الداخلية.

### `#dealix-build`

مرآة Development Factory / repository / verification.

معرّفات القنوات غير المثبتة تبقى `UNKNOWN_NOT_EVIDENCE_BACKED` حتى يتم اكتشافها من Slack مباشرة.

## مسار التنفيذ المطلوب

```text
#dealix-command
→ Slack Socket Mode ingress
→ President / canonical Company Autopilot
→ bounded canonical agents/workloads
→ execution receipt
→ Slack response
→ proof mirror
```

لا يعتبر إرسال رسالة Slack تنفيذًا بحد ذاته.

معيار القبول الحقيقي هو رد يحتوي على:

- `workload_id`
- `source_sha`
- `receipt_reference`

ثم وجود receipt مطابق على الـVPS يثبت أن canonical Company Autopilot استهلك الطلب بالفعل.

## Bridge contract

المكونات المستهدفة:

- service: `dealix-slack-founder.service`
- adapter: `/opt/dealix/control/bin/dealix_slack_founder_bridge.py`
- secret file: `/opt/dealix/control/etc/slack-founder.env`
- receipt dir: `/opt/dealix/control/runs/slack-founder-receipts`

المتغيرات المطلوبة:

- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`
- `DEALIX_SLACK_COMMAND_CHANNEL_ID=C0BTMAWR3NY`
- `DEALIX_SLACK_FOUNDER_USER_ID=<founder-user-id>`

الأسرار لا تدخل GitHub أو logs.

## Socket Mode

المطلوب في Slack App:

- App-level token مع `connections:write`
- Bot scopes بالحد الأدنى اللازم للأحداث والردود
- `app_mention` event
- إضافة التطبيق إلى private `#dealix-command`
- `files:read` فقط إذا كان مطلوبًا قراءة ملفات Founder Room

لا يتم إنشاء public HTTP ingress على الـVPS لهذا المسار.

## Pro — أقصى استفادة بدون lock-in

يمكن استخدام Pro مؤقتًا في:

- Canvases
- Lists
- Workflow Builder
- Conversation summaries
- Huddle notes
- Custom sidebar sections
- App integrations

لكن ممنوع أن تصبح أي ميزة Pro-only owner وحيدًا لـ:

- business truth
- authority
- proof
- commercial state
- execution state

### Canvases المقترحة

- Founder Operating Constitution
- Company Machine Map
- Revenue Desk Playbook
- Proof & Governance Playbook
- Development Factory Runbook

### Lists المقترحة

- Action Queue
- Approval Queue
- Relationship / Opportunity Queue
- Proof Queue
- Build Gap Queue

### Workflows المقترحة

- Founder Command Intake
- Approval Request
- Real Interaction Capture
- Proof Receipt Intake
- Proven Gap / Build Request
- Incident / Risk Capture

كلها mirrors/intake surfaces؛ canonical state يبقى داخل Dealix.

## Authority

Slack لا يرفع السلطة.

L0-L4 الداخلي يمكن تنفيذه تلقائيًا حسب السياسة الحالية.

L5 يبقى Specific Approval Required، بما فيه:

- customer-facing send
- public publish
- binding quote/discount
- payment/refund/spend
- legal commitment
- merge to main
- production/DNS/DB/secrets mutation

## Truth Firewall

```text
slack_message != execution
draft != sent
research != relationship
public_contact_data != consent
proposal != revenue
invoice != payment
synthetic != customer_proof
```

## Founder UX

الواجهة النهائية للمؤسس تبقى:

`CASH / DECISIONS / RISKS / APPROVALS / NEXT_ACTION`

أي تفاصيل تشغيلية أدنى يجب أن تديرها Company Autopilot والـagents داخليًا وتعود فقط عند الحاجة أو كدليل.

## Acceptance

لا نعلن Slack bridge = PASS إلا بعد تحقق كل التالي:

1. Socket Mode authenticated.
2. Bot installed in Workspace Dealix.
3. Bot invited to `#dealix-command`.
4. `dealix-slack-founder.service` active and restart-safe.
5. Founder command produces `workload_id`.
6. Response includes canonical `source_sha`.
7. Response includes receipt reference.
8. Receipt exists on VPS and matches response.
9. Company Autopilot consumption is proven, not inferred from service health alone.
10. No timer, scheduler or agent fleet جديدة أضيفت.

الحالة حتى يتم إثبات end-to-end receipt:

`BLOCKED_UNTIL_NEW_WORKSPACE_SOCKET_MODE_CREDENTIALS_AND_END_TO_END_RECEIPT`
