/* =============================================================
   Dealix Frontend — client-workspace.js
   Per-customer workspace page (landing/client.html).

   Reads ?customer_id=cus_xxx from URL → fetches
   /api/v1/companies/{id}/workspace → renders 9 sections.

   Failure mode: shows error banner; never breaks the page.
   ============================================================= */
(function () {
  'use strict';
  var api = window.DealixAPI;
  if (!api) return;

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function getCustomerId() {
    var params = new URLSearchParams(window.location.search);
    return params.get('customer_id') || params.get('id') || '';
  }

  function showError(msg) {
    $('dx-ws-loading').hidden = true;
    var e = $('dx-ws-error');
    e.hidden = false;
    e.textContent = msg;
  }

  function pillClass(level) {
    if (level === 'high') return 'high';
    if (level === 'medium') return 'warn';
    return 'ok';
  }

  function renderList(elId, items, mapper) {
    var el = $(elId);
    if (!items || items.length === 0) {
      el.innerHTML = '<li class="dx-ws__empty">—</li>';
      return;
    }
    el.innerHTML = items.map(mapper).join('');
  }

  function fmtDate(s) {
    if (!s) return '';
    return s.split('T')[0];
  }

  async function load() {
    var cid = getCustomerId();
    if (!cid) {
      showError('يرجى إضافة ?customer_id=cus_xxx في العنوان.');
      return;
    }

    var r = await api.get('/api/v1/companies/' + encodeURIComponent(cid) + '/workspace');
    if (!r || !r.ok) {
      showError('تعذر تحميل بيانات العميل. تأكد من معرّف العميل.');
      return;
    }
    var d = r.data;

    $('dx-ws-loading').hidden = true;
    $('dx-ws-content').hidden = false;

    // Hero
    $('dx-ws-company').textContent = (d.brain && d.brain.company_name) || cid;
    var sprint = d.current_sprint;
    if (sprint) {
      $('dx-ws-sprint').textContent =
        'السبرنت: ' + (sprint.service_id || '—') +
        ' · اليوم ' + (sprint.day || 0) + '/' + (sprint.sla_days || 7);
    } else {
      $('dx-ws-sprint').textContent = 'لم يبدأ سبرنت بعد';
    }
    $('dx-ws-asof').textContent = 'تم التحديث ' + fmtDate(d.as_of);

    // Metrics
    $('dx-ws-opps').textContent = d.opportunities_count || 0;
    $('dx-ws-drafts').textContent = d.drafts_count || 0;
    $('dx-ws-decisions').textContent = (d.open_decisions || []).length;

    // Decisions
    renderList('dx-ws-decisions-list', d.open_decisions, function (x) {
      return '<li><span>' + esc(x.label_ar || x.unit_type) + '</span>'
        + '<span class="dx-ws__pill ' + pillClass(x.risk_level) + '">' + esc(x.risk_level || 'low') + '</span></li>';
    });

    // Meetings
    renderList('dx-ws-meetings', d.meetings, function (m) {
      return '<li><span>' + esc(m.next_action_ar || m.outcome) + '</span>'
        + '<span class="dx-ws__pill">' + esc(fmtDate(m.occurred_at)) + '</span></li>';
    });

    // Invoices
    renderList('dx-ws-invoices', d.invoices, function (i) {
      var cls = i.status === 'paid' ? 'ok' : 'warn';
      return '<li><a href="' + esc(i.url || '#') + '" target="_blank">'
        + esc((i.amount_sar || 0).toFixed(0)) + ' SAR</a>'
        + '<span class="dx-ws__pill ' + cls + '">' + esc(i.status) + '</span></li>';
    });

    // Proof Packs
    renderList('dx-ws-proof', d.proof_packs, function (p) {
      return '<li><a href="' + esc(p.url) + '" target="_blank">Proof Pack</a>'
        + '<span class="dx-ws__pill">' + esc(fmtDate(p.occurred_at)) + '</span></li>';
    });

    // Risks
    renderList('dx-ws-risks', d.risks_blocked, function (rk) {
      return '<li><span>' + esc(rk.label_ar) + '</span>'
        + '<span class="dx-ws__pill ' + pillClass(rk.risk_level) + '">' + esc(rk.risk_level) + '</span></li>';
    });

    // Plan
    renderList('dx-ws-plan', d.next_7_days_plan, function (s) {
      return '<li><span>' + esc(s.label_ar) + '</span>'
        + '<span class="dx-ws__pill">' + esc(s.kind) + '</span></li>';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', load);
  } else { load(); }
}());
