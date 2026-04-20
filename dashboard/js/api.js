/* ========== Dealix API Client ==========
 * Centralized, retry-safe, auth-aware fetch wrapper.
 * Falls back to mock.json if API is unreachable (demo mode).
 */

// In-memory store (preview iframe blocks localStorage)
window.__dlxStore = window.__dlxStore || {};
const _store = window.__dlxStore;

const API_BASE_URL = (() => {
  if (_store.api_base) return _store.api_base;
  // Default production API (Cloudflare Tunnel)
  const DEFAULT_API = 'https://conduct-earthquake-mailing-constraint.trycloudflare.com';
  // If running on localhost, use same origin; otherwise use default API
  const origin = window.location.origin;
  if (origin.startsWith('http://localhost') || origin.startsWith('http://127.0.0.1')) {
    return origin;
  }
  return DEFAULT_API;
})();

const API_PREFIX = '/api/v1';

const ApiState = {
  demoMode: false,         // true when falling back to mock.json
  mockData: null,          // cached mock.json
  reachable: null,         // null = unknown, true = online, false = offline
  lastError: null,
};

/* Token management — uses in-memory store (iframe blocks localStorage) */
const Auth = {
  get token() { return _store.token || null; },
  set token(v) { if (v) { _store.token = v; } else { delete _store.token; } },
  get user() { return _store.user || null; },
  set user(v) { if (v) { _store.user = v; } else { delete _store.user; } },
  get tenant() { return _store.tenant || null; },
  set tenant(v) { if (v) { _store.tenant = v; } else { delete _store.tenant; } },
  clear() {
    this.token = null;
    this.user = null;
    this.tenant = null;
  }
};

class ApiError extends Error {
  constructor(message, { status = 0, code, body } = {}) {
    super(message);
    this.status = status;
    this.code = code;
    this.body = body;
  }
}

/* Core fetch with retry + auth */
async function rawFetch(path, { method = 'GET', body, retry = 1, headers = {} } = {}) {
  const url = API_BASE_URL + API_PREFIX + path;
  const hdrs = { 'Content-Type': 'application/json', ...headers };
  if (Auth.token) hdrs['Authorization'] = 'Bearer ' + Auth.token;

  const opts = { method, headers: hdrs };
  if (body !== undefined) opts.body = typeof body === 'string' ? body : JSON.stringify(body);

  try {
    const res = await fetch(url, opts);
    ApiState.reachable = true;

    if (res.status === 401) {
      Auth.clear();
      window.dispatchEvent(new CustomEvent('dealix:unauthorized'));
      throw new ApiError('انتهت الجلسة — الرجاء تسجيل الدخول', { status: 401 });
    }

    const text = await res.text();
    let data = null;
    try { data = text ? JSON.parse(text) : null; } catch { data = text; }

    if (!res.ok) {
      const msg = (data && data.detail) || (data && data.message) || res.statusText || 'خطأ في الخادم';
      throw new ApiError(msg, { status: res.status, body: data });
    }
    return data;
  } catch (err) {
    if (err instanceof ApiError) throw err;
    // Network error
    ApiState.reachable = false;
    if (retry > 0) {
      await new Promise(r => setTimeout(r, 600));
      return rawFetch(path, { method, body, retry: retry - 1, headers });
    }
    throw new ApiError('تعذر الوصول إلى الخادم', { status: 0, code: 'NETWORK' });
  }
}

/* Mock fallback loader */
async function loadMock() {
  if (ApiState.mockData) return ApiState.mockData;
  const res = await fetch('./data/mock.json');
  ApiState.mockData = await res.json();
  return ApiState.mockData;
}

