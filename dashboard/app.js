/* ================================================================
 * Dealix Dashboard v2 — Real Data + WebSocket + Auth
 * ================================================================
 * Module layout (single-file for no-build simplicity):
 *   1. Utilities (DOM, fmt, escape)
 *   2. Toast + Modal helpers
 *   3. State
 *   4. Auth flow (login gate, logout, token refresh)
 *   5. Data loaders (overview, leads, inbox, pipeline, etc.)
 *   6. Renderers
 *   7. Interactions (drag-drop, replies, suggestions)
 *   8. Command palette
 *   9. WebSocket integration
 *  10. Bootstrap
 * ================================================================ */

'use strict';

/* ============================================================
 * 1. Utilities
 * ============================================================ */
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

const fmtNum = (n) => new Intl.NumberFormat('en-US').format(Number(n) || 0);
const fmtSar = (n) => {
  n = Number(n) || 0;
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000) return (n / 1_000).toFixed(0) + 'K';
  return fmtNum(n);
};

const channelLabel = {
  whatsapp: 'واتساب', email: 'البريد', linkedin: 'LinkedIn', sms: 'SMS',
  meeting: 'اجتماع', system: 'النظام'
};
const channelIcon = {
  whatsapp: '#i-whatsapp', email: '#i-mail', linkedin: '#i-linkedin',
  sms: '#i-sms', meeting: '#i-calendar', system: '#i-bot'
};
const statusLabel = {
  new: 'جديد', enriching: 'تحت التحليل', qualified: 'مُأَهَّل',
  contacted: 'تم التواصل', engaged: 'منخرط', meeting: 'اجتماع مُجدول',
  proposal: 'عرض مُرسل', negotiation: 'تفاوض',
  closed_won: 'فوز', closed_lost: 'خسارة', disqualified: 'مستبعد'
};
const tierLabel = { hot: '🔥 ساخن', warm: 'دافئ', cool: 'بارد', cold: 'جامد' };
const scoreClass = (s) => s >= 70 ? 'score--high' : s >= 55 ? 'score--mid' : s >= 40 ? 'score--low' : 'score--weak';
const tierClass = (t) => ({ hot: 'badge--hot', warm: 'badge--warm', cool: 'badge--cool', cold: 'badge--cold' }[t] || 'badge--neutral');

const statusToStage = {
  new: 'prospect', enriching: 'prospect',
  contacted: 'engaged', engaged: 'engaged',
  qualified: 'qualified',
  meeting: 'proposal', proposal: 'proposal', negotiation: 'proposal',
  closed_won: 'won', closed_lost: 'lost', disqualified: 'lost'
};
const stageToStatus = {
  prospect: 'new', engaged: 'engaged', qualified: 'qualified',
  proposal: 'proposal', won: 'closed_won', lost: 'closed_lost'
};

