/* Dealix subscriber/founder access gate.
 *
 * Lightweight client-side overlay that hides page content until a
 * valid access token is provided. NOT a security boundary — server
 * endpoints remain the source of truth. This is a privacy/UX layer
 * so the founder + subscribers see internal dashboards while the
 * public sees a clean "subscribers only" message.
 *
 * Usage on any private page:
 *   <script src="/assets/js/access-gate.js"
 *           data-tier="founder"></script>
 *   tier values: "founder" (master) | "subscriber" (paid pilot+)
 *
 * First-time activation: visit the URL with
 *   ?access=<token>
 * and the token is stored in localStorage. Subsequent visits unlock
 * automatically.
 *
 * Tokens are configured via window.DEALIX_ACCESS_TOKENS BEFORE this
 * script loads, OR fall back to the built-in placeholders below.
 * Founder rotates real tokens via a private channel (WhatsApp,
 * email) — they never appear in the public site source.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'dealix_access_v1';

  // Default placeholder tokens. Production tokens MUST be set via
  // window.DEALIX_ACCESS_TOKENS in a private build/config step;
  // the placeholders below are deliberately not secrets and serve
  // only to keep the overlay functional pre-rotation.
  var DEFAULT_TOKENS = {
    founder:    'dealix-founder-2026',
    subscriber: 'dealix-pilot-2026',
  };

  var TOKENS = (window.DEALIX_ACCESS_TOKENS || DEFAULT_TOKENS);

  // Determine required tier from <script data-tier="founder|subscriber">
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

  function readStored() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (_) { return null; }
  }
  function writeStored(rec) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(rec)); }
    catch (_) {}
  }
  function clearStored() {
    try { localStorage.removeItem(STORAGE_KEY); } catch (_) {}
  }

  // Token → tier
  function tierForToken(tok) {
    if (!tok) return null;
    if (tok === TOKENS.founder)    return 'founder';
    if (tok === TOKENS.subscriber) return 'subscriber';
    return null;
  }

  // Tier hierarchy: founder ⊃ subscriber
  function tierUnlocks(tier, required) {
    if (required === 'subscriber') return tier === 'founder' || tier === 'subscriber';
    if (required === 'founder')    return tier === 'founder';
    return false;
  }

  function pickFromUrl() {
    var m = location.search.match(/[?&]access=([^&#]+)/);
    return m ? decodeURIComponent(m[1]) : null;
  }

  function injectStyles() {
    var css =
      '#dealix-gate{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;' +
      'background:radial-gradient(900px 500px at 80% -10%,rgba(168,85,247,.18),transparent 60%),' +
      'radial-gradient(900px 500px at 0% 10%,rgba(14,165,233,.18),transparent 60%),' +
      'linear-gradient(180deg,#050816 0%,#0b1124 60%,#1e1b4b 100%);' +
      'color:#e2e8f0;font-family:"IBM Plex Sans Arabic",system-ui,sans-serif;padding:24px;direction:rtl}' +
      '#dealix-gate .dg-card{max-width:520px;width:100%;background:rgba(15,23,42,.6);backdrop-filter:blur(12px);' +
      'border:1px solid rgba(148,163,184,.20);border-radius:20px;padding:36px;display:grid;gap:16px}' +
      '#dealix-gate h2{margin:0;font-size:24px;font-weight:700;background:linear-gradient(90deg,#22d3ee,#a855f7);' +
      '-webkit-background-clip:text;background-clip:text;color:transparent}' +
      '#dealix-gate p{margin:0;font-size:14px;line-height:1.7;color:#94a3b8}' +
      '#dealix-gate label{display:grid;gap:6px;font-size:13px;color:#cbd5e1;font-weight:600}' +
      '#dealix-gate input{padding:12px 14px;border-radius:8px;border:1px solid rgba(148,163,184,.28);' +
      'background:rgba(2,6,23,.4);color:#e2e8f0;font-family:inherit;font-size:14px;direction:ltr}' +
      '#dealix-gate input:focus{outline:none;border-color:#22d3ee;box-shadow:0 0 0 3px rgba(34,211,238,.15)}' +
      '#dealix-gate button{padding:12px 18px;border-radius:10px;border:0;background:#0ea5e9;color:#fff;' +
      'font-family:inherit;font-size:14px;font-weight:600;cursor:pointer;transition:transform 140ms,box-shadow 140ms}' +
      '#dealix-gate button:hover{transform:translateY(-1px);box-shadow:0 8px 24px rgba(14,165,233,.3)}' +
      '#dealix-gate .dg-err{color:#fca5a5;font-size:13px;display:none}' +
      '#dealix-gate .dg-err.show{display:block}' +
      '#dealix-gate .dg-foot{font-size:12px;color:#64748b;margin-top:8px}' +
      '#dealix-gate .dg-foot a{color:#22d3ee;text-decoration:none}' +
      'body.dg-locked{overflow:hidden}';
    var style = document.createElement('style');
    style.id = 'dealix-gate-styles';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function showGate(required) {
    injectStyles();
    document.body.classList.add('dg-locked');
    // Hide all main content visually (server-side data may still be in DOM —
    // that's fine; this is privacy/UX, not security).
    var hideStyle = document.createElement('style');
    hideStyle.id = 'dealix-gate-hide';
    hideStyle.textContent = 'body > *:not(#dealix-gate):not(#dealix-gate-styles):not(#dealix-gate-hide){visibility:hidden!important}';
    document.head.appendChild(hideStyle);

    var html =
      '<div id="dealix-gate" role="dialog" aria-labelledby="dg-title" aria-modal="true">' +
        '<div class="dg-card">' +
          '<h2 id="dg-title">منطقة محميّة</h2>' +
          '<p>هذه الصفحة للمؤسس أو مشتركي الـ Pilot فقط. أدخل رمز الوصول الذي استلمته منّا.</p>' +
          '<p style="font-family:Inter,sans-serif">This page is private. Enter your access code (founder or subscriber tier).</p>' +
          '<label for="dg-input">رمز الوصول · Access code' +
            '<input id="dg-input" type="password" autocomplete="off" placeholder="dealix-..." />' +
          '</label>' +
          '<p class="dg-err" id="dg-err">رمز غير صحيح · Invalid code.</p>' +
          '<button id="dg-submit">فتح الصفحة · Unlock</button>' +
          '<p class="dg-foot">ليس عندك رمز؟ ' +
            '<a href="/start.html">احجز Pilot للحصول عليه</a> · ' +
            '<a href="/">عُد للرئيسيّة</a></p>' +
        '</div>' +
      '</div>';
    var div = document.createElement('div');
    div.innerHTML = html;
    document.body.appendChild(div.firstChild);

    var input = document.getElementById('dg-input');
    var btn = document.getElementById('dg-submit');
    var err = document.getElementById('dg-err');

    function attempt() {
      var tok = (input.value || '').trim();
      var tier = tierForToken(tok);
      if (tier && tierUnlocks(tier, required)) {
        writeStored({ tier: tier, ts: new Date().toISOString() });
        unlockPage();
      } else {
        err.classList.add('show');
        input.focus(); input.select();
      }
    }
    btn.addEventListener('click', attempt);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') attempt(); });
    setTimeout(function () { input.focus(); }, 50);
  }

  function unlockPage() {
    var g = document.getElementById('dealix-gate');
    var s = document.getElementById('dealix-gate-styles');
    var h = document.getElementById('dealix-gate-hide');
    if (g) g.parentNode.removeChild(g);
    if (s) s.parentNode.removeChild(s);
    if (h) h.parentNode.removeChild(h);
    document.body.classList.remove('dg-locked');
    // Tag body for any optional CSS hooks
    var stored = readStored();
    if (stored && stored.tier) {
      document.body.setAttribute('data-access-tier', stored.tier);
    }
  }

  function start() {
    var required = getRequiredTier();

    // 1. Check URL ?access=...
    var fromUrl = pickFromUrl();
    if (fromUrl) {
      var t = tierForToken(fromUrl);
      if (t && tierUnlocks(t, required)) {
        writeStored({ tier: t, ts: new Date().toISOString() });
        // Clean URL
        if (history.replaceState) {
          history.replaceState({}, '', location.pathname + location.hash);
        }
        return; // don't show gate
      }
    }

    // 2. Check localStorage
    var stored = readStored();
    if (stored && stored.tier && tierUnlocks(stored.tier, required)) {
      // Tag body and continue
      document.body.setAttribute('data-access-tier', stored.tier);
      return;
    }

    // 3. Show gate
    showGate(required);
  }

  // Run as early as possible — but the body must exist so we can hide it.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }

  // Expose tiny logout hook for the founder
  window.dealixAccessLogout = function () {
    clearStored();
    location.reload();
  };
})();