/* Map API endpoints to mock fallbacks */
async function mockFallback(path, method) {
  const m = await loadMock();
  // Normalize path
  if (path === '/overview' || path.startsWith('/overview?')) {
    return {
      kpis: {
        active_leads: m.kpis.active_leads,
        hot_leads: m.kpis.hot_leads,
        meetings_week: m.kpis.meetings_this_week,
        pipeline_value_sar: m.kpis.pipeline_value_sar
      },
      funnel: Object.entries(m.funnel).map(([stage, count]) => ({ stage, count })),
      recent_activity: m.activity_feed.map(a => ({
        actor: a.actor, action: a.text, target: a.lead, channel: a.channel, at: a.ts
      })),
      channel_performance: m.channels_performance.map(c => ({
        channel: c.channel, sent: c.sent, replied: c.replied, conv_rate: c.conversion
      }))
    };
  }
  if (path.startsWith('/leads?') || path === '/leads') {
    return { items: m.leads, total: m.leads.length, page: 1 };
  }
  const leadMatch = path.match(/^\/leads\/([^/]+)$/);
  if (leadMatch) {
    return m.leads.find(l => l.id === leadMatch[1]) || null;
  }
  if (path === '/conversations' || path.startsWith('/conversations?')) {
    return {
      items: m.conversations.map(c => ({
        phone: c.id, name: c.sender_name, channel: c.channel,
        last_preview: c.preview, unread: c.unread, last_at: c.ts,
        company_ar: c.company_ar
      }))
    };
  }
  const msgMatch = path.match(/^\/conversations\/([^/]+)\/messages$/);
  if (msgMatch) {
    const c = m.conversations.find(x => x.id === msgMatch[1]);
    return { items: (c?.messages || []).map(msg => ({
      direction: msg.from === 'us' ? 'outbound' : 'inbound',
      body: msg.text, at: msg.ts, sid: 'mock-' + Math.random().toString(36).slice(2, 8)
    })) };
  }
  if (path.match(/\/ai-suggest$/)) {
    return { suggestions: m.ai_suggestions || [
      'مرحباً، شكراً على تواصلك. هل يناسبك اتصال مدته 15 دقيقة لمناقشة التفاصيل؟',
      'ممتاز، أرسل لك عرضاً مفصلاً اليوم. ما أولوياتكم الرئيسية؟',
      'أكيد، نقدر نخصص الباقة حسب احتياجكم. كم عدد المستخدمين المتوقّع؟'
    ] };
  }
  if (path.match(/\/reply$/)) {
    return { message: { direction: 'outbound', body: '', at: new Date().toISOString() }, sid: 'mock-sid', status: 'queued' };
  }
  if (path === '/pipeline') {
    const stages = ['prospect', 'engaged', 'qualified', 'proposal', 'won', 'lost'];
    const statusToStage = {
      new: 'prospect', enriching: 'prospect',
      contacted: 'engaged', engaged: 'engaged',
      qualified: 'qualified',
      meeting: 'proposal', proposal: 'proposal', negotiation: 'proposal',
      closed_won: 'won', closed_lost: 'lost', disqualified: 'lost'
    };
    const cols = stages.map(s => ({ stage: s, leads: [] }));
    m.leads.forEach(l => {
      const st = statusToStage[l.status] || 'prospect';
      cols.find(c => c.stage === st).leads.push(l);
    });
    return { columns: cols };
  }
  if (path.match(/\/leads\/[^/]+\/stage$/)) {
    return { lead: {}, activity: {} };
  }
  if (path === '/agents') return m.agents;
  if (path.match(/\/agents\/[^/]+\/toggle$/)) {
    return { agent: { id: 'mock', status: 'idle' } };
  }
  if (path === '/sources') return m.sources;
  if (path.match(/\/sources\/[^/]+\/discover$/)) {
    return { job_id: 'mock-job-' + Date.now(), status: 'queued' };
  }
  if (path.startsWith('/analytics/mrr')) {
    return { points: m.mrr_trend.map(x => ({ date: x.month, value: x.mrr })) };
  }
  if (path.startsWith('/analytics/conversion')) {
    return { channels: m.channels_performance };
  }
  if (path === '/readiness-matrix') {
    return {
      counts: { live: 5, partial: 12, pilot: 3, target: 9, deprecated: 0 },
      services: []
    };
  }
  if (path === '/playbooks') return m.playbooks;
  if (path === '/settings') {
    return {
      org: { name: 'Dealix Demo', currency: 'SAR', timezone: 'Asia/Riyadh' },
      team: [{ email: 'sami@dealix.sa', role: 'admin' }],
      api_keys: [
        { name: 'Groq', masked: 'gsk_***************abcd', rotated_at: null },
        { name: 'Twilio', masked: 'AC***************xyz', rotated_at: null },
        { name: 'SendGrid', masked: 'SG.***************123', rotated_at: null }
      ],
      notifications: { slack_webhook: '' },
      compliance: { pdpl_consent_default: true, retention_days: 365 }
    };
  }
  return null;
}