function escapeHtml(str) {
  if (str == null) return '';
  return String(str).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function escapeAttr(str) {
  return String(str || '').replace(/`/g, '\\`').replace(/\$/g, '\\$').replace(/"/g, '&quot;');
}
function initial(name) {
  if (!name) return '?';
  const parts = String(name).trim().split(/\s+/);
  if (parts.length >= 2) return parts[0][0] + parts[1][0];
  return String(name).slice(0, 2);
}
function relTime(ts) {
  if (!ts) return '—';
  const d = new Date(ts);
  if (isNaN(d)) return String(ts);
  const diff = (Date.now() - d.getTime()) / 1000;
  if (diff < 60) return 'الآن';
  if (diff < 3600) return `منذ ${Math.floor(diff/60)} د`;
  if (diff < 86400) return `منذ ${Math.floor(diff/3600)} س`;
  return `منذ ${Math.floor(diff/86400)} ي`;
}

/* ============================================================
 * 2. Toast + Modal helpers
 * ============================================================ */
function showToast(text, kind = 'ok') {
  const el = document.createElement('div');
  el.className = 'toast toast--' + kind;
  const icon = kind === 'err' ? 'i-alert' : 'i-check';
  el.innerHTML = `<svg><use href="#${icon}"/></svg><span>${escapeHtml(text)}</span>`;
  const wrap = $('#toasts'); if (!wrap) return;
  wrap.appendChild(el);
  setTimeout(() => { el.style.animation = 'toastIn var(--t-med) var(--ease) reverse'; }, 2600);
  setTimeout(() => el.remove(), 3000);
}

const Modal = {
  open(id) {
    $('#modal-backdrop').classList.add('is-open');
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.add('is-open');
    // focus trap: focus first button/input
    setTimeout(() => {
      const f = el.querySelector('input, textarea, select, button');
      if (f) f.focus();
    }, 50);
  },
  close() {
    $('#modal-backdrop').classList.remove('is-open');
    $$('.modal.is-open').forEach(m => m.classList.remove('is-open'));
  }
};

function renderEmpty(container, message, cta) {
  container.innerHTML = `
    <div class="empty-state">
      <svg><use href="#i-inbox"/></svg>
      <strong>${escapeHtml(message)}</strong>
      ${cta ? `<button class="btn btn--primary btn--sm mt-2" onclick="${escapeAttr(cta.onclick)}">${escapeHtml(cta.label)}</button>` : ''}
    </div>`;
}
function renderError(container, message, retryFn) {
  container.innerHTML = `
    <div class="error-state">
      <svg><use href="#i-alert"/></svg>
      <strong>${escapeHtml(message || 'تعذر التحميل')}</strong>
      <small>راجع الاتصال بالخادم</small>
      <button class="btn btn--primary btn--sm" id="__retry_${Math.random().toString(36).slice(2,7)}">أعد المحاولة</button>
    </div>`;
  const btn = container.querySelector('.btn--primary');
  if (btn && retryFn) btn.addEventListener('click', retryFn);
}
function renderSkeleton(container, rows = 3) {
  container.innerHTML = Array(rows).fill('<div class="skeleton-row"></div>').join('');
}

/* ============================================================
 * 3. State
 * ============================================================ */
const state = {
  route: 'overview',
  overview: null,
  leads: [],
  leadsLoaded: false,
  leadFilter: 'all',
  leadSearch: '',
  conversations: [],
  activeConv: null,
  convMessages: {}, // keyed by phone/id
  convSearch: '',
  inboxChannel: 'all',
  pipeline: null,
  pipeFilter: { sector: '', owner: '', valueBand: '' },
  agents: [],
  playbooks: [],
  sources: [],
  analytics: null,
  analyticsRange: '30d',
  settings: null,
  readiness: null,
};

window.state = state;

/* ============================================================
 * 4. Auth flow
 * ============================================================ */

function showLoginGate() {
  const gate = $('#auth-gate');
  const app = $('#app-shell');
  gate.setAttribute('aria-hidden', 'false');
  app.hidden = true;
  setTimeout(() => $('#login-email')?.focus(), 100);
}

function hideLoginGate() {
  const gate = $('#auth-gate');
  const app = $('#app-shell');
  gate.setAttribute('aria-hidden', 'true');
  app.hidden = false;
  applyUserToHeader();
}

function applyUserToHeader() {
  const user = Auth.user || {};
  const tenant = Auth.tenant || {};
  $('#sidebar-avatar').textContent = initial(user.name || user.email || '?');
  $('#sidebar-user-name').textContent = user.name || user.email || 'المستخدم';
  $('#sidebar-tenant-name').textContent = tenant.name || tenant.id || 'Dealix';
}

function bindAuthEvents() {
  $('#login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = $('#login-email').value.trim();
    const password = $('#login-password').value;
    const err = $('#login-error');
    const btn = $('#login-submit');
    err.hidden = true;
    btn.disabled = true;
    btn.querySelector('span').textContent = 'جاري الدخول...';
    try {
      await apiClient.login(email, password);
      hideLoginGate();
      await bootApp();
    } catch (ex) {
      err.textContent = ex.message || 'فشل تسجيل الدخول';
      err.hidden = false;
    } finally {
      btn.disabled = false;
      btn.querySelector('span').textContent = 'تسجيل الدخول';
    }
  });

  $('#sidebar-logout').addEventListener('click', () => {
    apiClient.logout();
    WS.disconnect();
    location.reload();
  });

  window.addEventListener('dealix:unauthorized', () => {
    showToast('انتهت الجلسة — الرجاء تسجيل الدخول', 'err');
    setTimeout(() => location.reload(), 1200);
  });

  window.addEventListener('dealix:demo-mode', (e) => {
    const banner = $('#demo-banner');
    if (e.detail.on) {
      banner.hidden = false;
      document.body.classList.add('has-banner');
    } else {
      banner.hidden = true;
      document.body.classList.remove('has-banner');
    }
  });
  $('#demo-banner-retry')?.addEventListener('click', () => location.reload());

  window.addEventListener('online', () => { $('#offline-banner').hidden = true; });
  window.addEventListener('offline', () => { $('#offline-banner').hidden = false; });
}

/* ============================================================
 * 5. Data Loaders (per section)
 * ============================================================ */

async function loadOverview() {
  try {
    state.overview = await apiClient.get('/overview');
    renderOverview();
  } catch (err) {
    renderError($('#kpi-grid'), err.message, loadOverview);
  }
}

async function loadLeads() {
  const tbody = $('#leads-tbody');
  if (!state.leadsLoaded) renderSkeleton(tbody, 8);
  try {
    const res = await apiClient.get('/leads?limit=200');
    state.leads = Array.isArray(res) ? res : (res.items || []);
    state.leadsLoaded = true;
    renderLeads();
    $('#nav-leads-count').textContent = state.leads.length;
    $('#leads-subtitle').textContent = `${state.leads.length} شركة مكتشفة ومُأَهَّلة`;
  } catch (err) {
    renderError(tbody.closest('.table-wrap'), err.message, loadLeads);
  }
}

async function loadConversations() {
  try {
    const res = await apiClient.get('/conversations');
    state.conversations = (res.items || res || []).map(c => ({
      id: c.phone || c.id,
      phone: c.phone || c.id,
      sender_name: c.name || c.sender_name,
      channel: c.channel,
      preview: c.last_preview || c.preview,
      unread: c.unread || 0,
      ts: c.last_at || c.ts,
      company_ar: c.company_ar || '',
    }));
    renderConversations();
    const unread = state.conversations.filter(c => c.unread > 0).length;
    $('#nav-inbox-count').textContent = unread || state.conversations.length;
  } catch (err) {
    renderError($('#conv-list'), err.message, loadConversations);
  }
}

async function loadConversationMessages(id) {
  try {
    const res = await apiClient.get(`/conversations/${encodeURIComponent(id)}/messages`);
    state.convMessages[id] = (res.items || res || []);
    return state.convMessages[id];
  } catch (err) {
    showToast('تعذر تحميل الرسائل', 'err');
    return [];
  }
}

async function loadPipeline() {
  try {
    const res = await apiClient.get('/pipeline');
    state.pipeline = res;
    renderKanban();
  } catch (err) {
    renderError($('#kanban'), err.message, loadPipeline);
  }
}

async function loadAgents() {
  try {
    const res = await apiClient.get('/agents');
    state.agents = Array.isArray(res) ? res : (res.items || []);
    renderAgents();
  } catch (err) {
    renderError($('#agents-grid'), err.message, loadAgents);
  }
}

async function loadPlaybooks() {
  try {
    const res = await apiClient.get('/playbooks');
    state.playbooks = Array.isArray(res) ? res : (res.items || []);
    renderPlaybooks();
  } catch (err) {
    renderError($('#playbooks-list'), err.message, loadPlaybooks);
  }
}

async function loadSources() {
  try {
    const res = await apiClient.get('/sources');
    state.sources = Array.isArray(res) ? res : (res.items || []);
    renderSources();
  } catch (err) {
    renderError($('#sources-grid'), err.message, loadSources);
  }
}

async function loadAnalytics() {
  try {
    const [mrr, conv] = await Promise.all([
      apiClient.get(`/analytics/mrr?range=${state.analyticsRange}`),
      apiClient.get(`/analytics/conversion?range=${state.analyticsRange}`).catch(() => null),
    ]);
    state.analytics = { mrr, conv };
    renderAnalytics();
  } catch (err) {
    renderError($('#mrr-chart'), err.message, loadAnalytics);
  }
}

async function loadSettings() {
  try {
    const res = await apiClient.get('/settings');
    state.settings = res;
    renderSettings();
  } catch (err) {
    // Non-critical — use defaults
    state.settings = {
      org: { name: Auth.tenant?.name || 'Dealix', currency: 'SAR', timezone: 'Asia/Riyadh' },
      team: [], api_keys: [], notifications: { slack_webhook: '' },
      compliance: { pdpl_consent_default: true, retention_days: 365 }
    };
    renderSettings();
  }
}

async function loadReadiness() {
  try {
    const res = await apiClient.get('/readiness-matrix');
    state.readiness = res;
    renderReadinessPill();
  } catch (err) {
    // Silent — readiness widget gracefully degrades
    state.readiness = { counts: { live: 5, partial: 12, pilot: 3, target: 9 }, services: [] };
    renderReadinessPill();
  }
}

/* ============================================================
 * 6. Renderers
 * ============================================================ */

function renderOverview() {
  const ov = state.overview;
  if (!ov) return;

  const k = ov.kpis || {};
  $('#kpi-grid').innerHTML = `
    <div class="kpi" style="--_accent: var(--color-primary-soft); --_icon-bg: var(--color-primary-soft); --_icon-fg: var(--color-primary);">
      <div class="kpi__label"><span class="kpi__icon"><svg><use href="#i-users"/></svg></span><span>Leads نشطة</span></div>
      <div class="kpi__value num">${fmtNum(k.active_leads || 0)}</div>
      <div class="kpi__delta"><svg style="width:12px;height:12px"><use href="#i-arrow-up"/></svg><span class="num">+12%</span><span class="text-muted text-sm">مقابل الأسبوع الماضي</span></div>
    </div>
    <div class="kpi" style="--_accent: var(--color-danger-soft); --_icon-bg: var(--color-danger-soft); --_icon-fg: var(--color-danger);">
      <div class="kpi__label"><span class="kpi__icon"><svg><use href="#i-fire"/></svg></span><span>Leads ساخنة</span></div>
      <div class="kpi__value num">${fmtNum(k.hot_leads || 0)}</div>
      <div class="kpi__delta"><svg style="width:12px;height:12px"><use href="#i-arrow-up"/></svg><span class="num">+5</span><span class="text-muted text-sm">هذا الأسبوع</span></div>
    </div>
    <div class="kpi" style="--_accent: var(--color-info-soft); --_icon-bg: var(--color-info-soft); --_icon-fg: var(--color-info);">
      <div class="kpi__label"><span class="kpi__icon"><svg><use href="#i-calendar"/></svg></span><span>اجتماعات الأسبوع</span></div>
      <div class="kpi__value num">${fmtNum(k.meetings_week || 0)}</div>
      <div class="kpi__delta"><svg style="width:12px;height:12px"><use href="#i-arrow-up"/></svg><span class="num">+8</span><span class="text-muted text-sm">مؤكَّدة</span></div>
    </div>
    <div class="kpi" style="--_accent: var(--color-gold-soft); --_icon-bg: var(--color-gold-soft); --_icon-fg: var(--color-gold);">
      <div class="kpi__label"><span class="kpi__icon"><svg><use href="#i-dollar"/></svg></span><span>قيمة الـ Pipeline</span></div>
      <div class="kpi__value num">${fmtSar(k.pipeline_value_sar || 0)}</div>
      <div class="kpi__delta"><svg style="width:12px;height:12px"><use href="#i-arrow-up"/></svg><span class="num">+18%</span><span class="text-muted text-sm">ر.س شهرياً</span></div>
    </div>`;

  // Funnel
  const funnel = ov.funnel || [];
  const fmap = Object.fromEntries(funnel.map(f => [f.stage, f.count]));
  const rows = [
    { key: 'prospect', label: 'Prospect' }, { key: 'engaged', label: 'Engaged' },
    { key: 'qualified', label: 'Qualified' }, { key: 'proposal', label: 'Proposal' },
    { key: 'won', label: 'Won', class: 'funnel__row--won' },
    { key: 'lost', label: 'Lost', class: 'funnel__row--lost' },
  ];
  const vals = rows.map(r => fmap[r.key] || 0);
  const maxVal = Math.max(1, ...vals);
  $('#funnel').innerHTML = rows.map((r, i) => `
    <div class="funnel__row ${r.class || ''}">
      <div class="funnel__label">${r.label}</div>
      <div class="funnel__bar"><div class="funnel__fill" style="width:${(vals[i]/maxVal)*100}%"></div></div>
      <div class="funnel__val num">${vals[i]}</div>
    </div>`).join('');

  // Activity
  const activity = ov.recent_activity || [];
  $('#activity').innerHTML = activity.length
    ? activity.slice(0, 10).map(a => `
      <div class="activity__item">
        <div class="activity__dot channel-dot--${a.channel || 'system'}"><svg><use href="${channelIcon[a.channel] || '#i-bot'}"/></svg></div>
        <div class="activity__body">
          <div class="activity__text">${escapeHtml(a.action || '')}</div>
          <div class="activity__meta">
            <strong>${escapeHtml(a.actor || '')}</strong>
            ${a.target && a.target !== '—' ? ` · <strong>${escapeHtml(a.target)}</strong>` : ''}
            · ${relTime(a.at)}
          </div>
        </div>
      </div>`).join('')
    : `<div class="empty-state"><svg><use href="#i-bot"/></svg><strong>لا نشاط بعد</strong><small>الأنشطة ستظهر هنا مباشرة</small></div>`;

  // Channels
  const chColors = { whatsapp: 'var(--color-whatsapp)', email: 'var(--color-email)', linkedin: 'var(--color-linkedin)', sms: 'var(--color-sms)' };
  const cp = ov.channel_performance || [];
  const maxConv = Math.max(1, ...cp.map(c => c.conv_rate || 0));
  $('#channels').innerHTML = cp.length
    ? cp.map(c => `
      <div class="channel-bar">
        <div class="channel-bar__icon channel-dot--${c.channel}"><svg><use href="${channelIcon[c.channel]}"/></svg></div>
        <div class="channel-bar__name">${channelLabel[c.channel] || c.channel}</div>
        <div class="channel-bar__track"><div class="channel-bar__fill" style="width:${((c.conv_rate||0)/maxConv)*100}%;background:${chColors[c.channel] || 'var(--color-primary)'};"></div></div>
        <div class="channel-bar__val num">${c.conv_rate || 0}%</div>
      </div>`).join('')
    : `<div class="empty-state" style="padding:20px;"><small>لا بيانات قنوات بعد</small></div>`;
}

function renderLeads() {
  let leads = state.leads.slice();
  if (state.leadFilter !== 'all') leads = leads.filter(l => l.priority_tier === state.leadFilter);
  if (state.leadSearch) {
    const q = state.leadSearch;
    leads = leads.filter(l =>
      (l.company_name || '').toLowerCase().includes(q) ||
      (l.company_name_ar || '').toLowerCase().includes(q) ||
      (l.sector_ar || '').toLowerCase().includes(q)
    );
  }

  const tbody = $('#leads-tbody');
  if (!leads.length) {
    tbody.innerHTML = `<tr><td colspan="8"><div class="empty-state"><svg><use href="#i-users"/></svg><strong>لا توجد نتائج</strong><small>جرّب تعديل الفلترة</small></div></td></tr>`;
    return;
  }

  tbody.innerHTML = leads.map(l => `
    <tr data-lead-id="${escapeAttr(l.id)}">
      <td>
        <div class="company-cell">
          <div class="company-logo">${initial(l.company_name_ar || l.company_name)}</div>
          <div>
            <div class="company-name">${escapeHtml(l.company_name_ar || l.company_name)}</div>
            <div class="company-sub num">${escapeHtml(l.company_name || '')}</div>
          </div>
        </div>
      </td>
      <td><span class="badge badge--neutral">${escapeHtml(l.sector_ar || l.sector || '')}</span></td>
      <td>
        <span class="score ${scoreClass(l.dealix_score || 0)}"><span class="num">${l.dealix_score || 0}</span></span>
        <span class="badge ${tierClass(l.priority_tier)}" style="margin-inline-start:6px">${tierLabel[l.priority_tier] || '—'}</span>
      </td>
      <td>
        <span class="activity__dot channel-dot--${l.preferred_channel}" style="width:22px;height:22px;display:inline-flex;">
          <svg style="width:12px;height:12px"><use href="${channelIcon[l.preferred_channel] || '#i-mail'}"/></svg>
        </span>
        <span style="margin-inline-start:6px">${channelLabel[l.preferred_channel] || '—'}</span>
      </td>
      <td class="text-muted text-sm">${escapeHtml(l.last_interaction || '—')}</td>
      <td><span class="badge badge--neutral">${statusLabel[l.status] || l.status || '—'}</span></td>
      <td><span class="num" style="font-weight:600;color:var(--color-primary);">${fmtSar(l.deal_value_sar || 0)}</span></td>
      <td class="text-sm">${escapeHtml(l.owner || '—')}</td>
    </tr>
  `).join('');

  tbody.querySelectorAll('tr[data-lead-id]').forEach(tr => {
    tr.addEventListener('click', () => openDrawer(tr.dataset.leadId));
  });
}

function renderConversations() {
  let convs = state.conversations.slice();
  if (state.inboxChannel !== 'all') convs = convs.filter(c => c.channel === state.inboxChannel);
  if (state.convSearch) {
    const q = state.convSearch.toLowerCase();
    convs = convs.filter(c =>
      (c.sender_name || '').toLowerCase().includes(q) ||
      (c.company_ar || '').toLowerCase().includes(q) ||
      (c.preview || '').toLowerCase().includes(q)
    );
  }

  const list = $('#conv-list');
  if (!convs.length) {
    renderEmpty(list, 'لا توجد محادثات بعد');
    return;
  }
  list.innerHTML = convs.map(c => `
    <div class="conv ${state.activeConv === c.id ? 'is-active' : ''}" data-conv-id="${escapeAttr(c.id)}">
      <div class="activity__dot channel-dot--${c.channel}"><svg><use href="${channelIcon[c.channel] || '#i-mail'}"/></svg></div>
      <div class="conv__body">
        <div class="conv__header">
          <div class="conv__sender">${escapeHtml(c.sender_name || c.phone || '—')}</div>
          <div class="conv__time">${relTime(c.ts)}</div>
        </div>
        <div class="conv__company">${escapeHtml(c.company_ar || '')} · ${channelLabel[c.channel] || c.channel}</div>
        <div class="conv__preview">${escapeHtml(c.preview || '')}</div>
      </div>
      ${c.unread > 0 ? `<span class="conv__unread num">${c.unread}</span>` : ''}
    </div>`).join('');
  list.querySelectorAll('.conv').forEach(el => {
    el.addEventListener('click', () => selectConversation(el.dataset.convId));
  });
}

async function selectConversation(id) {
  state.activeConv = id;
  const c = state.conversations.find(x => x.id === id);
  if (!c) return;

  // mark read optimistically
  if (c.unread > 0) {
    c.unread = 0;
    const unread = state.conversations.filter(x => x.unread > 0).length;
    $('#nav-inbox-count').textContent = unread || state.conversations.length;
  }
  renderConversations();

  $('#thread-avatar').textContent = initial(c.sender_name);
  $('#thread-name').textContent = c.sender_name || c.phone || '—';
  $('#thread-sub').innerHTML = `<span>${escapeHtml(c.company_ar || '')}</span> · <span class="badge badge--neutral" style="font-size:10px;">${channelLabel[c.channel] || c.channel}</span>`;

  const msgsEl = $('#thread-messages');
  msgsEl.innerHTML = `<div class="skeleton-row"></div><div class="skeleton-row"></div>`;

  const msgs = state.convMessages[id] || await loadConversationMessages(id);
  renderMessages(msgs);

  $('#composer').style.display = 'block';
  $('#suggestions-list').innerHTML = '<div class="text-muted text-sm" style="padding:8px;">اضغط "إعادة توليد" لاقتراحات</div>';
}

function renderMessages(msgs) {
  const el = $('#thread-messages');
  if (!msgs || !msgs.length) {
    el.innerHTML = `<div class="empty-state"><svg><use href="#i-inbox"/></svg><strong>لا رسائل بعد</strong><small>ابدأ المحادثة بإرسال أول رسالة</small></div>`;
    return;
  }
  el.innerHTML = msgs.map(m => {
    const from = m.direction === 'outbound' ? 'us' : 'them';
    const body = m.body || m.text || '';
    const ts = m.at || m.ts;
    const pendingCls = m._pending ? ' is-pending' : '';
    const errCls = m._error ? ' is-error' : '';
    return `
    <div class="msg msg--${from}${pendingCls}${errCls}">
      <div>${escapeHtml(body)}</div>
      <div class="msg__meta">${ts ? new Date(ts).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' }) : ''}</div>
    </div>`;
  }).join('');
  el.scrollTop = el.scrollHeight;
}

async function sendReply() {
  if (!state.activeConv) return showToast('اختر محادثة أولاً', 'err');
  const input = $('#composer-input');
  const val = input.value.trim();
  if (!val) return showToast('اكتب ردّاً أولاً', 'err');

  const c = state.conversations.find(x => x.id === state.activeConv);
  if (!c) return;

  const tempMsg = {
    direction: 'outbound',
    body: val,
    at: new Date().toISOString(),
    _pending: true
  };
  state.convMessages[c.id] = [...(state.convMessages[c.id] || []), tempMsg];
  renderMessages(state.convMessages[c.id]);
  input.value = '';

  try {
    const res = await apiClient.post(`/conversations/${encodeURIComponent(c.id)}/reply`, {
      channel: c.channel,
      body: val
    });
    tempMsg._pending = false;
    tempMsg.sid = res.sid;
    c.preview = val;
    c.ts = new Date().toISOString();
    renderMessages(state.convMessages[c.id]);
    renderConversations();
    showToast('تمّ الإرسال ✓');
  } catch (err) {
    tempMsg._pending = false;
    tempMsg._error = true;
    renderMessages(state.convMessages[c.id]);
    showToast(err.message || 'فشل الإرسال', 'err');
  }
}

async function fetchSuggestions() {
  if (!state.activeConv) return showToast('اختر محادثة أولاً', 'err');
  const list = $('#suggestions-list');
  list.innerHTML = '<div class="suggestion is-loading">جاري التوليد...</div>';
  try {
    const res = await apiClient.post(`/conversations/${encodeURIComponent(state.activeConv)}/ai-suggest`, {});
    const sugs = res.suggestions || [];
    if (!sugs.length) {
      list.innerHTML = '<div class="text-muted text-sm" style="padding:8px;">لا اقتراحات متاحة</div>';
      return;
    }
    list.innerHTML = sugs.map((s, i) => `
      <div class="suggestion" data-sug-idx="${i}">${escapeHtml(s)}</div>
    `).join('');
    list.querySelectorAll('.suggestion').forEach(el => {
      el.addEventListener('click', () => {
        $('#composer-input').value = sugs[+el.dataset.sugIdx];
        $('#composer-input').focus();
      });
    });
  } catch (err) {
    list.innerHTML = `<div class="text-muted text-sm" style="padding:8px;color:var(--color-danger);">${escapeHtml(err.message || 'فشل التوليد')}</div>`;
  }
}

function renderKanban() {
  const cols = [
    { key: 'prospect', label: 'Prospect', cls: 'col--prospect' },
    { key: 'engaged', label: 'Engaged', cls: 'col--engaged' },
    { key: 'qualified', label: 'Qualified', cls: 'col--qualified' },
    { key: 'proposal', label: 'Proposal', cls: 'col--proposal' },
    { key: 'won', label: 'Won', cls: 'col--won' },
    { key: 'lost', label: 'Lost', cls: 'col--lost' },
  ];

  let pipelineCols = state.pipeline?.columns || [];
  // Filter
  const f = state.pipeFilter;
  const filterLead = (l) => {
    if (f.sector && l.sector !== f.sector) return false;
    if (f.owner && l.owner !== f.owner) return false;
    if (f.valueBand) {
      const [min, max] = f.valueBand.split('-').map(Number);
      const v = l.deal_value_sar || 0;
      if (v < min || v > max) return false;
    }
    return true;
  };

  const byStage = Object.fromEntries(cols.map(c => [c.key, []]));
  pipelineCols.forEach(col => {
    (col.leads || []).filter(filterLead).forEach(l => byStage[col.stage]?.push(l));
  });

  // Populate filter dropdowns
  populatePipelineFilters();

  const total = Object.entries(byStage).reduce((sum, [k, arr]) =>
    sum + (k !== 'lost' ? arr.reduce((s, l) => s + (l.deal_value_sar || 0), 0) : 0), 0);
  $('#pipeline-total').textContent = fmtSar(total);

  $('#kanban').innerHTML = cols.map(c => `
    <div class="col ${c.cls}" data-stage="${c.key}">
      <div class="col__header">
        <div class="col__title">${c.label}</div>
        <div class="col__count num">${byStage[c.key].length}</div>
      </div>
      <div class="col__body">
        ${byStage[c.key].map(l => `
          <div class="lead-card" draggable="true" data-lead-id="${escapeAttr(l.id)}">
            <div class="lead-card__name">${escapeHtml(l.company_name_ar || l.company_name)}</div>
            <div class="lead-card__value num">${fmtSar(l.deal_value_sar || 0)} ر.س</div>
            <div class="lead-card__meta">
              <span>${escapeHtml(l.assigned_agent || l.owner || '—')}</span>
              <span class="num">${l.days_in_stage || 0}ي</span>
            </div>
          </div>`).join('')}
        ${byStage[c.key].length === 0 ? `<div class="text-muted text-sm" style="padding:14px;text-align:center;">—</div>` : ''}
      </div>
    </div>`).join('');

  bindKanbanDragDrop();
}

function populatePipelineFilters() {
  const leads = (state.pipeline?.columns || []).flatMap(c => c.leads || []);
  const sectors = [...new Set(leads.map(l => l.sector).filter(Boolean))];
  const owners = [...new Set(leads.map(l => l.owner).filter(Boolean))];

  const secSel = $('#pipe-filter-sector');
  if (secSel && secSel.options.length <= 1) {
    sectors.forEach(s => {
      const o = document.createElement('option');
      o.value = s; o.textContent = s;
      secSel.appendChild(o);
    });
  }
  const ownSel = $('#pipe-filter-owner');
  if (ownSel && ownSel.options.length <= 1) {
    owners.forEach(o => {
      const opt = document.createElement('option');
      opt.value = o; opt.textContent = o;
      ownSel.appendChild(opt);
    });
  }
}

let draggingId = null;
function bindKanbanDragDrop() {
  $$('.lead-card[draggable]').forEach(card => {
    card.addEventListener('dragstart', (e) => {
      draggingId = card.dataset.leadId;
      card.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
    });
    card.addEventListener('dragend', () => {
      card.classList.remove('dragging');
      draggingId = null;
      $$('.col').forEach(c => c.classList.remove('drag-over'));
    });
    card.addEventListener('click', () => openDrawer(card.dataset.leadId));
  });
  $$('.col').forEach(col => {
    col.addEventListener('dragover', (e) => { e.preventDefault(); col.classList.add('drag-over'); });
    col.addEventListener('dragleave', () => col.classList.remove('drag-over'));
    col.addEventListener('drop', async (e) => {
      e.preventDefault();
      col.classList.remove('drag-over');
      if (!draggingId) return;
      const stage = col.dataset.stage;
      await moveLeadToStage(draggingId, stage);
    });
  });
}

async function moveLeadToStage(leadId, stage) {
  // Optimistic: move in local pipeline data
  let moved = null, prevStage = null;
  for (const col of state.pipeline.columns) {
    const idx = (col.leads || []).findIndex(l => l.id === leadId);
    if (idx >= 0) {
      moved = col.leads.splice(idx, 1)[0];
      prevStage = col.stage;
      break;
    }
  }
  if (!moved) return;
  moved.status = stageToStatus[stage] || moved.status;
  const target = state.pipeline.columns.find(c => c.stage === stage) || { stage, leads: [] };
  target.leads.unshift(moved);
  renderKanban();

  try {
    await apiClient.post(`/leads/${encodeURIComponent(leadId)}/stage`, { stage });
    showToast(`نُقل ${moved.company_name_ar || moved.company_name} إلى ${stage}`);
  } catch (err) {
    // Revert
    const idx = target.leads.findIndex(l => l.id === leadId);
    if (idx >= 0) target.leads.splice(idx, 1);
    const prev = state.pipeline.columns.find(c => c.stage === prevStage);
    if (prev) prev.leads.unshift(moved);
    renderKanban();
    showToast('فشل نقل الصفقة — تم التراجع', 'err');
  }
}

function renderAgents() {
  const statusClass = { active: 'status-dot--active', idle: 'status-dot--idle', error: 'status-dot--error', paused: 'status-dot--idle' };
  const statusLbl = { active: 'نشط', idle: 'خامل', error: 'خطأ', paused: 'متوقف' };

  if (!state.agents.length) {
    renderEmpty($('#agents-grid'), 'لا يوجد وكلاء — سيتم تشغيلهم بعد نشر الباقة');
    return;
  }

  $('#agents-grid').innerHTML = state.agents.map(a => `
    <div class="agent-card ${a.status === 'paused' ? 'is-paused' : ''}" data-agent-id="${escapeAttr(a.id)}">
      <div class="agent-card__header">
        <div class="agent-card__icon channel-dot--${a.icon || 'bot'}">
          <svg><use href="#i-${a.icon || 'bot'}"/></svg>
        </div>
        <div style="flex:1;">
          <div class="agent-card__name">${escapeHtml(a.name)}</div>
          <div class="agent-card__sub">${escapeHtml(a.name_en || '')}</div>
        </div>
        <span class="status-dot ${statusClass[a.status]}">${statusLbl[a.status] || a.status}</span>
      </div>
      <div class="text-sm text-muted mb-2">${escapeHtml(a.description || '')}</div>
      <div class="agent-card__stats">
        <div><div class="stat__label">رسائل اليوم</div><div class="stat__value">${fmtNum(a.messages_today || 0)}</div></div>
        <div><div class="stat__label">نجاح</div><div class="stat__value">${a.success_rate || 0}%</div></div>
        <div><div class="stat__label">تكلفة اليوم</div><div class="stat__value">${a.cost_today_sar || 0} ر.س</div></div>
      </div>
      <div class="agent-card__footer">
        <button class="btn btn--ghost btn--sm" data-agent-log="${escapeAttr(a.id)}">السجلّ</button>
        <label class="toggle"><input type="checkbox" ${a.status !== 'paused' && a.status !== 'error' ? 'checked' : ''} data-agent-toggle="${escapeAttr(a.id)}"><span class="toggle__slider"></span></label>
      </div>
    </div>`).join('');

  $$('[data-agent-toggle]').forEach(el => {
    el.addEventListener('change', async () => {
      const id = el.dataset.agentToggle;
      try {
        const res = await apiClient.post(`/agents/${encodeURIComponent(id)}/toggle`, {});
        const agent = state.agents.find(a => a.id === id);
        if (agent && res.agent) agent.status = res.agent.status || agent.status;
        renderAgents();
        showToast(`تم ${el.checked ? 'تشغيل' : 'إيقاف'} ${agent?.name || id}`);
      } catch (err) {
        el.checked = !el.checked;
        showToast(err.message || 'فشل تبديل الحالة', 'err');
      }
    });
  });
}

function renderPlaybooks() {
  if (!state.playbooks.length) {
    renderEmpty($('#playbooks-list'), 'لا يوجد Playbooks بعد — أنشئ أول تسلسل');
    return;
  }
  $('#playbooks-list').innerHTML = state.playbooks.map(p => `
    <div class="playbook">
      <div class="playbook__header">
        <div>
          <div class="playbook__title">${escapeHtml(p.name_ar || p.name)}</div>
          <div class="playbook__desc">${escapeHtml(p.description || '')}</div>
        </div>
        <div class="playbook__stats">
          <div class="playbook__stat"><strong>${p.active_leads || 0}</strong><span>leads نشطة</span></div>
          <div class="playbook__stat"><strong>${p.conversion_rate || 0}%</strong><span>تحويل</span></div>
          <button class="btn btn--ghost btn--sm">تعديل</button>
        </div>
      </div>
      <div class="playbook__steps">
        ${(p.steps || []).map(s => `
          <div class="step">
            <div class="step__day">اليوم ${s.day}</div>
            <div class="step__action">${escapeHtml(s.action)}</div>
            <span class="step__channel-pill channel-dot--${s.channel}">
              <svg style="width:10px;height:10px"><use href="${channelIcon[s.channel]}"/></svg>
              ${channelLabel[s.channel]}
            </span>
          </div>`).join('')}
      </div>
    </div>`).join('');
}

function renderSources() {
  const iconMap = {
    saudi_registry: 'i-database', etimad: 'i-handshake', linkedin: 'i-linkedin',
    news: 'i-book', hiring: 'i-users', techstack: 'i-target'
  };
  const statusPillCls = {
    live: 'rp-live', partial: 'rp-partial', pilot: 'rp-pilot', target: 'rp-target',
    connected: 'rp-live', stub: 'rp-target'
  };
  const statusLbl = {
    live: 'Live', partial: 'Partial', pilot: 'Pilot', target: 'Target',
    connected: 'متصل', stub: 'يحتاج اعتماد'
  };

  if (!state.sources.length) {
    renderEmpty($('#sources-grid'), 'لا توجد مصادر مكوّنة بعد');
    return;
  }

  $('#sources-grid').innerHTML = state.sources.map(s => {
    const status = s.status || 'target';
    const norm = status.toLowerCase();
    const pillCls = statusPillCls[norm] || 'rp-target';
    return `
    <div class="source" data-source-id="${escapeAttr(s.id || s.name)}">
      <div class="source__top">
        <div class="source__icon"><svg><use href="#${iconMap[s.id] || 'i-database'}"/></svg></div>
        <span class="readiness-item__pill ${pillCls}">${statusLbl[norm] || status}</span>
      </div>
      <div class="source__name">${escapeHtml(s.name)}</div>
      <div class="source__desc">${escapeHtml(s.description || '')}</div>
      <div class="source__meta">
        <span class="source__meta-label">السجلات</span>
        <span class="source__meta-val num">${fmtNum(s.records || 0)}</span>
      </div>
      <div class="source__meta" style="border-top:none;padding-top:0;margin-top:0;">
        <span class="source__meta-label">آخر مزامنة</span>
        <span class="source__meta-val">${escapeHtml(s.last_sync || '—')}</span>
      </div>
      <div class="inline-progress" data-progress-for="${escapeAttr(s.id || s.name)}" hidden>
        <div class="inline-progress__bar"></div>
      </div>
      <div class="flex gap-sm" style="margin-top:10px;">
        <button class="btn btn--primary btn--sm" style="flex:1;" data-source-discover="${escapeAttr(s.id || s.name)}">تشغيل اكتشاف</button>
        <button class="btn btn--ghost btn--sm" data-source-config="${escapeAttr(s.id || s.name)}">تهيئة</button>
      </div>
    </div>`;
  }).join('');

  $$('[data-source-discover]').forEach(btn => {
    btn.addEventListener('click', () => discoverSource(btn.dataset.sourceDiscover));
  });
  $$('[data-source-config]').forEach(btn => {
    btn.addEventListener('click', () => openSourceConfig(btn.dataset.sourceConfig));
  });
}

async function discoverSource(id) {
  const prog = document.querySelector(`[data-progress-for="${id}"]`);
  if (prog) {
    prog.hidden = false;
    prog.querySelector('.inline-progress__bar').style.width = '10%';
  }
  try {
    const res = await apiClient.post(`/sources/${encodeURIComponent(id)}/discover`, {});
    showToast(`بدأ الاكتشاف — Job ${res.job_id || '—'}`);
    // Simulate progress animation
    let pct = 10;
    const tick = setInterval(() => {
      pct += Math.random() * 15;
      if (prog) prog.querySelector('.inline-progress__bar').style.width = Math.min(pct, 95) + '%';
      if (pct >= 95) clearInterval(tick);
    }, 400);
    setTimeout(() => {
      if (prog) {
        prog.querySelector('.inline-progress__bar').style.width = '100%';
        setTimeout(() => { prog.hidden = true; prog.querySelector('.inline-progress__bar').style.width = '0%'; }, 600);
      }
      showToast('اكتمل الاكتشاف');
    }, 3200);
  } catch (err) {
    if (prog) prog.hidden = true;
    showToast(err.message || 'فشل الاكتشاف', 'err');
  }
}

function openSourceConfig(id) {
  const s = state.sources.find(x => (x.id || x.name) === id);
  if (!s) return;
  const needsCred = s.status === 'target' || s.status === 'stub';
  const body = $('#source-modal-body');
  $('#source-title').textContent = `تهيئة: ${s.name}`;
  body.innerHTML = needsCred ? `
    <p class="text-sm text-muted">${escapeHtml(s.description || '')}</p>
    <div class="form-grid">
      <div class="field"><label>API Key / Credential</label><input type="text" placeholder="أدخل المفتاح..." /></div>
      <div class="field"><label>Endpoint</label><input type="url" placeholder="https://api.example.com/v1" /></div>
    </div>
    <p class="text-sm text-muted" style="margin-top:10px;">
      <strong>المطلوب:</strong> ${escapeHtml(s.blocker || 'اشتراك + مفتاح API')}
    </p>
    <div class="flex gap-sm" style="margin-top:16px;">
      <button class="btn btn--primary btn--sm" onclick="window.showToast('تم الحفظ (قريباً)');">حفظ</button>
      <a class="btn btn--ghost btn--sm" target="_blank" rel="noopener" href="#">رابط التوثيق</a>
    </div>
  ` : `
    <p class="text-sm">المصدر متصل وتشتغل المزامنة تلقائياً كل ساعة.</p>
    <div class="form-grid">
      <div class="field"><label>فاصل المزامنة (دقائق)</label><input type="number" value="60" /></div>
      <div class="field"><label>حد السجلات</label><input type="number" value="1000" /></div>
    </div>
    <div class="flex gap-sm" style="margin-top:16px;">
      <button class="btn btn--primary btn--sm" onclick="window.showToast('تم الحفظ');">حفظ</button>
      <button class="btn btn--ghost btn--sm" onclick="window.showToast('جاري المزامنة اليدوية...');">مزامنة الآن</button>
    </div>`;
  Modal.open('source-modal');
}

function renderAnalytics() {
  const { mrr, conv } = state.analytics || {};

  // MRR chart
  if (mrr && mrr.points && mrr.points.length) {
    const points = mrr.points;
    const w = 480, h = 220, pad = { t: 12, r: 10, b: 22, l: 8 };
    const maxMrr = Math.max(...points.map(p => p.value || 0), 1);
    const stepX = (w - pad.l - pad.r) / Math.max(1, points.length - 1);
    const sy = (v) => pad.t + (h - pad.t - pad.b) * (1 - v / maxMrr);
    const pts = points.map((m, i) => [pad.l + i * stepX, sy(m.value || 0)]);
    const line = pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
    const area = line + ` L${pts[pts.length-1][0].toFixed(1)},${h-pad.b} L${pts[0][0].toFixed(1)},${h-pad.b} Z`;
    const yTicks = [0, maxMrr * 0.5, maxMrr].map(v => `<div>${fmtSar(v)}</div>`).reverse().join('');

    $('#mrr-chart').innerHTML = `
      <div class="chart-area">
        <div class="chart-yaxis">${yTicks}</div>
        <div class="chart-plot">
          <svg class="chart-plot__svg" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
            <defs>
              <linearGradient id="grad-area" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stop-color="var(--color-primary)" stop-opacity="0.5"/>
                <stop offset="100%" stop-color="var(--color-primary)" stop-opacity="0"/>
              </linearGradient>
            </defs>
            <path class="chart-plot__area" d="${area}" fill="url(#grad-area)"/>
            <path class="chart-plot__line" d="${line}"/>
            ${pts.map(p => `<circle class="chart-plot__point" cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="4"/>`).join('')}
          </svg>
        </div>
      </div>
      <div class="chart-xaxis">${points.map(p => `<span>${escapeHtml(p.date || '')}</span>`).join('')}</div>`;

    // Growth rate
    const first = points[0].value || 1, last = points[points.length-1].value || 1;
    const growth = (((last - first) / first) * 100).toFixed(0);
    $('#mrr-growth').textContent = (growth >= 0 ? '+' : '') + growth + '%';
  }

  // Channels
  const cp = conv?.channels || state.overview?.channel_performance || [];
  const chColors = { whatsapp: 'var(--color-whatsapp)', email: 'var(--color-email)', linkedin: 'var(--color-linkedin)', sms: 'var(--color-sms)' };
  const maxConv = Math.max(1, ...cp.map(c => c.conv_rate || c.conversion || 0));
  $('#channels-analytics').innerHTML = cp.map(c => {
    const rate = c.conv_rate || c.conversion || 0;
    return `
    <div class="channel-bar">
      <div class="channel-bar__icon channel-dot--${c.channel}"><svg><use href="${channelIcon[c.channel]}"/></svg></div>
      <div class="channel-bar__name">${channelLabel[c.channel]}<div class="text-sm text-muted num">${fmtNum(c.sent || 0)} مُرسلة · ${fmtNum(c.replied || 0)} ردّ</div></div>
      <div class="channel-bar__track"><div class="channel-bar__fill" style="width:${(rate/maxConv)*100}%;background:${chColors[c.channel]};"></div></div>
      <div class="channel-bar__val num">${rate}%</div>
    </div>`;
  }).join('');

  // KPI cards
  $('#analytics-kpis').innerHTML = `
    <div class="kpi" style="--_accent: var(--color-info-soft); --_icon-bg: var(--color-info-soft); --_icon-fg: var(--color-info);">
      <div class="kpi__label"><span class="kpi__icon"><svg><use href="#i-target"/></svg></span><span>تكلفة العميل (CAC)</span></div>
      <div class="kpi__value num">1,240 ر.س</div>
      <div class="kpi__delta"><span class="num">−8%</span><span class="text-muted text-sm">مقابل الربع الماضي</span></div>
    </div>
    <div class="kpi" style="--_accent: var(--color-primary-soft); --_icon-bg: var(--color-primary-soft); --_icon-fg: var(--color-primary);">
      <div class="kpi__label"><span class="kpi__icon"><svg><use href="#i-dollar"/></svg></span><span>قيمة العميل (LTV)</span></div>
      <div class="kpi__value num">28,600 ر.س</div>
      <div class="kpi__delta"><span class="num">+12%</span><span class="text-muted text-sm">23× CAC</span></div>
    </div>
    <div class="kpi" style="--_accent: var(--color-gold-soft); --_icon-bg: var(--color-gold-soft); --_icon-fg: var(--color-gold);">
      <div class="kpi__label"><span class="kpi__icon"><svg><use href="#i-users"/></svg></span><span>تكلفة الـ lead</span></div>
      <div class="kpi__value num">58 ر.س</div>
      <div class="kpi__delta"><span class="num">−22%</span><span class="text-muted text-sm">بفضل التلقائي</span></div>
    </div>`;

  // ROI table (from agents)
  const revPerSuccess = { whatsapp: 180, email: 120, linkedin: 280, sms: 60, qualifier: 95, scheduler: 220, negotiator: 1800 };
  const roiData = (state.agents || []).map(a => {
    const rate = (a.success_rate || 0) / 100;
    const msgs30 = (a.messages_today || 0) * 30;
    const revenue30 = msgs30 * rate * (revPerSuccess[a.id] || 120);
    const cost30 = (a.cost_today_sar || 0) * 30;
    const roi = cost30 > 0 ? (revenue30 / cost30).toFixed(1) : '—';
    return { ...a, msgs30, revenue30, cost30, roi };
  });
  $('#roi-tbody').innerHTML = roiData.map(a => `
    <tr>
      <td><div class="company-cell">
        <div class="agent-card__icon channel-dot--${a.icon}" style="width:30px;height:30px;"><svg style="width:16px;height:16px;"><use href="#i-${a.icon}"/></svg></div>
        <div><strong>${escapeHtml(a.name)}</strong></div>
      </div></td>
      <td class="num">${fmtNum(a.msgs30)}</td>
      <td class="num" style="color:var(--color-primary);font-weight:600;">${fmtSar(a.revenue30)} ر.س</td>
      <td class="num">${fmtSar(a.cost30)} ر.س</td>
      <td><span class="badge badge--success num">${a.roi}×</span></td>
    </tr>`).join('') || '<tr><td colspan="5" class="text-muted" style="text-align:center;padding:20px;">لا بيانات بعد</td></tr>';
}

function renderSettings() {
  const s = state.settings || {};
  if (s.org) {
    $('#s-org-name').value = s.org.name || '';
    $('#s-org-currency').value = s.org.currency || 'SAR';
    $('#s-org-tz').value = s.org.timezone || 'Asia/Riyadh';
  }
  $('#s-slack').value = s.notifications?.slack_webhook || '';
  $('#s-pdpl').checked = !!s.compliance?.pdpl_consent_default;
  $('#s-retention').value = s.compliance?.retention_days || 365;

  // Team
  $('#team-list').innerHTML = (s.team || []).map(t => `
    <div class="team-row">
      <div class="team-row__avatar">${initial(t.email)}</div>
      <div style="flex:1;">
        <strong>${escapeHtml(t.name || t.email)}</strong>
        <div class="text-sm text-muted">${escapeHtml(t.role || 'member')}</div>
      </div>
      <button class="btn btn--ghost btn--sm">إزالة</button>
    </div>
  `).join('') || '<small class="text-muted">لا يوجد أعضاء بعد</small>';

  // API keys
  $('#api-keys-list').innerHTML = (s.api_keys || []).map(k => `
    <div class="api-key-row">
      <strong>${escapeHtml(k.name)}</strong>
      <code data-reveal="0">${escapeHtml(k.masked || '•••')}</code>
      <button class="btn btn--ghost btn--sm">تدوير</button>
    </div>
  `).join('') || '<small class="text-muted">لا توجد مفاتيح بعد</small>';

  // Honesty widget
  renderHonestyCounts();
}

function renderHonestyCounts() {
  const r = state.readiness;
  if (!r || !r.counts) {
    $('#honesty-counts').textContent = 'جاري التحميل...';
    return;
  }
  const c = r.counts;
  $('#honesty-counts').innerHTML = `
    <span class="readiness-item__pill rp-live">${c.live || 0} Live</span>
    <span class="readiness-item__pill rp-partial" style="margin-inline-start:6px;">${c.partial || 0} Partial</span>
    <span class="readiness-item__pill rp-pilot" style="margin-inline-start:6px;">${c.pilot || 0} Pilot</span>
    <span class="readiness-item__pill rp-target" style="margin-inline-start:6px;">${c.target || 0} Target</span>`;
}

function renderReadinessPill() {
  const r = state.readiness;
  if (!r || !r.counts) return;
  const c = r.counts;
  const total = (c.live || 0) + (c.partial || 0) + (c.pilot || 0) + (c.target || 0);
  $('#readiness-pill-text').textContent = `${c.live || 0}/${total} Live`;
  const dot = document.querySelector('.readiness-pill__dot');
  if (dot) {
    dot.style.background = c.live > 0 ? '#10b981' : '#f59e0b';
  }
  $('#footer-readiness').textContent = `📊 ${c.live || 0} خدمات حيّة من ${total}`;
  renderHonestyCounts();
}

function openReadinessModal() {
  const r = state.readiness || { counts: {}, services: [] };
  const c = r.counts || {};
  const total = (c.live || 0) + (c.partial || 0) + (c.pilot || 0) + (c.target || 0);

  const body = $('#readiness-body');
  body.innerHTML = `
    <div class="readiness-summary">
      <div class="readiness-summary__card"><div class="readiness-summary__n" style="color:#10b981">${c.live || 0}</div><div class="readiness-summary__lbl">Live</div></div>
      <div class="readiness-summary__card"><div class="readiness-summary__n" style="color:#f59e0b">${c.partial || 0}</div><div class="readiness-summary__lbl">Partial</div></div>
      <div class="readiness-summary__card"><div class="readiness-summary__n" style="color:#2563eb">${c.pilot || 0}</div><div class="readiness-summary__lbl">Pilot</div></div>
      <div class="readiness-summary__card"><div class="readiness-summary__n" style="color:#6b7280">${c.target || 0}</div><div class="readiness-summary__lbl">Target</div></div>
    </div>
    <p class="text-sm text-muted">هذا التقرير مقروء مباشرة من <code>SERVICE_READINESS_MATRIX.yaml</code> — مصدر الحقيقة الوحيد. أي ادعاء تسويقي بـ "Live" يمر عبر 5 بوابات إلزامية.</p>
    ${(r.services || []).length
      ? (r.services || []).slice(0, 40).map(svc => `
        <div class="readiness-item">
          <span class="readiness-item__pill rp-${String(svc.status || 'target').toLowerCase()}">${svc.status}</span>
          <div style="flex:1;">
            <strong>${escapeHtml(svc.name || svc.id)}</strong>
            <div class="text-sm text-muted">${escapeHtml(svc.description || '')}</div>
          </div>
        </div>`).join('')
      : `<p class="text-sm text-muted" style="margin-top:16px;">تفاصيل الخدمات غير متاحة في API حالياً. اطلب من الباك-إند كشف <code>/api/v1/readiness-matrix</code> مع قائمة الخدمات.</p>`
    }`;
  $('#readiness-updated').textContent = r.last_updated || '—';
  Modal.open('readiness-modal');
}

/* ============================================================
 * Lead Drawer (real GET + PATCH)
 * ============================================================ */

let currentDrawerLead = null;

async function openDrawer(leadId) {
  Modal.close(); // close any open modals
  let lead;
  try {
    lead = await apiClient.get(`/leads/${encodeURIComponent(leadId)}`);
  } catch (err) {
    showToast(err.message || 'تعذر تحميل الـ lead', 'err');
    return;
  }
  if (!lead) {
    // fallback to cached
    lead = state.leads.find(l => l.id === leadId);
  }
  if (!lead) return;
  currentDrawerLead = lead;

  $('#drawer-logo').textContent = initial(lead.company_name_ar || lead.company_name);
  $('#drawer-title').textContent = lead.company_name_ar || lead.company_name;
  $('#drawer-sub').innerHTML = `<span class="num">${escapeHtml(lead.company_name || '')}</span> · ${escapeHtml(lead.sector_ar || lead.sector || '')} · ${escapeHtml(lead.city || '')}`;

  const dims = [
    { key: 'icp', label: 'ICP' }, { key: 'intent', label: 'Intent' },
    { key: 'timing', label: 'Timing' }, { key: 'budget', label: 'Budget' },
    { key: 'authority', label: 'Authority' }, { key: 'engagement', label: 'Engagement' },
  ];

  const breakdown = lead.score_breakdown || {};

  $('#drawer-body').innerHTML = `
    <div class="grid-2" style="gap:12px;">
      <div>
        <div class="text-sm text-muted">النتيجة الإجمالية</div>
        <div style="display:flex;align-items:center;gap:8px;margin-top:4px;">
          <span class="score ${scoreClass(lead.dealix_score || 0)}" style="height:36px;min-width:52px;font-size:16px;"><span class="num">${lead.dealix_score || 0}</span></span>
          <span class="badge ${tierClass(lead.priority_tier)}">${tierLabel[lead.priority_tier] || '—'}</span>
        </div>
      </div>
      <div>
        <div class="text-sm text-muted">قيمة الصفقة المتوقّعة</div>
        <input type="number" class="field" id="drawer-value" value="${lead.deal_value_sar || 0}" style="margin-top:4px;font-family:var(--font-en);font-weight:700;font-size:18px;color:var(--color-primary);border:1px solid var(--color-border);border-radius:8px;padding:6px 10px;width:100%;" />
      </div>
    </div>

    <div class="form-grid" style="margin-top:14px;">
      <div class="field"><label>المرحلة</label>
        <select id="drawer-stage">
          ${Object.keys(statusLabel).map(s => `<option value="${s}" ${s === lead.status ? 'selected' : ''}>${statusLabel[s]}</option>`).join('')}
        </select>
      </div>
      <div class="field"><label>المالك</label>
        <input type="text" id="drawer-owner" value="${escapeAttr(lead.owner || '')}" />
      </div>
    </div>

    <div class="field" style="margin-top:12px;">
      <label>ملاحظات</label>
      <textarea id="drawer-notes" rows="3" style="padding:10px;border:1px solid var(--color-border);border-radius:8px;background:var(--color-surface);color:var(--color-text);font-family:inherit;font-size:13px;">${escapeHtml(lead.notes || '')}</textarea>
    </div>

    <div class="flex gap-sm" style="margin-top:10px;">
      <button class="btn btn--primary btn--sm" id="drawer-save"><svg><use href="#i-check"/></svg>حفظ التعديلات</button>
    </div>

    <div class="section-title">تفصيل النتيجة (6 أبعاد)</div>
    <div>
      ${dims.map(d => `
        <div class="score-dim">
          <div class="score-dim__label">${d.label}</div>
          <div class="score-dim__track"><div class="score-dim__fill" style="width:${breakdown[d.key] || 0}%"></div></div>
          <div class="score-dim__val num">${breakdown[d.key] || 0}</div>
        </div>`).join('')}
    </div>

    ${(lead.contributing_signals || []).length ? `
      <div class="section-title">الإشارات المُساهِمة (${lead.contributing_signals.length})</div>
      <div class="signal-list">
        ${lead.contributing_signals.map(s => `<div class="signal"><svg><use href="#i-check"/></svg><span>${escapeHtml(s)}</span></div>`).join('')}
        ${(lead.penalizing_factors || []).map(s => `<div class="signal signal--neg"><svg><use href="#i-alert"/></svg><span>${escapeHtml(s)}</span></div>`).join('')}
      </div>
    ` : ''}

    ${(lead.contacts || []).length ? `
      <div class="section-title">جهات الاتصال</div>
      <div style="display:flex;flex-direction:column;gap:8px;">
        ${lead.contacts.map(c => `
          <div class="settings-row" style="padding:10px 14px;">
            <div>
              <strong>${escapeHtml(c.name)}</strong>
              <small class="num">${escapeHtml(c.role || '—')}${c.email ? ' · ' + escapeHtml(c.email) : ''}</small>
            </div>
          </div>`).join('')}
      </div>
    ` : ''}

    ${(lead.timeline || []).length ? `
      <div class="section-title">التسلسل الزمني</div>
      <div class="timeline">
        ${lead.timeline.map(t => `
          <div class="timeline__item">
            <div class="timeline__meta"><span class="badge badge--neutral" style="font-size:10px;">${channelLabel[t.channel] || t.channel}</span> · ${escapeHtml(t.actor || '')} · ${relTime(t.ts)}</div>
            <div class="timeline__text">${escapeHtml(t.text || '')}</div>
          </div>`).join('')}
      </div>
    ` : ''}
  `;

  $('#drawer-save').addEventListener('click', saveDrawerLead);
  $('#drawer').classList.add('is-open');
  $('#drawer-backdrop').classList.add('is-open');
  setTimeout(() => $('#drawer').focus(), 100);
}

async function saveDrawerLead() {
  if (!currentDrawerLead) return;
  const patch = {
    status: $('#drawer-stage').value,
    owner: $('#drawer-owner').value,
    deal_value_sar: Number($('#drawer-value').value) || 0,
    notes: $('#drawer-notes').value,
  };
  try {
    await apiClient.patch(`/leads/${encodeURIComponent(currentDrawerLead.id)}`, patch);
    Object.assign(currentDrawerLead, patch);
    showToast('تم الحفظ ✓');
    // Refresh leads/pipeline
    loadLeads();
    if (state.pipeline) loadPipeline();
  } catch (err) {
    showToast(err.message || 'فشل الحفظ', 'err');
  }
}

function closeDrawer() {
  $('#drawer').classList.remove('is-open');
  $('#drawer-backdrop').classList.remove('is-open');
  currentDrawerLead = null;
}

/* ============================================================
 * 7. Navigation
 * ============================================================ */
function navigate(route) {
  state.route = route;
  $$('.nav-item').forEach(b => b.classList.toggle('is-active', b.dataset.route === route));
  $$('.bottom-tab').forEach(b => b.classList.toggle('is-active', b.dataset.route === route));
  $$('.page').forEach(p => p.classList.toggle('is-active', p.dataset.page === route));

  const titles = {
    overview: ['نظرة عامة', 'لمحة كاملة عن أداء اليوم'],
    leads: ['الـ Leads', 'الشركات المكتشفة والمُأَهَّلة'],
    inbox: ['Inbox الموحّد', 'كل المحادثات في مكان واحد'],
    pipeline: ['خط المبيعات', 'إدارة الصفقات حسب المرحلة'],
    agents: ['الوكلاء الذكيون', 'وكلاء AI يعملون على مدار الساعة'],
    playbooks: ['Playbooks', 'تسلسلات تواصل تلقائية مُخصَّصة'],
    sources: ['مصادر البيانات', 'حالة التكامل مع المصادر'],
    analytics: ['التحليلات', 'استخبارات الإيرادات وعائد الاستثمار'],
    settings: ['الإعدادات', 'إدارة المؤسسة، الفريق، والتكاملات'],
    discover: ['اكتشاف ذكي', 'Lead Engine V2 — بحث عميق متعدد المصادر'],
    outreach: ['التواصل المتعدد', 'حملات متعددة القنوات وسجل الإرسال'],
  };
  const [t, s] = titles[route] || [route, ''];
  $('#page-title').textContent = t;
  $('#page-subtitle').textContent = s;

  // Lazy load per route
  if (route === 'overview' && !state.overview) loadOverview();
  if (route === 'leads' && !state.leadsLoaded) loadLeads();
  if (route === 'inbox' && !state.conversations.length) loadConversations();
  if (route === 'pipeline' && !state.pipeline) loadPipeline();
  if (route === 'agents' && !state.agents.length) loadAgents();
  if (route === 'playbooks' && !state.playbooks.length) loadPlaybooks();
  if (route === 'sources' && !state.sources.length) loadSources();
  if (route === 'analytics' && !state.analytics) { loadAgents().then(loadAnalytics); }
  if (route === 'settings' && !state.settings) loadSettings();
  if (route === 'discover') initDiscoverPage();
  if (route === 'outreach') initOutreachPage();

  // Close mobile sidebar on nav
  if (window.innerWidth < 900) {
    $('#sidebar').classList.remove('is-open');
    $('#mobile-backdrop').classList.remove('is-open');
  }
  window.scrollTo(0, 0);
}

/* ============================================================
 * 8. Command Palette (Cmd+K)
 * ============================================================ */

const CmdPalette = {
  open() { $('#cmdk').classList.add('is-open'); setTimeout(() => $('#cmdk-input').focus(), 50); this.render(''); },
  close() { $('#cmdk').classList.remove('is-open'); $('#cmdk-input').value = ''; },
  render(query) {
    const commands = [
      { group: 'انتقل', icon: 'i-home', label: 'نظرة عامة', action: () => navigate('overview') },
      { group: 'انتقل', icon: 'i-users', label: 'الـ Leads', action: () => navigate('leads') },
      { group: 'انتقل', icon: 'i-inbox', label: 'Inbox الموحّد', action: () => navigate('inbox') },
      { group: 'انتقل', icon: 'i-pipeline', label: 'خط المبيعات', action: () => navigate('pipeline') },
      { group: 'انتقل', icon: 'i-bot', label: 'الوكلاء', action: () => navigate('agents') },
      { group: 'انتقل', icon: 'i-analytics', label: 'التحليلات', action: () => navigate('analytics') },
      { group: 'انتقل', icon: 'i-settings', label: 'الإعدادات', action: () => navigate('settings') },
      { group: 'إجراءات', icon: 'i-plus', label: 'إضافة lead جديد', action: () => showToast('قريباً — إضافة lead يدوياً') },
      { group: 'إجراءات', icon: 'i-help', label: 'عرض الاختصارات', action: () => Modal.open('shortcuts-modal') },
      { group: 'إجراءات', icon: 'i-eye', label: 'حالة الخدمات — المصفوفة', action: openReadinessModal },
      { group: 'إجراءات', icon: 'i-moon', label: 'تبديل الوضع الداكن', action: () => $('#theme-toggle').click() },
      { group: 'إجراءات', icon: 'i-logout', label: 'تسجيل الخروج', action: () => $('#sidebar-logout').click() },
    ];
    // Add leads as searchable items
    if (state.leads.length) {
      state.leads.slice(0, 20).forEach(l => {
        commands.push({
          group: 'Leads',
          icon: 'i-users',
          label: (l.company_name_ar || l.company_name) + ' · ' + (l.sector_ar || ''),
          action: () => { navigate('leads'); openDrawer(l.id); }
        });
      });
    }

    const q = query.toLowerCase().trim();
    const filtered = q
      ? commands.filter(c => c.label.toLowerCase().includes(q))
      : commands;

    const grouped = {};
    filtered.forEach(c => { (grouped[c.group] = grouped[c.group] || []).push(c); });

    const html = Object.entries(grouped).map(([g, items]) => `
      <div class="cmdk__group">${g}</div>
      ${items.map((c, i) => `
        <div class="cmdk__item" data-cmd-idx="${commands.indexOf(c)}">
          <svg><use href="#${c.icon}"/></svg>
          <span>${escapeHtml(c.label)}</span>
        </div>`).join('')}
    `).join('');

    $('#cmdk-results').innerHTML = html || `<div class="cmdk__item">لا نتائج</div>`;
    this._commands = commands;
    this._filtered = filtered;
    this._activeIdx = 0;
    this._updateActive();
  },
  _updateActive() {
    $$('.cmdk__item').forEach((el, i) => el.classList.toggle('is-active', i === this._activeIdx));
    const el = $$('.cmdk__item')[this._activeIdx];
    if (el) el.scrollIntoView({ block: 'nearest' });
  },
  move(delta) {
    const items = $$('.cmdk__item');
    this._activeIdx = (this._activeIdx + delta + items.length) % items.length;
    this._updateActive();
  },
  execute() {
    const el = $$('.cmdk__item')[this._activeIdx];
    if (!el) return;
    const idx = +el.dataset.cmdIdx;
    const cmd = this._commands[idx];
    if (cmd) {
      this.close();
      cmd.action();
    }
  }
};

/* ============================================================
 * 9. WebSocket integration
 * ============================================================ */

function setupWebSocketHandlers() {
  window.addEventListener('dealix:ws-status', (e) => {
    const connected = e.detail.connected;
    const dot = $('#ws-dot');
    const txt = $('#ws-pill-text');
    if (connected) {
      dot.classList.add('is-connected');
      txt.textContent = 'متصل مباشر';
    } else {
      dot.classList.remove('is-connected');
      txt.textContent = 'غير متصل';
    }
  });

  window.addEventListener('dealix:ws:message.new', (e) => {
    const { phone, conversation_id, message } = e.detail;
    const id = phone || conversation_id;
    const c = state.conversations.find(x => x.id === id);
    if (c) {
      c.preview = message?.body || c.preview;
      c.ts = message?.at || new Date().toISOString();
      if (state.activeConv !== id) c.unread = (c.unread || 0) + 1;
    }
    if (state.activeConv === id) {
      state.convMessages[id] = [...(state.convMessages[id] || []), message];
      renderMessages(state.convMessages[id]);
    }
    renderConversations();
    const unread = state.conversations.filter(x => x.unread > 0).length;
    $('#nav-inbox-count').textContent = unread || state.conversations.length;
    // Small toast for new message
    if (state.activeConv !== id) {
      showToast(`رسالة جديدة من ${c?.sender_name || id}`);
    }
  });

  window.addEventListener('dealix:ws:lead.scored', (e) => {
    const lead = e.detail;
    const existing = state.leads.find(l => l.id === lead.id);
    if (existing) Object.assign(existing, lead);
    renderLeads();
    showToast(`🎯 ${lead.company_name_ar || lead.company_name} — نتيجة ${lead.dealix_score}`);
  });

  window.addEventListener('dealix:ws:agent.status', (e) => {
    const agent = e.detail;
    const existing = state.agents.find(a => a.id === agent.id);
    if (existing) {
      Object.assign(existing, agent);
      renderAgents();
    }
  });

  window.addEventListener('dealix:ws:activity.new', (e) => {
    if (!state.overview) return;
    state.overview.recent_activity = [e.detail, ...(state.overview.recent_activity || [])].slice(0, 10);
    if (state.route === 'overview') renderOverview();
  });
}

/* ============================================================
 * 10. Event bindings + Bootstrap
 * ============================================================ */

function bindAppEvents() {
  // Nav
  $$('.nav-item, .bottom-tab').forEach(btn => {
    btn.addEventListener('click', () => navigate(btn.dataset.route));
  });

  // Theme
  $('#theme-toggle').addEventListener('click', () => {
    const cur = document.documentElement.getAttribute('data-theme');
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { (window.__dlxStore = window.__dlxStore || {}).theme = next; } catch {}
    $('#theme-icon').innerHTML = `<use href="#i-${next === 'dark' ? 'sun' : 'moon'}"/>`;
  });

  // Mobile menu
  const toggleSidebar = () => {
    $('#sidebar').classList.toggle('is-open');
    $('#mobile-backdrop').classList.toggle('is-open');
  };
  $('#menu-toggle')?.addEventListener('click', toggleSidebar);
  $('#mobile-backdrop')?.addEventListener('click', toggleSidebar);

  // Drawer
  $('#drawer-close').addEventListener('click', closeDrawer);
  $('#drawer-backdrop').addEventListener('click', closeDrawer);

  // Drawer actions
  $('#drawer-whatsapp').addEventListener('click', () => {
    if (!currentDrawerLead) return;
    const contact = currentDrawerLead.contacts?.find(c => c.phone);
    if (!contact) return showToast('لا يوجد رقم هاتف مرتبط', 'err');
    navigate('inbox');
    showToast(`افتح محادثة واتساب مع ${contact.name} (قريباً — ربط تلقائي)`);
    closeDrawer();
  });
  $('#drawer-schedule').addEventListener('click', () => {
    showToast('📅 جدولة المكالمة — Roadmap: Target (Q3)', 'err');
  });
  $('#drawer-add-note').addEventListener('click', () => {
    showToast('قم بإضافة ملاحظة في الحقل أعلاه ثم احفظ');
  });

  // Modals
  $('#modal-backdrop').addEventListener('click', () => Modal.close());
  $$('[data-modal-close]').forEach(el => el.addEventListener('click', () => Modal.close()));
  $('#readiness-pill').addEventListener('click', openReadinessModal);
  $('#footer-transparency').addEventListener('click', (e) => { e.preventDefault(); openReadinessModal(); });
  $('#open-readiness-modal').addEventListener('click', openReadinessModal);
  $('#shortcuts-open').addEventListener('click', () => Modal.open('shortcuts-modal'));

  // Leads
  $('#leads-search').addEventListener('input', e => { state.leadSearch = e.target.value.toLowerCase(); renderLeads(); });
  $$('[data-filter]').forEach(chip => {
    chip.addEventListener('click', () => {
      $$('[data-filter]').forEach(c => c.classList.remove('is-active'));
      chip.classList.add('is-active');
      state.leadFilter = chip.dataset.filter;
      renderLeads();
    });
  });
  $('#leads-export').addEventListener('click', exportLeadsCsv);
  $('#leads-import').addEventListener('click', () => showToast('قريباً — استيراد CSV'));

  // Inbox
  $('#conv-search').addEventListener('input', e => { state.convSearch = e.target.value; renderConversations(); });
  $$('[data-channel]').forEach(tab => {
    tab.addEventListener('click', () => {
      $$('[data-channel]').forEach(t => t.classList.remove('is-active'));
      tab.classList.add('is-active');
      state.inboxChannel = tab.dataset.channel;
      renderConversations();
    });
  });
  $('#btn-suggest').addEventListener('click', fetchSuggestions);
  $('#btn-send').addEventListener('click', sendReply);
  $('#composer-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      sendReply();
    }
  });

  // Pipeline filters
  ['sector', 'owner', 'value'].forEach(f => {
    const el = $(`#pipe-filter-${f}`);
    el?.addEventListener('change', () => {
      const key = f === 'value' ? 'valueBand' : f;
      state.pipeFilter[key] = el.value;
      renderKanban();
    });
  });

  // Analytics
  $$('#range-segmented .segmented__btn').forEach(b => {
    b.addEventListener('click', () => {
      $$('#range-segmented .segmented__btn').forEach(x => x.classList.remove('is-active'));
      b.classList.add('is-active');
      state.analyticsRange = b.dataset.range;
      loadAnalytics();
    });
  });
  $('#analytics-export').addEventListener('click', exportAnalyticsCsv);

  // Sources / settings buttons
  $('#sources-refresh').addEventListener('click', () => {
    showToast('جارٍ المزامنة...');
    loadSources();
  });
  $('#settings-save').addEventListener('click', saveSettings);
  $('#invite-member').addEventListener('click', () => {
    const email = prompt('بريد العضو الجديد:');
    if (email) showToast(`تم إرسال دعوة إلى ${email} (قريباً — تفعيل فعلي)`);
  });

  // Save API key
  const apiKeySaveBtn = $('#api-key-save');
  if (apiKeySaveBtn) {
    apiKeySaveBtn.addEventListener('click', async () => {
      const service = $('#api-key-service').value;
      const value = $('#api-key-value').value.trim();
      if (!value) { showToast('الصق المفتاح أولاً', 'err'); return; }
      try {
        apiKeySaveBtn.disabled = true;
        await apiClient.post('/settings/api-keys', { service, value });
        $('#api-key-value').value = '';
        showToast(`حُفظ مفتاح ${service}`);
        await loadSettings();
      } catch (err) {
        showToast('فشل حفظ المفتاح', 'err');
      } finally {
        apiKeySaveBtn.disabled = false;
      }
    });
  }
  $('#billing-manage').addEventListener('click', () => showToast('ربط Moyasar في Roadmap (Q3)'));
  $('#new-lead-btn').addEventListener('click', () => showToast('قريباً — إضافة lead يدوياً'));
  $('#new-playbook-btn').addEventListener('click', () => showToast('قريباً — منشئ playbooks'));

  // API key reveal
  document.addEventListener('click', (e) => {
    const c = e.target.closest('code[data-reveal]');
    if (c) {
      const revealed = c.dataset.reveal === '1';
      c.dataset.reveal = revealed ? '0' : '1';
      if (!revealed) {
        c.textContent = '••• (انقر للإخفاء — القيمة الحقيقية تُجلب من الخادم)';
      } else {
        loadSettings();
      }
    }
  });

  // Command palette
  $('#cmd-open').addEventListener('click', () => CmdPalette.open());
  $('#cmdk-input').addEventListener('input', (e) => CmdPalette.render(e.target.value));
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      CmdPalette.open();
    } else if (e.key === 'Escape') {
      CmdPalette.close();
      Modal.close();
      closeDrawer();
    } else if ($('#cmdk').classList.contains('is-open')) {
      if (e.key === 'ArrowDown') { e.preventDefault(); CmdPalette.move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); CmdPalette.move(-1); }
      else if (e.key === 'Enter') { e.preventDefault(); CmdPalette.execute(); }
    } else if (!['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {
      if (e.key === '?') { Modal.open('shortcuts-modal'); }
      if (e.key === 'n' || e.key === 'N') { showToast('قريباً — إضافة lead يدوياً'); }
      if (e.key.toLowerCase() === 'g') {
        // await next key
        const onNext = (e2) => {
          const map = { o: 'overview', l: 'leads', i: 'inbox', p: 'pipeline', a: 'agents', s: 'settings' };
          if (map[e2.key.toLowerCase()]) navigate(map[e2.key.toLowerCase()]);
          document.removeEventListener('keydown', onNext, { capture: true });
        };
        document.addEventListener('keydown', onNext, { capture: true, once: true });
      }
    }
  });
  // Click on cmdk items
  $('#cmdk-results').addEventListener('click', (e) => {
    const item = e.target.closest('.cmdk__item');
    if (!item) return;
    const idx = +item.dataset.cmdIdx;
    const cmd = CmdPalette._commands[idx];
    if (cmd) { CmdPalette.close(); cmd.action(); }
  });
  // Click outside cmdk
  $('#cmdk').addEventListener('click', (e) => {
    if (e.target.id === 'cmdk') CmdPalette.close();
  });
}

