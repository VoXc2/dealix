/* =============================================================
   Dealix Frontend — role-page.js
   Single shell for /role/{role}.html landing pages.

   Reads <body data-role="ceo"> and binds:
     - copy block from ROLE_COPY[role]
     - 3 sample decisions from /api/v1/role-briefs/daily?role={role}
     - CTA → /onboarding.html

   Failure mode: any API error swaps in static demo decisions and shows
   the .dx-demo-banner. The page never breaks.
   ============================================================= */
(function () {
  'use strict';

  var api = window.DealixAPI;
  if (!api) return;

  var ROLE_COPY = {
    ceo: {
      label: 'المدير التنفيذي', emoji: '🧭',
      headline: 'لوحة القيادة بدلاً من ٢٠٠ دشبورد',
      pitch: 'كل صباح: ٣ قرارات مرتبة، Proof Pack أسبوعي، وضع الـ pipeline في رسالة واحدة. لا meetings داخلية، لا بحث في reports.',
      bullets: ['Proof Pack موجَّه للمستثمر أسبوعياً', 'لا live charge بدون موافقتك', 'اتخذ ٣ قرارات في ٥ دقائق'],
    },
    sales: {
      label: 'مدير المبيعات', emoji: '📈',
      headline: 'Pipeline ينظف نفسه — لا متابعات منسية',
      pitch: 'Dealix يلاحظ الصفقات الراكدة، يجهّز Follow-up عربي، ويمرّره لموافقتك. CRM workflow بدون workflow.',
      bullets: ['تنبيه قبل ركود الصفقة بـ ٤٨ ساعة', 'objection responses جاهزة (٨ فئات)', 'Pilot 499 close script — 10 دقائق'],
    },
    growth: {
      label: 'مدير النمو', emoji: '🚀',
      headline: 'تجربة واحدة في الأسبوع — قابلة للقياس',
      pitch: 'كل أسبوع نقترح تجربة واحدة بناءً على أضعف قناة في الـ funnel. تختار، تعتمد، نتابع — لا تخمين.',
      bullets: ['Self-Growth loop يحلل ٧ أيام', 'A/B بحدود — لا مواقع ثابتة', 'تقرير learning أسبوعي'],
    },
    revops: {
      label: 'RevOps', emoji: '⚙️',
      headline: 'الـ funnel مرئي — والتسريبات مُعلَّمة',
      pitch: 'lead → mql → sql → pilot → paying — كل انتقال مُسجَّل. تعرف بالضبط أين تخسر العملاء.',
      bullets: ['stage transitions في ledger', 'تنبيه على conversion drop', 'نموذج WoW deltas جاهز'],
    },
    cs: {
      label: 'Customer Success', emoji: '💚',
      headline: 'NPS + churn risk + SLA — في صفحة واحدة',
      pitch: 'كل tickets/sessions/customers في dashboard واحد. SLA breach يظهر قبل ١٢ ساعة من الحدوث.',
      bullets: ['breach warning قبل ٦ ساعات', 'NPS + churn risk per customer', 'auto-routing P0/P1'],
    },
    finance: {
      label: 'المالية', emoji: '💰',
      headline: 'MRR + ARR + cash forecast — يومي',
      pitch: 'Moyasar payments → MRR → ARR run-rate. توقعات الـ runway بدون spreadsheet.',
      bullets: ['MRR من ledger مباشرة', 'partner commission محسوب', 'ARR runway forecast'],
    },
    compliance: {
      label: 'الامتثال', emoji: '🛡️',
      headline: 'PDPL + WhatsApp ToS — مفروضة بـ default',
      pitch: '٨ live-action gates افتراضي False. كل outbound يحتاج موافقة. غير قابل للتجاوز بدون audit log.',
      bullets: ['8 gates default-False', 'audit trail per approval', 'reverse-DPI per عميل'],
    },
    partner: {
      label: 'شريك (وكالة)', emoji: '🤝',
      headline: 'بدلاً من scraping — partner referrals مُتعقَّبة',
      pitch: 'كل lead من الوكالة مرتبط بـ partner_id. commission محسوبة لحظياً. Proof Pack خاص بالوكالة.',
      bullets: ['attribution per partner', 'commission تلقائي', 'partner-scoped Proof Pack'],
    },
  };

  // role aliases — short URL → backend role identifier
  var ROLE_ALIAS = {
    sales: 'sales_manager',
    growth: 'growth_manager',
    cs: 'customer_success',
    partner: 'agency_partner',
  };

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function decisionCard(d) {
    var risk = d.risk_level || 'low';
    var badge = d.risk_badge || '';
    var why = d.why_now_ar || '';
    var rec = d.recommended_action_ar || '';
    return '<article class="dx-card" data-risk="' + escapeHtml(risk) + '">'
      + '<header class="dx-card__head">'
      +   '<span class="dx-card__type">' + escapeHtml(d.title_ar || 'قرار') + '</span>'
      +   (badge ? '<span class="dx-pill" data-priority="' + escapeHtml(badge) + '">' + escapeHtml(badge) + '</span>' : '')
      + '</header>'
      + '<p style="margin:.5rem 0; color:#374151;"><strong>لماذا الآن؟</strong> ' + escapeHtml(why) + '</p>'
      + '<p style="margin:.5rem 0;"><strong>التوصية:</strong> ' + escapeHtml(rec) + '</p>'
      + '</article>';
  }

  function fallbackDecisions(slug) {
    return [{
      title_ar: 'قرار مثال (demo)',
      why_now_ar: 'هذه نماذج — اشترك لرؤية القرارات الحقيقية من بياناتك.',
      recommended_action_ar: 'ابدأ معالج التأهيل لـ ٤ خطوات.',
      risk_level: 'low',
      risk_badge: 'P3',
    }];
  }

  async function loadDecisions(slug) {
    var role = ROLE_ALIAS[slug] || slug;
    var r = await api.get('/api/v1/role-briefs/daily?role=' + encodeURIComponent(role));
    var decisions = (r && r.ok && r.data && Array.isArray(r.data.top_decisions))
      ? r.data.top_decisions : null;
    if (!decisions || decisions.length === 0) {
      return { decisions: fallbackDecisions(slug), isDemo: true };
    }
    return { decisions: decisions.slice(0, 3), isDemo: false };
  }

  function renderShell(slug, copy) {
    var pitch = document.getElementById('dx-role-pitch');
    if (pitch) {
      pitch.innerHTML =
          '<span class="dx-hero__eyebrow">'
        + escapeHtml(copy.emoji) + ' '
        + escapeHtml(copy.label) + '</span>'
        + '<h1 class="dx-hero__title">' + escapeHtml(copy.headline) + '</h1>'
        + '<p class="dx-hero__sub">' + escapeHtml(copy.pitch) + '</p>'
        + '<ul style="margin:1rem 0; padding-inline-start:1.25rem; line-height:1.8;">'
        + copy.bullets.map(function (b) { return '<li>' + escapeHtml(b) + '</li>'; }).join('')
        + '</ul>'
        + '<div style="margin-top:1.25rem;">'
        +   '<a class="dx-btn dx-btn--primary" href="onboarding.html">ابدأ التأهيل (٤ خطوات)</a> '
        +   '<a class="dx-btn dx-btn--ghost" href="proof-pack.html">شاهد Proof Pack</a>'
        + '</div>';
    }
  }

  async function init() {
    var body = document.body;
    var slug = body && body.getAttribute('data-role');
    if (!slug) return;
    var copy = ROLE_COPY[slug] || ROLE_COPY.ceo;
    document.title = copy.label + ' — Dealix';
    renderShell(slug, copy);

    var holder = document.getElementById('dx-role-decisions');
    if (!holder) return;
    holder.innerHTML = '<p style="color:#6b7280">جاري تحميل قرارات اليوم…</p>';
    var data = await loadDecisions(slug);
    holder.innerHTML = data.decisions.map(decisionCard).join('');
    if (data.isDemo) {
      var banner = document.getElementById('dx-demo-banner');
      if (banner) banner.style.display = 'block';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