/* Public apiClient */
const apiClient = {
  async request(path, method = 'GET', body) {
    try {
      const data = await rawFetch(path, { method, body });
      if (ApiState.demoMode) {
        ApiState.demoMode = false;
        window.dispatchEvent(new CustomEvent('dealix:demo-mode', { detail: { on: false } }));
      }
      return data;
    } catch (err) {
      ApiState.lastError = err;
      // Only use mock for GETs (and safe POST patterns like ai-suggest/discover that are idempotent-ish)
      const allowMock = method === 'GET' || /\/(ai-suggest|discover|reply|toggle|stage)$/.test(path);
      const shouldFallback = err.status === 0 || err.code === 'NETWORK' || err.status === 404 || err.status >= 500;
      if (shouldFallback && allowMock) {
        if (!ApiState.demoMode) {
          ApiState.demoMode = true;
          window.dispatchEvent(new CustomEvent('dealix:demo-mode', { detail: { on: true } }));
        }
        const mock = await mockFallback(path, method);
        if (mock !== null) return mock;
      }
      throw err;
    }
  },
  get(path) { return this.request(path, 'GET'); },
  post(path, body) { return this.request(path, 'POST', body); },
  patch(path, body) { return this.request(path, 'PATCH', body); },
  del(path) { return this.request(path, 'DELETE'); },

  /* Auth-specific — does NOT use Authorization header, does NOT fallback */
  async login(email, password) {
    try {
      const data = await rawFetch('/auth/login', { method: 'POST', body: { email, password }, retry: 0 });
      Auth.token = data.token;
      Auth.user = data.user;
      Auth.tenant = data.tenant;
      return data;
    } catch (err) {
      const noBackend = err.status === 0 || err.status === 404 || err.status >= 500;
      if (noBackend) {
        // Offline or no backend — allow demo login
        if ((email === 'demo@dealix.sa' || email === 'sami@dealix.sa') && password === 'demo1234') {
          const fake = {
            token: 'demo-token-' + Date.now(),
            user: { id: 'u-demo', email, name: 'سامي العسيري', role: 'admin' },
            tenant: { id: 't-demo', name: 'Dealix Demo', plan: 'Growth' }
          };
          Auth.token = fake.token; Auth.user = fake.user; Auth.tenant = fake.tenant;
          ApiState.demoMode = true;
          window.dispatchEvent(new CustomEvent('dealix:demo-mode', { detail: { on: true } }));
          return fake;
        }
        throw new ApiError('الخادم غير متاح. جرّب demo@dealix.sa / demo1234 لمعاينة الوضع التجريبي.', { status: 0 });
      }
      throw err;
    }
  },
  logout() {
    Auth.clear();
    window.dispatchEvent(new CustomEvent('dealix:logout'));
  },
  isAuthenticated() { return !!Auth.token; },
  API_BASE_URL,
  wsUrl() {
    const proto = API_BASE_URL.startsWith('https') ? 'wss' : 'ws';
    const host = API_BASE_URL.replace(/^https?:\/\//, '');
    return `${proto}://${host}${API_PREFIX}/ws?token=${encodeURIComponent(Auth.token || '')}`;
  }
};

window.apiClient = apiClient;
window.Auth = Auth;
window.ApiState = ApiState;
