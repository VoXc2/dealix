# العربية

## موصّل التقويم — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

موصّل التقويم يربط Dealix بـ Google Calendar وCalendly لجدولة المواعيد ومتابعة الحجوزات. القاعدة الثابتة: أي حدث يدعو مشاركاً خارجياً يمر عبر بوّابة الموافقة.

### النطاق

- **Google Calendar:** إنشاء أحداث مباشرة على تقويم محدّد مع مشاركين اختياريين.
- **Calendly:** توفير رابط حجز عام، جلب الأحداث المجدولة، استقبال خطافات الحجز.
- **غير مدعوم:** حذف أحداث بالجملة، إرسال دعوات لمشاركين دون موافقة على التواصل.

### Google Calendar

ينفّذ `GoogleCalendarClient` في `integrations/calendar.py`:

- `create_event` ينشئ حدثاً بعنوان ووصف ووقت بدء/انتهاء ومشاركين، ويُرجِع `CalendarEventResult` بـ `event_id` و`html_link` و`meeting_link`.
- المصادقة عبر ملف مفتاح حساب خدمة JSON؛ المسار يُقرأ من `google_calendar_credentials_file`.
- الخاصية `configured` تؤكد توفّر بيانات الاعتماد قبل أي محاولة.

### Calendly

ينفّذ `CalendlyClient` في `integrations/calendar.py`:

- `scheduling_link` يُرجِع رابط الحجز العام — لا يرسل شيئاً، يوفّر رابطاً للعميل لاختيار وقته.
- `list_scheduled_events` يجلب الأحداث المجدولة الأخيرة مع إعادة محاولة بتراجع أسّي.
- خطافات Calendly الواردة تُتحقَّق توقيعاتها قبل المعالجة (انظر `platform/integrations/webhook_security.md`).

### الموثوقية والحوكمة

- حد المعدّل لـ `calendly`: 60 نداء/دقيقة، مهلة 8 ثوانٍ، 3 محاولات.
- إعادة المحاولة بتراجع أسّي عبر `tenacity` على المهلات وأخطاء HTTP.
- الفشل النهائي يُدفَع إلى DLQ ولا يكسر سير العمل.
- إنشاء حدث يدعو مشاركاً خارجياً إجراء يمر عبر `external_action_requires_approval`.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| عميل Google Calendar | `integrations/calendar.py` (`GoogleCalendarClient`) |
| عميل Calendly | `integrations/calendar.py` (`CalendlyClient`) |
| سياسة الموصّل | `dealix/connectors/connector_facade.py` (`calendly` في `DEFAULT_POLICIES`) |
| موصّل Calendly ديناميكي | `dealix/connectors/connector_facade.py` (`CalendlyDynamic`) |
| أمان خطافات الويب | `platform/integrations/webhook_security.md` |

---

# English

## Calendar Connector — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The calendar connector links Dealix to Google Calendar and Calendly for scheduling meetings and tracking bookings. The fixed rule: any event that invites an external participant passes the approval gate.

### Scope

- **Google Calendar:** create events directly on a specified calendar with optional attendees.
- **Calendly:** provide a public booking link, fetch scheduled events, receive booking webhooks.
- **Not supported:** bulk event deletion, sending invites to participants without outreach consent.

### Google Calendar

`GoogleCalendarClient` in `integrations/calendar.py` implements:

- `create_event` creates an event with a summary, description, start/end time, and attendees, returning a `CalendarEventResult` with `event_id`, `html_link`, and `meeting_link`.
- Authentication is via a service-account JSON key file; the path is read from `google_calendar_credentials_file`.
- The `configured` property confirms credentials are available before any attempt.

### Calendly

`CalendlyClient` in `integrations/calendar.py` implements:

- `scheduling_link` returns the public booking link — it sends nothing, it provides a link for the customer to pick their time.
- `list_scheduled_events` fetches recent scheduled events with exponential backoff retry.
- Inbound Calendly webhooks are signature-verified before processing (see `platform/integrations/webhook_security.md`).

### Reliability and governance

- Rate limit for `calendly`: 60 calls/minute, 8-second timeout, 3 retries.
- Exponential backoff retry via `tenacity` on timeouts and HTTP errors.
- Final failure is pushed to the DLQ and does not break the workflow.
- Creating an event that invites an external participant is an action that passes `external_action_requires_approval`.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Google Calendar client | `integrations/calendar.py` (`GoogleCalendarClient`) |
| Calendly client | `integrations/calendar.py` (`CalendlyClient`) |
| Connector policy | `dealix/connectors/connector_facade.py` (`calendly` in `DEFAULT_POLICIES`) |
| Dynamic Calendly connector | `dealix/connectors/connector_facade.py` (`CalendlyDynamic`) |
| Webhook security | `platform/integrations/webhook_security.md` |
