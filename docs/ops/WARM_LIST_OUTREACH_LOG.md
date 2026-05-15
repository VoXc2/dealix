# Warm List Outreach Log

**نسخ هذا الملف لكل أسبوع.** كل صف = اتصال واحد. لا حذف ولا تعديل بعد التسجيل (audit trail).

**القواعد:**
- Warm = تعرفه شخصياً أو عبر معرّف موثوق. لا cold ولا scraping.
- WhatsApp فقط بـ explicit consent مسجّل.
- LinkedIn / Email يكتفى بـ draft → human-posts-manually (لا automate).
- Pre-call: حضّر `landing/services.html` + 3 أمثلة من العميل.
- Post-call: سجّل النتيجة هنا خلال 24 ساعة، حدّث `data/value-ledger.jsonl` لو ظهر استحقاق.

---

## Week of YYYY-MM-DD

| # | Date | Contact | Company | Sector | Channel | Intro source | Stage | Offer pitched | Decision | Next step | Owner | Notes |
|---|------|---------|---------|--------|---------|--------------|-------|---------------|----------|-----------|-------|-------|
| 1 |      |         |         |        |         |              |       |               |          |           |       |       |
| 2 |      |         |         |        |         |              |       |               |          |           |       |       |
| 3 |      |         |         |        |         |              |       |               |          |           |       |       |
| 4 |      |         |         |        |         |              |       |               |          |           |       |       |
| 5 |      |         |         |        |         |              |       |               |          |           |       |       |

### Field conventions

- **Stage:** `intro_sent` → `call_booked` → `call_done` → `proposal_sent` → `paid` / `lost` / `holding`.
- **Channel:** `whatsapp_warm` / `email_warm` / `linkedin_warm` / `phone` / `in_person`. (Never `cold_*`.)
- **Offer pitched:** must be one of the official 6 — `lead_intelligence_sprint`, `ai_quick_win_sprint`, `company_brain_sprint`, `ai_support_desk_sprint`, `ai_governance_program`, `client_ai_policy_pack`. Anything else = draft a custom scope first; do not commit.
- **Decision:** `yes_paid`, `yes_proposal_pending`, `no_fit`, `no_budget`, `no_timing`, `hold`, `info_only`.
- **Next step:** must have a date. If empty, the row is incomplete.

---

## Weekly Rollup (auto-fill end of week)

| Metric | Value |
|--------|-------|
| Conversations started | |
| Calls done | |
| Proposals sent | |
| Paid (number) | |
| Paid (SAR) | |
| In-flight (proposal pending) | |
| Lost — fit / budget / timing | |
| Top objection of the week | |
| Top winning angle of the week | |

**Friction log entries to file:** anything with response_time > 48h, anyone who asked for a feature we don't have, anyone who churned silently.

---

## Governance reminders (non-negotiables)

1. **Verified value only when source-referenced.** Quoting a number from a call without `source_ref` = `estimated` tier, never claimable externally.
2. **No bulk send.** Each row is a 1:1 conversation. If you find yourself templating > 5 in a row, stop and re-segment.
3. **Approval-first.** Anything that touches client data ⇒ Source Passport on file before any AI processing. Reference `auto_client_acquisition/data_os/source_passport.py::validate`.
4. **PDPL Art. 13 disclosure** in first email/message: "We process your contact data under Art. 13 of the Saudi PDPL — opt out anytime."
5. **No promises.** Replace "guaranteed", "100%", "definitely" with "we have observed X in Y engagements." Claim-safety gate is in `auto_client_acquisition/governance_os/claim_safety.py`.

---

## Templates (copy these)

### Warm intro — WhatsApp / Email

> صباح الخير {Name}. {Mutual} ذكر لي اهتمامكم بـ{topic}. أبني محرّك مبيعات لشركات B2B سعودية على بيانات نظيفة (PDPL، ZATCA). فيه عرض ابتدائي بـ1,500 ريال يطلع لك خريطة الفرص داخل البيانات الحالية. مهتم نتكلم 20 دقيقة هذا الأسبوع؟

### Post-call follow-up

> {Name}، شكراً على وقتك اليوم. ملخص اللي اتفقنا عليه:
> - {1 line on scope}
> - {1 line on timeline}
> - السعر: {amount} SAR — يشمل {deliverable}
> مرفق مقترح موقّع جاهز للتوقيع الإلكتروني. لو تحتاج تعديل بالنطاق، نتكلم قبل الجمعة.

### Soft decline acknowledgment

> {Name}، فهمت السبب وأقدّر صراحتك. حابب لو سمحت أحط اسمكم في قائمة المتابعة كل 60 يوم — تنفع تكتفي بـ"لا" ثانية لو ما تغيّر شيء.

---

_Source of truth: this file is the human-readable companion to `data/value-ledger.jsonl` and `data/friction-log/`. The CSV export from `scripts/export_outreach_ready.py` populates the table when the API is live._
