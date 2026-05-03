/* =============================================================
   Dealix Frontend — api.js
   Typed API client with base URL detection + safe fallback.

   Usage:
     import { api } from './api.js';
     // or as global: window.DealixAPI

     const data = await api.get('/api/v1/command-center/snapshot');
     const result = await api.post('/api/v1/public/demo-request', {...});

   API base URL resolution order:
     1. window.DEALIX_API_BASE_URL (set inline by page)
     2. localStorage('dealix_api_base')
     3. window.DEALIX_API_BASE (legacy alias used by script.js)
     4. https://api.dealix.me  (production default)
     5. http://localhost:8000  (only when on localhost)

   Failure mode:
     Fetches return null on network error — UI must render demo data
     and show .dx-demo-banner. Never lets backend outage break the page.
   ============================================================= */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.DealixAPI = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function detectBase() {
    try {
      if (typeof window === 'undefined') return 'https://api.dealix.me';
      if (window.DEALIX_API_BASE_URL) return String(window.DEALIX_API_BASE_URL).replace(/\/$/, '');
      try {
        const stored = window.localStorage && window.localStorage.getItem('dealix_api_base');
        if (stored) return stored.replace(/\/$/, '');
      } catch (_) { /* sandboxed iframes block storage */ }
      if (window.DEALIX_API_BASE) return String(window.DEALIX_API_BASE).replace(/\/$/, '');
      const host = window.location && window.location.hostname;
      if (host === 'localhost' || host === '127.0.0.1') return 'http://localhost:8000';
      return 'https://api.dealix.me';
    } catch (_) {
      return 'https://api.dealix.me';
    }
  }

  const BASE = detectBase();
  const DEFAULT_TIMEOUT_MS = 10000;

  function buildUrl(path) {
    if (/^https?:\/\//.test(path)) return path;
    return BASE + (path.startsWith('/') ? path : '/' + path);
  }

  function withTimeout(ms) {
    if (typeof AbortController === 'undefined') return null;
    const ctrl = new AbortController();
    const id = setTimeout(() => ctrl.abort(), ms);
    return { signal: ctrl.signal, clear: () => clearTimeout(id) };
  }

  async function request(method, path, body, opts) {
    opts = opts || {};
    const url = buildUrl(path);
    const timeout = opts.timeout != null ? opts.timeout : DEFAULT_TIMEOUT_MS;
    const aborter = withTimeout(timeout);
    const headers = Object.assign(
      { 'Accept': 'application/json' },
      body ? { 'Content-Type': 'application/json' } : {},
      opts.headers || {}
    );
    try {
      const res = await fetch(url, {
        method: method,
        headers: headers,
        body: body ? JSON.stringify(body) : undefined,
        signal: aborter ? aborter.signal : undefined,
        credentials: opts.credentials || 'omit',
        mode: 'cors',
      });
      if (aborter) aborter.clear();
      const text = await res.text();
      let json = null;
      try { json = text ? JSON.parse(text) : null; } catch (_) { json = null; }
      if (!res.ok) {
        return { ok: false, status: res.status, data: json, error: 'http_' + res.status };
      }
      return { ok: true, status: res.status, data: json, error: null };
    } catch (exc) {
      if (aborter) aborter.clear();
      const isAbort = exc && (exc.name === 'AbortError');
      return {
        ok: false,
        status: 0,
        data: null,
        error: isAbort ? 'timeout' : 'network_error',
        message: exc && exc.message ? String(exc.message) : '',
      };
    }
  }

  return {
    base: BASE,
    get: function (path, opts) { return request('GET', path, null, opts); },
    post: function (path, body, opts) { return request('POST', path, body, opts); },
    put: function (path, body, opts) { return request('PUT', path, body, opts); },
    del: function (path, opts) { return request('DELETE', path, null, opts); },
    /**
     * fetchOrDemo(path, demoData)
     * Tries the API; on any failure returns demoData with isDemo=true.
     * Pages MUST show the .dx-demo-banner when isDemo=true.
     */
    fetchOrDemo: async function (path, demoData, opts) {
      const r = await request('GET', path, null, opts);
      if (r.ok && r.data != null) return { data: r.data, isDemo: false };
      return { data: demoData, isDemo: true };
    },
  };
}));