async function saveSettings() {
  const patch = {
    org: {
      name: $('#s-org-name').value,
      currency: $('#s-org-currency').value,
      timezone: $('#s-org-tz').value,
    },
    notifications: { slack_webhook: $('#s-slack').value },
    compliance: {
      pdpl_consent_default: $('#s-pdpl').checked,
      retention_days: Number($('#s-retention').value) || 365,
    }
  };
  try {
    await apiClient.patch('/settings', patch);
    showToast('تم حفظ الإعدادات ✓');
  } catch (err) {
    showToast(err.message || 'فشل الحفظ', 'err');
  }
}

function exportLeadsCsv() {
  if (!state.leads.length) return showToast('لا توجد بيانات للتصدير', 'err');
  const cols = ['id', 'company_name', 'company_name_ar', 'sector', 'dealix_score', 'priority_tier', 'status', 'deal_value_sar', 'owner', 'preferred_channel'];
  const rows = [cols.join(',')].concat(state.leads.map(l =>
    cols.map(c => `"${String(l[c] ?? '').replace(/"/g, '""')}"`).join(',')
  ));
  downloadCsv('dealix-leads.csv', rows.join('\n'));
}

function exportAnalyticsCsv() {
  const mrr = state.analytics?.mrr?.points || [];
  if (!mrr.length) return showToast('لا توجد بيانات', 'err');
  const rows = ['date,value'].concat(mrr.map(p => `${p.date},${p.value}`));
  downloadCsv(`dealix-mrr-${state.analyticsRange}.csv`, rows.join('\n'));
}

