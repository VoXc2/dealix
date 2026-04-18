/* ========== Dealix Dashboard — Single-page application ========== */

const state = {
  data: null,
  route: 'overview',
  leadFilter: 'all',
  leadSearch: '',
  inboxChannel: 'all',
  activeConv: null,
};

/* ---------- Utilities ---------- */

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

const fmtNum = (n) => new Intl.NumberFormat('en-US').format(n);
const fmtSar = (n) => {
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

/* ---------- Boot ---------- */

// In-memory theme storage (iframe/sandbox friendly)
const memStore = {};
const safeStorage = {
  get(k) { return memStore[k] || null; },
  set(k, v) { memStore[k] = v; }
};

async function boot() {
  // Theme
  const savedTheme = safeStorage.get('dealix-theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon();

  // Simulated mock API delay
  await new Promise(r => setTimeout(r, 220));

  try {
    const res = await fetch('./data/mock.json');
    state.data = await res.json();
  } catch (e) {
    console.error('Failed to load mock data', e);
    return;
  }

  bindEvents();
  renderAll();
}

function bindEvents() {
  // Nav
  $$('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => navigate(btn.dataset.route));
  });

  // Theme toggle
  $('#theme-toggle').addEventListener('click', () => {
    const cur = document.documentElement.getAttribute('data-theme');
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    safeStorage.set('dealix-theme', next);
    updateThemeIcon();
  });

  // Mobile menu
  const toggleSidebar = () => {
    $('#sidebar').classList.toggle('is-open');
    $('#mobile-backdrop').classList.toggle('is-open');
  };
  $('#menu-toggle').addEventListener('click', toggleSidebar);
  $('#mobile-backdrop').addEventListener('click', toggleSidebar);

  // Drawer
  $('#drawer-backdrop').addEventListener('click', closeDrawer);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrawer(); });

  // Leads search/filter
  $('#leads-search').addEventListener('input', e => {
    state.leadSearch = e.target.value.toLowerCase();
    renderLeads();
  });
  $$('[data-filter]').forEach(chip => {
    chip.addEventListener('click', () => {
      $$('[data-filter]').forEach(c => c.classList.remove('is-active'));
      chip.classList.add('is-active');
      state.leadFilter = chip.dataset.filter;
      renderLeads();
    });
  });

  // Channel tabs
  $$('[data-channel]').forEach(tab => {
    tab.addEventListener('click', () => {
      $$('[data-channel]').forEach(t => t.classList.remove('is-active'));
      tab.classList.add('is-active');
      state.inboxChannel = tab.dataset.channel;
      renderConversations();
    });
  });

  // AI suggest button
  $('#btn-suggest').addEventListener('click', () => {
    if (!state.activeConv) return showToast('اختر محادثة أولاً');
    renderSuggestions();
    showToast('تمّ توليد 3 اقتراحات');
  });
}

function updateThemeIcon() {
  const theme = document.documentElement.getAttribute('data-theme');
  $('#theme-icon').innerHTML = `<use href="#i-${theme === 'dark' ? 'sun' : 'moon'}"/>`;
}

/* ---------- Navigation ---------- */

function navigate(route) {
  state.route = route;
  $$('.nav-item').forEach(b => b.classList.toggle('is-active', b.dataset.route === route));
  $$('.page').forEach(p => p.classList.toggle('is-active', p.dataset.page === route));

  const titles = {
    overview: ['نظرة عامة', 'لمحة كاملة عن أداء اليوم — 18 أبريل 2026'],
    leads: ['الـ Leads', '30 شركة مُكتشفة من 5 مصادر بيانات'],
    inbox: ['Inbox الموحّد', 'كل المحادثات في مكان واحد'],
    pipeline: ['خط المبيعات', 'إدارة الصفقات حسب المرحلة'],
    agents: ['الوكلاء الذكيون', '7 وكلاء AI يعملون على مدار الساعة'],
    playbooks: ['Playbooks', '3 تسلسلات تواصل تلقائية مُخصَّصة'],
    sources: ['مصادر البيانات', 'حالة التكامل مع المصادر السعودية والعالمية'],
    analytics: ['التحليلات', 'استخبارات الإيرادات وعائد الاستثمار'],
    settings: ['الإعدادات', 'إدارة المؤسسة، الفريق، والتكاملات'],
  };
  const [t, s] = titles[route] || [route, ''];
  $('#page-title').textContent = t;
  $('#page-subtitle').textContent = s;

  // Close mobile sidebar on nav
  if (window.innerWidth < 900) {
    $('#sidebar').classList.remove('is-open');
    $('#mobile-backdrop').classList.remove('is-open');
  }
  window.scrollTo(0, 0);
}

