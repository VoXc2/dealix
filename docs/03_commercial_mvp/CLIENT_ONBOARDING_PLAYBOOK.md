# Client Onboarding Playbook — دليل تأهيل العميل
# كتيّب تأهيل عميل سبرنت ذكاء الإيرادات | Revenue Intelligence Sprint Onboarding SOP

> **Purpose / الغرض:** Bilingual SOP for every touchpoint from contract signature to post-sprint retainer pitch. One owner: Founder. Cross-links: [SPRINT_DELIVERY_PLAYBOOK.md](./SPRINT_DELIVERY_PLAYBOOK.md) | [DIAGNOSTIC_DELIVERY_SOP.md](./DIAGNOSTIC_DELIVERY_SOP.md) | [RETAINER_PATH.md](./RETAINER_PATH.md) | [../../templates/PROPOSAL_SPRINT_ARABIC_FULL.md.j2](../../templates/PROPOSAL_SPRINT_ARABIC_FULL.md.j2)

---

## Day 0 — Contract Signed + Payment Received + Welcome Sent
## اليوم 0 — توقيع العقد + استلام الدفعة + إرسال الترحيب

### Founder checklist / قائمة تحقق المؤسس

- [ ] Proposal acceptance recorded in writing (email or WhatsApp message screenshot).
- [ ] Moyasar payment link confirmed cleared (first 50% — 249.50 SAR).
- [ ] Engagement ID assigned: `SPRINT-<YYYYMMDD>-<CLIENT_HANDLE>`.
- [ ] Folder created: `engagements/<engagement_id>/`.
- [ ] Welcome email sent within two hours of payment clearance.
- [ ] WhatsApp confirmation sent (requires founder approval before send).
- [ ] Day 1 kickoff time confirmed in writing.

### Welcome email template / قالب بريد الترحيب

**Subject / الموضوع:** أهلاً بـ {{ company_name }} في Dealix — بدء سبرنت ذكاء الإيرادات / Welcome to Dealix — Sprint Kickoff Confirmed

---

أهلاً {{ contact_name }}،

نؤكّد استلام دفعتكم الأولى (249.50 ريال) ونرحّب بكم في **سبرنت ذكاء الإيرادات**.

**رقم المشروع:** `{{ engagement_id }}`
**موعد جلسة الانطلاق:** غداً، {{ kickoff_time }}
**مدة الجلسة:** 45 دقيقة
**قناة الجلسة:** {{ meeting_link }}

ما تحتاج تحضيره قبل الجلسة:
- ملف بياناتكم (CSV أو تصدير CRM أو قائمة يدوية)
- الشخص المسؤول عن متابعة السبرنت من جهتكم
- سؤال عمل واحد تريدون الإجابة عنه

لا تُرسَل أي رسائل باسمكم دون موافقتكم الصريحة.

للتواصل: {{ founder_whatsapp }}

---

Hello {{ contact_name }},

We confirm receipt of your first payment (249.50 SAR) and welcome you to the **Revenue Intelligence Sprint**.

**Engagement ID:** `{{ engagement_id }}`
**Kickoff session:** Tomorrow, {{ kickoff_time }}
**Duration:** 45 minutes
**Meeting link:** {{ meeting_link }}

Please prepare before the session:
- Your data file (CSV, CRM export, or manual list)
- A named workflow owner on your side
- One business question you want answered

Nothing will be sent on your behalf without your explicit approval.

---

### Day 0 WhatsApp confirmation template
### قالب واتساب — تأكيد اليوم 0

```
أهلاً {{ contact_name }} —

تأكيد: وصل الدفع بنجاح. رقم مشروعكم: {{ engagement_id }}.

جلسة الانطلاق غداً {{ kickoff_time }}. أرسلت لكم بريد إلكتروني بالتفاصيل.

— {{ founder_name }} | Dealix
```

**حوكمة:** يتطلب موافقة المؤسس قبل الإرسال.

---

## Day 1 — Intake Session (45 min) + Source Passport
## اليوم 1 — جلسة الاستلام + جواز المصدر

### Session agenda / أجندة الجلسة

| Minute | Topic (EN) | الموضوع (AR) |
|--------|------------|--------------|
| 0–5 | Introductions + sprint overview | مقدمات + نظرة عامة على السبرنت |
| 5–15 | Data file review — source, volume, fields | مراجعة ملف البيانات — المصدر، الحجم، الحقول |
| 15–25 | Single workflow declaration | تحديد سير العمل الواحد |
| 25–35 | Source Passport: ownership, purpose, retention | جواز المصدر: الملكية، الغرض، الاحتفاظ |
| 35–45 | Day-by-day expectations + approval protocol | التوقعات اليومية + بروتوكول الموافقة |

### Data collection template / قالب جمع البيانات

