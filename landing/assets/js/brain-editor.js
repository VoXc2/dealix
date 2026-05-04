/* =============================================================
   Dealix Frontend — brain-editor.js
   Reads ?customer_id=cus_xxx → fetches GET /companies/{id}/brain →
   renders form fields → PATCH on save.

   Failure modes shown inline; never silent.
   ============================================================= */
(function () {
  'use strict';
  var api = window.DealixAPI;
  if (!api) return;

  function $(id) { return document.getElementById(id); }
  function val(id) { return ($(id) && $(id).value) || ''; }
  function setVal(id, v) { if ($(id)) $(id).value = (v == null) ? '' : v; }

  function getCustomerId() {
    var p = new URLSearchParams(window.location.search);
    return p.get('customer_id') || p.get('id') || '';
  }

  function status(kind, msg) {
    var el = $('dx-status');
    if (!el) return;
    el.className = 'dx-status is-shown ' + (kind || 'ok');
    el.textContent = msg;
    if (kind === 'ok') {
      setTimeout(function () { el.classList.remove('is-shown'); }, 3500);
    }
  }

  function csv(s) {
    return String(s || '')
      .split(',')
      .map(function (x) { return x.trim(); })
      .filter(Boolean);
  }

  function renderSummary(d) {
    var ps = d.proof_summary || {};
    var html = '';
    html += '<strong>الـ Brain حالياً:</strong> ';
    html += d.company_name ? '<span class="dx-pill">' + d.company_name + '</span>' : '';
    html += d.sector ? '<span class="dx-pill">' + d.sector + '</span>' : '';
    html += d.city ? '<span class="dx-pill">' + d.city + '</span>' : '';
    html += '<br>';
    var approved = (d.approved_channels || []).map(function (c) {
      return '<span class="dx-pill dx-pill--allowed">' + c + '</span>';
    }).join('');
    var blocked = (d.blocked_channels || []).map(function (c) {
      return '<span class="dx-pill dx-pill--blocked">' + c + '</span>';
    }).join('');
    html += '<small>قنوات مسموحة:</small> ' + (approved || '—') + '<br>';
    html += '<small>قنوات محظورة:</small> ' + (blocked || '—') + '<br>';
    if (ps.events_total !== undefined) {
      html += '<small>Proof events:</small> ' + ps.events_total
        + ' · <small>أثر إيرادي:</small> ' + (ps.estimated_revenue_impact_sar || 0) + ' SAR';
    }
    var sum = $('dx-summary');
    if (sum) sum.innerHTML = html;
  }

  async function load() {
    var cid = getCustomerId();
    if (!cid) {
      status('error', 'يرجى إضافة ?customer_id=cus_xxx في العنوان.');
      return;
    }
    var sumEl = $('dx-summary');
    if (sumEl) sumEl.textContent = 'جاري التحميل…';

    var r = await api.get('/api/v1/companies/' + encodeURIComponent(cid) + '/brain');
    if (!r || !r.ok) {
      status('error', 'تعذر تحميل الـ Brain. تأكد من معرّف العميل.');
      return;
    }
    var d = r.data;

    var custId = $('dx-cust-id'); if (custId) custId.textContent = cid;
    var updated = $('dx-updated'); if (updated) updated.textContent = (d.updated_at || '').split('T')[0] || '—';

    setVal('dx-company-name', d.company_name);
    setVal('dx-website', d.website);
    setVal('dx-sector', d.sector);
    setVal('dx-city', d.city);
    setVal('dx-offer', d.offer_ar);
    setVal('dx-icp', d.ideal_customer_ar);
    setVal('dx-deal-value', d.average_deal_value_sar || 0);
    setVal('dx-tone', d.tone_ar || 'professional_saudi_arabic');
    setVal('dx-approved-channels', (d.approved_channels || []).join(', '));
    setVal('dx-blocked-channels', (d.blocked_channels || []).join(', '));
    setVal('dx-forbidden-claims', (d.forbidden_claims || []).join(', '));

    renderSummary(d);
  }

  async function save() {
    var cid = getCustomerId();
    if (!cid) { status('error', 'لا يوجد customer_id.'); return; }

    var btn = $('dx-save');
    if (btn) { btn.disabled = true; btn.textContent = 'جاري الحفظ…'; }

    var payload = {
      company_name: val('dx-company-name'),
      website: val('dx-website') || null,
      sector: val('dx-sector') || null,
      city: val('dx-city') || null,
      offer_ar: val('dx-offer') || null,
      ideal_customer_ar: val('dx-icp') || null,
      average_deal_value_sar: parseFloat(val('dx-deal-value')) || 0,
      tone_ar: val('dx-tone'),
      approved_channels: csv(val('dx-approved-channels')),
      blocked_channels: csv(val('dx-blocked-channels')),
      forbidden_claims: csv(val('dx-forbidden-claims')),
    };

    var r = await api.put
      ? await fetch(api.base + '/api/v1/companies/' + encodeURIComponent(cid) + '/brain', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'omit',
          body: JSON.stringify(payload),
        }).then(function (res) { return res.json().then(function (d) { return { ok: res.ok, status: res.status, data: d }; }); })
      : { ok: false };

    if (btn) { btn.disabled = false; btn.textContent = 'احفظ الـ Brain'; }

    if (!r.ok) {
      status('error', 'فشل الحفظ — راجع الـ console.');
      console.error('Brain save failed:', r);
      return;
    }
    status('ok', '✓ تم الحفظ — التغيير ينعكس على كل LLM output الآن.');
    renderSummary(r.data);
  }

  function bind() {
    var sb = $('dx-save'); if (sb) sb.addEventListener('click', save);
    var rb = $('dx-reload'); if (rb) rb.addEventListener('click', load);
  }

  function init() {
    bind();
    load();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
}());