/* ---------- Render all ---------- */

function renderAll() {
  renderOverview();
  renderLeads();
  renderInbox();
  renderKanban();
  renderAgents();
  renderPlaybooks();
  renderSources();
  renderAnalytics();
  $('#nav-leads-count').textContent = state.data.leads.length;
  $('#nav-inbox-count').textContent = state.data.conversations.filter(c => c.unread > 0).length;
}

/* ---------- Overview ---------- */

function renderOverview() {
  const k = state.data.kpis;
  $('#kpi-active').textContent = fmtNum(k.active_leads);
  $('#kpi-hot').textContent = fmtNum(k.hot_leads);
  $('#kpi-meetings').textContent = fmtNum(k.meetings_this_week);
  $('#kpi-pipeline').textContent = fmtSar(k.pipeline_value_sar);

  // Funnel
  const f = state.data.funnel;
  const maxVal = Math.max(f.prospect, f.engaged, f.qualified, f.proposal, f.won, f.lost);
  const funnelRows = [
    { key: 'prospect', label: 'Prospect', val: f.prospect, class: '' },
    { key: 'engaged', label: 'Engaged', val: f.engaged, class: '' },
    { key: 'qualified', label: 'Qualified', val: f.qualified, class: '' },
    { key: 'proposal', label: 'Proposal', val: f.proposal, class: '' },
    { key: 'won', label: 'Won', val: f.won, class: 'funnel__row--won' },
    { key: 'lost', label: 'Lost', val: f.lost, class: 'funnel__row--lost' },
  ];
  $('#funnel').innerHTML = funnelRows.map(r => `
    <div class="funnel__row ${r.class}">
      <div class="funnel__label">${r.label}</div>
      <div class="funnel__bar"><div class="funnel__fill" style="width:${(r.val/maxVal)*100}%"></div></div>
      <div class="funnel__val num">${r.val}</div>
    </div>
  `).join('');

  // Activity
  $('#activity').innerHTML = state.data.activity_feed.map(a => `
    <div class="activity__item">
      <div class="activity__dot channel-dot--${a.channel}">
        <svg><use href="${channelIcon[a.channel] || '#i-bot'}"/></svg>
      </div>
      <div class="activity__body">
        <div class="activity__text">${escapeHtml(a.text)}</div>
        <div class="activity__meta">
          <strong>${escapeHtml(a.actor)}</strong>
          ${a.lead !== '—' ? ` · <strong>${escapeHtml(a.lead)}</strong>` : ''}
          · ${relTime(a.ts)}
        </div>
      </div>
    </div>
  `).join('');

  // Channels
  const chColors = {
    whatsapp: 'var(--color-whatsapp)', email: 'var(--color-email)',
    linkedin: 'var(--color-linkedin)', sms: 'var(--color-sms)'
  };
  const maxConv = Math.max(...state.data.channels_performance.map(c => c.conversion));
  $('#channels').innerHTML = state.data.channels_performance.map(c => `
    <div class="channel-bar">
      <div class="channel-bar__icon channel-dot--${c.channel}">
        <svg><use href="${channelIcon[c.channel]}"/></svg>
      </div>
      <div class="channel-bar__name">${channelLabel[c.channel]}</div>
      <div class="channel-bar__track">
        <div class="channel-bar__fill" style="width:${(c.conversion/maxConv)*100}%;background:${chColors[c.channel]};"></div>
      </div>
      <div class="channel-bar__val num">${c.conversion}%</div>
    </div>
  `).join('');
}