```json
{
  "engagement_id": "{{ engagement_id }}",
  "company_name": "{{ company_name }}",
  "workflow_owner": "NAME | TITLE | PHONE",
  "data_source": "crm_export | csv | manual_entry",
  "data_file": "FILENAME.csv",
  "record_count_estimate": 0,
  "primary_workflow": "ONE SENTENCE — e.g. dormant account revival",
  "business_question": "ONE SENTENCE",
  "languages_required": ["ar", "en"],
  "pii_flag": true,
  "sensitivity": "s1 | s2 | s3",
  "retention_days": 90,
  "allowed_use": "sprint_only"
}
```

### Source Passport — minimum required fields
### جواز المصدر — الحقول الإلزامية

- `owner`: company legal name
- `source_type`: `client_upload` / `crm_export` / `manual_entry` (never `scraped`)
- `allowed_use`: `sprint_only` (expands to `retainer` only if client signs renewal)
- `pii_flag`: true/false
- `sensitivity`: S1 (public) / S2 (internal) / S3 (confidential)
- `retention_days`: 90 default
- `signed_by`: client workflow owner name + date

**Gate:** Sprint does not proceed to Day 2 without a signed Source Passport.

### Day 1 end-of-day client update template
### قالب تحديث العميل — نهاية اليوم 1

```
{{ contact_name }} —

اليوم 1 مكتمل. ✓ جواز المصدر موقَّع. ✓ ملف البيانات مُستلَم.

غداً: استيراد البيانات وفحص الجودة. ستصلك درجة جودة بياناتكم قبل الساعة 6م.

لا يوجد قرار مطلوب منكم الآن.

— {{ founder_name }} | Dealix
```

**حوكمة:** يتطلب موافقة المؤسس قبل الإرسال.

---

## Days 1–7 — Daily Workflow
## الأيام 1–7 — سير العمل اليومي

### Day 2 / اليوم 2

**Founder actions:**
1. Run data import preview (non-destructive sample read).
2. Compute DQ score across six dimensions: completeness, validity, uniqueness, consistency, timeliness, conformance.
3. Produce deduplication report with merge rules.
4. Decision gate: DQ < 40 → pause, propose Data Pack; DQ 40–70 → proceed with documented caveats; DQ ≥ 70 → proceed clean.

**Client update template:**
```
{{ contact_name }} — تحديث اليوم 2.

درجة جودة بياناتكم: {{ dq_score }}/100.
{{ dq_note }}

غداً: ترتيب الحسابات واختيار أفضل 10.

— {{ founder_name }} | Dealix
```

---

### Day 3 / اليوم 3

**Founder actions:**
1. Run account scoring on the imported, deduped, DQ-checked dataset.
2. Produce ranked list of top 10 accounts with: fit score, signal strength, governance risk flag, human-readable justification for each.
3. Review: every explanation must be readable and verifiable. Demote any opaque rank.

**Client update template:**
```
{{ contact_name }} — تحديث اليوم 3.

ترتيب الحسابات مكتمل. أفضل 10 حسابات مُحدَّدة مع مبررات واضحة.

غداً: توليد مسودّات التواصل ومراجعة الحوكمة.

— {{ founder_name }} | Dealix
```

---

### Day 4 / اليوم 4

**Founder actions:**
1. Generate bilingual draft pack (AR + EN). All drafts marked `draft_only`.
2. Apply 7-decision governance matrix: ALLOW / DRAFT_ONLY / REQUIRE_APPROVAL / REDACT / BLOCK / RATE_LIMIT / REROUTE.
3. Review every BLOCK and every REDACT. Log all decisions.
4. Confirm: no draft is sent from Dealix infrastructure. Client decides if and when to send each draft.

**Client update template:**
```
{{ contact_name }} — تحديث اليوم 4.

مسودّات التواصل جاهزة للمراجعة ({{ draft_count }} مسودة).
{{ blocked_count }} مسودة أُوقفت لأسباب امتثالية — سيتضمّن التقرير النهائي التفاصيل.

لا شيء يُرسَل باسمكم. كل مسودة تتطلب موافقتكم قبل الإرسال.

غداً: تجميع حزمة الإثبات.

— {{ founder_name }} | Dealix
```

---

### Day 5 / اليوم 5

**Founder actions:**
1. Assemble 14-section Proof Pack: intake, passport, DQ, dedupe, scoring, drafts, governance decisions, redactions, approvals, value-tier mapping, capital asset registration, limitations, methodology, signatures.
2. Compute proof score. Minimum 70 to proceed to handoff.
3. If proof score < 70: extend sprint one day for remediation; do not deliver below threshold.

**Client update template:**
```
{{ contact_name }} — تحديث اليوم 5.

حزمة الإثبات جاهزة. درجة الإثبات: {{ proof_score }}/100.

غداً: جلسة تسليم 60 دقيقة — نستعرض كل شيء معاً.
سأرسل رابط الجلسة الآن.

— {{ founder_name }} | Dealix
```

---

### Day 6 / اليوم 6

**Founder actions:**
1. Conduct 60-minute bilingual handoff session (AR + EN).
2. Walk through Proof Pack section by section.
3. Assess retainer readiness: proof_score ≥ 80 AND adoption_score ≥ 70 AND named workflow owner persists.
4. If criteria met: present retainer offer. If not: offer second sprint or graceful close-out.