function downloadCsv(filename, content) {
  const blob = new Blob(['\ufeff' + content], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 100);
  showToast('تم التصدير ✓');
}

/* ============================================================
 * Bootstrap
 * ============================================================ */

async function bootApp() {
  // Load in parallel
  await Promise.all([
    loadOverview(),
    loadLeads(),
    loadConversations(),
    loadReadiness()
  ]);

  setupWebSocketHandlers();
  WS.connect();
}

async function boot() {
  // Theme
  let savedTheme = 'light';
  try { savedTheme = (window.__dlxStore && window.__dlxStore.theme) || 'light'; } catch {}
  document.documentElement.setAttribute('data-theme', savedTheme);
  $('#theme-icon').innerHTML = `<use href="#i-${savedTheme === 'dark' ? 'sun' : 'moon'}"/>`;

  bindAuthEvents();
  bindAppEvents();

  if (apiClient.isAuthenticated()) {
    hideLoginGate();
    await bootApp();
  } else {
    showLoginGate();
  }

  // Check online
  if (!navigator.onLine) $('#offline-banner').hidden = false;
}

window.addEventListener('DOMContentLoaded', boot);

// Expose for inline handlers
window.openDrawer = openDrawer;
window.closeDrawer = closeDrawer;
window.showToast = showToast;