/* ---------- Leads ---------- */

function renderLeads() {
  let leads = state.data.leads.slice();
  if (state.leadFilter !== 'all') leads = leads.filter(l => l.priority_tier === state.leadFilter);
  if (state.leadSearch) {
    const q = state.leadSearch;
    leads = leads.filter(l =>
      l.company_name.toLowerCase().includes(q) ||
      (l.company_name_ar || '').toLowerCase().includes(q) ||
      (l.sector_ar || '').toLowerCase().includes(q)
    );
  }

  $('#leads-tbody').innerHTML = leads.map(l => `
    <tr onclick="openDrawer('${l.id}')">
      <td>
        <div class="company-cell">
          <div class="company-logo">${initial(l.company_name_ar)}</div>
          <div>
            <div class="company-name">${escapeHtml(l.company_name_ar)}</div>
            <div class="company-sub num">${escapeHtml(l.company_name)}</div>
          </div>
        </div>
      </td>
      <td><span class="badge badge--neutral">${escapeHtml(l.sector_ar)}</span></td>
      <td>
        <span class="score ${scoreClass(l.dealix_score)}"><span class="num">${l.dealix_score}</span></span>
        <span class="badge ${tierClass(l.priority_tier)}" style="margin-inline-start:6px">${tierLabel[l.priority_tier]}</span>
      </td>
      <td>
        <span class="activity__dot channel-dot--${l.preferred_channel}" style="width:22px;height:22px;display:inline-flex;">
          <svg style="width:12px;height:12px"><use href="${channelIcon[l.preferred_channel]}"/></svg>
        </span>
        <span style="margin-inline-start:6px">${channelLabel[l.preferred_channel]}</span>
      </td>
      <td class="text-muted text-sm">${escapeHtml(l.last_interaction)}</td>
      <td><span class="badge badge--neutral">${statusLabel[l.status] || l.status}</span></td>
      <td><span class="num" style="font-weight:600;color:var(--color-primary);">${fmtSar(l.deal_value_sar)}</span></td>
      <td class="text-sm">${escapeHtml(l.owner)}</td>
    </tr>
  `).join('') || `<tr><td colspan="8" class="text-muted" style="text-align:center;padding:30px;">لا توجد نتائج مطابقة</td></tr>`;
}

/* ---------- Drawer ---------- */

