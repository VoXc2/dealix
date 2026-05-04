/* =============================================================
   Dealix Frontend — service-tower.js
   Fetches /api/v1/services/catalog and re-renders the Service Tower.
   Falls back to the static markup already in services.html on error
   (which means: do nothing — the page stays as-is).
   ============================================================= */
(function () {
  'use strict';

  function findGrid() {
    return document.querySelector('.dx-bundle-grid');
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function renderBundle(b) {
    const items = (b.deliverables_ar || []).map(function (d) {
      return '<li>' + escapeHtml(d) + '</li>';
    }).join('');
    const sla = b.sla_ar
      ? '<p class="dx-bundle__sla"><span>SLA:</span> <strong>' + escapeHtml(b.sla_ar) + '</strong></p>'
      : '';
    const safety = b.safe_policy_ar
      ? '<p class="dx-bundle__safety-note">' + escapeHtml(b.safe_policy_ar) + '</p>'
      : '';
    const cta = (b.cta_path || 'private-beta.html');
    const isHighlight = b.highlight ? ' dx-bundle--highlight' : '';
    const trackCta = 'bundle_' + b.id;

    return '<article class="dx-bundle' + isHighlight + '">'
      + '<header class="dx-bundle__head">'
      + '<h3 class="dx-bundle__name">' + escapeHtml(b.name_ar || b.name_en || b.id) + '</h3>'
      + '<span class="dx-bundle__price">' + escapeHtml(b.price_label || 'Custom') + '</span>'
      + '</header>'
      + '<p class="dx-bundle__for">' + escapeHtml(b.for_whom_ar || '') + '</p>'
      + '<ul class="dx-bundle__list">' + items + '</ul>'
      + sla
      + safety
      + '<a href="' + escapeHtml(cta) + '"'
      + ' class="dx-btn dx-btn--primary dx-btn--block dx-bundle__cta"'
      + ' data-track="cta_clicked"'
      + ' data-track-cta="' + escapeHtml(trackCta) + '"'
      + ' data-track-source="services_api">التفاصيل</a>'
      + '</article>';
  }

  async function load() {
    const grid = findGrid();
    if (!grid) return;
    if (!window.DealixAPI) return; // api.js not loaded
    const r = await window.DealixAPI.get('/api/v1/services/catalog');
    if (!r.ok || !r.data || !Array.isArray(r.data.bundles)) {
      // Show subtle demo banner if the API was unreachable
      const banner = document.createElement('div');
      banner.className = 'dx-demo-banner';
      banner.setAttribute('role', 'status');
      banner.textContent = 'الباقات تُعرض من النسخة الثابتة — API غير متصل.';
      grid.parentNode.insertBefore(banner, grid);
      return;
    }
    const bundles = r.data.bundles;
    const html = bundles.map(renderBundle).join('\n');
    grid.innerHTML = html;
    if (window.DealixAnalytics) {
      window.DealixAnalytics.track('service_recommended', { source: 'catalog_load', count: bundles.length });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', load);
  } else {
    load();
  }
}());