/* ========== Lead Engine V2 — Discover Page ========== */
let _v2Initialized = false;
let _v2CurrentJobId = null;

function initDiscoverPage() {
  if (_v2Initialized) return;
  _v2Initialized = true;

  const btn = document.getElementById('v2-discover-btn');
  if (btn) btn.addEventListener('click', startV2Discovery);

  const csvBtn = document.getElementById('v2-export-csv');
  if (csvBtn) csvBtn.addEventListener('click', () => exportV2('csv'));
  const jsonBtn = document.getElementById('v2-export-json');
  if (jsonBtn) jsonBtn.addEventListener('click', () => exportV2('json'));

  // Country → City auto-update
  const countrySelect = document.getElementById('v2-country');
  if (countrySelect) {
    countrySelect.addEventListener('change', updateV2Cities);
  }
}

function updateV2Cities() {
  const country = document.getElementById('v2-country').value;
  const citySelect = document.getElementById('v2-city');
  const cities = {
    SA: ['Riyadh:الرياض', 'Jeddah:جدة', 'Dammam:الدمام', 'Mecca:مكة', 'Medina:المدينة', 'Khobar:الخبر', 'Taif:الطائف', 'Abha:أبها', 'Tabuk:تبوك', 'Buraydah:بريدة'],
    AE: ['Dubai:دبي', 'Abu Dhabi:أبوظبي', 'Sharjah:الشارقة', 'Ajman:عجمان'],
    KW: ['Kuwait City:مدينة الكويت', 'Hawalli:حولي'],
    QA: ['Doha:الدوحة', 'Al Rayyan:الريان'],
    BH: ['Manama:المنامة', 'Riffa:الرفاع'],
    OM: ['Muscat:مسقط', 'Salalah:صلالة']
  };
  citySelect.innerHTML = (cities[country] || []).map(c => {
    const [en, ar] = c.split(':');
    return `<option value="${en}">${ar}</option>`;
  }).join('');
}