function openDrawer(leadId) {
  const l = state.data.leads.find(x => x.id === leadId);
  if (!l) return;

  $('#drawer-logo').textContent = initial(l.company_name_ar);
  $('#drawer-title').textContent = l.company_name_ar;
  $('#drawer-sub').innerHTML = `<span class="num">${escapeHtml(l.company_name)}</span> · ${escapeHtml(l.sector_ar)} · ${escapeHtml(l.city)}`;

  const dims = [
    { key: 'icp', label: 'ICP' }, { key: 'intent', label: 'Intent' },
    { key: 'timing', label: 'Timing' }, { key: 'budget', label: 'Budget' },
    { key: 'authority', label: 'Authority' }, { key: 'engagement', label: 'Engagement' },
  ];

  $('#drawer-body').innerHTML = `
    <div class="grid-2" style="gap:12px;">
      <div>
        <div class="text-sm text-muted">النتيجة الإجمالية</div>
        <div style="display:flex;align-items:center;gap:8px;margin-top:4px;">
          <span class="score ${scoreClass(l.dealix_score)}" style="height:36px;min-width:52px;font-size:16px;"><span class="num">${l.dealix_score}</span></span>
          <span class="badge ${tierClass(l.priority_tier)}">${tierLabel[l.priority_tier]}</span>
        </div>
      </div>
      <div>
        <div class="text-sm text-muted">قيمة الصفقة المتوقّعة</div>
        <div style="font-family:var(--font-en);font-weight:700;font-size:20px;margin-top:4px;color:var(--color-primary);">
          ${fmtSar(l.deal_value_sar)} <span style="font-size:11px;color:var(--color-text-muted);">ر.س</span>
        </div>
      </div>
    </div>

    <div class="section-title">تفصيل النتيجة (6 أبعاد)</div>
    <div>
      ${dims.map(d => `
        <div class="score-dim">
          <div class="score-dim__label">${d.label}</div>
          <div class="score-dim__track"><div class="score-dim__fill" style="width:${l.score_breakdown[d.key]}%"></div></div>
          <div class="score-dim__val num">${l.score_breakdown[d.key]}</div>
        </div>
      `).join('')}
    </div>

    <div class="section-title">الإشارات المُساهِمة (${l.contributing_signals.length})</div>
    <div class="signal-list">
      ${l.contributing_signals.map(s => `
        <div class="signal"><svg><use href="#i-check"/></svg><span>${escapeHtml(s)}</span></div>
      `).join('')}
      ${(l.penalizing_factors || []).map(s => `
        <div class="signal signal--neg"><svg><use href="#i-alert"/></svg><span>${escapeHtml(s)}</span></div>
      `).join('')}
    </div>

    ${l.contacts && l.contacts.length ? `
      <div class="section-title">جهات الاتصال</div>
      <div style="display:flex;flex-direction:column;gap:8px;">
        ${l.contacts.map(c => `
          <div class="settings-row" style="padding:10px 14px;">
            <div>
              <strong>${escapeHtml(c.name)}</strong>
              <small class="num">${escapeHtml(c.role || '—')}${c.email ? ' · ' + escapeHtml(c.email) : ''}</small>
            </div>
          </div>
        `).join('')}
      </div>
    ` : ''}

    ${l.tech_stack && l.tech_stack.length ? `
      <div class="section-title">البصمة التقنية</div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;">
        ${l.tech_stack.map(t => `<span class="chip" style="cursor:default;" class="num">${escapeHtml(t)}</span>`).join('')}
      </div>
    ` : ''}

    ${l.news_events && l.news_events.length ? `
      <div class="section-title">أخبار ذات صلة</div>
      <div class="signal-list">
        ${l.news_events.map(n => `
          <div class="signal">
            <svg><use href="#i-external"/></svg>
            <div><strong style="font-weight:600;">${escapeHtml(n.headline)}</strong><div class="text-sm text-muted">${escapeHtml(n.source)}</div></div>
          </div>
        `).join('')}
      </div>
    ` : ''}

    <div class="section-title">التسلسل الزمني</div>
    <div class="timeline">
      ${l.timeline.map(t => `
        <div class="timeline__item">
          <div class="timeline__meta"><span class="badge badge--neutral" style="font-size:10px;">${channelLabel[t.channel] || t.channel}</span> · ${escapeHtml(t.actor)} · ${relTime(t.ts)}</div>
          <div class="timeline__text">${escapeHtml(t.text)}</div>
        </div>
      `).join('')}
    </div>
  `;

  $('#drawer').classList.add('is-open');
  $('#drawer-backdrop').classList.add('is-open');
}

function closeDrawer() {
  $('#drawer').classList.remove('is-open');
  $('#drawer-backdrop').classList.remove('is-open');
}

/* ---------- Inbox ---------- */

function renderInbox() {
  renderConversations();
}

function renderConversations() {
  let convs = state.data.conversations.slice();
  if (state.inboxChannel !== 'all') convs = convs.filter(c => c.channel === state.inboxChannel);

  $('#conv-list').innerHTML = convs.map(c => `
    <div class="conv ${state.activeConv === c.id ? 'is-active' : ''}" onclick="selectConversation('${c.id}')">
      <div class="activity__dot channel-dot--${c.channel}">
        <svg><use href="${channelIcon[c.channel]}"/></svg>
      </div>
      <div class="conv__body">
        <div class="conv__header">
          <div class="conv__sender">${escapeHtml(c.sender_name)}</div>
          <div class="conv__time">${relTime(c.ts)}</div>
        </div>
        <div class="conv__company">${escapeHtml(c.company_ar)} · ${channelLabel[c.channel]}</div>
        <div class="conv__preview">${escapeHtml(c.preview)}</div>
      </div>
      ${c.unread > 0 ? `<span class="conv__unread num">${c.unread}</span>` : ''}
    </div>
  `).join('') || `<div class="text-muted text-sm" style="padding:20px;text-align:center;">لا توجد محادثات</div>`;
}