**Handoff session agenda:**
- 0–10 min: Sprint summary (what ran, what was found)
- 10–25 min: Top 10 accounts walkthrough
- 25–40 min: Draft pack and governance decisions review
- 40–50 min: Proof Pack score and capital assets
- 50–60 min: Next step recommendation (retainer / second sprint / close-out)

---

### Day 7 / اليوم 7

**Founder actions:**
1. Register at least one Capital Ledger asset (scoring rule, template, sector insight, or proof example).
2. Draft case-safe summary using the template in `docs/case-studies/`.
3. Collect second payment (249.50 SAR) — send Moyasar link if not already paid on Day 6.
4. Mark engagement `status=delivered` in the registry.

**Day 7 WhatsApp close template:**
```
{{ contact_name }} —

السبرنت مكتمل. حزمة الإثبات والملفات في صندوق بريدكم.

رابط الدفعة الثانية (249.50 ريال): {{ payment_link }}

شكراً لثقتكم. نتحدث لاحقاً عن الخطوة التالية.

— {{ founder_name }} | Dealix
```

**حوكمة:** يتطلب موافقة المؤسس قبل الإرسال.

---

## Day 7 Delivery Checklist / قائمة تحقق التسليم — اليوم 7

- [ ] Source Passport signed and filed.
- [ ] DQ baseline score recorded.
- [ ] Deduplication report present.
- [ ] Top 10 ranked accounts with explainable justifications.
- [ ] Bilingual draft pack (AR + EN) marked `draft_only`.
- [ ] Governance decisions log complete (7-decision matrix).
- [ ] Redaction and block summary present.
- [ ] 14-section Proof Pack complete, proof score ≥ 70.
- [ ] At least one Capital Ledger asset registered.
- [ ] 60-minute handoff session completed.
- [ ] Case-safe summary draft committed.
- [ ] Second payment received.
- [ ] Engagement marked `status=delivered`.

---

## Post-Sprint — Retainer Pitch Timing and Script
## ما بعد السبرنت — توقيت عرض الاحتفاظ وسكريبت المحادثة

### Timing / التوقيت

The retainer conversation belongs at Day 6 (handoff session), not Day 7. By Day 6 the client has seen the Proof Pack. Evidence is in front of them. The conversation is grounded in data, not in a sales pitch.

If the client is not ready at Day 6, send a follow-up on Day 14 post-sprint.

### Eligibility criteria / معايير الأهلية

- `proof_score >= 80`
- `adoption_score >= 70`
- Named workflow owner remains committed post-sprint
- Source Passport renewable for ongoing use
- At least one Capital Ledger asset deposited

### Retainer pitch script (bilingual) / سكريبت عرض الاحتفاظ

**Arabic:**
بناءً على نتائج السبرنت — درجة الإثبات {{ proof_score }} وسير العمل الواضح — نرى أن شركتكم مؤهّلة للانتقال إلى **عقد الاحتفاظ الشهري بإدارة عمليات الإيرادات**. العقد بـ 2,999 ريال شهرياً (المستوى الأساسي) أو 4,999 ريال شهرياً (المستوى الكامل). يتضمّن: تجديد جواز المصدر، تحديث ترتيب الحسابات بانتظام، توليد مسودّات جديدة، ومراجعة حوكمة مستمرة. هل تودّون الاطلاع على نطاق العقد التفصيلي؟

**English:**
Based on your sprint results — proof score {{ proof_score }} and a clear workflow — your company qualifies for the **Managed Revenue Ops retainer**. The retainer is 2,999 SAR/month (lower tier) or 4,999 SAR/month (full tier). It covers: Source Passport renewal, cadenced account ranking, fresh draft packs, and ongoing governance review. Would you like to see the detailed retainer scope?

### Retainer follow-up WhatsApp (Day 14 post-sprint)
```
{{ contact_name }} —

مرّت أسبوعان على التسليم. كيف سارت الأمور مع القائمة؟

إذا وجدتم قيمة في المنهجية وتريدون الاستمرار شهرياً، يسعدني إرسال نطاق عقد الاحتفاظ.

— {{ founder_name }} | Dealix
```

**حوكمة:** يتطلب موافقة المؤسس قبل الإرسال.

---

## Cross-References / مراجع متقاطعة

- Sprint day-by-day method: [SPRINT_DELIVERY_PLAYBOOK.md](./SPRINT_DELIVERY_PLAYBOOK.md)
- Arabic proposal template: [../../templates/PROPOSAL_SPRINT_ARABIC_FULL.md.j2](../../templates/PROPOSAL_SPRINT_ARABIC_FULL.md.j2)
- English proposal template: [../../templates/PROPOSAL_SPRINT_ENGLISH_FULL.md.j2](../../templates/PROPOSAL_SPRINT_ENGLISH_FULL.md.j2)
- Retainer details: [RETAINER_PATH.md](./RETAINER_PATH.md)
- Source Passport schema: [../04_data_os/SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md)
- Non-negotiables: [../00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md)

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
