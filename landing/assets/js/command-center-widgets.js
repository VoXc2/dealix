/* =============================================================
   Dealix Frontend — command-center-widgets.js
   3 live widgets injected at top of command-center.html:
     1. Daily Ops history (last 4 runs)
     2. Cost summary (last 7 days)
     3. Unsafe actions blocked (last 7 days)

   Markup contract:
     <div data-widget="daily-ops"></div>
     <div data-widget="cost-summary"></div>
     <div data-widget="unsafe-blocked"></div>
   ============================================================= */
(function () {
  'use strict';

  function api() { return window.DealixAPI || null; }

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

  function tile(label, value, sub) {
    return ''
      + '<div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:0.75rem 1rem;">'
      + '<div style="font-size:1.25rem; font-weight:800; color:#0f172a;">' + escapeHtml(value) + '</div>'
      + '<div style="font-size:0.75rem; color:#475569;">' + escapeHtml(label) + '</div>'
      + (sub ? '<div style="font-size:0.6875rem; color:#64748b; margin-top:0.25rem;">' + escapeHtml(sub) + '</div>' : '')
      + '</div>';
  }

  function fail(el, msg) {
    el.innerHTML = '<div class="dx-demo-banner" role="status">' + escapeHtml(msg) + '</div>';
  }

  // ── Daily Ops widget ────────────────────────────────────────
  async function renderDailyOps() {
    const el = document.querySelector('[data-widget="daily-ops"]');
    if (!el || !api()) return;
    const r = await api().get('/api/v1/daily-ops/history?limit=4');
    if (!r.ok || !r.data) return fail(el, 'Daily Ops history غير متاح الآن.');
    const runs = r.data.runs || [];
    const tiles = runs.length
      ? runs.map(function (run) {
          const when = (run.started_at || '').slice(11, 16);
          const win = run.window || '';
          return tile(
            win + ' · ' + when,
            run.decisions_total || 0,
            (run.risks_blocked_total || 0) + ' refusals'
          );
        }).join('')
      : tile('لا توجد runs بعد', '0', 'شغّل /api/v1/daily-ops/run');
    el.innerHTML = ''
      + '<header style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">'
      + '<h3 style="margin:0; font-size:0.9375rem; font-weight:700;">Daily Ops · آخر ٤ runs</h3>'
      + '<a href="#" data-track="cta_clicked" data-track-cta="daily_ops_run" '
      + 'style="font-size:0.75rem; color:#0A4D3F; font-weight:600; text-decoration:none;" '
      + 'id="dx-run-morning">شغّل morning →</a>'
      + '</header>'
      + '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:0.5rem;">'
      + tiles
      + '</div>';
    const trigger = document.getElementById('dx-run-morning');
    if (trigger) {
      trigger.addEventListener('click', async function (ev) {
        ev.preventDefault();
        await api().post('/api/v1/daily-ops/run', { window: 'morning' });
        renderDailyOps();
      });
    }
  }

  // ── Cost Summary widget ─────────────────────────────────────
  async function renderCostSummary() {
    const el = document.querySelector('[data-widget="cost-summary"]');
    if (!el || !api()) return;
    const r = await api().get('/api/v1/observability/costs/summary?days=7');
    if (!r.ok || !r.data) return fail(el, 'Cost summary غير متاح الآن.');
    const d = r.data;
    el.innerHTML = ''
      + '<header style="margin-bottom:0.5rem;">'
      + '<h3 style="margin:0; font-size:0.9375rem; font-weight:700;">التكلفة · آخر ٧ أيام</h3>'
      + '<small style="color:#64748b;">مرشّح بـ trace_redactor — لا PII في الـ ledger</small>'
      + '</header>'
      + '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:0.5rem;">'
      + tile('التكلفة الإجمالية', fmtSar(d.total_cost_sar))
      + tile('agent runs', d.run_count || 0)
      + tile('input tokens', (d.input_tokens || 0).toLocaleString())
      + tile('avg latency (ms)', Math.round(d.avg_latency_ms || 0))
      + tile('error rate', (Math.round((d.error_rate || 0) * 1000) / 10) + '%')
      + '</div>';
  }

  // ── Unsafe Blocked widget ───────────────────────────────────
  async function renderUnsafeBlocked() {
    const el = document.querySelector('[data-widget="unsafe-blocked"]');
    if (!el || !api()) return;
    const r = await api().get('/api/v1/observability/unsafe/summary?days=7');
    if (!r.ok || !r.data) return fail(el, 'Unsafe-actions ledger غير متاح الآن.');
    const d = r.data;
    const sev = d.by_severity || { high: 0, medium: 0, low: 0 };
    const patternRows = Object.entries(d.by_pattern || {}).slice(0, 5)
      .map(function (kv) {
        return '<li style="display:flex; justify-content:space-between; padding:0.25rem 0; border-bottom:1px dashed #e2e8f0; font-size:0.8125rem;">'
          + '<code style="font-family:ui-monospace,monospace;">' + escapeHtml(kv[0]) + '</code>'
          + '<strong>' + escapeHtml(kv[1]) + '</strong>'
          + '</li>';
      }).join('');
    el.innerHTML = ''
      + '<header style="margin-bottom:0.5rem;">'
      + '<h3 style="margin:0; font-size:0.9375rem; font-weight:700;">⛔ refusals · آخر ٧ أيام</h3>'
      + '<small style="color:#64748b;">'
      + (d.no_unsafe_action_executed ? '✓ صفر unsafe actions executed (invariant)' : 'invariant violated')
      + '</small></header>'
      + '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(120px, 1fr)); gap:0.5rem;">'
      + tile('high', sev.high || 0, 'PDPL/ToS')
      + tile('medium', sev.medium || 0, 'soft policy')
      + tile('low', sev.low || 0, 'informational')
      + '</div>'
      + (patternRows ? '<ul style="list-style:none; padding:0; margin:0.75rem 0 0;">' + patternRows + '</ul>' : '');
  }

  function init() {
    Promise.all([
      renderDailyOps(),
      renderCostSummary(),
      renderUnsafeBlocked(),
    ]).catch(function () { /* widgets fail open */ });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
