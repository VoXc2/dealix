(function () {
  'use strict';

  var CARDS = [
    { key: 'services',          ar: 'الخدمات',                en: 'Services' },
    { key: 'reliability',       ar: 'الموثوقية',              en: 'Reliability' },
    { key: 'live_gates',        ar: 'البوابات الحيّة',         en: 'Live Gates' },
    { key: 'daily_loop',        ar: 'الحلقة اليومية',          en: 'Daily Loop' },
    { key: 'weekly_scorecard',  ar: 'البطاقة الأسبوعية',       en: 'Weekly Scorecard' },
    { key: 'ceo_brief',         ar: 'موجز الرئيس التنفيذي',     en: 'CEO Brief' }
  ];

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  // Live gates flag anything not exactly "BLOCKED" and not starting with "BLOCKED " as alert.
  function isGateAlert(value) {
    if (value === null || value === undefined) return false;
    var s = String(value).trim();
    if (s === 'BLOCKED') return false;
    if (s.indexOf('BLOCKED ') === 0) return false;
    return true;
  }

  function renderValue(key, k, v) {
    if (v === null || v === undefined) return '<span class="empty">—</span>';
    if (typeof v === 'object') {
      try { return '<code>' + escapeHtml(JSON.stringify(v)) + '</code>'; }
      catch (e) { return '<span class="empty">—</span>'; }
    }
    var classes = '';
    if (key === 'live_gates' && isGateAlert(v)) classes = ' alert';
    return '<span class="v' + classes + '">' + escapeHtml(v) + '</span>';
  }

  function renderCardBody(key, payload) {
    if (payload === null || payload === undefined) {
      return '<div class="empty">لا توجد بيانات / no data</div>';
    }
    if (typeof payload !== 'object' || Array.isArray(payload)) {
      var v = Array.isArray(payload) ? payload.join(', ') : payload;
      return '<div class="kv"><span class="k">value</span>' + renderValue(key, 'value', v) + '</div>';
    }
    var keys = Object.keys(payload);
    if (keys.length === 0) return '<div class="empty">لا توجد بيانات / no data</div>';
    var rows = keys.map(function (k) {
      return '<div class="kv"><span class="k">' + escapeHtml(k) + '</span>' + renderValue(key, k, payload[k]) + '</div>';
    });
    return rows.join('');
  }

  function render(root, data) {
    var html = '<div class="grid">';
    CARDS.forEach(function (card) {
      html += '<div class="card" data-card="' + card.key + '">';
      html += '<h2>' + escapeHtml(card.ar) + ' <span class="en">' + escapeHtml(card.en) + '</span></h2>';
      html += renderCardBody(card.key, data ? data[card.key] : null);
      html += '</div>';
    });
    html += '</div>';
    root.innerHTML = html;
  }

  function setStatus(state, text) {
    var el = document.getElementById('status');
    if (!el) return;
    el.className = 'status ' + state;
    el.textContent = text;
  }

  function setUpdated() {
    var el = document.getElementById('updated');
    if (!el) return;
    var d = new Date();
    el.textContent = '· ' + d.toISOString().replace('T', ' ').slice(0, 19) + 'Z';
  }

  function showError(root, err) {
    setStatus('err', 'تعذّر التحميل / failed');
    root.innerHTML = '<div class="err-box">' + escapeHtml(String(err && err.message ? err.message : err)) + '</div>';
  }

  function load() {
    var root = document.getElementById('root');
    if (!root) return;
    var base = (root.getAttribute('data-api-base') || 'https://api.dealix.me').replace(/\/+$/, '');
    var endpoint = root.getAttribute('data-endpoint') || '/api/v1/founder/dashboard';
    var url = base + endpoint;
    setStatus('loading', 'يحمّل… / loading');
    fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' }, credentials: 'omit' })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status + ' from ' + url);
        return r.json();
      })
      .then(function (data) {
        render(root, data);
        setStatus('ok', 'محدَّث / live');
        setUpdated();
      })
      .catch(function (err) { showError(root, err); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', load);
  } else {
    load();
  }
})();
