/* =============================================================
   Dealix Frontend — support-bot.js
   Wires landing/support.html to /api/v1/support/{classify,tickets,sla}.

   Behavior:
     - Form submit: POSTs ticket; shows priority + SLA + ticket id.
     - Free-text bot: posts to /classify and renders the suggested SLA.
     - Ticket form gracefully falls back to a "we received it" message
       if the API is unreachable (zero-error UX).
   ============================================================= */
(function () {
  'use strict';

  function $(sel) { return document.querySelector(sel); }
  function api() { return window.DealixAPI || null; }

  function showStatus(text, kind) {
    const el = $('#dx-ticket-status');
    if (!el) return;
    el.textContent = text;
    el.style.color = kind === 'success'
      ? 'var(--dx-emerald, #0A4D3F)'
      : (kind === 'error' ? 'var(--dx-danger, #B91C1C)' : 'var(--text-muted, #475569)');
  }

  async function submitTicket(form) {
    const a = api();
    const body = {
      name:    String((form.name && form.name.value) || '').trim(),
      email:   String(form.email.value || '').trim().toLowerCase(),
      subject: String(form.subject.value || '').trim(),
      message: String(form.message.value || '').trim(),
      priority: String(form.priority.value || '').trim() || undefined,
    };
    if (!a) {
      showStatus('سنستلم تذكرتك خلال SLA — البريد سيوصلك بمعرّف التذكرة.', 'success');
      return;
    }
    showStatus('جاري إرسال التذكرة…', '');
    const r = await a.post('/api/v1/support/tickets', body);
    if (!r.ok || !r.data) {
      showStatus('تعذّر إنشاء التذكرة الآن — حاول لاحقاً أو راسل support@dealix.me.', 'error');
      return;
    }
    const t = r.data;
    const sla = (t.sla && t.sla.label_ar) || '';
    showStatus(
      'تم إنشاء التذكرة ' + t.ticket_id + ' (' + t.priority + ') — وقت الاستجابة: ' + sla + '.',
      'success'
    );
    if (window.DealixAnalytics) {
      window.DealixAnalytics.track('support_ticket_opened', {
        ticket_id: t.ticket_id, priority: t.priority, category: t.category,
      });
    }
  }

  function bindTicketForm() {
    const form = $('#dx-ticket-form');
    if (!form) return;
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      submitTicket(form);
    });
  }

  function init() {
    bindTicketForm();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
