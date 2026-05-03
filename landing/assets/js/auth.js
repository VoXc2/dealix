/* =============================================================
   Dealix Frontend — auth.js
   Magic-link client (cookie-based session).

   Public methods on window.DealixAuth:
     sendMagicLink(email)   → POST /api/v1/auth/magic-link/send
     getMe()                → GET  /api/v1/auth/me   (uses session cookie)
     logout()               → POST /api/v1/auth/logout
   ============================================================= */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.DealixAuth = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function api() {
    return (typeof window !== 'undefined' && window.DealixAPI) ? window.DealixAPI : null;
  }

  async function sendMagicLink(email) {
    const a = api();
    if (!a) return { ok: false, error: 'no_api_client' };
    const r = await a.post('/api/v1/auth/magic-link/send', { email: String(email || '').trim().toLowerCase() }, {
      credentials: 'include',
    });
    return { ok: r.ok, data: r.data, error: r.error };
  }

  async function getMe() {
    const a = api();
    if (!a) return { ok: false, error: 'no_api_client' };
    const r = await a.get('/api/v1/auth/me', { credentials: 'include' });
    return { ok: r.ok, data: r.data, error: r.error };
  }

  async function logout() {
    const a = api();
    if (!a) return { ok: false };
    const r = await a.post('/api/v1/auth/logout', {}, { credentials: 'include' });
    return { ok: r.ok };
  }

  return {
    sendMagicLink: sendMagicLink,
    getMe: getMe,
    logout: logout,
  };
}));
