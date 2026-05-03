/* =============================================================
   Dealix Frontend — role-briefs.js
   Renders the daily role brief (CEO / Sales / Growth / RevOps / CS /
   Agency / Finance / Compliance) into a target container.

   Markup contract:
     <div data-role-brief data-default-role="sales_manager"></div>
   ============================================================= */
(function () {
  'use strict';

  const ROLES = [
    { id: 'ceo',              label: 'المدير التنفيذي' },
    { id: 'sales_manager',    label: 'مدير المبيعات' },
    { id: 'growth_manager',   label: 'مدير النمو' },
    { id: 'revops',           label: 'RevOps' },
    { id: 'customer_success', label: 'Customer Success' },
    { id: 'finance',          label: 'المالية' },
    { id: 'compliance',       label: 'الامتثال' },
  ];

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function renderSwitcher(container, current, onSelect) {
    container.innerHTML = ''
      + '<div class="dx-role-switcher" style="margin-bottom:1rem; flex-wrap:wrap;">'
      + ROLES.map(function (r) {
          const active = r.id === current;
          return '<button class="dx-role-switcher__btn"'
            + ' data-role="' + r.id + '"'
            + ' aria-selected="' + (active ? 'true' : 'false') + '"'
            + (active ? ' aria-current="true"' : '')
            + '>' + escapeHtml(r.label) + '</button>';
        }).join('')
      + '</div>'
      + '<div data-role-brief-body></div>';
    container.querySelector('.dx-role-switcher').addEventListener('click', function (ev) {
      const btn = ev.target.closest('[data-role]');
      if (!btn) return;
      onSelect(btn.getAttribute('data-role'));
    });
  }

  function decisionCard(d) {
    const buttons = (d.buttons_ar || []).slice(0, 3).map(function (b) {
      return '<button>' + escapeHtml(b) + '</button>';
    }).join('');
    const proof = (d.proof_impact || []).map(function (p) {
      return '<span class="dx-badge dx-proof-badge">' + escapeHtml(p) + '</span>';
    }).join('');
    const risk = d.risk_level || 'low';
    return '<article class="dx-card" data-type="' + escapeHtml(d.type || 'opportunity')
      + '" data-risk="' + escapeHtml(risk) + '">'
      + '<header class="dx-card__head">'
      + '<span class="dx-card__icon">' + (risk === 'high' ? '⚠' : risk === 'medium' ? '🟡' : '🟢') + '</span>'
      + '<span class="dx-card__type">' + escapeHtml(d.type || '—') + '</span>'
      + '<span class="dx-risk-badge dx-risk-badge--' + escapeHtml(risk) + '">' + escapeHtml(risk) + '</span>'
      + '</header>'
      + '<h3 class="dx-card__title">' + escapeHtml(d.title_ar || '') + '</h3>'
      + '<div class="dx-card__why"><strong>لماذا الآن:</strong> ' + escapeHtml(d.why_now_ar || '') + '</div>'
      + '<div class="dx-card__action"><strong>الإجراء:</strong> ' + escapeHtml(d.recommended_action_ar || '') + '</div>'
      + '<footer class="dx-card__proof">' + proof + '</footer>'
      + '<nav class="dx-card__buttons">' + buttons + '</nav>'
      + '</article>';
  }

  function renderBody(body, brief) {
    const summary = brief.summary || {};
    const decisions = brief.top_decisions || [];
    const blocked = brief.blocked_today_ar || [];

    const summaryHtml = Object.keys(summary).length
      ? '<div class="dx-cards-grid" style="grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:0.5rem; margin-bottom:1rem;">'
        + Object.entries(summary).map(function (kv) {
          return '<div style="background:var(--bg-muted, #f8fafc); padding:0.5rem 0.75rem; border-radius:6px;">'
            + '<strong style="display:block; font-size:1.125rem;">' + escapeHtml(kv[1]) + '</strong>'
            + '<span style="font-size:0.6875rem; color:var(--text-muted, #475569);">' + escapeHtml(kv[0].replace(/_/g, ' ')) + '</span>'
            + '</div>';
        }).join('')
        + '</div>'
      : '';

    const decisionsHtml = decisions.length
      ? '<div class="dx-cards-grid">' + decisions.map(decisionCard).join('') + '</div>'
      : '<div class="dx-cards-empty"><p>لا توجد قرارات أولوية الآن — راجع لاحقاً.</p></div>';

    const blockedHtml = blocked.length
      ? '<aside style="margin-top:1rem; padding:0.75rem; background:color-mix(in srgb, var(--dx-amber, #D97706) 8%, transparent); border-radius:8px; border-inline-start:3px solid var(--dx-amber, #D97706);">'
        + '<strong style="display:block; margin-bottom:0.25rem;">ممنوع اليوم:</strong>'
        + '<ul style="margin:0; padding-inline-start:1.25rem; font-size:0.875rem;">'
        + blocked.map(function (b) { return '<li>' + escapeHtml(b) + '</li>'; }).join('')
        + '</ul></aside>'
      : '';

    body.innerHTML = summaryHtml + decisionsHtml + blockedHtml;
  }

  async function loadFor(role, body) {
    body.innerHTML = '<div class="dx-card-skeleton"></div><div class="dx-card-skeleton"></div>';
    if (!window.DealixAPI) {
      body.innerHTML = '<div class="dx-cards-empty"><p>API client not loaded.</p></div>';
      return;
    }
    const r = await window.DealixAPI.get('/api/v1/role-briefs/daily?role=' + encodeURIComponent(role));
    if (!r.ok || !r.data) {
      body.innerHTML = '<div class="dx-cards-empty"><p>الـ Brief غير متاح حالياً — جرّب لاحقاً.</p></div>';
      return;
    }
    renderBody(body, r.data);
    if (window.DealixAnalytics) {
      window.DealixAnalytics.track('card_viewed', {
        role: role,
        decision_count: (r.data.top_decisions || []).length,
        source: 'role_brief',
      });
    }
  }

  function init() {
    const container = document.querySelector('[data-role-brief]');
    if (!container) return;
    let current = container.getAttribute('data-default-role') || 'sales_manager';
    renderSwitcher(container, current, function (r) {
      current = r;
      renderSwitcher(container, current, arguments.callee);
      const body = container.querySelector('[data-role-brief-body]');
      loadFor(current, body);
    });
    const body = container.querySelector('[data-role-brief-body]');
    loadFor(current, body);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
