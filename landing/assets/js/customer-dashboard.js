/* Dealix — Customer Operations Console orchestrator.
 *
 * 3-state rendering driven by URL params:
 *   State A — no params           → public DEMO (hardcoded realistic data)
 *   State B — ?org=<handle>       → SIGNED-UP (DEMO + company-name overlay)
 *   State C — ?org=...&access=... → LIVE (fetch APIs, DEMO fallback on error)
 *
 * The page is fully rendered on load with realistic DEMO data — JS only
 * mutates the state pill, the company name, and (in State C) tries to
 * upgrade individual sections with live data. Failures are silent and
 * keep DEMO content visible (anti-vapor: never show a broken section).
 */
(function () {
  'use strict';

  var API_BASE = (window.DEALIX_API_BASE || 'https://api.dealix.me').replace(/\/$/, '');

  function param(name) {
    var m = location.search.match(new RegExp('[?&]' + name + '=([^&#]+)'));
    return m ? decodeURIComponent(m[1]) : null;
  }

  function setState(mode, orgHandle) {
    var pill = document.getElementById('state-pill');
    var text = document.getElementById('state-pill-text');
    if (!pill || !text) return;

    pill.classList.remove('state-pill--demo', 'state-pill--org', 'state-pill--live');

    if (mode === 'live') {
      pill.classList.add('state-pill--live');
      text.textContent = 'LIVE · ' + (orgHandle || '');
      markSrc('LIVE', 'src-pill--live');
    } else if (mode === 'org') {
      pill.classList.add('state-pill--org');
      text.textContent = 'PRE-LAUNCH · ' + (orgHandle || '');
    } else {
      pill.classList.add('state-pill--demo');
      text.textContent = 'DEMO MODE';
    }
  }

  function markSrc(label, cls) {
    var srcs = document.querySelectorAll('.src-pill');
    srcs.forEach(function (el) {
      el.textContent = label;
      el.classList.add(cls);
    });
  }

  function setCompanyName(name) {
    var el = document.getElementById('company-name');
    if (el && name) el.textContent = name;
  }

  function fetchJson(path, opts) {
    opts = opts || {};
    var ctrl = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, 6000);
    return fetch(API_BASE + path, {
      method: opts.method || 'GET',
      headers: opts.headers || { 'Accept': 'application/json' },
      body: opts.body ? JSON.stringify(opts.body) : undefined,
      signal: ctrl.signal,
    }).then(function (r) {
      clearTimeout(timer);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  function renderOpsCards(stats) {
    var grid = document.getElementById('ops-grid');
    if (!grid || !stats) return;
    var cards = [
      { num: stats.leads_today, label: 'leads اليوم', sub: stats.leads_today_sub },
      { num: stats.qualified, label: 'مؤهّلة (Qualified)', sub: stats.qualified_sub },
      { num: stats.in_pipeline, label: 'في Pipeline نشط', sub: stats.pipeline_sub },
      { num: stats.drafts_pending, label: 'drafts بانتظار موافقتك', sub: 'على /decisions.html' },
      { num: stats.proof_events_week, label: 'proof events هذا الأسبوع', sub: 'claim×evidence pairs' },
      { num: stats.nps, label: 'NPS · آخر استبيان', sub: stats.nps_sub },
    ];
    grid.innerHTML = cards.map(function (c) {
      return '<div class="ops-card"><div class="ops-card__num">' + (c.num != null ? c.num : '—') +
             '</div><div class="ops-card__label">' + c.label +
             '</div><div class="ops-card__sub">' + (c.sub || '') + '</div></div>';
    }).join('');
  }

  function renderSequenceTimeline(state, history) {
    var container = document.getElementById('seq-timeline');
    if (!container) return;
    var current = document.getElementById('current-state');
    if (current && state) current.textContent = state;

    var STATES = [
      'lead_intake', 'diagnostic_requested', 'diagnostic_sent',
      'pilot_offered', 'payment_pending', 'paid_or_committed',
      'in_delivery', 'proof_pack_ready', 'proof_pack_sent',
      'upsell_recommended', 'nurture', 'blocked',
    ];
    var done = new Set(history || []);
    container.innerHTML = STATES.map(function (s, i) {
      var cls = '';
      var icon = String(i + 1);
      if (done.has(s)) { cls = 'seq-step--done'; icon = '✓'; }
      else if (s === state) { cls = 'seq-step--active'; icon = '●'; }
      else if (s === 'blocked') { icon = '—'; }
      return '<div class="seq-step ' + cls + '">' +
               '<div class="seq-step__icon">' + icon + '</div>' +
               '<div class="seq-step__label">' + s + '</div>' +
             '</div>';
    }).join('');
  }

  function renderRadar(opportunities) {
    var grid = document.getElementById('radar-grid');
    if (!grid || !Array.isArray(opportunities) || opportunities.length === 0) return;
    grid.innerHTML = opportunities.slice(0, 6).map(function (o) {
      var signal = (o.primary_signal || o.signal_type || 'OPPORTUNITY').toUpperCase();
      var score = Math.round(o.priority_score != null ? o.priority_score : (o.score || 0));
      var title = o.headline || o.company_name || 'فرصة جديدة';
      var why = o.why_now_ar || o.why_now || 'سياق التوقيت قيد المعالجة.';
      var action = o.suggested_angle_ar || o.action_ar || ('قناة مقترحة: ' + (o.suggested_channel || 'whatsapp'));
      var city = o.city || '';
      var src = o.source || (o.evidence_url ? new URL(o.evidence_url).hostname : '—');
      return [
        '<article class="radar-card">',
          '<div class="radar-card__head">',
            '<span class="radar-card__signal">', signal, '</span>',
            '<div class="radar-card__score">', score, '<small>/100</small></div>',
          '</div>',
          '<h3 class="radar-card__title">', escapeHtml(title), '</h3>',
          '<p class="radar-card__why">', escapeHtml(why), '</p>',
          '<p class="radar-card__action">', escapeHtml(action), '</p>',
          '<div class="radar-card__meta">',
            city ? '<span class="radar-card__meta-item">📍 ' + escapeHtml(city) + '</span>' : '',
            '<span class="radar-card__meta-item">🔗 ' + escapeHtml(String(src)) + '</span>',
          '</div>',
        '</article>',
      ].join('');
    }).join('');
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function loadLive(orgHandle) {
    fetchJson('/api/v1/customer-portal/' + encodeURIComponent(orgHandle))
      .then(function (data) {
        if (!data) return;
        var enriched = data.enriched_view || {};
        if (enriched.ops_summary) renderOpsCards(enriched.ops_summary);
        if (enriched.sequences) {
          renderSequenceTimeline(enriched.sequences.current_state, enriched.sequences.history);
        }
        if (enriched.radar_today && enriched.radar_today.opportunities && enriched.radar_today.opportunities.length) {
          renderRadar(enriched.radar_today.opportunities);
        }
        if (data.company_name) setCompanyName(data.company_name);
        // Phase 3 Wave 5: degraded banner — show when active customer
        // mode but key sections fall back to insufficient_data
        maybeShowDegradedBanner(enriched);
      })
      .catch(function () { /* silent — DEMO content stays visible */ });
  }

  function maybeShowDegradedBanner(enriched) {
    var degradedSections = [];
    if (enriched.full_ops_score && enriched.full_ops_score.source === 'insufficient_data') {
      degradedSections.push('Full-Ops Score');
    }
    if (enriched.proof_summary && enriched.proof_summary.source === 'insufficient_data') {
      degradedSections.push('Proof Summary');
    }
    if (enriched.payment_state && enriched.payment_state.source === 'insufficient_data') {
      degradedSections.push('Payment State');
    }
    if (enriched.support_summary && enriched.support_summary.source === 'insufficient_data') {
      degradedSections.push('Support Summary');
    }
    if (degradedSections.length === 0) return;
    var banner = document.getElementById('cp-degraded-banner');
    var list = document.getElementById('cp-degraded-list');
    if (!banner) return;
    banner.classList.add('show');
    if (list) {
      list.textContent = degradedSections.length + ' قسم/أقسام تظهر بيانات تجريبيّة: ' + degradedSections.join(' · ');
    }
  }

  function init() {
    var org = param('org');
    var access = param('access');

    if (org && access) {
      setState('live', org);
      setCompanyName(prettyName(org));
      loadLive(org);
    } else if (org) {
      setState('org', org);
      setCompanyName(prettyName(org));
    } else {
      setState('demo');
    }
  }

  function prettyName(handle) {
    return handle
      .replace(/[-_]/g, ' ')
      .replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
