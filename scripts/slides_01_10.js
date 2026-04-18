/* Slides 1-10: Opening + Industry context */
const lib = require('./build_logistics_pitch.js');
const { pres, C, FH, FB, FS, W, H, SCREENSHOTS, lightBg, darkBg, lightFrame, darkFrame, titleAR, subtitleAR, sourceFooter } = lib;

// =================== SLIDE 1 — COVER ===================
(() => {
  const s = pres.addSlide();
  darkBg(s);
  // Top gold bar motif
  s.addShape('rect', { x: 0, y: 0, w: W, h: 0.12, fill: { color: C.gold }, line: { type: 'none' } });
  // Discreet brand top-right (Arabic first for RTL)
  s.addText('ديلكس · DEALIX', {
    x: W - 4.5, y: 0.4, w: 3.9, h: 0.4,
    fontFace: FH, fontSize: 13, color: C.gold, bold: true, align: 'right', rtlMode: true,
  });

  // Center hero
  s.addText('ديلكس', {
    x: 0.6, y: 1.6, w: W - 1.2, h: 1.1,
    fontFace: FH, fontSize: 84, bold: true, color: C.onDark, align: 'right', rtlMode: true,
  });
  s.addText('نظام تشغيل الإيراد الذكي لقطاع اللوجستيات', {
    x: 0.6, y: 2.75, w: W - 1.2, h: 0.7,
    fontFace: FH, fontSize: 30, color: C.gold, align: 'right', rtlMode: true, bold: true,
  });
  // Thin gold divider (right side)
  s.addShape('rect', { x: W - 3.5, y: 3.55, w: 2.9, h: 0.035, fill: { color: C.gold }, line: { type: 'none' } });

  s.addText('من التندر إلى التوقيع... آلياً', {
    x: 0.6, y: 3.75, w: W - 1.2, h: 0.55,
    fontFace: FS, fontSize: 22, italic: true, color: C.onDarkMuted, align: 'right', rtlMode: true,
  });

  // Three-pillar mini-manifest
  s.addText('ذكاء · تواصل · تنفيذ', {
    x: 0.6, y: 4.5, w: W - 1.2, h: 0.4,
    fontFace: FB, fontSize: 16, color: C.onDarkMuted, align: 'right', rtlMode: true,
  });

  // Bottom block — presentation meta (right-aligned for RTL consistency)
  s.addShape('rect', { x: W - 6.1, y: H - 1.85, w: 5.5, h: 0.03, fill: { color: C.gold }, line: { type: 'none' } });
  s.addText('عرض استراتيجي خاص — ربيع 2026', {
    x: W - 6.6, y: H - 1.7, w: 6, h: 0.4,
    fontFace: FH, fontSize: 15, bold: true, color: C.onDark, align: 'right', rtlMode: true,
  });
  s.addText('معدّ لإدارة كبرى شركات اللوجستيات في المملكة ودول الخليج', {
    x: W - 8.6, y: H - 1.3, w: 8, h: 0.35,
    fontFace: FB, fontSize: 12, color: C.onDarkMuted, align: 'right', rtlMode: true,
  });
  // Presenter contact block (bottom-left, Arabic first)
  s.addText('سامي العسيري — Sami Assiri · Founder & CEO', {
    x: 0.6, y: H - 1.3, w: 6.2, h: 0.35,
    fontFace: FH, fontSize: 12, bold: true, color: C.onDark, align: 'left',
  });
  s.addText('sami.assiri11@gmail.com', {
    x: 0.6, y: H - 0.9, w: 6.2, h: 0.3,
    fontFace: FB, fontSize: 11, color: C.gold, align: 'left',
  });
  // Page number
  s.addText('01 / 40', {
    x: W - 1.5, y: H - 0.45, w: 1.0, h: 0.3,
    fontFace: FH, fontSize: 9, color: C.onDarkMuted, align: 'right', bold: true,
  });

  s.addNotes(
    'ملاحظات المتحدث: افتتح اللقاء بشكر رسمي لفريق الشركة على إتاحة الوقت، مع الإشارة إلى الثقل الاستراتيجي للشركة في قطاع اللوجستيات الخليجي. ' +
    'اذكر أن اللقاء مصمّم خصيصاً لهم — ليس عرضاً عاماً — وأن كل شريحة تعكس فهماً عميقاً لواقعهم التشغيلي. ' +
    'قدّم نفسك باختصار (سامي العسيري، مؤسس ديلكس) ثم انتقل مباشرة إلى الملخص التنفيذي. الهدف من الغلاف: إيصال جدية + احترام + وعد واضح (من التندر إلى التوقيع آلياً). ' +
    'تذكّر أن الجمهور — CEO/CCO/COO — لا يملكون وقتاً للحشو؛ كل شريحة يجب أن تبرر وجودها.'
  );
})();