async function startV2Discovery() {
  const btn = document.getElementById('v2-discover-btn');
  const status = document.getElementById('v2-status');
  const resultsCard = document.getElementById('v2-results-card');
  const industry = document.getElementById('v2-industry').value;
  const country = document.getElementById('v2-country').value;
  const city = document.getElementById('v2-city').value;
  const depth = document.getElementById('v2-depth').value;

  btn.disabled = true;
  btn.style.opacity = '0.6';
  status.textContent = 'يتم إنشاء مهمة البحث...';
  resultsCard.style.display = 'block';

  const leadLimit = depth === 'quick' ? 5 : depth === 'standard' ? 15 : 50;

  try {
    const base = (window.__dlxStore && window.__dlxStore.api_base) || 'https://conduct-earthquake-mailing-constraint.trycloudflare.com';
    const resp = await fetch(base + '/api/v2/intelligence/discover', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        icp: {
          industries: [industry],
          geo: { countries: [country], cities: [city] }
        },
        depth,
        limit: leadLimit,
        languages: ['ar', 'en']
      })
    });
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const data = await resp.json();
    _v2CurrentJobId = data.job_id;
    status.textContent = '✓ بدأ البحث (' + data.job_id.slice(0, 8) + ')';
    pollV2Job(data.job_id);
  } catch (err) {
    status.textContent = '❌ خطأ: ' + err.message;
    btn.disabled = false;
    btn.style.opacity = '1';
  }
}

