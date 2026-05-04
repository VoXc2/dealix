/* =============================================================
   Dealix Frontend — whatsapp-preview.js
   Read-only WhatsApp-style brief preview + Copy/Send.

   Markup contract:
     <div data-whatsapp-preview data-default-role="ceo"></div>

   Endpoints:
     GET  /api/v1/whatsapp/brief?role=X        → {role, text, lines, decision_count}
     POST /api/v1/whatsapp/brief/send-internal → 403/501 today (gate False)

   Failure mode: if the backend is unreachable or returns no text, we show
   a static placeholder so the page never breaks.
   ============================================================= */
(function () {
  'use strict';

  var api = window.DealixAPI;
  if (!api) return;

  var ROLES = [
    { id: 'ceo',                  label: 'CEO' },
    { id: 'sales_manager',        label: 'Sales' },
    { id: 'growth_manager',       label: 'Growth' },
    { id: 'revops',               label: 'RevOps' },
    { id: 'customer_success',     label: 'CS' },
    { id: 'finance',              label: 'Finance' },
    { id: 'compliance',           label: 'Compliance' },
    { id: 'meeting_intelligence', label: 'Meetings' },
  ];

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function bubbleStyles() {
    return ''
      + '.dx-wa-shell { display:flex; flex-direction:column; gap:.75rem; }'
      + '.dx-wa-tabs { display:flex; gap:.4rem; flex-wrap:wrap; }'
      + '.dx-wa-tabs button { background:#f1f5f9; border:1px solid #e2e8f0; padding:.4rem .8rem;'
      + '  border-radius:999px; font-family:inherit; cursor:pointer; font-size:.85rem; }'
      + '.dx-wa-tabs button[aria-current="true"] { background:#10b981; color:white; border-color:#059669; }'
      + '.dx-wa-bubble { background:#dcfce7; border-radius:14px 14px 14px 4px; padding:1rem 1.1rem;'
      + '  white-space:pre-wrap; line-height:1.7; max-width:520px; box-shadow:0 1px 2px rgba(0,0,0,.05);'
      + '  font-family:-apple-system, "IBM Plex Sans Arabic", sans-serif; font-size:.95rem; }'
      + '.dx-wa-bubble.is-empty { background:#fef3c7; color:#78350f; }'
      + '.dx-wa-meta { font-size:.8rem; color:#64748b; }'
      + '.dx-wa-actions { display:flex; gap:.5rem; flex-wrap:wrap; }'
      + '.dx-wa-actions button { background:#fff; border:1px solid #cbd5e1; padding:.5rem 1rem;'
      + '  border-radius:8px; font-family:inherit; cursor:pointer; }'
      + '.dx-wa-actions button.dx-wa-primary { background:#10b981; color:white; border-color:#059669; }'
      + '.dx-wa-status { font-size:.85rem; padding:.5rem .75rem; border-radius:6px; display:none; }'
      + '.dx-wa-status.is-shown { display:block; }'
      + '.dx-wa-status.ok { background:#dcfce7; color:#065f46; }'
      + '.dx-wa-status.warn { background:#fef3c7; color:#78350f; }';
  }

  function renderShell(host, currentRole) {
    var styleId = 'dx-wa-styles';
    if (!document.getElementById(styleId)) {
      var s = document.createElement('style');
      s.id = styleId;
      s.textContent = bubbleStyles();
      document.head.appendChild(s);
    }
    host.innerHTML = ''
      + '<div class="dx-wa-shell">'
      +   '<div class="dx-wa-tabs">'
      +     ROLES.map(function (r) {
            var active = r.id === currentRole;
            return '<button data-role="' + r.id + '"'
              + ' aria-current="' + (active ? 'true' : 'false') + '">'
              + escapeHtml(r.label) + '</button>';
          }).join('')
      +   '</div>'
      +   '<div class="dx-wa-meta" data-meta>—</div>'
      +   '<div class="dx-wa-bubble" data-bubble>جاري التحميل…</div>'
      +   '<div class="dx-wa-actions">'
      +     '<button data-act="copy">نسخ النص</button>'
      +     '<button data-act="send" class="dx-wa-primary">إرسال داخلي (Internal)</button>'
      +     '<button data-act="refresh">تحديث</button>'
      +   '</div>'
      +   '<div class="dx-wa-status" data-status></div>'
      + '</div>';
  }

  function setStatus(host, msg, kind) {
    var el = host.querySelector('[data-status]');
    if (!el) return;
    if (!msg) {
      el.classList.remove('is-shown', 'ok', 'warn');
      el.textContent = '';
      return;
    }
    el.classList.remove('ok', 'warn');
    el.classList.add('is-shown', kind || 'ok');
    el.textContent = msg;
  }

  async function loadBrief(host, role) {
    var bubble = host.querySelector('[data-bubble]');
    var meta = host.querySelector('[data-meta]');
    if (bubble) bubble.classList.remove('is-empty');
    if (bubble) bubble.textContent = 'جاري التحميل…';
    if (meta) meta.textContent = '—';

    var r = await api.get('/api/v1/whatsapp/brief?role=' + encodeURIComponent(role));
    var text = (r && r.ok && r.data && r.data.text) || '';
    var dec = (r && r.ok && r.data && r.data.decision_count) || 0;
    var lines = (r && r.ok && r.data && r.data.lines) || 0;
    if (!text) {
      bubble.classList.add('is-empty');
      bubble.textContent = 'لا توجد بيانات لهذا الدور بعد — الـ ledger فارغ أو الـ backend غير مُفعَّل.';
      meta.textContent = 'role: ' + role;
      return;
    }
    bubble.textContent = text;
    meta.textContent = 'role: ' + role + ' · decisions: ' + dec + ' · lines: ' + lines;
  }

  async function copyText(host) {
    var bubble = host.querySelector('[data-bubble]');
    if (!bubble) return;
    var text = bubble.textContent || '';
    try {
      await navigator.clipboard.writeText(text);
      setStatus(host, 'تم النسخ — الصق في WhatsApp Web يدوياً.', 'ok');
    } catch (_) {
      setStatus(host, 'لم نتمكن من النسخ تلقائياً — اختر النص يدوياً.', 'warn');
    }
  }

  async function sendInternal(host) {
    var btns = host.querySelectorAll('[data-role][aria-current="true"]');
    var role = btns[0] ? btns[0].getAttribute('data-role') : 'ceo';
    setStatus(host, 'جاري الإرسال…', 'ok');
    var r = await api.post('/api/v1/whatsapp/brief/send-internal', { role: role });
    if (r && r.ok) {
      setStatus(host, 'تم الطلب (سيُسجَّل في audit log).', 'ok');
    } else if (r && r.status === 403) {
      setStatus(host, 'الإرسال مُعطَّل — gate=false (افتراضي آمن). استخدم نسخ بدلاً.', 'warn');
    } else if (r && r.status === 501) {
      setStatus(host, 'transport غير مكوَّن بعد. استخدم نسخ بدلاً.', 'warn');
    } else {
      setStatus(host, 'تعذَّر الإرسال — الإعداد ناقص. استخدم نسخ.', 'warn');
    }
  }

  function bind(host) {
    host.addEventListener('click', function (ev) {
      var roleBtn = ev.target.closest('[data-role]');
      if (roleBtn) {
        var current = host.querySelectorAll('[data-role]');
        Array.prototype.forEach.call(current, function (b) {
          b.setAttribute('aria-current', b === roleBtn ? 'true' : 'false');
        });
        loadBrief(host, roleBtn.getAttribute('data-role'));
        return;
      }
      var actBtn = ev.target.closest('[data-act]');
      if (!actBtn) return;
      var act = actBtn.getAttribute('data-act');
      if (act === 'copy') copyText(host);
      else if (act === 'send') sendInternal(host);
      else if (act === 'refresh') {
        var cur = host.querySelector('[data-role][aria-current="true"]');
        loadBrief(host, cur ? cur.getAttribute('data-role') : 'ceo');
      }
    });
  }

  function init() {
    var hosts = document.querySelectorAll('[data-whatsapp-preview]');
    Array.prototype.forEach.call(hosts, function (host) {
      var def = host.getAttribute('data-default-role') || 'ceo';
      renderShell(host, def);
      bind(host);
      loadBrief(host, def);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
