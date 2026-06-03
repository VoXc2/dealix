/* Executive Command Center frontend orchestrator.
 *
 * 4-state UX:
 *   DEMO       → no params (default DEMO data baked in HTML)
 *   SIGNED_UP  → ?org=<handle>
 *   ACTIVE     → ?org=<handle>&access=<token> (fetches API)
 *   DEGRADED   → API responded but with degraded sections
 *
 * Endpoint: GET /api/v1/executive-command-center/{handle}
 */
(function () {
  'use strict';

  var API_BASE = (window.DEALIX_API_BASE || 'https://api.dealix.me').replace(/\/$/, '');

  function param(name) {
    var m = location.search.match(new RegExp('[?&]' + name + '=([^&#]+)'));
    return m ? decodeURIComponent(m[1]) : null;
  }

  function setState(mode, orgHandle, degradedCount) {
    var pill = document.getElementById('state-pill');
    var text = document.getElementById('state-pill-text');
    if (!pill || !text) return;

    pill.classList.remove('state-pill--demo', 'state-pill--org', 'state-pill--live', 'state-pill--degraded');

    if (mode === 'degraded') {
      pill.classList.add('state-pill--degraded');
      text.textContent = 'DEGRADED · ' + (degradedCount || 0) + ' sections';
      var banner = document.getElementById('degraded-banner');
      if (banner) banner.style.display = 'flex';
    } else if (mode === 'live') {
      pill.classList.add('state-pill--live');
      text.textContent = 'LIVE · ' + (orgHandle || '');
      hideDemoTags();
    } else if (mode === 'org') {
      pill.classList.add('state-pill--org');
      text.textContent = 'PRE-LAUNCH · ' + (orgHandle || '');
    } else {
      pill.classList.add('state-pill--demo');
      text.textContent = 'DEMO MODE';
    }
  }

  function hideDemoTags() {
    var tags = document.querySelectorAll('.demo-tag');
    tags.forEach(function (t) { t.style.display = 'none'; });
  }

  function setText(id, val) {
    var el = document.getElementById(id);
    if (el && val !== undefined && val !== null) el.textContent = String(val);
  }

  function fetchJson(path) {
    var ctrl = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, 6000);
    return fetch(API_BASE + path, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      signal: ctrl.signal,
    }).then(function (r) {
      clearTimeout(timer);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  function renderView(view, hadDegraded) {
    if (!view) return;
    setText('company-name', view.customer_handle ? prettyName(view.customer_handle) + ' — Executive Command Center' : null);

    if (view.executive_summary && view.executive_summary.headline_ar) {
      setText('executive-summary', view.executive_summary.headline_ar);
    }

    if (view.full_ops_score) {
      setText('full-ops-score', view.full_ops_score.score);
      setText('readiness-label', view.full_ops_score.readiness_label || 'Internal Only');
    }

    if (view.revenue_radar) {
      setText('revenue-num', view.revenue_radar.confirmed_payments_count || 0);
    }
    if (view.sales_pipeline) {
      setText('sales-num', view.sales_pipeline.sessions_total || 0);
    }
    if (view.support_inbox) {
      setText('support-num', view.support_inbox.open_tickets || 0);
    }
    if (view.delivery_operations) {
      setText('delivery-num', view.delivery_operations.in_delivery_count || 0);
    }
    if (view.finance_state) {
      var by_status = view.finance_state.by_status || {};
      var total = Object.values(by_status).reduce(function (a, b) { return a + b; }, 0);
      setText('finance-num', total);
    }
    if (view.proof_ledger) {
      setText('proof-num', view.proof_ledger.proof_events_count || 0);
    }
    if (view.risks_compliance) {
      setText('risk-num', view.risks_compliance.critical_count || 0);
    }
    if (view.approval_center) {
      setText('approval-num', view.approval_center.pending_count || 0);
    }

    // Replace decisions list if provided
    if (view.today_3_decisions && view.today_3_decisions.length) {
      var decList = document.getElementById('dec-list');
      if (decList) {
        decList.innerHTML = view.today_3_decisions.slice(0, 3).map(function (d) {
          return [
            '<article class="ecc-decision-card">',
              '<span class="ecc-decision-card__type">', escapeHtml(d.action_type || ''), '</span>',
              '<p class="ecc-decision-card__summary">', escapeHtml(d.summary_ar || d.summary_en || ''), '</p>',
            '</article>',
          ].join('');
        }).join('');
      }
    }

    // Degraded banner
    if (hadDegraded && view.degraded_sections && view.degraded_sections.length) {
      var list = document.getElementById('degraded-list');
      if (list) {
        list.textContent = view.degraded_sections.map(function (d) { return d.section; }).join(' · ');
      }
    }
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function prettyName(handle) {
    return handle.replace(/[-_]/g, ' ').replace(/\b\w/g, function (c) {
      return c.toUpperCase();
    });
  }

  function loadLive(orgHandle) {
    fetchJson('/api/v1/executive-command-center/' + encodeURIComponent(orgHandle))
      .then(function (data) {
        if (!data || !data.view) return;
        var view = data.view;
        var hadDegraded = view.degraded_sections && view.degraded_sections.length > 0;
        var mode = hadDegraded ? 'degraded' : 'live';
        setState(mode, orgHandle, view.degraded_sections ? view.degraded_sections.length : 0);
        renderView(view, hadDegraded);
      })
      .catch(function () { /* silent — DEMO content stays */ });
  }

  function init() {
    var org = param('org');
    var access = param('access');

    if (org && access) {
      setState('live', org);
      setText('company-name', prettyName(org) + ' — Executive Command Center');
      loadLive(org);
    } else if (org) {
      setState('org', org);
      setText('company-name', prettyName(org) + ' — Executive Command Center (Preview)');
    } else {
      setState('demo');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