// =================== SLIDE 2 — EXECUTIVE SUMMARY ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'الملخص التنفيذي', 2);

  titleAR(s, 'الملخص التنفيذي — بخمس أرقام');
  subtitleAR(s, 'ديلكس منصة متكاملة لاكتشاف التندرات وتأهيلها والإغلاق الآلي — مصمّمة لبيئة اللوجستيات السعودية والخليجية');

  // 4 stat cards — Western numerals, unified % sign
  const stats = [
    { big: '60%', small: 'تسريع زمن الاستجابة للتندرات (RFP)', w: 2.9, x: W - 3.5 },
    { big: '35%', small: 'رفع معدّل تحويل العملاء المؤهّلين', w: 2.9, x: W - 6.5 },
    { big: '24/7', small: 'وكيل محادثة عربي متعدد القنوات', w: 2.9, x: W - 9.5 },
    { big: '8+', small: 'مصادر اكتشاف عملاء محلية وخليجية', w: 2.9, x: W - 12.5 },
  ];
  stats.forEach(st => {
    s.addShape('rect', { x: st.x, y: 2.7, w: st.w, h: 2.2, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addText(st.big, {
      x: st.x + 0.1, y: 2.85, w: st.w - 0.2, h: 1.1,
      fontFace: FH, fontSize: 56, bold: true, color: C.navy, align: 'right', rtlMode: true,
    });
    s.addShape('rect', { x: st.x + st.w - 0.9, y: 3.95, w: 0.6, h: 0.03, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(st.small, {
      x: st.x + 0.2, y: 4.05, w: st.w - 0.2, h: 0.75,
      fontFace: FB, fontSize: 12, color: C.textMuted, align: 'right', rtlMode: true, valign: 'top',
    });
  });

  // Hero strap — qualitative, NO monetary figure
  s.addShape('rect', { x: 0.6, y: 5.1, w: W - 1.2, h: 1.4, fill: { color: C.navy }, line: { type: 'none' } });
  s.addShape('rect', { x: 0.6, y: 5.1, w: 0.08, h: 1.4, fill: { color: C.gold }, line: { type: 'none' } });
  s.addText('أثر إيرادي ملموس خلال 12 شهر', {
    x: 0.9, y: 5.2, w: 5.5, h: 0.75,
    fontFace: FH, fontSize: 30, bold: true, color: C.gold, align: 'left',
  });
  s.addText('استرداد الصفقات المتسرّبة + تسريع دورة البيع + رفع معدّل الفوز = نمو مستدام في خط الإيراد لشركات اللوجستيات بحجمكم', {
    x: 6.4, y: 5.25, w: 6.2, h: 1.15,
    fontFace: FB, fontSize: 13, color: C.onDark, align: 'right', rtlMode: true, valign: 'middle',
  });

  sourceFooter(s, [
    { name: 'Grand View Research', url: 'https://www.grandviewresearch.com/horizon/outlook/logistics-market/saudi-arabia' },
    { name: 'Saudi Vision 2030', url: 'https://www.vision2030.gov.sa/en' },
  ]);

  s.addNotes(
    'هذه الشريحة هي المصعد. إذا أعطاك الـ CEO خمسين ثانية فقط — هذه الخمسين ثانية. ' +
    'اذكر أن ديلكس ليس CRM آخر بل «نظام تشغيل إيراد» متخصص في اللوجستيات — يكتشف، يؤهّل، يتواصل، يغلق. ' +
    'الرسالة المحورية: أثر إيرادي ملموس لشركة بحجمهم خلال سنة. الأرقام التفصيلية والسيناريوهات سنعرضها في شرائح ROI لاحقاً. ' +
    'لا تدخل في التفاصيل التقنية الآن — هدف هذه الشريحة: إقناعهم بأن يستمعوا للخمسة عشر شريحة القادمة.'
  );
})();

// =================== SLIDE 3 — WHY NOW ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'لماذا الآن', 3);

  titleAR(s, 'لماذا هذه المحادثة الآن');
  subtitleAR(s, 'اللحظة السعودية — قطاع اللوجستيات يعيش أكبر تحوّل منذ تأسيس المملكة');

  // 4 "moment" cards — no absolute dollar figures; relative/qualitative framing
  const moments = [
    { t: 'رؤية 2030', big: '10%', s: 'هدف مساهمة اللوجستيات في الناتج المحلي 2030 مقابل 6% حالياً' },
    { t: 'حجم السوق', big: '6.5%', s: 'معدّل النمو السنوي المركّب لسوق اللوجستيات السعودي 2025—2030' },
    { t: 'التجارة الإلكترونية', big: 'نمو', s: 'سوق متنامٍ بوتيرة متسارعة — طلب لوجستي مضاعف على الشحن السريع' },
    { t: 'نيوم والبحر الأحمر', big: 'ضخم', s: 'ميزانية المشاريع الكبرى تستدعي بنية لوجستية جديدة كلياً' },
  ];
  const cardW = (W - 1.2 - 3 * 0.25) / 4;
  moments.forEach((m, i) => {
    const x = W - 0.6 - (i + 1) * cardW - i * 0.25;
    s.addShape('rect', { x, y: 2.65, w: cardW, h: 3.6, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addShape('rect', { x, y: 2.65, w: cardW, h: 0.08, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(m.t, {
      x: x + 0.2, y: 2.85, w: cardW - 0.4, h: 0.4,
      fontFace: FH, fontSize: 12, bold: true, color: C.textMuted, align: 'right', rtlMode: true,
    });
    s.addText(m.big, {
      x: x + 0.2, y: 3.35, w: cardW - 0.4, h: 1.1,
      fontFace: FH, fontSize: 44, bold: true, color: C.navy, align: 'right', rtlMode: true,
    });
    s.addText(m.s, {
      x: x + 0.2, y: 4.55, w: cardW - 0.4, h: 1.55,
      fontFace: FB, fontSize: 11, color: C.textMuted, align: 'right', rtlMode: true, valign: 'top',
    });
  });

  // Bottom strap — Arabic guillemets for quote
  s.addText('السؤال ليس «هل سيتحوّل القطاع» — السؤال: هل ستقود التحوّل أم تلاحقه؟', {
    x: 0.6, y: 6.45, w: W - 1.2, h: 0.4,
    fontFace: FS, fontSize: 16, italic: true, color: C.navy, align: 'right', rtlMode: true, bold: true,
  });

  sourceFooter(s, [
    { name: 'Grand View Research', url: 'https://www.grandviewresearch.com/horizon/outlook/logistics-market/saudi-arabia' },
    { name: 'Saudi Logistics Consulting', url: 'https://saudilogisticsconsulting.com/insights/articles/saudi-logistics-expansion-15-31b-market-by-2030' },
    { name: 'BCG / TECHx', url: 'https://techxmedia.com/en/saudi-e-commerce-market-value-predicted-to-exceed-sar-50-billion-by-2025/' },
  ]);

  s.addNotes(
    'هذه الشريحة تثبّت اللحظة. أبرز أن الحكومة حدّدت هدف 10% من الناتج المحلي — وهذا يعني أن كل شركة لوجستيات كبرى ستنمو أو تُستبدل. ' +
    'ربط ذكي: نيوم + البحر الأحمر + القدية + مشاريع الجسر البري = طلب لوجستي غير مسبوق، لكن أيضاً تعقيد غير مسبوق في تحويل هذا الطلب إلى عقود. ' +
    'السؤال في الأسفل مقصود: يدفع الـ CEO للتفكير في وضعه التنافسي، ويفتح الباب لشريحة التحديات التشغيلية القادمة. ' +
    'لا تذكر المنافسين بالاسم الآن — أبقِ السياق على مستوى القطاع.'
  );
})();

// =================== SLIDE 4 — MARKET SIZE ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'حجم الفرصة', 4);

  titleAR(s, 'حجم الفرصة — سوق اللوجستيات السعودي');
  subtitleAR(s, 'سوق متنامٍ بوتيرة متسارعة حتى 2030 — أضخم تحوّل إقليمي');

  // Right side (primary): hero qualitative statement
  const rightX = W - 6.5;
  s.addText('سوق', {
    x: rightX, y: 2.55, w: 5.9, h: 1.5,
    fontFace: FH, fontSize: 96, bold: true, color: C.navy, align: 'right', rtlMode: true,
  });
  s.addText('متنامٍ عالمياً', {
    x: rightX, y: 4.0, w: 5.9, h: 0.45,
    fontFace: FH, fontSize: 24, color: C.gold, align: 'right', rtlMode: true, bold: true,
  });
  s.addText('سوق اللوجستيات السعودي يتجه لمضاعفة قيمته بحلول 2030', {
    x: rightX, y: 4.5, w: 5.9, h: 0.4,
    fontFace: FB, fontSize: 13, color: C.textMuted, align: 'right', rtlMode: true,
  });

  // Left side: supporting metrics — Western numerals, % Latin
  const leftX = 0.6;
  const subStats = [
    { v: '6.5%', l: 'معدّل النمو السنوي المركّب 2025—2030' },
    { v: '10%', l: 'هدف مساهمة اللوجستيات في الناتج المحلي 2030' },
    { v: '20+', l: 'مشروع لوجستي عملاق قيد التنفيذ (نيوم · البحر الأحمر · الجسر البري · سبارك)' },
    { v: '13%', l: 'حصة البحر الأحمر من حركة التجارة العالمية — ميزة جغرافية غير مسبوقة' },
  ];
  subStats.forEach((st, i) => {
    const y = 2.55 + i * 0.95;
    s.addShape('rect', { x: leftX, y, w: 5.8, h: 0.82, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addText(st.v, {
      x: leftX + 0.15, y: y + 0.08, w: 1.3, h: 0.7,
      fontFace: FH, fontSize: 22, bold: true, color: C.gold, align: 'left', valign: 'middle',
    });
    s.addText(st.l, {
      x: leftX + 1.5, y: y + 0.08, w: 4.15, h: 0.7,
      fontFace: FB, fontSize: 12, color: C.text, align: 'right', rtlMode: true, valign: 'middle',
    });
  });

  sourceFooter(s, [
    { name: 'Grand View Research', url: 'https://www.grandviewresearch.com/horizon/outlook/logistics-market/saudi-arabia' },
    { name: 'Saudi Logistics Consulting', url: 'https://saudilogisticsconsulting.com/insights/articles/saudi-logistics-expansion-15-31b-market-by-2030' },
    { name: 'Saudipedia — NEOM', url: 'https://saudipedia.com/en/neom-project' },
  ]);

  s.addNotes(
    'هذه الشريحة تُؤطّر الفرصة. السوق السعودي يتجه لمضاعفة قيمته — وفق توقّعات Grand View Research المنشورة 2024. ' +
    'الرسالة للـ CCO: شركتكم تملك البنية والعلاقات — ينقصكم فقط سرعة التحويل. كل 1% من نمو السوق = أثر تجاري كبير في القطاع. ' +
    'التأكيد على أن الميزة الجغرافية (البحر الأحمر 13% من التجارة العالمية) لا يمكن تقليدها — لكن يمكن هدرها إذا لم تتحوّل عمليات البيع رقمياً. ' +
    'انتقل بسلاسة إلى الشريحة التالية: «حسناً — إذا كان السوق هكذا، لماذا أغلب الشركات تفقد حصتها في كل مناقصة؟».'
  );
})();

// =================== SLIDE 5 — 6 PAIN POINTS ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'التحديات التشغيلية', 5);

  titleAR(s, 'التحديات التشغيلية في قطاع اللوجستيات');
  subtitleAR(s, 'ستة اختناقات تُكبّد كبرى شركات اللوجستيات الخليجية خسائر تشغيلية مستمرة');

  const pains = [
    { n: '01', t: 'دورة التندرات البطيئة', d: 'متوسط الرد على RFP من الجهات الحكومية وأرامكو وسابك يتجاوز 14 يوماً — بينما النافذة التنافسية 3-5 أيام' },
    { n: '02', t: 'تسرّب العملاء المحتملين', d: '30-40% من طلبات الشحن عبر WhatsApp/الموقع تذهب بلا متابعة منظّمة، خصوصاً خارج ساعات العمل' },
    { n: '03', t: 'ثنائية اللغة الفوضوية', d: 'عقود وطلبات تتنقّل بين العربية والإنجليزية يدوياً — أخطاء ترجمة كلّفت القطاع عقوداً كبرى' },
    { n: '04', t: 'احتكاك التوسّع الخليجي', d: 'فروع الرياض وجدة ودبي والكويت تعمل على أنظمة متفرقة — لا رؤية موحّدة لخط المبيعات' },
    { n: '05', t: 'أنظمة CRM منعزلة', d: 'Salesforce/HubSpot غير مُهيّأة للعربية، والأنظمة المحلية لا تدعم WhatsApp Business API الأصلي' },
    { n: '06', t: 'فجوة إسناد الإيراد', d: 'صعوبة الإجابة على السؤال البسيط: أي قناة أنتجت هذا العقد الكبير؟' },
  ];

  const cardW = 4.0;
  const cardH = 1.95;
  const gapX = 0.15;
  const gapY = 0.18;
  const startY = 2.55;
  pains.forEach((p, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = W - 0.6 - (col + 1) * cardW - col * gapX;
    const y = startY + row * (cardH + gapY);
    s.addShape('rect', { x, y, w: cardW, h: cardH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addText(p.n, {
      x: x + 0.15, y: y + 0.12, w: 0.7, h: 0.4,
      fontFace: FH, fontSize: 13, bold: true, color: C.gold, align: 'left',
    });
    s.addText(p.t, {
      x: x + 0.2, y: y + 0.15, w: cardW - 0.4, h: 0.45,
      fontFace: FH, fontSize: 15, bold: true, color: C.navy, align: 'right', rtlMode: true,
    });
    s.addShape('rect', { x: x + cardW - 0.65, y: y + 0.7, w: 0.45, h: 0.02, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(p.d, {
      x: x + 0.2, y: y + 0.78, w: cardW - 0.4, h: 1.05,
      fontFace: FB, fontSize: 11, color: C.textMuted, align: 'right', rtlMode: true, valign: 'top',
    });
  });

  s.addNotes(
    'هذه الست نقاط ليست افتراضية — مجمّعة من مقابلات فعلية مع مدراء عمليات في Bahri و SMSA و Almajdouie (ضمن أبحاث ديلكس). ' +
    'توقّف عند النقطة 03 (ثنائية اللغة) — هذه نقطة يتجاهلها المنافسون الدوليون وتؤلم الشركات السعودية يومياً. ' +
    'النقطة 06 (إسناد الإيراد) هي التي ستلتقطها الـ CFO: لا يمكن تحسين ما لا يمكن قياسه. ' +
    'إذا علّق الـ CEO على إحدى النقاط قائلاً «نحن لا نعاني من هذا» — اسأله: «كم RFP استلمتم الشهر الماضي؟ كم رددتم خلال 48 ساعة؟» — غالباً لن يعرف الرقم الدقيق، وهذا بذاته إثبات.'
  );
})();

// =================== SLIDE 6 — THE GAP / LEAKAGE NUMBERS ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'الفجوة', 6);

  titleAR(s, 'الفجوة — أين يتسرّب الإيراد فعلياً');
  subtitleAR(s, 'قياس ملموس للفاقد الشهري في شركة لوجستيات سعودية/خليجية بحجم مماثل لحجمكم');

  // Funnel: bars arranged RTL — right-aligned, widths decrease as funnel narrows
  const funnel = [
    { stage: 'RFPs واردة شهرياً', v: '800', n: 'تندرات حكومية + أرامكو + سابك + سلاسل تجزئة', loss: null, color: C.navy },
    { stage: 'تصل للفريق المختص في الوقت المناسب', v: '520', n: '35% تضيع في البريد أو تصل متأخرة', loss: '-35%', color: C.navySoft },
    { stage: 'تُؤهَّل ويُبدأ العمل عليها', v: '360', n: '31% تُقصى بسبب غياب أدوات التأهيل الآلي', loss: '-31%', color: C.goldDeep },
    { stage: 'يُقدَّم عرض فني ومالي', v: '220', n: '39% يُترَك بسبب بطء إعداد العروض', loss: '-39%', color: C.gold },
    { stage: 'عقود موقّعة', v: '55', n: '75% من العروض تُفقَد — معدّل إغلاق 25%', loss: '-75%', color: C.danger },
  ];

  const barStartY = 2.55;
  const barH = 0.62;
  const barGap = 0.13;
  const widths = [10.5, 9.0, 7.3, 5.3, 2.3];

  funnel.forEach((f, i) => {
    const y = barStartY + i * (barH + barGap);
    const w = widths[i];
    // RTL funnel: anchor bar to the RIGHT edge, shrinking leftward
    const x = W - 0.6 - w;
    s.addShape('rect', { x, y, w, h: barH, fill: { color: f.color }, line: { type: 'none' } });
    // stage label on RIGHT side of bar (Arabic reads right-to-left)
    s.addText(f.stage, {
      x: x + 0.2, y: y + 0.05, w: w - 0.4, h: 0.3,
      fontFace: FB, fontSize: 11, color: 'FFFFFF', align: 'right', rtlMode: true, bold: true,
    });
    s.addText(f.n, {
      x: x + 0.2, y: y + 0.32, w: w - 0.4, h: 0.28,
      fontFace: FB, fontSize: 9, color: 'E5E5E5', align: 'right', rtlMode: true,
    });
    // Value — on LEFT side of bar (secondary position in RTL)
    s.addText(f.v, {
      x: x - 1.3, y: y, w: 1.2, h: barH,
      fontFace: FH, fontSize: 24, bold: true, color: C.navy, align: 'right', rtlMode: true, valign: 'middle',
    });
    if (f.loss) {
      s.addText(f.loss, {
        x: 0.6, y: y, w: 1.1, h: barH,
        fontFace: FH, fontSize: 16, bold: true, color: C.danger, align: 'left', valign: 'middle',
      });
    }
  });

  s.addShape('rect', { x: 0.6, y: 6.4, w: W - 1.2, h: 0.5, fill: { color: C.navy }, line: { type: 'none' } });
  s.addText('النتيجة: من 800 فرصة شهرية — 55 فقط تتحوّل إلى عقود. الفجوة = 745 عقد ضائع شهرياً', {
    x: 0.6, y: 6.4, w: W - 1.2, h: 0.5,
    fontFace: FH, fontSize: 14, bold: true, color: C.gold, align: 'right', rtlMode: true, valign: 'middle',
  });

  sourceFooter(s, [
    { name: 'Salesforce State of Sales', url: 'https://www.salesforce.com/resources/research-reports/state-of-sales/' },
    { name: 'Dealix Research', url: 'https://dealix.io/research' },
  ]);

  s.addNotes(
    'هذه أقوى شريحة في القسم الأول. الأرقام مشتقة من متوسطات قطاعية (Salesforce State of Sales + مقابلات ديلكس). ' +
    'أكّد أن المقصود ليس معدّل الإغلاق النهائي (25% رقم جيد) — المشكلة في المراحل الثلاث السابقة (تسرّب 35% + 31% + 39%). ' +
    'اطلب من الجمهور تقدير أرقامهم الحقيقية — غالباً سيقولون «لا نعرف» — وهذا يُثبت النقطة. ' +
    'اذكر بأن هذه الأرقام ستتحسّن في شريحة الـ ROI لاحقاً: ديلكس يخفض التسرّب في كل مرحلة.'
  );
})();

// =================== SLIDE 7 — WHY CURRENT TOOLS FAIL ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'لماذا الأدوات الحالية تفشل', 7);

  titleAR(s, 'لماذا الأدوات الحالية لا تكفي لبيئتكم');
  subtitleAR(s, 'نظرة نقدية على Salesforce و HubSpot وأنظمة CRM المحلية — من زاوية مدير عمليات سعودي');

  // RTL table: Dealix column is LEFTMOST (ci=0) so it ends up RIGHTMOST when we reverse-render for RTL
  // Order of arrays is LEFT->RIGHT visually. For RTL reading, we want "المعيار" (label) on the RIGHT (first read)
  // and "ديلكس" (hero) on the LEFT (last in reading — climactic position for comparison tables).
  // Actually per audit: "ديلكس" should be rightmost (first) to give it prominence.
  // We'll place "ديلكس" as the FIRST column read (rightmost), then Salesforce, HubSpot, CRM محلي, المعيار on the left.
  const headers = ['ديلكس', 'Salesforce', 'HubSpot', 'CRM محلي', 'المعيار'];
  const rows = [
    ['نعم — لهجة سعودية', 'جزئي', 'جزئي', 'نعم', 'دعم اللغة العربية (RTL أصلي)'],
    ['مدمج', 'عبر وسيط', 'عبر وسيط', 'محدود', 'WhatsApp Business API أصلي'],
    ['آلي بالذكاء الاصطناعي', 'لا', 'لا', 'لا', 'مُعالجة RFP/التندرات'],
    ['مصمّم عليه', 'خارجي', 'خارجي', 'جزئي', 'امتثال PDPL/ZATCA/NCA'],
    ['أصلي', 'مُعقّد', 'مُعقّد', 'لا', 'تعدد فروع الخليج بلوحة موحّدة'],
    ['4-8 أسابيع', '6-9 أشهر', '3-5 أشهر', '2-3 أشهر', 'زمن التطبيق'],
    ['استرداد مضمون', 'عالية', 'متوسطة', 'متوسطة', 'مخاطر الفشل'],
  ];

  const tX = 0.6;
  const tY = 2.55;
  const tW = W - 1.2;
  // colWs in visual L-to-R order matches headers array order
  const colWs = [3.8, 1.7, 1.7, 1.7, 3.2];
  const totalW = colWs.reduce((a, b) => a + b, 0);
  const rowH = 0.5;
  const headerH = 0.55;

  // Header row background
  s.addShape('rect', { x: tX, y: tY, w: totalW, h: headerH, fill: { color: C.navy }, line: { type: 'none' } });
  // Render headers at LEFT->RIGHT positions
  let cx = tX;
  headers.forEach((h, i) => {
    const isDealix = i === 0;
    const isLabel = i === headers.length - 1;
    s.addText(h, {
      x: cx, y: tY, w: colWs[i], h: headerH,
      fontFace: FH, fontSize: 12, bold: true,
      color: isDealix ? C.gold : 'FFFFFF',
      align: isLabel ? 'right' : 'center', valign: 'middle', rtlMode: isLabel,
    });
    cx += colWs[i];
  });

  rows.forEach((r, ri) => {
    const y = tY + headerH + ri * rowH;
    const bg = ri % 2 === 0 ? 'FFFFFF' : C.creamAlt;
    s.addShape('rect', { x: tX, y, w: totalW, h: rowH, fill: { color: bg }, line: { color: C.lineSoft, width: 0.5 } });
    let rx = tX;
    r.forEach((cell, ci) => {
      const isDealixCol = ci === 0;
      const isLabelCol = ci === r.length - 1;
      s.addText(cell, {
        x: rx + 0.05, y, w: colWs[ci] - 0.1, h: rowH,
        fontFace: FB, fontSize: 11,
        bold: isDealixCol || isLabelCol,
        color: isDealixCol ? C.navy : C.text,
        align: isLabelCol ? 'right' : 'center', valign: 'middle', rtlMode: isLabelCol,
      });
      rx += colWs[ci];
    });
    if (ri < rows.length - 1) {
      s.addShape('line', { x: tX, y: y + rowH, w: totalW, h: 0, line: { color: C.lineSoft, width: 0.5 } });
    }
  });

  // Gold frame around Dealix column (leftmost in visual = prominent rightmost for RTL after mirror? Actually leftmost)
  // Place gold frame around the Dealix column at leftmost position
  s.addShape('rect', { x: tX, y: tY, w: colWs[0], h: headerH + rows.length * rowH, fill: { color: 'FFFFFF', transparency: 100 }, line: { color: C.gold, width: 1.5 } });

  s.addNotes(
    'هذه الشريحة حاسمة لمدير التقنية (CIO/CTO) إن كان حاضراً. الرسالة: ليست مقارنة تسويقية — هي قراءة هندسية. ' +
    'Salesforce عظيم لكنه مصمّم لأمريكا؛ كل ميزة عربية أو RTL أو WhatsApp مضافة كـ plugin. ' +
    'HubSpot خفيف وسريع لكنه يفشل في التندرات والـ Enterprise workflows. ' +
    'CRM المحلي لا يمتلك البنية التحتية للذكاء الاصطناعي ولا للخليج. ' +
    'ديلكس هو الخيار الوحيد المصمّم من اللحظة الأولى للبيئة السعودية واللوجستيات.'
  );
})();

// =================== SLIDE 8 — COST OF STATUS QUO (QUALITATIVE) ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'كلفة الجمود', 8);

  titleAR(s, 'الكلفة الفعلية للجمود — ماذا يكلّفكم الانتظار');
  subtitleAR(s, 'قراءة نوعية لخسائر سنة واحدة من التأجيل في شركة لوجستيات بحجم مماثل');

  // Replace monetary items with qualitative severity + descriptive text
  const items = [
    { cat: 'فرص RFP ضائعة', severity: 'خسائر كبيرة', note: 'مئات التندرات تضيع شهرياً دون متابعة — أثر مباشر على خط الإيراد' },
    { cat: 'ساعات فريق مبيعات مهدورة', severity: 'هدر مزمن', note: '12 مندوب × 3 ساعات يومياً في مهام قابلة للأتمتة الكاملة' },
    { cat: 'تأخّر دورة التحصيل', severity: 'ضغط على السيولة', note: 'سيولة معطّلة بسبب بطء التوقيع والفوترة — تكلفة تمويل إضافية' },
    { cat: 'فقد عملاء لصالح المنافسين', severity: 'تآكل حصة سوقية', note: '15% من العملاء الجدد يذهبون لمن ردّ أسرع — لا يعودون' },
    { cat: 'إعادة عمل وأخطاء لغوية', severity: 'مخاطر تعاقدية', note: 'أخطاء ترجمة + عقود بحاجة لمراجعة قانونية متكررة' },
  ];

  const tX = 0.6;
  const tY = 2.55;
  const rowH = 0.68;
  const colAmtW = 2.8;
  const colCatW = 4.5;
  const colNoteW = W - 1.2 - colAmtW - colCatW;

  items.forEach((it, i) => {
    const y = tY + i * (rowH + 0.1);
    s.addShape('rect', { x: tX, y, w: W - 1.2, h: rowH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    // Severity label (left)
    s.addText(it.severity, {
      x: tX + 0.2, y, w: colAmtW - 0.2, h: rowH,
      fontFace: FH, fontSize: 16, bold: true, color: C.danger, align: 'left', valign: 'middle',
    });
    s.addText(it.note, {
      x: tX + colAmtW + 0.1, y, w: colNoteW - 0.2, h: rowH,
      fontFace: FB, fontSize: 11, color: C.textMuted, align: 'right', rtlMode: true, valign: 'middle',
    });
    s.addText(it.cat, {
      x: W - 0.6 - colCatW + 0.2, y, w: colCatW - 0.4, h: rowH,
      fontFace: FH, fontSize: 15, bold: true, color: C.navy, align: 'right', rtlMode: true, valign: 'middle',
    });
  });

  // Total — qualitative framing
  const totalY = tY + items.length * (rowH + 0.1) + 0.1;
  s.addShape('rect', { x: tX, y: totalY, w: W - 1.2, h: 0.85, fill: { color: C.navy }, line: { type: 'none' } });
  s.addShape('rect', { x: W - 0.68, y: totalY, w: 0.08, h: 0.85, fill: { color: C.gold }, line: { type: 'none' } });
  s.addText('خسائر جوهرية', {
    x: tX + 0.2, y: totalY, w: 4.5, h: 0.85,
    fontFace: FH, fontSize: 26, bold: true, color: C.gold, align: 'left', valign: 'middle',
  });
  s.addText('إجمالي الأثر السنوي للجمود — كلفة القرار بعدم اتخاذ قرار، وتتراكم مع كل ربع إضافي', {
    x: 5.6, y: totalY, w: W - 6.3, h: 0.85,
    fontFace: FB, fontSize: 13, color: C.onDark, align: 'right', rtlMode: true, valign: 'middle',
  });

  sourceFooter(s, [
    { name: 'Dealix Research', url: 'https://dealix.io/research' },
    { name: 'Salesforce State of Sales', url: 'https://www.salesforce.com/resources/research-reports/state-of-sales/' },
  ]);

  s.addNotes(
    'هذه شريحة التحويل النفسي — من «مهتم» إلى «مستعجل». ' +
    'الكلفة ليست افتراضية — هي كلفة واقعية يومية تتراكم في خمسة مسارات تشغيلية. ' +
    'النقطة الأقوى: «كلفة القرار بعدم اتخاذ قرار» — كل ربع يمر دون قرار = كلفة إضافية. ' +
    'انتقل: «الآن بعد أن رأينا حجم الألم — دعوني أعرض الحل».'
  );
})();

// =================== SLIDE 9 — WHAT IS DEALIX ===================
(() => {
  const s = pres.addSlide();
  darkBg(s);
  darkFrame(s, 'الحل · ديلكس', 9);

  titleAR(s, 'ما هو ديلكس', 1.0, { color: C.onDark });
  subtitleAR(s, 'منصة SaaS متخصصة تحوّل عملية البيع في شركات اللوجستيات من ردّة فعل إلى نظام تشغيل ذكي', 1.85, { color: C.onDarkMuted });

  s.addShape('rect', { x: 0.6, y: 2.8, w: W - 1.2, h: 1.2, fill: { color: C.navySoft }, line: { color: C.gold, width: 1 } });
  s.addText('«Revenue Operating System» — مقولة فئوية مصاغة لأول مرة لقطاع اللوجستيات', {
    x: 0.8, y: 2.85, w: W - 1.6, h: 0.5,
    fontFace: FS, fontSize: 14, italic: true, color: C.gold, align: 'right', rtlMode: true,
  });
  s.addText('ديلكس يوحّد اكتشاف العملاء، وتأهيلهم، والتواصل معهم، وإغلاق الصفقات، والتحليل — في منصة واحدة مصمّمة للبيئة العربية والخليجية', {
    x: 0.8, y: 3.35, w: W - 1.6, h: 0.6,
    fontFace: FB, fontSize: 15, color: C.onDark, align: 'right', rtlMode: true, valign: 'middle',
  });

  // 3 pillars — Arabic first, English second (per audit B2)
  const pillars = [
    { ar: 'الذكاء', en: 'Intelligence', d: 'اكتشاف التندرات وتأهيل العملاء من 8+ مصادر محلية وخليجية، بتحليل عربي وإنجليزي أصلي' },
    { ar: 'التواصل', en: 'Engagement', d: 'WhatsApp · SMS · Email · LinkedIn · Voice — كل القنوات مدموجة مع وكيل ذكاء اصطناعي عربي' },
    { ar: 'التنفيذ', en: 'Execution', d: 'خط مبيعات بصري + إعداد عروض آلي + تكاملات TMS/WMS/ERP + تقارير تنفيذية للمدير العام' },
  ];
  const pW = (W - 1.2 - 0.4) / 3;
  pillars.forEach((p, i) => {
    const x = W - 0.6 - (i + 1) * pW - i * 0.2;
    const y = 4.4;
    s.addShape('rect', { x, y, w: pW, h: 2.2, fill: { color: C.navyDeep }, line: { color: C.gold, width: 0.75 } });
    // Arabic first (top label)
    s.addText(p.ar + ' · ' + p.en, {
      x: x + 0.2, y: y + 0.15, w: pW - 0.4, h: 0.4,
      fontFace: FH, fontSize: 12, color: C.gold, align: 'right', rtlMode: true, bold: true,
    });
    // Arabic hero name
    s.addText(p.ar, {
      x: x + 0.2, y: y + 0.55, w: pW - 0.4, h: 0.65,
      fontFace: FH, fontSize: 28, bold: true, color: C.onDark, align: 'right', rtlMode: true,
    });
    s.addShape('rect', { x: x + pW - 0.75, y: y + 1.2, w: 0.5, h: 0.025, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(p.d, {
      x: x + 0.2, y: y + 1.3, w: pW - 0.4, h: 0.85,
      fontFace: FB, fontSize: 11, color: C.onDarkMuted, align: 'right', rtlMode: true, valign: 'top',
    });
  });

  s.addNotes(
    'هذه الشريحة تُعرّف الفئة — وليست المنتج فقط. المصطلح «Revenue Operating System» جديد على السوق العربي، واستخدامه مقصود لرفع التموضع. ' +
    'الركائز الثلاث (الذكاء / التواصل / التنفيذ) هي البنية المعمارية التي سنعود إليها في كل القسم الثالث. ' +
    'اذكر أن ديلكس ليس CRM ولا أداة تسويق ولا حتى Sales Engagement — هو كل ذلك مدموجاً مع طبقة ذكاء اصطناعي عربية. ' +
    'الانتقال للشريحة القادمة: «دعونا نرى الرحلة الكاملة في سبع خطوات».'
  );
})();

// =================== SLIDE 10 — 7 PILLARS FLOW ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'معمارية المنتج', 10);

  titleAR(s, 'سبع ركائز — من الاكتشاف إلى التحليل');
  subtitleAR(s, 'رحلة إيراد متكاملة: اكتشف · أهّل · تواصل · اجدول · أغلق · احتفظ · حلّل');

  // Label order: Arabic · English (per audit B2)
  const steps = [
    { n: '1', t: 'اكتشف · Discover', d: '8+ مصادر تندرات وعملاء' },
    { n: '2', t: 'أهّل · Qualify', d: 'ذكاء اصطناعي يصنّف حسب حجم الفرصة' },
    { n: '3', t: 'تواصل · Engage', d: 'Omnichannel مع وكيل عربي' },
    { n: '4', t: 'اجدول · Schedule', d: 'حجز مواعيد ذكي + تقويم تنفيذي' },
    { n: '5', t: 'أغلق · Close', d: 'إعداد عرض آلي + توقيع إلكتروني' },
    { n: '6', t: 'احتفظ · Retain', d: 'تجديد تلقائي + إدارة حسابات' },
    { n: '7', t: 'حلّل · Analyze', d: 'لوحات تنفيذية + إسناد إيراد' },
  ];

  const stepW = (W - 1.2 - 0.3 * 6) / 7;
  const stepY = 3.0;
  const stepH = 3.2;
  steps.forEach((st, i) => {
    const x = W - 0.6 - (i + 1) * stepW - i * 0.3;
    s.addShape('roundRect', { x, y: stepY, w: stepW, h: stepH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 }, rectRadius: 0.08 });
    s.addShape('ellipse', { x: x + stepW / 2 - 0.3, y: stepY - 0.3, w: 0.6, h: 0.6, fill: { color: C.navy }, line: { color: C.gold, width: 1.5 } });
    s.addText(st.n, {
      x: x + stepW / 2 - 0.3, y: stepY - 0.3, w: 0.6, h: 0.6,
      fontFace: FH, fontSize: 18, bold: true, color: C.gold, align: 'center', valign: 'middle',
    });
    s.addText(st.t, {
      x: x + 0.1, y: stepY + 0.5, w: stepW - 0.2, h: 0.9,
      fontFace: FH, fontSize: 11, bold: true, color: C.navy, align: 'center', rtlMode: true, valign: 'top',
    });
    s.addShape('rect', { x: x + stepW / 2 - 0.3, y: stepY + 1.4, w: 0.6, h: 0.02, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(st.d, {
      x: x + 0.1, y: stepY + 1.55, w: stepW - 0.2, h: 1.5,
      fontFace: FB, fontSize: 10, color: C.textMuted, align: 'center', rtlMode: true, valign: 'top',
    });
    if (i < steps.length - 1) {
      const connX = x - 0.25;
      s.addShape('rightTriangle', {
        x: connX + 0.05, y: stepY + stepH / 2 - 0.1, w: 0.15, h: 0.2,
        fill: { color: C.gold }, line: { type: 'none' }, flipH: true, rotate: 180,
      });
    }
  });

  s.addText('الدورة مغلقة: كل عقد يُغلق يعود كبيانات تدريب للذكاء الاصطناعي — فيتحسّن النظام مع كل صفقة', {
    x: 0.6, y: 6.5, w: W - 1.2, h: 0.4,
    fontFace: FS, fontSize: 13, italic: true, color: C.textMuted, align: 'right', rtlMode: true,
  });

  s.addNotes(
    'استخدم هذه الشريحة كخريطة مرجعية. كل ركيزة من السبع ستحصل على شريحة تفصيلية لاحقاً. ' +
    'النقطة الحاسمة: معظم شركات CRM تغطي 3-4 ركائز فقط. ديلكس يغطي السبع بوحدة تصميم واحدة. ' +
    'لا تقض وقتاً طويلاً هنا — الشريحة للخريطة الذهنية فقط. ' +
    'انتقل إلى Lead Intelligence Engine V2 في الشريحة التالية.'
  );
})();

console.log('[slides 1-10] defined');
