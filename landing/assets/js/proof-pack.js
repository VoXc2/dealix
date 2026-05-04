/* =============================================================
   Dealix Frontend — proof-pack.js
   Wires landing/proof-pack.html to /api/v1/proof-ledger/customer/{id}/pack.

   Behavior:
     - URL param ?customer_id=X loads live data; else keeps the static demo.
     - Renders totals, what_was_created, what_was_protected, next_action.
     - Falls back gracefully when API is unreachable.
   ============================================================= */
(function () {
  'use strict';

  function getCustomerId() {
    try {
      const params = new URLSearchParams(location.search || '');
      return (params.get('customer_id') || '').trim();
    } catch (_) {
      return '';
    }
  }

  function fmt(n) {
    return (Number(n || 0)).toLocaleString('en-US');
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function renderPack(container, pack) {
    const totals = pack.totals || {};
    const created = pack.what_was_created || [];
    const protected_ = pack.what_was_protected || [];
    const banner = '<div class="dx-pill dx-pill--success" style="margin-bottom:1rem;">'
      + 'Proof Pack حي — تم تحديثه من Proof Ledger' + '</div>';

    const totalsHtml = ''
      + '<div class="dx-cards-grid" style="grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:0.75rem;">'
      + tile('فرص + drafts', totals.created_units || 0)
      + tile('مخاطر تم منعها', totals.protected_units || 0)
      + tile('Proof Packs', totals.proof_events || 0)
      + tile('بانتظار موافقة', totals.pending_approvals || 0)
      + tile('أثر الإيراد (ر.س)', fmt(totals.estimated_revenue_impact_sar))
      + '</div>';

    const createdHtml = created.length
      ? '<ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:0.5rem;">'
        + created.map(function (c) {
          return '<li>✓ ' + escapeHtml(c.label_ar) + ' — <strong>' + (c.count || 0) + '</strong></li>';
        }).join('')
        + '</ul>'
      : '<p style="color:var(--text-muted, #475569);">لم تُسجَّل وحدات إنجاز بعد لهذه الفترة.</p>';

    const protectedHtml = protected_.length
      ? '<ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:0.5rem;">'
        + protected_.map(function (p) {
          const risk = p.risk_level === 'high' ? 'عالٍ' : (p.risk_level === 'medium' ? 'متوسط' : 'منخفض');
          return '<li>⚠ ' + escapeHtml(p.label_ar) + ' — مخاطرة ' + escapeHtml(risk) + '</li>';
        }).join('')
        + '</ul>'
      : '<p style="color:var(--text-muted, #475569);">لم تُسجَّل مخاطر محظورة في هذه الفترة.</p>';

    container.innerHTML = ''
      + banner
      + '<section style="margin-top:1rem;"><h3 style="font-size:0.9375rem; margin:0 0 0.5rem; color:var(--dx-emerald);">١. ما تم إنجازه</h3>' + totalsHtml + '</section>'
      + '<section style="margin-top:1rem;"><h3 style="font-size:0.9375rem; margin:0 0 0.5rem; color:var(--dx-emerald);">قائمة الإنجاز</h3>' + createdHtml + '</section>'
      + '<section style="margin-top:1rem;"><h3 style="font-size:0.9375rem; margin:0 0 0.5rem; color:var(--dx-amber);">٢. ما تم حمايته</h3>' + protectedHtml + '</section>'
      + '<section style="margin-top:1rem;"><h3 style="font-size:0.9375rem; margin:0 0 0.5rem; color:var(--dx-charcoal);">٣. الخطوة التالية الموصى بها</h3>'
      + '<p style="font-size:0.9375rem; line-height:1.7; margin:0; padding:0.75rem; background:color-mix(in srgb, var(--dx-emerald) 6%, transparent); border-radius:8px; border-inline-start:3px solid var(--dx-emerald);">'
      + escapeHtml(pack.next_recommended_action_ar || '—') + '</p></section>';

    function tile(label, value) {
      return '<div style="background:var(--bg-muted, #f8fafc); padding:0.75rem; border-radius:8px; text-align:center;">'
        + '<strong style="font-size:1.5rem; display:block;">' + escapeHtml(value) + '</strong>'
        + '<span style="font-size:0.6875rem; color:var(--text-muted, #475569);">' + escapeHtml(label) + '</span>'
        + '</div>';
    }
  }

  async function load() {
    const cid = getCustomerId();
    if (!cid) return; // keep static demo
    if (!window.DealixAPI) return;
    const card = document.querySelector('.dx-card[data-type="proof"]');
    if (!card) return;
    const r = await window.DealixAPI.get('/api/v1/proof-ledger/customer/' + encodeURIComponent(cid) + '/pack');
    if (!r.ok || !r.data || !r.data.pack) return;
    // Replace the demo body of the card with live data
    const dynamic = document.createElement('div');
    dynamic.id = 'dx-proof-live';
    card.appendChild(dynamic);
    renderPack(dynamic, r.data.pack);
    if (window.DealixAnalytics) {
      window.DealixAnalytics.track('proof_pack_viewed', {
        customer_id: cid, event_count: r.data.event_count || 0, source: 'live',
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', load);
  } else {
    load();
  }
}());