function selectConversation(id) {
  state.activeConv = id;
  const c = state.data.conversations.find(x => x.id === id);
  if (!c) return;

  renderConversations();

  $('#thread-avatar').textContent = initial(c.sender_name);
  $('#thread-name').textContent = c.sender_name;
  $('#thread-sub').innerHTML = `<span>${escapeHtml(c.company_ar)}</span> · <span class="badge badge--neutral" style="font-size:10px;">${channelLabel[c.channel]}</span>`;

  $('#thread-messages').innerHTML = c.messages.map(m => `
    <div class="msg msg--${m.from}">
      <div>${escapeHtml(m.text)}</div>
      <div class="msg__meta">${new Date(m.ts).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' })}</div>
    </div>
  `).join('');
  $('#thread-messages').scrollTop = $('#thread-messages').scrollHeight;

  $('#composer').style.display = 'block';
  renderSuggestions();
}

function renderSuggestions() {
  // For conv-001 use lead-003 specific suggestions; else generic ones
  const c = state.data.conversations.find(x => x.id === state.activeConv);
  let sugs;
  if (c && c.id === 'conv-001') {
    sugs = state.data.ai_suggestions;
  } else {
    // generic suggestions contextual to channel
    sugs = [
      'مرحباً، شكراً على تواصلك. نستطيع جدولة مكالمة 15 دقيقة لعرض تفاصيل أكثر — متى يناسبك؟',
      'أكيد، أرسل لك الوثائق التفصيلية خلال ساعة. هل تفضّل PDF أم Google Doc؟',
      'تمام، نستطيع نضبط الباقة حسب احتياجكم. كم عدد المستخدمين المتوقّع في السنة الأولى؟',
    ];
  }
  $('#suggestions-list').innerHTML = sugs.map(s => `
    <div class="suggestion" onclick="pickSuggestion(this, \`${escapeAttr(s)}\`)">${escapeHtml(s)}</div>
  `).join('');
}

function pickSuggestion(el, text) {
  $('#composer-input').value = text;
  $('#composer-input').focus();
}

function sendReply() {
  const val = $('#composer-input').value.trim();
  if (!val) return showToast('اكتب ردّاً أولاً');
  const c = state.data.conversations.find(x => x.id === state.activeConv);
  if (!c) return;
  c.messages.push({ from: 'us', text: val, ts: new Date().toISOString() });
  c.preview = val;
  c.ts = new Date().toISOString();
  $('#composer-input').value = '';
  selectConversation(state.activeConv);
  showToast('تمّ إرسال الرد ✓');
}

/* ---------- Pipeline ---------- */

