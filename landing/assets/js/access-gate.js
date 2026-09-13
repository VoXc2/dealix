/* Dealix private-surface UX guard.
 *
 * SECURITY BOUNDARY: NONE.
 * This script MUST NOT contain or validate secrets, bearer tokens, API keys,
 * founder codes, subscriber codes, or URL credentials. Private data and API
 * authorization belong to the authenticated server/API layer.
 *
 * The page is shown only when a trusted application shell has injected an
 * authorization context before this script loads:
 *
 *   window.DEALIX_ACCESS_CONTEXT = {
 *     authorized: true,
 *     tier: 'founder' | 'subscriber'
 *   };
 *
 * A visitor can modify browser state, so this context is only a presentation
 * signal. Sensitive data must never be shipped in static HTML or unlocked by
 * this script. Missing/invalid context fails closed.
 */
(function () {
  'use strict';

  function getRequiredTier() {
    var scripts = document.getElementsByTagName('script');
    for (var i = scripts.length - 1; i >= 0; i--) {
      var s = scripts[i];
      if (s.src && s.src.indexOf('access-gate.js') !== -1) {
        return s.getAttribute('data-tier') || 'subscriber';
      }
    }
    return 'subscriber';
  }

  function tierUnlocks(tier, required) {
    if (required === 'subscriber') return tier === 'founder' || tier === 'subscriber';
    if (required === 'founder') return tier === 'founder';
    return false;
  }

  function normalizedContext() {
    var raw = window.DEALIX_ACCESS_CONTEXT;
    if (!raw || raw.authorized !== true) return null;
    var tier = String(raw.tier || '').toLowerCase();
    if (tier !== 'founder' && tier !== 'subscriber') return null;
    return { authorized: true, tier: tier };
  }

  function injectStyles() {
    if (document.getElementById('dealix-gate-styles')) return;
    var css =
      '#dealix-gate{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;' +
      'background:linear-gradient(180deg,#050816 0%,#0b1124 60%,#1e1b4b 100%);' +
      'color:#e2e8f0;font-family:"IBM Plex Sans Arabic",system-ui,sans-serif;padding:24px;direction:rtl}' +
      '#dealix-gate .dg-card{max-width:560px;width:100%;background:rgba(15,23,42,.72);' +
      'border:1px solid rgba(148,163,184,.20);border-radius:20px;padding:36px;display:grid;gap:14px}' +
      '#dealix-gate h2{margin:0;font-size:24px;font-weight:700;color:#e2e8f0}' +
      '#dealix-gate p{margin:0;font-size:14px;line-height:1.8;color:#94a3b8}' +
      '#dealix-gate a{color:#22d3ee;text-decoration:none;font-weight:600}' +
      'body.dg-locked{overflow:hidden}';
    var style = document.createElement('style');
    style.id = 'dealix-gate-styles';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function lockPage(required) {
    injectStyles();
    document.body.classList.add('dg-locked');

    var hideStyle = document.createElement('style');
    hideStyle.id = 'dealix-gate-hide';
    hideStyle.textContent = 'body > *:not(#dealix-gate):not(#dealix-gate-styles):not(#dealix-gate-hide){visibility:hidden!important}';
    document.head.appendChild(hideStyle);

    var gate = document.createElement('div');
    gate.id = 'dealix-gate';
    gate.setAttribute('role', 'dialog');
    gate.setAttribute('aria-modal', 'true');
    gate.innerHTML =
      '<div class="dg-card">' +
        '<h2>منطقة خاصة · Private workspace</h2>' +
        '<p>هذه الصفحة لا تستخدم رموز وصول ثابتة أو مفاتيح داخل المتصفح. يلزم سياق جلسة مصادق عليه من طبقة التطبيق.</p>' +
        '<p dir="ltr">No browser token, URL credential, or localStorage value can unlock this page. Authentication and data authorization are server responsibilities.</p>' +
        '<p>المستوى المطلوب: <strong>' + required + '</strong></p>' +
        '<p><a href="/">العودة إلى Dealix</a></p>' +
      '</div>';
    document.body.appendChild(gate);
  }

  function unlockPresentation(ctx) {
    document.body.setAttribute('data-access-tier', ctx.tier);
  }

  function start() {
    var required = getRequiredTier();
    var ctx = normalizedContext();
    if (ctx && tierUnlocks(ctx.tier, required)) {
      unlockPresentation(ctx);
      return;
    }
    lockPage(required);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