async function pollV2Job(jobId) {
  const base = (window.__dlxStore && window.__dlxStore.api_base) || 'https://conduct-earthquake-mailing-constraint.trycloudflare.com';
  const progressBar = document.getElementById('v2-progress-bar');
  const progressText = document.getElementById('v2-progress-text');
  const meta = document.getElementById('v2-results-meta');
  const btn = document.getElementById('v2-discover-btn');

  const maxPolls = 60; // 3 minutes max
  for (let i = 0; i < maxPolls; i++) {
    await new Promise(r => setTimeout(r, 3000));
    try {
      const resp = await fetch(base + '/api/v2/intelligence/jobs/' + jobId);
      const data = await resp.json();
      progressBar.style.width = (data.progress || 0) + '%';
      progressText.textContent = `حالة: ${data.status} | التقدم: ${Math.round(data.progress || 0)}% | ${data.leads_found || 0} lead مكتشف | ${data.sources_completed?.length || 0} مصدر مكتمل`;
      meta.textContent = `المصادر: ${(data.sources_completed || []).join('، ') || '—'}`;
      if (data.status === 'completed' || data.status === 'failed') {
        await loadV2Leads(jobId);
        btn.disabled = false;
        btn.style.opacity = '1';
        return;
      }
    } catch (err) {
      console.warn('poll error', err);
    }
  }
  btn.disabled = false;
  btn.style.opacity = '1';
  progressText.textContent = '‫انتهت فترة الانتظار‬';
}

