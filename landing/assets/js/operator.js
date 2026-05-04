/* =============================================================
   Dealix Frontend — operator.js
   Wires landing/operator.html to /api/v1/operator/chat/message.

   The page already has a quick-reply intent grid; this script:
     - On quick-reply click: POSTs the intent_hint to the API and
       renders the recommended bundle + safety note.
     - Falls back to the static intent map (already in operator.html
       inline script) if the API is unreachable.

   This script does NOT replace the existing inline behavior — it
   listens for the same data-intent buttons but takes precedence by
   calling the API first; the inline fallback only triggers when API
   fails.
   ============================================================= */
(function () {
  'use strict';

  function $(sel) { return document.querySelector(sel); }
  function api() { return window.DealixAPI || null; }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function appendBubble(text, who) {
    const body = $('#dx-chat-body');
    if (!body) return;
    const div = document.createElement('div');
    div.className = 'dx-chat__msg dx-chat__msg--' + (who === 'user' ? 'user' : 'bot');
    div.innerHTML = text;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }

  function renderRecommendation(payload) {
    const reason = escapeHtml(payload.reason_ar || '');
    let html = reason;
    const b = payload.recommended_bundle;
    if (b) {
      html += '<br><br><strong>' + escapeHtml(b.name_ar) + '</strong> · ' + escapeHtml(b.price_label) + '<br>';
      const items = (b.deliverables_ar || []).slice(0, 4)
        .map(function (d) { return '✓ ' + escapeHtml(d); })
        .join('<br>');
      html += items;
      if (b.cta_path) {
        html += '<br><a href="' + escapeHtml(b.cta_path)
          + '" style="color:#fff; text-decoration:underline; font-weight:600;">'
          + 'اعرض التفاصيل ←</a>';
      }
    }
    if (payload.blocked) {
      html += '<br><br><span style="color:#fff; font-weight:600;">⚠ هذا الطلب لا يمكن خدمته بأمان.</span>';
    }
    appendBubble(html, 'bot');
  }

  // Block the inline handler by stopping propagation BEFORE it fires.
  // We use { capture: true } so we run first.
  function bindIntents() {
    const quick = $('#dx-chat-quick');
    if (!quick) return;
    quick.addEventListener('click', async function (ev) {
      const btn = ev.target.closest('[data-intent]');
      if (!btn) return;
      const a = api();
      if (!a) return; // let inline fallback run
      // Take over from the inline handler
      ev.stopImmediatePropagation();
      ev.preventDefault();
      const intent = btn.getAttribute('data-intent');
      appendBubble(escapeHtml(btn.textContent.trim()), 'user');
      const r = await a.post('/api/v1/operator/chat/message', {
        intent_hint: intent,
        text: btn.textContent.trim(),
      });
      if (!r.ok || !r.data) {
        appendBubble('تعذّر التواصل مع Operator الآن — راجع <a href="services.html" style="color:#fff;">الباقات</a>.', 'bot');
        return;
      }
      renderRecommendation(r.data);
      if (window.DealixAnalytics) {
        const evt = r.data.blocked
          ? 'operator_blocked_unsafe'
          : 'operator_service_recommended';
        window.DealixAnalytics.track(evt, {
          intent: r.data.intent,
          bundle_id: r.data.recommended_bundle && r.data.recommended_bundle.id,
        });
      }
    }, { capture: true });
  }

  function init() {
    bindIntents();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
