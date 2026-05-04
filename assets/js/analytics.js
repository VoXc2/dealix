/* =============================================================
   Dealix Frontend — analytics.js
   PostHog event taxonomy + safe wrappers.

   Usage:
     <script src="assets/js/analytics.js"></script>
     <script>
       DealixAnalytics.track('cta_clicked', { cta: 'pilot', page: 'index' });
     </script>

   PostHog is loaded via posthog_snippet.html (existing).
   If not loaded, all calls are no-ops (no errors).
   ============================================================= */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.DealixAnalytics = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // Canonical event taxonomy. Pages MUST use these names — no ad-hoc events.
  const EVENTS = Object.freeze({
    // Navigation / CTAs
    CTA_CLICKED:                  'cta_clicked',
    PAGE_VIEWED:                  'page_viewed',

    // Funnel: discovery → diagnostic → pilot
    DIAGNOSTIC_STARTED:           'diagnostic_started',
    DIAGNOSTIC_SUBMITTED:         'diagnostic_submitted',
    SERVICE_RECOMMENDED:          'service_recommended',
    PILOT_CLICKED:                'pilot_clicked',

    // Cards (Command Center)
    CARD_VIEWED:                  'card_viewed',
    CARD_APPROVED:                'card_approved',
    CARD_EDITED:                  'card_edited',
    CARD_SKIPPED:                 'card_skipped',

    // Trust / Proof
    PROOF_PACK_VIEWED:            'proof_pack_viewed',
    TRUST_CENTER_VIEWED:          'trust_center_viewed',

    // Pricing
    PRICING_VIEWED:               'pricing_viewed',

    // Support
    SUPPORT_TICKET_OPENED:        'support_ticket_opened',
    SUPPORT_BOT_CLASSIFIED:       'support_bot_classified',

    // Operator (AI service consultant)
    OPERATOR_INTENT_CLASSIFIED:   'operator_intent_classified',
    OPERATOR_SERVICE_RECOMMENDED: 'operator_service_recommended',
    OPERATOR_BLOCKED_UNSAFE:      'operator_blocked_unsafe',

    // Partner / Agency
    AGENCY_PARTNER_CLICKED:       'agency_partner_clicked',
    PARTNER_APPLICATION_SUBMITTED:'partner_application_submitted',
  });

  function getPostHog() {
    try {
      if (typeof window !== 'undefined' && window.posthog && typeof window.posthog.capture === 'function') {
        return window.posthog;
      }
    } catch (_) { /* ignore */ }
    return null;
  }

  function track(eventName, properties) {
    if (!eventName || typeof eventName !== 'string') return;
    properties = Object.assign({}, properties || {});
    // Always tag with page + locale
    try {
      properties.page = properties.page || (typeof location !== 'undefined' ? location.pathname : '');
      properties.locale = properties.locale || (document && document.documentElement && document.documentElement.lang) || 'ar';
      properties.dx_v = '1.0.0-pr-fe-1';
    } catch (_) { /* ignore */ }
    const ph = getPostHog();
    if (ph) {
      try { ph.capture(eventName, properties); } catch (_) { /* ignore */ }
    }
    // Console mirror in dev for debugging.
    try {
      const host = (location && location.hostname) || '';
      if (host === 'localhost' || host === '127.0.0.1') {

        console.info('[DealixAnalytics]', eventName, properties);
      }
    } catch (_) { /* ignore */ }
  }

  function pageView(pageName) {
    track(EVENTS.PAGE_VIEWED, { name: pageName || (document && document.title) || '' });
  }

  /**
   * Auto-bind: any element with data-track="event_name" emits the event on click.
   * Optional data-track-* attributes become event properties.
   *   <button data-track="cta_clicked" data-track-cta="pilot" data-track-source="hero">
   */
  function bindAuto(rootNode) {
    const r = rootNode || (typeof document !== 'undefined' ? document : null);
    if (!r) return;
    const handler = function (ev) {
      const t = ev.target.closest && ev.target.closest('[data-track]');
      if (!t) return;
      const evName = t.getAttribute('data-track');
      if (!evName) return;
      const props = {};
      for (const attr of t.attributes) {
        if (attr.name.startsWith('data-track-')) {
          const key = attr.name.replace('data-track-', '').replace(/-/g, '_');
          props[key] = attr.value;
        }
      }
      track(evName, props);
    };
    r.addEventListener('click', handler, { capture: true });
  }

  // Auto-init on DOMContentLoaded if available
  try {
    if (typeof document !== 'undefined') {
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { bindAuto(document); });
      } else {
        bindAuto(document);
      }
    }
  } catch (_) { /* ignore */ }

  return {
    EVENTS: EVENTS,
    track: track,
    pageView: pageView,
    bindAuto: bindAuto,
  };
}));
