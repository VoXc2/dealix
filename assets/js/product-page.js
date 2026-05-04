/* =============================================================
   Dealix Frontend — product-page.js
   Reads <body data-product="..."> on landing/products/*.html and
   binds product-specific copy + 3 sample live decisions for the
   underlying role.
   ============================================================= */
(function () {
  'use strict';
  var api = window.DealixAPI;
  if (!api) return;

  var PRODUCT_COPY = {
    command: {
      label: 'Dealix Command', emoji: '🧭', role: 'ceo',
      headline: 'القيادة اليومية للنمو — للمدير التنفيذي',
      pitch: 'كل صباح ٣ قرارات مرتّبة. أين الإيراد؟ ما المخاطر؟ ما الـ Proof؟ ما القرار التالي؟ بدون اجتماعات داخلية، بدون 200 dashboard.',
      bullets: ['أهم 3 قرارات يومياً', 'Revenue at-stake مباشر', 'Proof Pack أسبوعي للمستثمر', 'Live-action gates مرئية'],
      pricing_ar: '2,999 SAR / شهر شامل الضريبة (Executive Growth OS)',
    },
    sell: {
      label: 'Dealix Sell', emoji: '📈', role: 'sales_manager',
      headline: 'Pipeline ينظف نفسه — لمدير المبيعات',
      pitch: 'صفقات تحتاج متابعة، اعتراضات بردود جاهزة، عروض Pilot معدّة، فواتير جاهزة للإرسال. Sales Ops layer خفيف فوق ما عندك.',
      bullets: ['Stale alerts قبل ٤٨ ساعة', '8 objection responses عربية', 'Close plan لكل صفقة', 'Invoice في ١٠ دقائق'],
      pricing_ar: 'مدمج في Executive Growth OS (2,999 SAR/شهر)',
    },
    grow: {
      label: 'Dealix Grow', emoji: '🚀', role: 'growth_manager',
      headline: 'تجربة واحدة في الأسبوع، قابلة للقياس — لمدير النمو',
      pitch: 'أفضل شريحة، أفضل قناة، أفضل رسالة. Self-Growth loop يحلل ٧ أيام ويقترح التجربة القادمة. لا تخمين، لا blast.',
      bullets: ['Segment + channel + message daily', 'Risk-blocked قبل الإرسال', 'Weekly learning report', 'Scorecard كل ٧ أيام'],
      pricing_ar: 'مدمج في Executive Growth OS (2,999 SAR/شهر)',
    },
    serve: {
      label: 'Dealix Serve', emoji: '💚', role: 'customer_success',
      headline: 'Onboarding + SLA + Renewal Risk في صفحة — لـ CS',
      pitch: 'كل tickets، sessions، customers في dashboard واحد. SLA breach يظهر قبل ١٢ ساعة من الحدوث.',
      bullets: ['Health score per customer', 'Renewal risk early signal', 'Auto-routing P0/P1', 'Upgrade signals مرئية'],
      pricing_ar: 'مدمج في Executive Growth OS (2,999 SAR/شهر)',
    },
    partner: {
      label: 'Dealix Partner', emoji: '🤝', role: 'agency_partner',
      headline: 'وكالات + شراكات + Co-branded Proof — للشريك',
      pitch: 'partner shortlist، scorecard، intro scripts، Proof Pack باسم الوكالة، tracking للـ revenue share. قناة توزيع، وليس عميل واحد.',
      bullets: ['Partner shortlist + scorecard', 'Co-branded Proof Pack', 'Referral attribution', 'Commission tracker'],
      pricing_ar: 'Partnership Growth: 3,000–7,500 SAR لكل سبرنت',
    },
    proof: {
      label: 'Dealix Proof', emoji: '📊', role: 'compliance',
      headline: 'الدليل الذي يجعل العميل يجدد',
      pitch: 'Proof Pack أسبوعي بـ HMAC signature. ما أُنجز، ما حُمي، ما ينتظر، الأثر المالي، الخطوة القادمة. مشاركة مع المجلس بثقة.',
      bullets: ['HMAC-signed (non-repudiable)', 'كل RWU في ledger لحظي', 'Risk blocked = حماية مرئية', 'Anti-claims (لا نضمن)'],
      pricing_ar: 'مدمج في كل خدمات Dealix',
    },
  };

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function decisionCard(d) {
    var risk = d.risk_level || 'low';
    var why = d.why_now_ar || '';
    var rec = d.recommended_action_ar || '';
    return '<article class="dx-card" data-risk="' + escapeHtml(risk) + '">'
      + '<header class="dx-card__head"><span class="dx-card__type">'
      + escapeHtml(d.title_ar || 'قرار') + '</span></header>'
      + '<p style="margin:.5rem 0;"><strong>لماذا الآن؟</strong> ' + escapeHtml(why) + '</p>'
      + '<p style="margin:.5rem 0;"><strong>التوصية:</strong> ' + escapeHtml(rec) + '</p>'
      + '</article>';
  }

  async function init() {
    var slug = (document.body.getAttribute('data-product') || '').toLowerCase();
    var copy = PRODUCT_COPY[slug];
    if (!copy) return;

    document.title = copy.label + ' — Dealix';
    var pitch = document.getElementById('dx-product-pitch');
    if (pitch) {
      pitch.innerHTML =
          '<span class="dx-hero__eyebrow">' + escapeHtml(copy.emoji) + ' ' + escapeHtml(copy.label) + '</span>'
        + '<h1 class="dx-hero__title">' + escapeHtml(copy.headline) + '</h1>'
        + '<p class="dx-hero__sub">' + escapeHtml(copy.pitch) + '</p>'
        + '<ul style="margin:1rem 0; padding-inline-start:1.25rem; line-height:1.8;">'
        + copy.bullets.map(function (b) { return '<li>' + escapeHtml(b) + '</li>'; }).join('')
        + '</ul>'
        + '<p style="font-weight:600; color:#047857;">' + escapeHtml(copy.pricing_ar) + '</p>'
        + '<div style="margin-top:1.25rem;">'
        +   '<a class="dx-btn dx-btn--primary" href="../onboarding.html">ابدأ Pilot 499</a> '
        +   '<a class="dx-btn dx-btn--ghost" href="../proof-pack.html">شاهد Proof Pack</a>'
        + '</div>';
    }

    var holder = document.getElementById('dx-product-decisions');
    if (!holder) return;
    holder.innerHTML = '<p style="color:#6b7280">جاري تحميل قرارات اليوم لهذا الدور…</p>';
    var r = await api.get('/api/v1/role-briefs/daily?role=' + encodeURIComponent(copy.role));
    var decisions = (r && r.ok && r.data && Array.isArray(r.data.top_decisions))
      ? r.data.top_decisions : [];
    if (decisions.length) {
      holder.innerHTML = decisions.slice(0, 3).map(decisionCard).join('');
    } else {
      holder.innerHTML = '<p style="color:#6b7280">لا قرارات اليوم — اشترك لترى قراراتك الفعلية.</p>';
      var banner = document.getElementById('dx-demo-banner');
      if (banner) banner.style.display = 'block';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
}());