function renderKanban() {
  const cols = [
    { key: 'prospect', label: 'Prospect', cls: 'col--prospect' },
    { key: 'engaged', label: 'Engaged', cls: 'col--engaged' },
    { key: 'qualified', label: 'Qualified', cls: 'col--qualified' },
    { key: 'proposal', label: 'Proposal', cls: 'col--proposal' },
    { key: 'won', label: 'Won', cls: 'col--won' },
    { key: 'lost', label: 'Lost', cls: 'col--lost' },
  ];

  const byStage = Object.fromEntries(cols.map(c => [c.key, []]));
  state.data.leads.forEach(l => {
    const stage = statusToStage[l.status] || 'prospect';
    byStage[stage].push(l);
  });

  const total = state.data.leads.reduce((s, l) => s + (statusToStage[l.status] !== 'lost' ? l.deal_value_sar : 0), 0);
  $('#pipeline-total').textContent = fmtSar(total);

  $('#kanban').innerHTML = cols.map(c => `
    <div class="col ${c.cls}" data-stage="${c.key}" ondragover="onColDragOver(event)" ondragleave="onColDragLeave(event)" ondrop="onColDrop(event, '${c.key}')">
      <div class="col__header">
        <div class="col__title">${c.label}</div>
        <div class="col__count num">${byStage[c.key].length}</div>
      </div>
      <div class="col__body">
        ${byStage[c.key].map(l => `
          <div class="lead-card" draggable="true" ondragstart="onCardDragStart(event, '${l.id}')" ondragend="onCardDragEnd(event)" onclick="openDrawer('${l.id}')">
            <div class="lead-card__name">${escapeHtml(l.company_name_ar)}</div>
            <div class="lead-card__value num">${fmtSar(l.deal_value_sar)} ر.س</div>
            <div class="lead-card__meta">
              <span>${escapeHtml(l.assigned_agent)}</span>
              <span class="num">${l.days_in_stage}ي</span>
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');
}

let draggingId = null;
function onCardDragStart(e, id) {
  draggingId = id;
  e.currentTarget.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
}
function onCardDragEnd(e) {
  e.currentTarget.classList.remove('dragging');
  draggingId = null;
  $$('.col').forEach(c => c.classList.remove('drag-over'));
}
function onColDragOver(e) { e.preventDefault(); e.currentTarget.classList.add('drag-over'); }
function onColDragLeave(e) { e.currentTarget.classList.remove('drag-over'); }
function onColDrop(e, stage) {
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');
  if (!draggingId) return;
  const lead = state.data.leads.find(l => l.id === draggingId);
  if (!lead) return;
  // Map stage back to a reasonable status
  const stageToStatus = {
    prospect: 'new', engaged: 'engaged', qualified: 'qualified',
    proposal: 'proposal', won: 'closed_won', lost: 'closed_lost'
  };
  lead.status = stageToStatus[stage];
  lead.days_in_stage = 0;
  renderKanban();
  showToast(`نُقل ${lead.company_name_ar} إلى ${stage}`);
}

/* ---------- Agents ---------- */

function renderAgents() {
  const statusClass = { active: 'status-dot--active', idle: 'status-dot--idle', error: 'status-dot--error' };
  const statusLbl = { active: 'نشط', idle: 'خامل', error: 'خطأ' };

  $('#agents-grid').innerHTML = state.data.agents.map(a => `
    <div class="agent-card">
      <div class="agent-card__header">
        <div class="agent-card__icon channel-dot--${a.icon}">
          <svg><use href="#i-${a.icon}"/></svg>
        </div>
        <div style="flex:1;">
          <div class="agent-card__name">${escapeHtml(a.name)}</div>
          <div class="agent-card__sub">${escapeHtml(a.name_en)}</div>
        </div>
        <span class="status-dot ${statusClass[a.status]}">${statusLbl[a.status]}</span>
      </div>
      <div class="text-sm text-muted mb-2">${escapeHtml(a.description)}</div>
      <div class="agent-card__stats">
        <div><div class="stat__label">رسائل اليوم</div><div class="stat__value">${fmtNum(a.messages_today)}</div></div>
        <div><div class="stat__label">نجاح</div><div class="stat__value">${a.success_rate}%</div></div>
        <div><div class="stat__label">تكلفة اليوم</div><div class="stat__value">${a.cost_today_sar} ر.س</div></div>
      </div>
      <div class="agent-card__footer">
        <button class="btn btn--ghost btn--sm" onclick="showToast('عرض السجلّ الكامل — قريباً')">السجلّ</button>
        <label class="toggle"><input type="checkbox" ${a.status !== 'error' ? 'checked' : ''} onchange="showToast('${a.status === 'active' ? 'تم إيقاف' : 'تم تشغيل'} ${a.name}')"><span class="toggle__slider"></span></label>
      </div>
    </div>
  `).join('');
}

/* ---------- Playbooks ---------- */

function renderPlaybooks() {
  $('#playbooks-list').innerHTML = state.data.playbooks.map(p => `
    <div class="playbook">
      <div class="playbook__header">
        <div>
          <div class="playbook__title">${escapeHtml(p.name_ar)}</div>
          <div class="playbook__desc">${escapeHtml(p.description)}</div>
        </div>
        <div class="playbook__stats">
          <div class="playbook__stat">
            <strong>${p.active_leads}</strong>
            <span>leads نشطة</span>
          </div>
          <div class="playbook__stat">
            <strong>${p.conversion_rate}%</strong>
            <span>تحويل</span>
          </div>
          <button class="btn btn--ghost btn--sm" onclick="showToast('قريباً — تعديل ${escapeAttr(p.name_ar)}')">تعديل</button>
        </div>
      </div>
      <div class="playbook__steps">
        ${p.steps.map(s => `
          <div class="step">
            <div class="step__day">اليوم ${s.day}</div>
            <div class="step__action">${escapeHtml(s.action)}</div>
            <span class="step__channel-pill channel-dot--${s.channel}">
              <svg style="width:10px;height:10px"><use href="${channelIcon[s.channel]}"/></svg>
              ${channelLabel[s.channel]}
            </span>
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');
}

/* ---------- Sources ---------- */

function renderSources() {
  const iconMap = {
    saudi_registry: 'i-database', etimad: 'i-handshake', linkedin: 'i-linkedin',
    news: 'i-book', hiring: 'i-users', techstack: 'i-target'
  };
  $('#sources-grid').innerHTML = state.data.sources.map(s => {
    const connected = s.status === 'connected';
    return `
      <div class="source">
        <div class="source__top">
          <div class="source__icon"><svg><use href="#${iconMap[s.id] || 'i-database'}"/></svg></div>
          <span class="badge ${connected ? 'badge--success' : 'badge--danger'} badge--dot">${connected ? 'متصل' : 'يحتاج اعتماد'}</span>
        </div>
        <div class="source__name">${escapeHtml(s.name)}</div>
        <div class="source__desc">${escapeHtml(s.description)}</div>
        <div class="source__meta">
          <span class="source__meta-label">السجلات</span>
          <span class="source__meta-val num">${fmtNum(s.records)}</span>
        </div>
        <div class="source__meta" style="border-top:none;padding-top:0;margin-top:0;">
          <span class="source__meta-label">آخر مزامنة</span>
          <span class="source__meta-val">${escapeHtml(s.last_sync)}</span>
        </div>
        <button class="btn ${connected ? 'btn--ghost' : 'btn--primary'} btn--sm" style="width:100%;justify-content:center;margin-top:10px;" onclick="showToast('${connected ? 'إعدادات' : 'إضافة اعتماد'} — قريباً')">
          ${connected ? 'تهيئة' : 'إضافة اعتماد'}
        </button>
      </div>
    `;
  }).join('');
}

/* ---------- Analytics ---------- */

function renderAnalytics() {
  // MRR chart — SVG line chart
  const mrr = state.data.mrr_trend;
  const w = 480, h = 220;
  const pad = { t: 12, r: 10, b: 22, l: 8 };
  const maxMrr = Math.max(...mrr.map(m => m.mrr));
  const stepX = (w - pad.l - pad.r) / (mrr.length - 1);
  const sy = (v) => pad.t + (h - pad.t - pad.b) * (1 - v / maxMrr);
  const pts = mrr.map((m, i) => [pad.l + i * stepX, sy(m.mrr)]);
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
    <div class="chart-xaxis">
      ${mrr.map(m => `<span>${m.month}</span>`).join('')}
    </div>
  `;

  // Channel conversions
  const chColors = {
    whatsapp: 'var(--color-whatsapp)', email: 'var(--color-email)',
    linkedin: 'var(--color-linkedin)', sms: 'var(--color-sms)'
  };
  const maxConv = Math.max(...state.data.channels_performance.map(c => c.conversion));
  $('#channels-analytics').innerHTML = state.data.channels_performance.map(c => `
    <div class="channel-bar">
      <div class="channel-bar__icon channel-dot--${c.channel}"><svg><use href="${channelIcon[c.channel]}"/></svg></div>
      <div class="channel-bar__name">${channelLabel[c.channel]}<div class="text-sm text-muted num">${fmtNum(c.sent)} مُرسلة · ${fmtNum(c.replied)} ردّ</div></div>
      <div class="channel-bar__track"><div class="channel-bar__fill" style="width:${(c.conversion/maxConv)*100}%;background:${chColors[c.channel]};"></div></div>
      <div class="channel-bar__val num">${c.conversion}%</div>
    </div>
  `).join('');

  // ROI table — revenue per successful message (reasonable demo numbers)
  const revPerSuccess = { whatsapp: 180, email: 120, linkedin: 280, sms: 60, qualifier: 95, scheduler: 220, negotiator: 1800 };
  const roiData = state.data.agents.map(a => {
    const rate = a.success_rate / 100;
    const msgs30 = a.messages_today * 30;
    const revenue30 = msgs30 * rate * (revPerSuccess[a.id] || 120);
    const cost30 = a.cost_today_sar * 30;
    const roi = cost30 > 0 ? (revenue30 / cost30).toFixed(1) : '—';
    return { ...a, msgs30, revenue30, cost30, roi };
  });
  $('#roi-tbody').innerHTML = roiData.map(a => `
    <tr>
      <td>
        <div class="company-cell">
          <div class="agent-card__icon channel-dot--${a.icon}" style="width:30px;height:30px;"><svg style="width:16px;height:16px;"><use href="#i-${a.icon}"/></svg></div>
          <div><strong>${escapeHtml(a.name)}</strong></div>
        </div>
      </td>
      <td class="num">${fmtNum(a.msgs30)}</td>
      <td class="num" style="color:var(--color-primary);font-weight:600;">${fmtSar(a.revenue30)} ر.س</td>
      <td class="num">${fmtSar(a.cost30)} ر.س</td>
      <td><span class="badge badge--success num">${a.roi}×</span></td>
    </tr>
  `).join('');
}

/* ---------- Toast ---------- */

function showToast(text) {
  const el = document.createElement('div');
  el.className = 'toast';
  el.innerHTML = `<svg><use href="#i-check"/></svg><span>${escapeHtml(text)}</span>`;
  $('#toasts').appendChild(el);
  setTimeout(() => { el.style.animation = 'toastIn var(--t-med) var(--ease) reverse'; }, 2600);
  setTimeout(() => el.remove(), 3000);
}

/* ---------- helpers ---------- */

function escapeHtml(str) {
  if (str == null) return '';
  return String(str).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
function escapeAttr(str) {
  return String(str).replace(/`/g, '\\`').replace(/\$/g, '\\$').replace(/"/g, '&quot;');
}
function initial(name) {
  if (!name) return '؟';
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) return parts[0][0] + parts[1][0];
  return name.slice(0, 2);
}
function relTime(ts) {
  if (!ts) return '—';
  const d = new Date(ts);
  const diff = (Date.now() - d.getTime()) / 1000;
  if (diff < 60) return 'الآن';
  if (diff < 3600) return `منذ ${Math.floor(diff/60)} د`;
  if (diff < 86400) return `منذ ${Math.floor(diff/3600)} س`;
  return `منذ ${Math.floor(diff/86400)} ي`;
}

/* ---------- Start ---------- */

window.addEventListener('DOMContentLoaded', boot);

// Expose functions needed by inline onclicks
window.openDrawer = openDrawer;
window.closeDrawer = closeDrawer;
window.selectConversation = selectConversation;
window.pickSuggestion = pickSuggestion;
window.sendReply = sendReply;
window.showToast = showToast;
window.onCardDragStart = onCardDragStart;
window.onCardDragEnd = onCardDragEnd;
window.onColDragOver = onColDragOver;
window.onColDragLeave = onColDragLeave;
window.onColDrop = onColDrop;
