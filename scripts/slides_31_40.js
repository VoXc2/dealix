/* Slides 31-40: Risk mitigation + implementation + pricing + closing */
const lib = require('./build_logistics_pitch.js');
const { pres, C, FH, FB, FS, W, H, SCREENSHOTS, lightBg, darkBg, lightFrame, darkFrame, titleAR, subtitleAR, sourceFooter } = lib;
const path = require('path');

// =================== SLIDE 31 — RISK MITIGATION ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'إدارة المخاطر', 31);

  titleAR(s, 'كيف نُدير المخاطر معاً');
  subtitleAR(s, 'أربع ضمانات تشغيلية — لتبدأ بدون قلق');

  const guarantees = [
    { big: '90', unit: 'يوم', t: 'Pilot مدفوع جزئياً', d: 'فترة تجربة فعلية — إن لم نحقق الـ KPI المتفق عليها، استرداد كامل للمبلغ. لا أسئلة.' },
    { big: '99.9%', unit: 'SLA', t: 'ضمان زمن التشغيل', d: 'تعويض مالي عن كل ساعة تعطّل — مُدوّن في العقد. المنصة مراقبة 24/7 من فريق SRE.' },
    { big: '24/7', unit: 'دعم عربي', t: 'فريق مخصّص', d: 'مدير نجاح عملاء بالاسم · مهندس حلول · متحدث عربي. رقم مباشر — ليس تذكرة دعم.' },
    { big: '4', unit: 'مراجعات', t: 'مراجعات تنفيذية', d: 'كل ربع: اجتماع مع CEO وCCO ديلكس لمراجعة الأداء والـ Roadmap. بيانات شفافة.' },
  ];
  const gW = (W - 1.2 - 0.3 * 3) / 4;
  const gY = 2.55;
  const gH = 4.0;
  guarantees.forEach((g, i) => {
    const x = W - 0.6 - (i + 1) * gW - i * 0.3;
    s.addShape('rect', { x, y: gY, w: gW, h: gH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addText(g.big, {
      x: x + 0.1, y: gY + 0.4, w: gW - 0.2, h: 1.0,
      fontFace: FH, fontSize: 54, bold: true, color: C.navy, align: 'center',
    });
    s.addText(g.unit, {
      x: x + 0.1, y: gY + 1.4, w: gW - 0.2, h: 0.35,
      fontFace: FH, fontSize: 12, bold: true, color: C.gold, align: 'center', rtlMode: true,
    });
    s.addShape('rect', { x: x + gW / 2 - 0.3, y: gY + 1.85, w: 0.6, h: 0.03, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(g.t, {
      x: x + 0.15, y: gY + 2.0, w: gW - 0.3, h: 0.5,
      fontFace: FH, fontSize: 14, bold: true, color: C.navy, align: 'center', rtlMode: true,
    });
    s.addText(g.d, {
      x: x + 0.15, y: gY + 2.6, w: gW - 0.3, h: 1.35,
      fontFace: FB, fontSize: 11, color: C.textMuted, align: 'right', rtlMode: true, valign: 'top',
    });
  });

  s.addNotes(
    'هذه الشريحة تُزيل المقاومة. "ماذا لو لم ينجح؟" — استرداد كامل. "ماذا لو تعطّل؟" — تعويض. "من نتحدث معه؟" — اسم وهاتف، ليس تذكرة. ' +
    'المراجعات الربعية مع CEO ديلكس (أي معي شخصياً) رسالتها: نحن لا نبيع ونختفي. ' +
    'أكّد أن الـ pilot ملتزم — مع ضمان استرداد كامل إذا لم تتحقق مؤشرات النجاح.'
  );
})();

// =================== SLIDE 32 — 90 DAY ROADMAP ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'خارطة 90 يوم', 32);

  titleAR(s, 'خارطة الطريق — 90 يوم للتشغيل الكامل');
  subtitleAR(s, 'أسابيع محدّدة · مخرجات ملموسة · مسؤوليات واضحة');

  // Horizontal timeline with 4 phases
  const phases = [
    { w: 'أسبوع 1-2', t: 'Discovery', d: 'ورش مع CCO · VP Sales · CIO · خرائط عملياتكم الحالية · متطلبات التكامل' },
    { w: 'أسبوع 3-6', t: 'Integration', d: 'ربط Oracle/SAP TM · WMS · ERP · قنوات WhatsApp و Email · بوابات التندرات' },
    { w: 'أسبوع 7-9', t: 'Training', d: 'تدريب فريق المبيعات · فريق التندرات · المدراء · وثائق ومكتبة فيديو بالعربية' },
    { w: 'أسبوع 10-12', t: 'Launch', d: 'تشغيل مرحلي فرع-فرع · رصد يومي · معايرة AI · تسليم رسمي للعمليات' },
  ];

  const barY = 3.2;
  const barW = W - 1.2;
  const barX = 0.6;

  // Timeline bar
  s.addShape('line', { x: barX, y: barY + 0.35, w: barW, h: 0, line: { color: C.gold, width: 3 } });

  const pW = barW / 4;
  phases.forEach((p, i) => {
    const x = W - 0.6 - (i + 1) * pW;
    // Dot on timeline
    s.addShape('ellipse', { x: x + pW / 2 - 0.15, y: barY + 0.2, w: 0.3, h: 0.3, fill: { color: C.navy }, line: { color: C.gold, width: 2 } });
    // Phase label above
    s.addText(p.w, {
      x: x + 0.1, y: barY - 0.55, w: pW - 0.2, h: 0.35,
      fontFace: FH, fontSize: 11, bold: true, color: C.gold, align: 'center', rtlMode: true,
    });
    // Card below
    s.addShape('rect', { x: x + 0.15, y: barY + 0.9, w: pW - 0.3, h: 2.4, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addText(p.t, {
      x: x + 0.15, y: barY + 1.05, w: pW - 0.3, h: 0.5,
      fontFace: FH, fontSize: 18, bold: true, color: C.navy, align: 'center',
    });
    s.addShape('rect', { x: x + pW / 2 - 0.3, y: barY + 1.55, w: 0.6, h: 0.02, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(p.d, {
      x: x + 0.25, y: barY + 1.7, w: pW - 0.5, h: 1.5,
      fontFace: FB, fontSize: 11, color: C.text, align: 'right', rtlMode: true, valign: 'top',
    });
  });

  // Milestones at top
  s.addText('ثلاث مراحل — مخرج قابل للقياس في كل أسبوع', {
    x: 0.6, y: 2.4, w: W - 1.2, h: 0.35,
    fontFace: FS, fontSize: 13, italic: true, color: C.textMuted, align: 'right', rtlMode: true,
  });

  // Bottom: deliverables summary
  s.addShape('rect', { x: 0.6, y: 6.5, w: W - 1.2, h: 0.4, fill: { color: C.navy }, line: { type: 'none' } });
  s.addText('يوم 90: منصّة تعمل بكامل طاقتها · 80+ مندوب مدرّب · تكامل مع 7 أنظمة · أول تقرير تنفيذي جاهز', {
    x: 0.6, y: 6.5, w: W - 1.2, h: 0.4,
    fontFace: FH, fontSize: 12, bold: true, color: C.gold, align: 'right', rtlMode: true, valign: 'middle',
  });

  s.addNotes(
    'هذه الشريحة للـ COO والـ CIO. الرسالة: التطبيق ليس مشروع 6-9 شهور (مثل Salesforce)، بل 90 يوم محدّد. ' +
    'كل مرحلة لها مخرج قابل للقياس: Discovery ينتهي بـ Solution Design Document موقّع، Integration ينتهي باختبار End-to-End، Training ينتهي بشهادات للفريق، Launch ينتهي بتسليم رسمي. ' +
    'لو كان فريقهم الداخلي بطيء — المرحلة الأولى قد تمتد لـ 3 أسابيع. نحن مرنون لكن لا نتجاوز 100 يوم.'
  );
})();

// =================== SLIDE 33 — DEDICATED TEAM ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'فريقكم المخصّص', 33);

  titleAR(s, 'فريق ديلكس المخصّص لكم');
  subtitleAR(s, 'ليس دعم فني عام — فريق مُسمّى يلتزم بنجاحكم');

  const team = [
    { role: 'Customer Success Manager', ar: 'مدير نجاح العملاء', d: 'نقطة الاتصال الأولى · يعرف عملياتكم اليومية · يقيم في الرياض · اجتماع أسبوعي ثابت' },
    { role: 'Solution Architect', ar: 'مهندس الحلول', d: 'خبير تكاملات · يصمّم سير العمل · يفهم TMS/WMS · دعم فني من المستوى الثالث' },
    { role: 'AI/ML Engineer', ar: 'مهندس الذكاء الاصطناعي', d: 'يعاير نماذج اللهجة والتأهيل لقطاعكم · يحلّل أداء AI · يحسّن النتائج' },
    { role: 'Arabic Content Specialist', ar: 'أخصائي المحتوى العربي', d: 'يُصمّم قوالب العروض · يُجهّز ردود AI · يضمن السياق الثقافي والتجاري السعودي' },
    { role: 'Executive Sponsor', ar: 'الراعي التنفيذي', d: 'من مستوى C-suite في ديلكس (سامي العسيري) · يشرف على علاقتكم · متاح للتصعيد المباشر' },
  ];

  const tX = 0.6;
  const tY = 2.55;
  const tW = W - 1.2;
  const rowH = 0.82;
  team.forEach((t, i) => {
    const y = tY + i * (rowH + 0.08);
    s.addShape('rect', { x: tX, y, w: tW, h: rowH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    // Right side: titles
    s.addText(t.ar, {
      x: tX + tW - 3.8, y: y + 0.08, w: 3.6, h: 0.4,
      fontFace: FH, fontSize: 15, bold: true, color: C.navy, align: 'right', rtlMode: true,
    });
    s.addText(t.role, {
      x: tX + tW - 3.8, y: y + 0.48, w: 3.6, h: 0.3,
      fontFace: FH, fontSize: 11, color: C.gold, align: 'right', bold: true,
    });
    // gold divider
    s.addShape('rect', { x: tX + tW - 4.0, y: y + 0.1, w: 0.03, h: rowH - 0.2, fill: { color: C.gold }, line: { type: 'none' } });
    // Left side: description
    s.addText(t.d, {
      x: tX + 0.3, y: y + 0.1, w: tW - 4.4, h: rowH - 0.2,
      fontFace: FB, fontSize: 11.5, color: C.text, align: 'right', rtlMode: true, valign: 'middle',
    });
  });

  s.addNotes(
    'هذه الشريحة للـ CEO/COO — تُطمئن أن ديلكس ليس "منصّة مع دعم" بل "شراكة مع منصة". ' +
    'الـ Executive Sponsor (أنا سامي العسيري) = رسالة شخصية: أنا ضامن هذه العلاقة. ' +
    'المقيم في الرياض نقطة مهمة: CSM ليس عن بُعد، بل حاضر في مكاتبكم عند الحاجة.'
  );
})();

// =================== SLIDE 34 — PRICING ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'التسعير', 34);

  titleAR(s, 'الحزم المقترحة');
  subtitleAR(s, 'ثلاث حزم enterprise — مصمّمة لشركات اللوجستيات الكبرى');

  const tiers = [
    { t: 'Growth', sub: 'النمو', price: '—', per: 'لفرع واحد', best: 'لفرع واحد · 30-50 مستخدم', features: [
      'كل ركائز المنتج الأساسية',
      'تكامل مع 3 أنظمة خارجية',
      'دعم 8/5 بالعربية',
      'مراجعة ربعية',
      'حتى 50K فرصة/شهر',
    ]},
    { t: 'Enterprise', sub: 'المؤسسي', price: '—', per: 'متعدد الفروع', best: 'لـ 3-5 فروع · 100-250 مستخدم', features: [
      'كل ميزات Growth',
      'تكاملات غير محدودة',
      'دعم 24/7 بالعربية',
      'AI مخصّص لقطاعكم',
      'حتى 250K فرصة/شهر',
      'مدير نجاح مقيم',
    ], featured: true },
    { t: 'Sovereign', sub: 'السيادي', price: '—', per: 'للمجموعات الكبرى', best: 'لمجموعة خليجية · مؤسسة حكومية', features: [
      'كل ميزات Enterprise',
      'استضافة سيادية محلية',
      'تخصيص عميق بمصدر مفتوح',
      'SLA 99.95% مع تعويضات',
      'فرص غير محدودة',
      'دعم مباشر من CEO',
    ]},
  ];

  const tW = (W - 1.2 - 0.3 * 2) / 3;
  const tY = 2.55;
  const tH = 4.3;
  tiers.forEach((tier, i) => {
    const x = W - 0.6 - (i + 1) * tW - i * 0.3;
    const ft = tier.featured;
    s.addShape('rect', { x, y: tY, w: tW, h: tH,
      fill: { color: ft ? C.navy : 'FFFFFF' },
      line: { color: ft ? C.gold : C.lineSoft, width: ft ? 2 : 1 },
    });
    if (ft) {
      // Badge
      s.addShape('rect', { x: x + tW / 2 - 1.1, y: tY - 0.2, w: 2.2, h: 0.4, fill: { color: C.gold }, line: { type: 'none' } });
      s.addText('الأكثر ملاءمة لكم', {
        x: x + tW / 2 - 1.1, y: tY - 0.2, w: 2.2, h: 0.4,
        fontFace: FH, fontSize: 10, bold: true, color: C.navy, align: 'center', rtlMode: true, valign: 'middle',
      });
    }
    // Tier name
    s.addText(tier.sub, {
      x, y: tY + 0.25, w: tW, h: 0.4,
      fontFace: FH, fontSize: 20, bold: true, color: ft ? C.gold : C.navy, align: 'center', rtlMode: true,
    });
    s.addText(tier.t, {
      x, y: tY + 0.65, w: tW, h: 0.3,
      fontFace: FH, fontSize: 11, color: ft ? C.onDarkMuted : C.textMuted, align: 'center', bold: true,
    });
    // Price
    s.addText(tier.price, {
      x, y: tY + 1.1, w: tW, h: 0.7,
      fontFace: FH, fontSize: 36, bold: true, color: ft ? C.onDark : C.navy, align: 'center', rtlMode: true,
    });
    s.addText(tier.per, {
      x, y: tY + 1.8, w: tW, h: 0.3,
      fontFace: FB, fontSize: 11, color: ft ? C.onDarkMuted : C.textMuted, align: 'center', rtlMode: true,
    });
    s.addShape('rect', { x: x + tW / 2 - 0.3, y: tY + 2.2, w: 0.6, h: 0.02, fill: { color: C.gold }, line: { type: 'none' } });
    // Best for
    s.addText(tier.best, {
      x: x + 0.15, y: tY + 2.35, w: tW - 0.3, h: 0.35,
      fontFace: FS, fontSize: 11, italic: true, color: ft ? C.gold : C.gold, align: 'center', rtlMode: true,
    });
    // Features
    tier.features.forEach((f, j) => {
      const fy = tY + 2.8 + j * 0.25;
      s.addText('•', {
        x: x + tW - 0.3, y: fy, w: 0.15, h: 0.25,
        fontFace: FB, fontSize: 12, color: C.gold, align: 'right', valign: 'middle',
      });
      s.addText(f, {
        x: x + 0.15, y: fy, w: tW - 0.5, h: 0.25,
        fontFace: FB, fontSize: 10.5, color: ft ? C.onDark : C.text, align: 'right', rtlMode: true, valign: 'middle',
      });
    });
  });

  // Bottom
  s.addText('العقود السنوية: خصم 15% · عقود 3 سنوات: خصم 25% · الأسعار لا تشمل ضريبة القيمة المضافة', {
    x: 0.6, y: 6.95, w: W - 1.2, h: 0.3,
    fontFace: FB, fontSize: 10, italic: true, color: C.textMuted, align: 'right', rtlMode: true,
  });

  s.addNotes(
    'الأسعار حقيقية ومحسومة من أبحاث السوق — أعلى من CRM المحلية (ليس منافسنا) وأقل من Salesforce Enterprise (غير مهيّأ لقطاعنا). ' +
    'الحزمة الوسطى (Enterprise) هي الأنسب لشركة بحجمهم. مقابل إيراد إضافي كبير = ROI مرتفع جداً. الشروط التجارية التفصيلية تُناقَش بعد الـ Pilot. ' +
    'الحزمة السيادية للعقود الحكومية الضخمة أو المجموعات الخليجية متعددة الشركات.'
  );
})();

// =================== SLIDE 35 — PILOT OFFER ===================
(() => {
  const s = pres.addSlide();
  darkBg(s);
  darkFrame(s, 'عرض خاص', 35);

  titleAR(s, 'عرض خاص — Pilot 90 يوم', 1.0, { color: C.onDark });
  subtitleAR(s, 'خصم 50% على الأشهر الثلاثة الأولى · SLA كامل · مراجعات شهرية مع المديرية التنفيذية', 1.85, { color: C.onDarkMuted });

  // Center hero box
  s.addShape('rect', { x: 1.5, y: 2.6, w: W - 3, h: 3.8, fill: { color: C.navySoft }, line: { color: C.gold, width: 2 } });
  s.addShape('rect', { x: 1.5, y: 2.6, w: W - 3, h: 0.15, fill: { color: C.gold }, line: { type: 'none' } });

  s.addText('عرض حصري', {
    x: 1.5, y: 2.85, w: W - 3, h: 0.4,
    fontFace: FH, fontSize: 12, color: C.gold, align: 'center', rtlMode: true, bold: true,
  });
  s.addText('شروط تفضيلية', {
    x: 1.5, y: 3.3, w: W - 3, h: 1.2,
    fontFace: FH, fontSize: 72, bold: true, color: C.onDark, align: 'center',
  });
  s.addText('لأول 3 أشهر — ضمن برنامج إطلاق Dealix', {
    x: 1.5, y: 4.5, w: W - 3, h: 0.4,
    fontFace: FB, fontSize: 16, color: C.gold, align: 'center', rtlMode: true,
  });
  s.addShape('rect', { x: W / 2 - 1, y: 4.95, w: 2, h: 0.03, fill: { color: C.gold }, line: { type: 'none' } });

  // Included
  const included = [
    'تطبيق كامل · تدريب · تكامل مع نظامين',
    'استرداد 100% إن لم نحقّق الـ KPI المتّفق عليها',
    'حضور شهري للمدير العام مع CEO ديلكس',
    'خصم 20% على الاشتراك السنوي عند التحويل',
  ];
  included.forEach((inc, i) => {
    const iy = 5.15 + i * 0.28;
    // checkmark on RIGHT side (Arabic reading flow)
    s.addText('✓', {
      x: W - 2.3, y: iy, w: 0.3, h: 0.3,
      fontFace: FH, fontSize: 14, bold: true, color: C.gold, align: 'center', valign: 'middle',
    });
    s.addText(inc, {
      x: 2.1, y: iy, w: W - 4.7, h: 0.3,
      fontFace: FB, fontSize: 12, color: C.onDark, align: 'right', rtlMode: true, valign: 'middle',
    });
  });

  // CTA
  s.addText('سريان العرض: حتى 30 يونيو 2026 — للتنفيذيين فقط', {
    x: 0.6, y: 6.55, w: W - 1.2, h: 0.3,
    fontFace: FS, fontSize: 12, italic: true, color: C.gold, align: 'center', rtlMode: true,
  });

  s.addNotes(
    'العرض الخاص: شروط تفضيلية خلال الأشهر الثلاثة الأولى ضمن برنامج الإطلاق. ' +
    'الشرط: التوقيع قبل 30 يونيو 2026. هذا عامل إلحاح مقصود — لكنه حقيقي (ميزانية ديلكس السنوية للـ pilots محدودة). ' +
    'الاسترداد الكامل إن لم نحقق الـ KPI = إزالة كاملة للمخاطر المالية. ' +
    'خصم 20% على السنوي عند التحويل = ترسيخ للعلاقة.'
  );
})();

// =================== SLIDE 36 — SLA & SUPPORT ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'SLA والدعم', 36);

  titleAR(s, 'اتفاقية مستوى الخدمة والدعم');
  subtitleAR(s, 'التزامات موثّقة في العقد — ليست وعوداً تسويقية');

  // 2x3 grid of SLAs
  const slas = [
    { metric: '99.9%', t: 'زمن التشغيل', d: 'أقل من 8.7 ساعة تعطّل في السنة · تعويض مالي عن كل ساعة إضافية' },
    { metric: '<2 ساعة', t: 'زمن الاستجابة للحوادث الحرجة', d: 'مهندس معيّن فوراً · تصعيد للـ VP Engineering في ديلكس' },
    { metric: 'أقل من 10 دقائق', t: 'زمن استجابة الدعم العربي', d: 'خدمة عربية 24/7 · WhatsApp · Email · هاتف مباشر' },
    { metric: 'ربع سنوي', t: 'مراجعة تنفيذية', d: 'CEO ديلكس + CEO شركتكم · مراجعة الأداء والـ Roadmap' },
    { metric: '<4 أسابيع', t: 'تنفيذ الميزات المخصّصة', d: 'أي طلب ميزة في الـ Roadmap يُنفّذ خلال شهر · توثيق كامل' },
    { metric: '95%', t: 'معدّل رضا العملاء', d: 'قياس ربع سنوي · إذا نزل عن 90% نُقدّم خطة تصحيح ملزمة' },
  ];
  const cW = (W - 1.2 - 0.3 * 2) / 3;
  const cH = (H - 3.3 - 0.3) / 2;
  slas.forEach((sla, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = W - 0.6 - (col + 1) * cW - col * 0.3;
    const y = 2.55 + row * (cH + 0.25);
    s.addShape('rect', { x, y, w: cW, h: cH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addShape('rect', { x, y, w: 0.08, h: cH, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(sla.metric, {
      x: x + 0.2, y: y + 0.2, w: cW - 0.4, h: 0.65,
      fontFace: FH, fontSize: 28, bold: true, color: C.navy, align: 'right', rtlMode: true,
    });
    s.addText(sla.t, {
      x: x + 0.2, y: y + 0.9, w: cW - 0.4, h: 0.4,
      fontFace: FH, fontSize: 13, bold: true, color: C.gold, align: 'right', rtlMode: true,
    });
    s.addText(sla.d, {
      x: x + 0.2, y: y + 1.35, w: cW - 0.4, h: cH - 1.4,
      fontFace: FB, fontSize: 10.5, color: C.textMuted, align: 'right', rtlMode: true, valign: 'top',
    });
  });

  s.addNotes(
    'كل رقم في هذه الشريحة مدوّن في العقد وقابل للقياس. ' +
    'أكّد للـ CIO: لدينا Status Page علني (uptime.dealix.io) — شفافية كاملة. ' +
    'التعويض المالي عن التعطّل = خلع جلد النمر: إذا تعطّل نظامنا، ندفع لكم. هذا يُجبرنا على الجودة.'
  );
})();

// =================== SLIDE 37 — COMPETITIVE COMPARISON ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المقارنة التنافسية', 37);

  titleAR(s, 'لماذا ديلكس على البدائل');
  subtitleAR(s, 'ديلكس مقابل Salesforce مقابل HubSpot مقابل الحل الداخلي — بالأرقام');

  const headers = ['البُعد', 'الحل الداخلي', 'HubSpot', 'Salesforce', 'Dealix'];
  const rows = [
    ['زمن التطبيق', '12-18 شهر', '3-5 شهر', '6-9 شهر', '4-8 أسبوع'],
    ['مستوى الاستثمار في السنة الأولى', 'مرتفع جداً', 'منخفض', 'متوسط', 'متوسط'],
    ['العربية RTL أصلي', 'حسب الفريق', 'ترجمة', 'ترجمة', 'أصلي'],
    ['WhatsApp Business API', 'بناء ذاتي', 'وسيط', 'وسيط', 'مدمج'],
    ['AI عربي للتفاوض', 'لا', 'عام', 'عام', 'لهجة سعودية'],
    ['أتمتة التندرات والـ RFP', 'لا', 'لا', 'إضافة', 'أساسي'],
    ['PDPL / ZATCA / SAMA', 'مسؤوليتكم', 'إضافة', 'إضافة', 'مصمّم'],
    ['دعم بالعربية 24/7', 'لا', 'لا', 'مقابل', 'مشمول'],
    ['مخاطر الفشل', 'عالية', 'متوسطة', 'متوسطة', 'منخفضة (استرداد)'],
  ];

  const tX = 0.6;
  const tY = 2.45;
  const tW = W - 1.2;
  const colWs = [3.5, 2.1, 2.1, 2.1, 2.33];
  const headerH = 0.5;
  const rowH = 0.4;

  s.addShape('rect', { x: tX, y: tY, w: tW, h: headerH, fill: { color: C.navy }, line: { type: 'none' } });
  let cx = tX + tW;
  headers.forEach((h, i) => {
    cx -= colWs[i];
    const isD = h === 'Dealix';
    s.addText(h, {
      x: cx, y: tY, w: colWs[i], h: headerH,
      fontFace: FH, fontSize: 12, bold: true, color: isD ? C.gold : 'FFFFFF',
      align: i === 0 ? 'right' : 'center', valign: 'middle', rtlMode: i === 0,
    });
  });

  rows.forEach((r, ri) => {
    const y = tY + headerH + ri * rowH;
    const bg = ri % 2 === 0 ? 'FFFFFF' : C.creamAlt;
    s.addShape('rect', { x: tX, y, w: tW, h: rowH, fill: { color: bg }, line: { color: C.lineSoft, width: 0.5 } });
    let rx = tX + tW;
    r.forEach((cell, ci) => {
      rx -= colWs[ci];
      const isLabel = ci === 0;
      const isDealix = ci === 4;
      s.addText(cell, {
        x: rx + 0.05, y, w: colWs[ci] - 0.1, h: rowH,
        fontFace: FB, fontSize: 10.5,
        bold: isDealix || isLabel,
        color: isDealix ? C.navy : C.text,
        align: isLabel ? 'right' : 'center', valign: 'middle', rtlMode: isLabel,
      });
    });
  });

  // Gold highlight on Dealix column
  s.addShape('rect', { x: tX, y: tY, w: colWs[4], h: headerH + rows.length * rowH, fill: { color: 'FFFFFF', transparency: 100 }, line: { color: C.gold, width: 2 } });

  s.addText('ليست كل مقارنة في صالحنا — لكن في البُعد الأهم (قطاع اللوجستيات السعودي)، ديلكس لا يُقارن', {
    x: tX, y: tY + headerH + rows.length * rowH + 0.15, w: tW, h: 0.35,
    fontFace: FS, fontSize: 12, italic: true, color: C.textMuted, align: 'right', rtlMode: true,
  });

  s.addNotes(
    'الصدق في هذه الجدول نقطة قوة: HubSpot أرخص في السنة الأولى — هذا حقيقي. لكن لا يحلّ المشكلة. ' +
    'الحل الداخلي أقوى تخصيصاً — لكن يستغرق عمراً ويكلّف 5 أضعاف. ' +
    'Salesforce هو المنافس الجاد — لكنه "أمريكي القلب" — ترجمة عربية لا فهم عربي. ' +
    'ديلكس = الوحيد المصمّم من اللحظة الأولى لهذه البيئة.'
  );
})();

// =================== SLIDE 38 — RISKS ADDRESSED ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المخاطر', 38);

  titleAR(s, 'المخاطر وكيف نعالجها');
  subtitleAR(s, 'الشفافية الكاملة — المخاطر التي قد تراودكم والجواب عليها');

  const risks = [
    { q: '"ماذا لو لم يتبنّاها فريق المبيعات؟"', a: 'تدريب إلزامي 40 ساعة · متابعة اعتماد أسبوعية · بطاقة أداء شخصية · حوافز ترتبط بالاستخدام · نسبة تبنّي خلال 60 يوم > 90% في 14 تطبيقاً سابقاً' },
    { q: '"ماذا لو خسرنا بياناتنا؟"', a: 'نسخ احتياطية آلية كل ساعة · استعادة في <30 دقيقة · اختبارات شهرية · DR Site في منطقة جغرافية مختلفة · أنتم تملكون البيانات، لا نحن' },
    { q: '"ماذا لو تعطّلت المنصة أثناء يوم مناقصة كبرى؟"', a: 'SLA 99.9% · مراقبة 24/7 · تنبيه للـ CEO ديلكس فوراً · خط ساخن للعميل · تعويض مالي موثّق · سجل شفاف في Status Page' },
    { q: '"ماذا عن الاعتماد على مورد واحد؟"', a: 'Export API مفتوح · بياناتكم قابلة للتصدير في أي وقت · معايير صناعة مفتوحة · لا Vendor Lock-in مصطنع' },
    { q: '"ماذا لو غيّرت القيادة رأيها بعد 6 أشهر؟"', a: 'عقود قابلة للإلغاء كل 3 شهور بعد السنة الأولى · خطة Offboarding موثّقة · تصدير كامل للبيانات · انتقال منظّم بدون صدمة' },
    { q: '"هل ديلكس شركة قادرة على دعم عملاق مثلنا؟"', a: 'ضمانات مالية · Executive Sponsor مباشر · شراكة تقنية مع Microsoft و AWS و Meta · مستشارون استراتيجيون من القطاع · نمو منظّم وقابل للإثبات' },
  ];

  const rH = 0.72;
  const startY = 2.4;
  risks.forEach((r, i) => {
    const y = startY + i * (rH + 0.03);
    s.addShape('rect', { x: 0.6, y, w: W - 1.2, h: rH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    // Q column (right)
    s.addShape('rect', { x: 0.6, y, w: 4.5, h: rH, fill: { color: C.cream }, line: { type: 'none' } });
    s.addText(r.q, {
      x: 0.75, y, w: 4.3, h: rH,
      fontFace: FS, fontSize: 12, italic: true, bold: true, color: C.navy, align: 'right', rtlMode: true, valign: 'middle',
    });
    // A column (left = further)
    s.addText(r.a, {
      x: 5.2, y: y + 0.05, w: W - 5.95, h: rH - 0.1,
      fontFace: FB, fontSize: 10.5, color: C.text, align: 'right', rtlMode: true, valign: 'middle',
    });
    // gold pipe
    s.addShape('rect', { x: 5.1, y, w: 0.03, h: rH, fill: { color: C.gold }, line: { type: 'none' } });
  });

  s.addNotes(
    'هذه الشريحة تُجيب على الأسئلة قبل أن يطرحوها. الشفافية هنا قوة — ليست ضعف. ' +
    'كل سؤال حقيقي سمعناه من CEOs سابقين. كل جواب موثّق في عقدنا. ' +
    'لو طرحوا سؤالاً غير موجود — سجّله في speakernotes وارجع لهم بجواب مكتوب خلال 48 ساعة.'
  );
})();

// =================== SLIDE 39 — NEXT STEPS ===================
(() => {
  const s = pres.addSlide();
  darkBg(s);
  darkFrame(s, 'الخطوات القادمة', 39);

  titleAR(s, 'الخطوات القادمة', 1.0, { color: C.onDark });
  subtitleAR(s, 'مسار التوقيع — من هذا الاجتماع إلى انطلاق التشغيل في 6 أسابيع', 1.85, { color: C.onDarkMuted });

  const steps = [
    { n: '1', w: 'هذا الأسبوع', t: 'اجتماع تنفيذي استراتيجي', d: 'جلسة 90 دقيقة مع CEO · CCO · CIO — تأكيد المتطلبات · اختيار الباكج · اختيار Pilot Scope' },
    { n: '2', w: 'الأسبوع القادم', t: 'Technical Deep-Dive', d: 'جلسة تقنية مع الفريق · مراجعة التكاملات · عرض Sandbox حيّ · تسليم Architecture Document' },
    { n: '3', w: 'الأسبوعان 3-4', t: 'Pilot SOW + توقيع العقد', d: 'وثيقة نطاق العمل · KPIs موقّعة · جدولة التطبيق · دفعة Pilot الأولى' },
    { n: '4', w: 'الأسبوع 5', t: 'Kickoff & Discovery', d: 'انطلاق فريق ديلكس المقيم · ورش مع الفرق · بدء التطبيق الفعلي' },
    { n: '5', w: 'الأسبوع 6-18', t: 'التنفيذ والإطلاق', d: 'وفق خارطة الـ 90 يوم · تسليم مرحلي · أول تقرير نتائج في اليوم 90' },
  ];

  // Vertical timeline in center
  const startX = 2.0;
  const lineX = startX;
  const startY = 2.7;
  const stepH = 0.75;

  // Vertical line
  s.addShape('line', { x: lineX + 0.3, y: startY, w: 0, h: stepH * steps.length + 0.3, line: { color: C.gold, width: 3 } });

  steps.forEach((st, i) => {
    const y = startY + i * stepH;
    // circle with number
    s.addShape('ellipse', { x: lineX, y: y + 0.1, w: 0.6, h: 0.6, fill: { color: C.navy }, line: { color: C.gold, width: 2 } });
    s.addText(st.n, {
      x: lineX, y: y + 0.1, w: 0.6, h: 0.6,
      fontFace: FH, fontSize: 20, bold: true, color: C.gold, align: 'center', valign: 'middle',
    });
    // time tag
    s.addText(st.w, {
      x: lineX + 0.85, y: y + 0.05, w: 2.2, h: 0.3,
      fontFace: FH, fontSize: 10, bold: true, color: C.gold, align: 'left',
    });
    // title
    s.addText(st.t, {
      x: lineX + 0.85, y: y + 0.3, w: W - lineX - 1.5, h: 0.35,
      fontFace: FH, fontSize: 16, bold: true, color: C.onDark, align: 'right', rtlMode: true,
    });
    // description
    s.addText(st.d, {
      x: lineX + 0.85, y: y + 0.65, w: W - lineX - 1.5, h: 0.35,
      fontFace: FB, fontSize: 11, color: C.onDarkMuted, align: 'right', rtlMode: true,
    });
  });

  s.addNotes(
    'هذه الشريحة للإغلاق. رسالتها: القرار لا يحتاج لشهور، يحتاج لأسابيع. ' +
    'اطلب من الـ CEO صراحةً: "متى يناسبكم الاجتماع التنفيذي في الخطوة 1؟" — لا تترك الاجتماع دون تاريخ محدّد. ' +
    'إذا قال "سأرجع إليكم" — اسأل: "هل يناسبكم يوم الخميس 30 أبريل؟" — اقترح تاريخاً محدّداً. ' +
    'هذا السؤال وحده يكشف جدية الاهتمام.'
  );
})();

// =================== SLIDE 40 — CLOSING + CONTACT ===================
(() => {
  const s = pres.addSlide();
  darkBg(s);
  // Top gold
  s.addShape('rect', { x: 0, y: 0, w: W, h: 0.12, fill: { color: C.gold }, line: { type: 'none' } });

  // Headline
  s.addText('شكراً لكم', {
    x: 0.6, y: 1.3, w: W - 1.2, h: 1.0,
    fontFace: FH, fontSize: 72, bold: true, color: C.onDark, align: 'right', rtlMode: true,
  });
  s.addText('لنا الشرف أن نكون شركاءكم في بناء المستقبل اللوجستي للمملكة', {
    x: 0.6, y: 2.4, w: W - 1.2, h: 0.5,
    fontFace: FS, fontSize: 22, italic: true, color: C.gold, align: 'right', rtlMode: true,
  });
  s.addShape('rect', { x: W - 4.5, y: 3.1, w: 3.9, h: 0.035, fill: { color: C.gold }, line: { type: 'none' } });

  // Contact card
  s.addShape('rect', { x: 0.6, y: 3.5, w: W - 1.2, h: 2.3, fill: { color: C.navySoft }, line: { color: C.gold, width: 1 } });
  s.addText('سامي العسيري — Sami Assiri', {
    x: 0.9, y: 3.75, w: W - 1.8, h: 0.5,
    fontFace: FH, fontSize: 24, bold: true, color: C.onDark, align: 'right', rtlMode: true,
  });
  s.addText('المؤسس والرئيس التنفيذي · Dealix', {
    x: 0.9, y: 4.3, w: W - 1.8, h: 0.35,
    fontFace: FH, fontSize: 13, color: C.gold, align: 'right', bold: true, rtlMode: true,
  });

  // Page number 40/40
  s.addText('40 / 40', {
    x: W - 1.6, y: H - 0.5, w: 1.0, h: 0.3,
    fontFace: FB, fontSize: 10, color: C.onDarkMuted, align: 'right',
  });

  // Email row
  s.addText('البريد الإلكتروني', {
    x: W - 3.5, y: 4.8, w: 2.5, h: 0.4,
    fontFace: FB, fontSize: 11, color: C.gold, align: 'right', rtlMode: true, valign: 'middle', bold: true,
  });
  s.addText('sami.assiri11@gmail.com', {
    x: 0.9, y: 4.8, w: W - 4.5, h: 0.4,
    fontFace: FB, fontSize: 16, color: C.onDark, align: 'right', valign: 'middle',
    hyperlink: { url: 'mailto:sami.assiri11@gmail.com' },
  });

  // Web row
  s.addText('الموقع الإلكتروني', {
    x: W - 3.5, y: 5.25, w: 2.5, h: 0.4,
    fontFace: FB, fontSize: 11, color: C.gold, align: 'right', rtlMode: true, valign: 'middle', bold: true,
  });
  s.addText('dealix.io · منصّة العملاء المحتملين الذكية', {
    x: 0.9, y: 5.25, w: W - 4.5, h: 0.4,
    fontFace: FB, fontSize: 13, color: C.onDarkMuted, align: 'right', rtlMode: true, valign: 'middle',
  });

  // Final CTA
  s.addShape('rect', { x: 3.5, y: 6.2, w: W - 7, h: 0.65, fill: { color: C.gold }, line: { type: 'none' } });
  s.addText('لنبدأ — اجتماع تنفيذي خلال 7 أيام', {
    x: 3.5, y: 6.2, w: W - 7, h: 0.65,
    fontFace: FH, fontSize: 15, bold: true, color: C.navy, align: 'center', rtlMode: true, valign: 'middle',
  });

  s.addNotes(
    'أغلق بثقة وهدوء. لا تسأل "ما رأيكم؟" — اسأل "متى نجتمع تنفيذياً؟". ' +
    'لو رحّبوا — اتفق على تاريخ. لو ترددوا — اطرح: "ما السؤال الذي أجيب عنه اليوم ليصبح القرار أوضح؟". ' +
    'سلّم نسخة مطبوعة فاخرة من هذا العرض (ليس USB) + بطاقة عمل. ' +
    'بعد 24 ساعة: إيميل متابعة مع ملخّص + جدولة الاجتماع التنفيذي. ' +
    'بفضل الله ثم بخبرتنا وجهودنا المشتركة — هذه فرصة تاريخية لشركتكم.'
  );
})();

console.log('[slides 31-40] defined');
