/* =============================================================
   Dealix Frontend — components-loader.js
   Lightweight HTML partial loader for static pages.

   Usage in HTML:
     <div data-include="components/nav.html"></div>
     <div data-include="components/footer.html"></div>

   The loader fetches each partial once, caches it, and replaces
   the placeholder. Idempotent + safe under file:// (logs warning).
   ============================================================= */
(function () {
  'use strict';

  const cache = new Map();

  async function fetchPartial(url) {
    if (cache.has(url)) return cache.get(url);
    const promise = (async () => {
      try {
        const res = await fetch(url, { credentials: 'omit' });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return await res.text();
      } catch (err) {

        console.warn('[components-loader] failed:', url, err && err.message);
        return null;
      }
    })();
    cache.set(url, promise);
    return promise;
  }

  function activeNavClass() {
    try {
      const path = (location && location.pathname) || '';
      const file = path.split('/').pop() || 'index.html';
      const links = document.querySelectorAll('.dx-nav__links a[href]');
      links.forEach((a) => {
        const href = a.getAttribute('href') || '';
        if (href.endsWith(file) || (file === 'index.html' && (href === '/' || href === 'index.html'))) {
          a.setAttribute('aria-current', 'page');
          a.classList.add('is-active');
        }
      });
    } catch (_) { /* ignore */ }
  }

  function bindMobileToggle() {
    const toggle = document.querySelector('.dx-nav__menu-toggle');
    const menu = document.querySelector('.dx-nav__links');
    if (!toggle || !menu) return;
    toggle.addEventListener('click', () => {
      menu.classList.toggle('is-open');
      const open = menu.classList.contains('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  async function injectAll() {
    const placeholders = document.querySelectorAll('[data-include]');
    if (!placeholders.length) return;
    await Promise.all(Array.from(placeholders).map(async (el) => {
      const src = el.getAttribute('data-include');
      if (!src) return;
      const html = await fetchPartial(src);
      if (html != null) {
        el.outerHTML = html;
      }
    }));
    // Post-injection wiring
    activeNavClass();
    bindMobileToggle();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectAll);
  } else {
    injectAll();
  }

  // Expose for tests
  window.DealixLoader = { injectAll: injectAll };
}());