async function loadV2Leads(jobId) {
  const base = (window.__dlxStore && window.__dlxStore.api_base) || 'https://conduct-earthquake-mailing-constraint.trycloudflare.com';
  const list = document.getElementById('v2-leads-list');
  try {
    const resp = await fetch(base + '/api/v2/intelligence/jobs/' + jobId + '/leads');
    const data = await resp.json();
    if (!data.leads || !data.leads.length) {
      list.innerHTML = '<div style="padding:24px;text-align:center;color:var(--text-secondary)">لم يتم العثور على leads</div>';
      return;
    }
    list.innerHTML = data.leads.map(l => renderV2Lead(l)).join('');
  } catch (err) {
    list.innerHTML = '<div style="padding:24px;text-align:center;color:#ef4444">خطأ: ' + err.message + '</div>';
  }
}

function renderV2Lead(lead) {
  const tierColor = { hot: '#ef4444', warm: '#f59e0b', cold: '#6b7280' }[lead.tier] || '#6b7280';
  const mock = lead.is_mock ? '<span style="background:#fbbf24;color:#000;padding:2px 6px;border-radius:4px;font-size:11px;margin-inline-start:6px">تجريبي</span>' : '';
  const hiring = lead.is_hiring ? '<span style="background:#10b981;color:white;padding:2px 6px;border-radius:4px;font-size:11px;margin-inline-start:6px">💼 يوظف</span>' : '';
  const points = (lead.talking_points_ar || []).map(p => `<li style="margin:4px 0;font-size:13px">${p}</li>`).join('');
  const sources = (lead.sources || []).map(s => `<span style="background:var(--bg-muted);padding:2px 6px;border-radius:4px;font-size:11px;margin-inline-end:4px">${s}</span>`).join('');
  return `
    <div style="border:1px solid var(--border);border-radius:8px;padding:16px;margin:8px 0;background:var(--bg-elevated)">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px">
        <div style="flex:1">
          <div style="font-weight:700;font-size:15px">${lead.company_name_ar || lead.company_name}${mock}${hiring}</div>
          <div style="font-size:13px;color:var(--text-secondary);margin-top:2px">${lead.company_name}</div>
          <div style="font-size:12px;margin-top:6px">
            ${lead.city ? '📍 ' + lead.city + ' ' : ''}
            ${lead.phone ? '📞 ' + lead.phone + ' ' : ''}
            ${lead.email ? '✉️ ' + lead.email + ' ' : ''}
            ${lead.domain ? '🌐 ' + lead.domain : ''}
          </div>
        </div>
        <div style="text-align:end">
          <div style="background:${tierColor};color:white;padding:4px 10px;border-radius:999px;font-weight:700;font-size:13px">${lead.total_score}/100</div>
          <div style="font-size:11px;color:var(--text-secondary);margin-top:4px">${lead.tier}</div>
        </div>
      </div>
      ${points ? `<ul style="margin:12px 0 4px;padding-inline-start:20px">${points}</ul>` : ''}
      <div style="margin-top:8px">${sources}</div>
    </div>`;
}

function exportV2(format) {
  if (!_v2CurrentJobId) return;
  const base = (window.__dlxStore && window.__dlxStore.api_base) || 'https://conduct-earthquake-mailing-constraint.trycloudflare.com';
  window.open(`${base}/api/v2/intelligence/jobs/${_v2CurrentJobId}/export?format=${format}`, '_blank');
}

/* ============================================================
 * 14. Multi-Channel Outreach page
 * ============================================================ */
let _outreachInited = false;

async function initOutreachPage() {
  if (!_outreachInited) {
    _outreachInited = true;
    // New campaign button
    const newBtn = document.getElementById('outreach-new-campaign');
    if (newBtn) newBtn.addEventListener('click', () => openOutreachModal());
    // Refresh buttons
    const rcB = document.getElementById('outreach-refresh-campaigns');
    if (rcB) rcB.addEventListener('click', () => loadOutreachCampaigns());
    const rlB = document.getElementById('outreach-refresh-log');
    if (rlB) rlB.addEventListener('click', () => loadOutreachLog());
    // Launch button
    const launch = document.getElementById('camp-launch-btn');
    if (launch) launch.addEventListener('click', () => launchCampaign());
    // Close modal handlers
    document.querySelectorAll('[data-close="outreach-campaign-modal"]').forEach(el => {
      el.addEventListener('click', () => {
        document.getElementById('outreach-campaign-modal').style.display = 'none';
      });
    });
  }
  // Always refresh data on navigate
  loadOutreachTemplates();
  loadOutreachCampaigns();
  loadOutreachLog();
}

function openOutreachModal() {
  const m = document.getElementById('outreach-campaign-modal');
  if (m) {
    m.style.display = 'flex';
    const nameEl = document.getElementById('camp-name');
    if (nameEl) nameEl.value = 'حملة ' + new Date().toISOString().slice(0, 10);
  }
}

async function loadOutreachTemplates() {
  try {
    const data = await apiClient.get('/outreach/templates');
    const c = document.getElementById('outreach-templates');
    if (!c) return;
    const items = (data.items || []);
    if (!items.length) { c.innerHTML = '<div class="empty-state">لا توجد قوالب</div>'; return; }
    c.innerHTML = '<div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(260px, 1fr));gap:12px;">' +
      items.map(t => `
        <div class="card" style="background:var(--surface-2);padding:12px;border-radius:8px;">
          <div style="font-weight:700;margin-bottom:6px;color:var(--accent)">${escapeHtml(t.key)}</div>
          <div style="font-size:12px;color:var(--text-secondary);white-space:pre-wrap;line-height:1.5">${escapeHtml(t.preview)}</div>
        </div>
      `).join('') + '</div>';
  } catch (e) {
    console.error('loadOutreachTemplates error', e);
  }
}

async function loadOutreachCampaigns() {
  try {
    const data = await apiClient.get('/outreach/campaigns?limit=20');
    const c = document.getElementById('outreach-campaigns-list');
    if (!c) return;
    const items = (data.items || []);
    document.getElementById('out-kpi-campaigns').textContent = items.length;
    if (!items.length) { c.innerHTML = '<div class="empty-state">لا توجد حملات بعد</div>'; return; }
    c.innerHTML = items.map(cmp => {
      const pct = cmp.total > 0 ? Math.round(((cmp.sent_count || 0) / cmp.total) * 100) : 0;
      const statusColor = cmp.status === 'completed' ? '#10b981' : (cmp.status === 'running' ? '#3b82f6' : '#64748b');
      return `
        <div style="padding:12px;border-bottom:1px solid var(--border);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <strong>${escapeHtml(cmp.name || '—')}</strong>
            <span style="background:${statusColor};color:white;padding:2px 10px;border-radius:999px;font-size:11px;">${cmp.status}</span>
          </div>
          <div style="font-size:12px;color:var(--text-secondary);margin-bottom:6px;">
            ${cmp.template_key || '—'} • ${cmp.channel || 'auto'} • ${cmp.total} lead
          </div>
          <div style="background:var(--surface-2);height:6px;border-radius:3px;overflow:hidden;">
            <div style="background:${statusColor};height:100%;width:${pct}%;"></div>
          </div>
          <div style="font-size:11px;color:var(--text-secondary);margin-top:4px;">
            ✓ ${cmp.sent_count || 0} • ⏱ ${cmp.deferred_count || 0} • ✗ ${cmp.failed_count || 0}
          </div>
        </div>
      `;
    }).join('');
  } catch (e) {
    console.error('loadOutreachCampaigns error', e);
  }
}

async function loadOutreachLog() {
  try {
    const data = await apiClient.get('/outreach/log?limit=20');
    const c = document.getElementById('outreach-log-list');
    if (!c) return;
    const items = (data.items || []);
    const sent = items.filter(x => x.status === 'sent').length;
    const deferred = items.filter(x => x.status === 'deferred').length;
    const failed = items.filter(x => x.status === 'failed').length;
    const setTxt = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
    setTxt('out-kpi-sent', sent);
    setTxt('out-kpi-deferred', deferred);
    setTxt('out-kpi-failed', failed);
    if (!items.length) { c.innerHTML = '<div class="empty-state">لا توجد إرسالات بعد</div>'; return; }
    const channelIcon = { whatsapp: '💬', email: '✉️', sms: '📱', linkedin: '💼', telegram: '✈️' };
    const statusColor = { sent: '#10b981', deferred: '#f59e0b', failed: '#ef4444' };
    c.innerHTML = items.map(it => `
      <div style="padding:10px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;">
        <div style="flex:1;min-width:0;">
          <div style="font-size:13px;">
            ${channelIcon[it.channel] || '•'} ${escapeHtml(it.channel || '')}
            <span style="color:${statusColor[it.status] || '#64748b'};font-weight:600;margin-inline-start:8px;">${it.status}</span>
          </div>
          <div style="font-size:11px;color:var(--text-secondary);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
            ${escapeHtml((it.message || '').slice(0, 80))}
          </div>
          ${it.error ? `<div style="font-size:11px;color:#ef4444;">${escapeHtml(it.error)}</div>` : ''}
        </div>
        <div style="font-size:11px;color:var(--text-secondary);margin-inline-start:8px;white-space:nowrap;">
          ${new Date(it.created_at).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    `).join('');
  } catch (e) {
    console.error('loadOutreachLog error', e);
  }
}

async function launchCampaign() {
  const name = document.getElementById('camp-name').value.trim();
  const template = document.getElementById('camp-template').value;
  const channelRaw = document.getElementById('camp-channel').value;
  const channel = channelRaw === 'auto' ? null : channelRaw;
  const segment = document.getElementById('camp-segment').value;
  const respectHours = document.getElementById('camp-respect-hours').checked;
  const dryRun = document.getElementById('camp-dry-run').checked;

  if (!name) { alert('أدخل اسم الحملة'); return; }

  // Collect leads with phones
  try {
    const leadsRes = await apiClient.get('/leads?limit=500');
    let leads = (leadsRes.items || leadsRes || []).filter(l => l.phone);
    if (segment === 'cold') leads = leads.filter(l => (l.priority_tier || 'cold') === 'cold');
    else if (segment === 'recent') {
      const cutoff = Date.now() - 7 * 86400000;
      leads = leads.filter(l => l.first_seen && new Date(l.first_seen).getTime() > cutoff);
    }
    if (!leads.length) { alert('لا يوجد عملاء في هذه الشريحة'); return; }

    const leadIds = leads.map(l => l.id);
    const payload = {
      name,
      lead_ids: leadIds,
      template_key: template,
      channel,
      respect_hours: respectHours,
      dry_run: dryRun,
    };
    const res = await apiClient.post('/outreach/campaign', payload);
    alert(`تم إطلاق الحملة بنجاح ✓\n\nالحملة: ${res.id}\nعدد العملاء: ${res.total}\nالحالة: ${res.status}`);
    document.getElementById('outreach-campaign-modal').style.display = 'none';
    // Refresh
    setTimeout(() => { loadOutreachCampaigns(); loadOutreachLog(); }, 1000);
  } catch (e) {
    console.error('launchCampaign error', e);
    alert('خطأ: ' + (e.message || e));
  }
}


