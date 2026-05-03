/* =============================================================
   Dealix Frontend — partner-portal.js
   Renders the Agency Partner Portal landing data:
     - dashboard KPIs from /api/v1/partners/{id}/dashboard
     - customers table from /api/v1/partners/{id}/customers
   When the API is unreachable OR the partner_id is unset, the
   page keeps its static demo content (no destructive replace).
   ============================================================= */
(function () {
  'use strict';

  function getPartnerId() {
    try {
      const params = new URLSearchParams(location.search || '');
      return (params.get('partner_id')
        || (window.localStorage && window.localStorage.getItem('dealix_partner_id'))
        || ''
      ).trim();
    } catch (_) {
      return '';
    }
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function fmtSar(n) {
    const v = Number(n || 0);
    return v.toLocaleString('en-US', { maximumFractionDigits: 2 }) + ' ر.س';
  }

  function renderKpis(panel, data) {
    const k = (data && data.kpis) || {};
    panel.innerHTML = ''
      + kpi('شركات تم جلبها', k.total_customers_brought || 0)
      + kpi('تدفع حالياً', k.currently_paying || 0)
      + kpi('MRR من إحالاتك', fmtSar(k.mrr_total_sar || 0))
      + kpi('Commission المتوقع شهرياً', fmtSar(k.expected_monthly_commission_sar || 0))
      + kpi('Commission المُكتسب', fmtSar(k.earned_to_date_sar || 0));

    function kpi(label, value) {
      return ''
        + '<div class="dx-card" style="text-align:center;">'
        + '<div style="font-size:0.75rem; color:#475569; margin-bottom:0.25rem;">' + escapeHtml(label) + '</div>'
        + '<div style="font-size:1.5rem; font-weight:800; color:#0A4D3F;">' + escapeHtml(value) + '</div>'
        + '</div>';
    }
  }

  function renderCustomers(tableBody, data) {
    const rows = (data && data.customers) || [];
    if (!rows.length) {
      tableBody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#475569; padding:1rem;">'
        + 'لا توجد شركات في بورتالك بعد.</td></tr>';
      return;
    }
    tableBody.innerHTML = rows.map(function (r) {
      const stagePill = pillForStage(r.stage);
      const statusPill = pillForStatus(r.status);
      const churnPill = pillForChurn(r.churn_risk);
      return ''
        + '<tr>'
        + '<td>' + escapeHtml(r.customer_id || '—') + '</td>'
        + '<td>' + escapeHtml((r.started_at || '').slice(0, 10)) + '</td>'
        + '<td>' + stagePill + '</td>'
        + '<td>' + escapeHtml(r.plan_id || r.plan || '—') + '</td>'
        + '<td>' + fmtSar(r.mrr_sar) + '</td>'
        + '<td>' + statusPill + '</td>'
        + '<td>' + churnPill + '</td>'
        + '</tr>';
    }).join('');
  }

  function pillForStage(stage) {
    const map = {
      paying:   ['success', 'يدفع'],
      pilot:    ['info',    'تجريبي'],
      churned:  ['danger',  'ألغى'],
      at_risk:  ['warning', 'متأخر'],
      trial:    ['info',    'تجريبي'],
    };
    const m = map[stage] || ['', stage || '—'];
    return '<span class="dx-pill dx-pill--' + escapeHtml(m[0]) + '">' + escapeHtml(m[1]) + '</span>';
  }

  function pillForStatus(status) {
    const map = {
      active:   ['success', 'نشط'],
      canceled: ['danger',  'ألغى'],
      paused:   ['warning', 'موقوف'],
      past_due: ['warning', 'متأخر'],
      trialing: ['info',    'تجريبي'],
    };
    const m = map[status] || ['', status || '—'];
    return '<span class="dx-pill dx-pill--' + escapeHtml(m[0]) + '">' + escapeHtml(m[1]) + '</span>';
  }

  function pillForChurn(risk) {
    const map = {
      low:    ['success', 'منخفض'],
      medium: ['warning', 'متوسط'],
      high:   ['danger',  'عالٍ'],
    };
    const m = map[risk] || ['', '—'];
    return '<span class="dx-pill dx-pill--' + escapeHtml(m[0]) + '">' + escapeHtml(m[1]) + '</span>';
  }

  async function init() {
    if (!window.DealixAPI) return;
    const partnerId = getPartnerId();
    if (!partnerId) return; // keep static demo content

    const kpisPanel = document.querySelector('[data-partner-kpis]');
    const customersBody = document.querySelector('[data-partner-customers]');

    if (kpisPanel) {
      const r = await window.DealixAPI.get('/api/v1/partners/' + encodeURIComponent(partnerId) + '/dashboard');
      if (r.ok && r.data) {
        renderKpis(kpisPanel, r.data);
      }
    }
    if (customersBody) {
      const r2 = await window.DealixAPI.get('/api/v1/partners/' + encodeURIComponent(partnerId) + '/customers');
      if (r2.ok && r2.data) {
        renderCustomers(customersBody, r2.data);
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
