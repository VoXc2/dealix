/* =============================================================
   Dealix Frontend — cards.js
   Renders role-based decision cards from /api/v1/cards/feed.
   ≤3 buttons enforced visually + by API contract.

   Markup contract (in command-center.html):
     <div data-cards-feed
          data-default-role="ceo">     <!-- empty container -->
     <div data-role-switcher></div>    <!-- empty switcher -->
   ============================================================= */
(function () {
  'use strict';

  const ROLES = [
    { id: 'ceo',      label: 'المدير التنفيذي' },
    { id: 'sales',    label: 'المبيعات' },
    { id: 'growth',   label: 'النمو' },
    { id: 'service',  label: 'تشغيل الخدمة' },
    { id: 'support',  label: 'الدعم' },
    { id: 'agency',   label: 'الوكالة الشريكة' },
  ];

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function riskIcon(level) {
    return level === 'high' ? '⚠' : (level === 'medium' ? '🟡' : '🟢');
  }

  function buildCardHTML(c) {
    const buttons = (c.buttons || []).slice(0, 3).map(function (b) {
      const action = escapeHtml(b.action || 'details');
      return '<button data-action="' + action + '"'
        + ' data-card-id="' + escapeHtml(c.id) + '"'
        + ' data-track="card_' + (b.action === 'approve' || b.primary ? 'approved' : 'edited') + '"'
        + ' data-track-card-type="' + escapeHtml(c.type) + '">'
        + escapeHtml(b.label_ar)
        + '</button>';
    }).join('');

    const proofBadges = (c.proof_impact || []).map(function (p) {
      return '<span class="dx-badge dx-proof-badge">' + escapeHtml(p) + '</span>';
    }).join('');

    const riskNote = c.risk_note_ar
      ? '<div class="dx-card__risk-note">' + escapeHtml(c.risk_note_ar) + '</div>'
      : '';

    return '<article class="dx-card" data-type="' + escapeHtml(c.type) + '"'
      + ' data-risk="' + escapeHtml(c.risk || 'low') + '">'
      + '<header class="dx-card__head">'
      + '<span class="dx-card__icon">' + riskIcon(c.risk) + '</span>'
      + '<span class="dx-card__type">' + escapeHtml(c.type.replace(/_/g, ' ')) + '</span>'
      + '<span class="dx-risk-badge dx-risk-badge--' + escapeHtml(c.risk || 'low') + '">'
      + escapeHtml(c.risk || 'low') + '</span>'
      + '</header>'
      + '<h3 class="dx-card__title">' + escapeHtml(c.title_ar) + '</h3>'
      + '<div class="dx-card__why"><strong>لماذا الآن:</strong> ' + escapeHtml(c.why_now_ar) + '</div>'
      + '<div class="dx-card__action"><strong>الإجراء المقترح:</strong> ' + escapeHtml(c.recommended_action_ar) + '</div>'
      + riskNote
      + '<footer class="dx-card__proof">' + proofBadges + '</footer>'
      + '<nav class="dx-card__buttons">' + buttons + '</nav>'
      + '</article>';
  }

  function renderEmpty(container) {
    container.innerHTML = ''
      + '<div class="dx-cards-empty">'
      + '<div class="dx-cards-empty__icon">📭</div>'
      + '<p class="dx-cards-empty__title">لا توجد كروت لهذا الدور حالياً</p>'
      + '<p>سيتحدّث الـ feed تلقائياً عند توفر إشارات جديدة.</p>'
      + '</div>';
  }

  function renderSwitcher(switcher, currentRole, onSelect) {
    switcher.innerHTML = ROLES.map(function (r) {
      const active = r.id === currentRole;
      return '<button class="dx-role-switcher__btn"'
        + ' data-role="' + r.id + '"'
        + ' aria-selected="' + (active ? 'true' : 'false') + '"'
        + (active ? ' aria-current="true"' : '')
        + '>' + escapeHtml(r.label) + '</button>';
    }).join('');
    switcher.classList.add('dx-role-switcher');
    switcher.addEventListener('click', function (ev) {
      const btn = ev.target.closest('[data-role]');
      if (!btn) return;
      onSelect(btn.getAttribute('data-role'));
    }, false);
  }

  async function loadFeed(container, role) {
    container.innerHTML = ''
      + '<div class="dx-card-skeleton"></div>'
      + '<div class="dx-card-skeleton"></div>'
      + '<div class="dx-card-skeleton"></div>';
    if (!window.DealixAPI) {
      renderEmpty(container);
      return;
    }
    const r = await window.DealixAPI.get('/api/v1/cards/feed?role=' + encodeURIComponent(role));
    if (!r.ok || !r.data) {
      renderEmpty(container);
      return;
    }
    const data = r.data;
    const html = (data.cards || []).map(buildCardHTML).join('\n');
    let banner = '';
    if (data.is_demo) {
      banner = '<div class="dx-demo-banner" role="status">'
        + escapeHtml(data.demo_label_ar || 'بيانات تجريبية')
        + ' — البيانات الحقيقية تظهر بعد ربط الإشارات.</div>';
    }
    container.innerHTML = banner + (html || '');
    if (!data.cards || data.cards.length === 0) {
      renderEmpty(container);
    }
    if (window.DealixAnalytics) {
      window.DealixAnalytics.track('card_viewed', { role: role, count: (data.cards || []).length, is_demo: !!data.is_demo });
    }
  }

  function bindCardActions() {
    document.addEventListener('click', async function (ev) {
      const btn = ev.target.closest('.dx-card__buttons button[data-card-id]');
      if (!btn) return;
      const cardId = btn.getAttribute('data-card-id');
      const action = btn.getAttribute('data-action');
      if (!cardId || !action) return;
      btn.disabled = true;
      btn.textContent = '…';
      try {
        if (window.DealixAPI && action !== 'details') {
          await window.DealixAPI.post('/api/v1/cards/' + encodeURIComponent(cardId) + '/decision', { action: action });
        }
      } finally {
        btn.disabled = false;
        if (action === 'approve') {
          btn.textContent = '✓ تم';
        } else {
          btn.textContent = action;
        }
      }
    });
  }

  function init() {
    const container = document.querySelector('[data-cards-feed]');
    const switcher = document.querySelector('[data-role-switcher]');
    if (!container) return;
    let currentRole = container.getAttribute('data-default-role') || 'ceo';
    if (switcher) {
      renderSwitcher(switcher, currentRole, function (newRole) {
        currentRole = newRole;
        // re-render switcher to update aria-selected
        renderSwitcher(switcher, currentRole, arguments.callee);
        loadFeed(container, currentRole);
      });
    }
    loadFeed(container, currentRole);
    bindCardActions();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose for tests
  window.DealixCards = { ROLES: ROLES, loadFeed: loadFeed, buildCardHTML: buildCardHTML };
}());
