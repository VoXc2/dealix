"use client";

import Link from "next/link";
import { useRef } from "react";
import type { CSSProperties, PointerEvent as ReactPointerEvent } from "react";

const corporatePillars = [
  {
    label: "STRATEGY",
    title: "Strategy & Transformation",
    text: "نحوّل أهداف النمو والتحول إلى رهانات مرتبة، operating model، اقتصاديات واضحة وخارطة تنفيذ قابلة للقياس.",
    href: "/services#strategy",
  },
  {
    label: "SYSTEMS",
    title: "Systems & Automation",
    text: "نبني طبقات AI وautomation وintegrations فوق الأدوات الحالية بدل فرض استبدال CRM أو ERP أو قنوات العمل.",
    href: "/services#systems",
  },
  {
    label: "INTELLIGENCE",
    title: "Intelligence & Market Access",
    text: "Saudi market intelligence، opportunity radar، partner routes وB2B decision support مبنية على evidence لا على ضوضاء السوق.",
    href: "/services#intelligence",
  },
  {
    label: "PRODUCTS",
    title: "Products & Ventures",
    text: "نحوّل الأنماط المتكررة المثبتة إلى منتجات وبرمجيات وواجهات API وأصول معرفة قابلة للتوسع.",
    href: "/company#products",
  },
];

const publicNavLinks = [
  { href: "/company", label: "الشركة" },
  { href: "/services", label: "الخدمات" },
  { href: "/sectors", label: "القطاعات" },
  { href: "/products", label: "المنتجات" },
  { href: "/dealix-os", label: "Dealix OS" },
  { href: "/proof-vault", label: "Proof" },
];

const featuredSectors = [
  { name: "الحكومة والقطاع العام", en: "Government & B2G", href: "/sectors/government-b2g" },
  { name: "الإنشاءات وEPC", en: "Construction & EPC", href: "/sectors/construction-epc" },
  { name: "الصناعة والتصنيع", en: "Industrial & Manufacturing", href: "/sectors/industrial-manufacturing" },
  { name: "المالية وFinTech", en: "Finance, FinTech & Insurance", href: "/sectors/finance-fintech-insurance" },
  { name: "التجزئة والتجارة الإلكترونية", en: "Retail & E-commerce", href: "/sectors/retail-commerce-ecommerce" },
  { name: "السياحة والضيافة", en: "Tourism & Hospitality", href: "/sectors/tourism-hospitality" },
  { name: "اللوجستيات وسلاسل الإمداد", en: "Logistics & Supply Chain", href: "/sectors/logistics-supply-chain" },
  { name: "التقنية وSaaS", en: "Technology, SaaS & SI", href: "/sectors/technology-saas-si" },
];

const capabilityHighlights = [
  "Strategy & Transformation", "AI Agents & Workflow Automation", "Revenue & Commercial Operations",
  "Customer Operations", "Knowledge & Document Intelligence", "Data & Decision Intelligence",
  "Procurement & Tender Intelligence", "Integration & MCP", "AI Governance & Reliability",
  "Cybersecurity Operations Readiness", "Finance Operations & Fatoora Readiness", "Managed AI Operations",
  "Saudi Market & Partner Intelligence", "Dealix OS & Productization",
];

const valueBlocks = [
  { label: "Revenue", title: "حركة اقتصادية، لا نشاط شكلي", text: "نربط الاستراتيجية والإشارات التجارية بأقرب next action يمكن أن يحرك Qualified Problem ثم Quote ثم Verified Payment." },
  { label: "Proof", title: "الدليل قبل الادعاء", text: "نفرّق بين activity وdelivery وoutcome وCustomer Proof، ونبني baseline وreceipts يمكن مراجعتها." },
  { label: "Command", title: "قرار يومي محكوم", text: "Company Brain + Opportunity Graph + Action Queue + approvals تتحول إلى مسار قيادة واحد بدل جزر أدوات منفصلة." },
];

const executionPath = [
  { step: "01", title: "Execution Diagnostic", text: "نبدأ بمشكلة واحدة. نفصل evidence عن assumptions ونحدد أصغر تدخل يستحق الاختبار." },
  { step: "02", title: "Qualified Discovery", text: "نثبت أصحاب القرار، البيانات، النطاق، المخاطر ومعيار القبول قبل أي التزام تجاري." },
  { step: "03", title: "Customer-Specific Outcome Sprint", text: "ننفذ الحل الأنسب: Build / Adapt / Integrate / Partner، بنطاق وسعر خاص بالعميل بعد Discovery." },
  { step: "04", title: "Proof Review", text: "نقارن النتيجة بالـbaseline ونوثق ما تحرك وما لم يتحرك بدون تحويل demo أو synthetic evidence إلى Customer Proof." },
  { step: "05", title: "Dealix Runtime", text: "إذا ثبتت القيمة والتكرار، يمكن أن يدخل Dealix OS كطبقة تشغيل مستمرة للمراقبة والتنفيذ والإثبات والتحسين." },
];

const truthRules = [
  ["Research", "Relationship"], ["Public contact", "Consent"], ["Draft", "Sent"],
  ["Quote", "Invoice"], ["Invoice", "Payment"], ["Synthetic / Demo", "Customer Proof"],
];

const systemFlow = [
  { label: "SIGNAL", title: "إشارة حقيقية", text: "سوق، عميل، تشغيل، تنظيم أو بيانات" },
  { label: "DECISION", title: "قرار موثّق", text: "أولوية، owner، evidence، risk" },
  { label: "ACTION", title: "تنفيذ محكوم", text: "صلاحيات واضحة وموافقة عند الأفعال الحساسة" },
  { label: "PROOF", title: "إثبات قابل للمراجعة", text: "Baseline → Evidence → Outcome → Acceptance" },
];

const deferredSectionStyle = {
  contentVisibility: "auto",
  containIntrinsicSize: "auto 720px",
} as CSSProperties;

export function InteractiveHome() {
  const heroRef = useRef<HTMLDivElement>(null);
  const pointerFrameRef = useRef<number | null>(null);
  const founderEmail = process.env.NEXT_PUBLIC_FOUNDER_EMAIL ?? "sami.assiri11@gmail.com";
  const founderPhone = process.env.NEXT_PUBLIC_FOUNDER_PHONE?.trim() || "+966 59 778 8539";
  const founderPhoneHref = `tel:${founderPhone.replace(/[^+\d]/g, "")}`;

  function handlePointerMove(event: ReactPointerEvent<HTMLDivElement>) {
    if (event.pointerType !== "mouse" || pointerFrameRef.current !== null) return;
    const clientX = event.clientX;
    const clientY = event.clientY;
    pointerFrameRef.current = window.requestAnimationFrame(() => {
      pointerFrameRef.current = null;
      const hero = heroRef.current;
      if (!hero) return;
      const rect = hero.getBoundingClientRect();
      hero.style.setProperty("--dx-pointer-x", `${clientX - rect.left}px`);
      hero.style.setProperty("--dx-pointer-y", `${clientY - rect.top}px`);
    });
  }

  function handlePointerLeave() {
    if (pointerFrameRef.current !== null) {
      window.cancelAnimationFrame(pointerFrameRef.current);
      pointerFrameRef.current = null;
    }
    const hero = heroRef.current;
    if (!hero) return;
    hero.style.setProperty("--dx-pointer-x", "72%");
    hero.style.setProperty("--dx-pointer-y", "30%");
  }

  return (
    <div className="dx-home">
      <header className="dx-nav-wrap">
        <nav className="dx-nav" aria-label="التنقل الرئيسي">
          <Link href="/" className="dx-logo-link" aria-label="Dealix — الصفحة الرئيسية"><img src="/dealix-logo.svg" alt="Dealix — Saudi AI Systems Company" className="dx-logo" width={400} height={96} loading="eager" decoding="async" fetchPriority="high" /></Link>
          <div className="dx-nav-links" role="list">{publicNavLinks.map((link) => <Link key={link.href} href={link.href}>{link.label}</Link>)}</div>
          <div className="dx-nav-actions">
            <details className="dx-mobile-menu">
              <summary aria-label="فتح قائمة التنقل"><span aria-hidden="true">☰</span></summary>
              <div className="dx-mobile-menu-panel">
                {publicNavLinks.map((link) => <Link key={link.href} href={link.href}>{link.label}</Link>)}
                <Link href="/safety">الحوكمة</Link>
              </div>
            </details>
            <Link href="/book" className="dx-nav-cta"><span className="dx-nav-cta-long">Execution Diagnostic</span><span className="dx-nav-cta-short">التشخيص</span> <span aria-hidden="true">↗</span></Link>
          </div>
        </nav>
      </header>

      <main className="dx-main">
        <section ref={heroRef} onPointerMove={handlePointerMove} onPointerLeave={handlePointerLeave} className="dx-hero" aria-labelledby="dx-hero-title">
          <div className="dx-hero-grid" aria-hidden="true" /><div className="dx-hero-glow" aria-hidden="true" /><div className="dx-orb dx-orb-one" aria-hidden="true" /><div className="dx-orb dx-orb-two" aria-hidden="true" />
          <div className="dx-hero-copy">
            <div className="dx-signal-pill"><span className="dx-live-dot" aria-hidden="true" />SAUDI B2B · STRATEGY · SYSTEMS · INTELLIGENCE · PRODUCTS</div>
            <h1 id="dx-hero-title">نبني طبقة الذكاء والتنفيذ التي<span className="dx-cyan-text"> تنقل الشركات من القرار إلى النتيجة.</span></h1>
            <p className="dx-hero-lead"><strong>Dealix شركة B2B للأنظمة الاستراتيجية والذكاء والتنفيذ.</strong> نصمم الاستراتيجية، نبني أنظمة AI وautomation، نلتقط intelligence من السوق، ثم نحوّل ما يثبت إلى منتجات قابلة للتوسع. <strong>Dealix OS هو منتجنا الرئيسي</strong> — AI Business Operating System — وليس حدود الشركة.</p>
            <div className="dx-actions" aria-label="الإجراءات الرئيسية"><Link href="/book" className="dx-btn dx-btn-primary">ابدأ بمشكلة تنفيذ حقيقية <span aria-hidden="true">→</span></Link><Link href="/company" className="dx-btn dx-btn-secondary">استكشف Dealix كشركة</Link></div>
            <div className="dx-trust-line" aria-label="مبادئ التشغيل"><span>Saudi-first B2B</span><span>Founder-led externally</span><span>Evidence-first</span><span>Approval-aware</span></div>
          </div>

          <div className="dx-command-card" aria-label="Dealix execution loop">
            <div className="dx-command-head"><span>DEALIX COMPANY EXECUTION MODEL</span><span className="dx-command-status"><i /> GOVERNED MODEL</span></div>
            <div className="dx-flow">{systemFlow.map((item, index) => (
              <div className="dx-flow-row" key={item.label} style={{ "--dx-delay": `${index * 0.14}s` } as CSSProperties}>
                <div className="dx-flow-index">0{index + 1}</div><div><span>{item.label}</span><strong>{item.title}</strong><p>{item.text}</p></div><div className="dx-flow-pulse" aria-hidden="true" />
              </div>
            ))}</div>
            <div className="dx-command-foot"><span>Signal</span><b>→</b><span>Decision</span><b>→</b><span>Action</span><b>→</b><span>Proof</span></div>
          </div>
        </section>

        <section className="dx-strip" aria-label="Dealix value system"><p>Strategy + Systems + Intelligence + Products</p><div className="dx-strip-line" aria-hidden="true"><span /></div><p>Revenue + Proof + Command</p></section>

        <section className="dx-section" style={deferredSectionStyle} aria-labelledby="dx-company-title">
          <div className="dx-section-head"><div><span className="dx-kicker">ONE COMPANY · FOUR ENGINES</span><h2 id="dx-company-title">أكبر من منتج واحد. وأبسط من شبكة شركات مبعثرة.</h2></div><p>Dealix تجمع الاستراتيجية والتنفيذ والذكاء والمنتجات تحت شركة واحدة. كل مسار له buyer ونتيجة وproof gate، بينما Dealix OS يبقى المنتج البرمجي الرئيسي الذي يتوسع فقط عندما تثبت القيمة.</p></div>
          <div className="dx-value-grid">{corporatePillars.map((item, index) => <article className="dx-value-card" key={item.label}><div className="dx-card-number">0{index + 1}</div><span className="dx-card-label">{item.label}</span><h3>{item.title}</h3><p>{item.text}</p><Link href={item.href} className="dx-text-link">استكشف المسار <span aria-hidden="true">↗</span></Link><div className="dx-card-signal" aria-hidden="true"><span /></div></article>)}</div>
        </section>

        <section className="dx-section" style={deferredSectionStyle} aria-labelledby="dx-capabilities-title">
          <div className="dx-section-head"><div><span className="dx-kicker">FULL CAPABILITY SYSTEM</span><h2 id="dx-capabilities-title">قدرات من الاستراتيجية إلى AI runtime — تُركب حسب الحالة.</h2></div><p>بدل بيع خدمة منفصلة لكل أداة، Dealix تجمع قدرات مترابطة يمكن تركيبها حول workflow واحد ثم توسيعها بعد إثبات القيمة.</p></div>
          <div className="dx-chip-grid">{capabilityHighlights.map((item) => <Link key={item} href="/services" className="dx-chip-card">{item}<span aria-hidden="true">↗</span></Link>)}</div>
          <div className="dx-actions"><Link href="/services" className="dx-btn dx-btn-secondary">شاهد كتالوج الخدمات الكامل</Link></div>
        </section>

        <section className="dx-section dx-sector-section" style={deferredSectionStyle} aria-labelledby="dx-sectors-title">
          <div className="dx-section-head"><div><span className="dx-kicker">SECTOR-SPECIFIC EXECUTION</span><h2 id="dx-sectors-title">قطاعك يغيّر الـworkflow والـbuyer والـproof المطلوب.</h2></div><p>نستخدم Company Machine بملفات قطاعية مختلفة؛ البحث القطاعي يساعدنا على بدء التشخيص ولا يتحول وحده إلى claim عن عميل محدد.</p></div>
          <div className="dx-sector-grid">{featuredSectors.map((sector) => <Link className="dx-sector-card" href={sector.href} key={sector.href}><span>{sector.en}</span><strong>{sector.name}</strong><b aria-hidden="true">↗</b></Link>)}</div>
          <div className="dx-actions"><Link href="/sectors" className="dx-btn dx-btn-secondary">استكشف جميع القطاعات</Link></div>
        </section>

        <section className="dx-system" style={deferredSectionStyle} aria-labelledby="dx-product-title">
          <div className="dx-system-copy"><span className="dx-kicker dx-kicker-light">FLAGSHIP PRODUCT</span><h2 id="dx-product-title">Dealix OS هو المنتج. Dealix هي الشركة التي تبني حوله منظومة قيمة كاملة.</h2><p>Dealix OS يوحّد Company Brain وOpportunity Graph وAction Queue وApproval Authority وProof Ledger في مسار Signal → Decision → Action → Proof فوق أدوات العميل الحالية.</p><Link href="/dealix-os" className="dx-text-link">استكشف Dealix OS <span aria-hidden="true">↗</span></Link></div>
          <div className="dx-path" role="list">{executionPath.map((item) => <article className="dx-path-item" key={item.step} role="listitem"><span>{item.step}</span><div><h3>{item.title}</h3><p>{item.text}</p></div></article>)}</div>
        </section>

        <section className="dx-section" style={deferredSectionStyle} aria-labelledby="dx-value-title">
          <div className="dx-section-head"><div><span className="dx-kicker">THE ECONOMIC OPERATING SYSTEM</span><h2 id="dx-value-title">لا نقيس الشركة بعدد الـagents أو المنشورات. نقيسها بحركة اقتصادية ودليل.</h2></div><p>كل استراتيجية، automation أو محتوى يجب أن يخدم مسارًا يمكن تتبعه من Signal إلى Qualified Problem ثم تنفيذ وProof — بدون خلط activity مع business value.</p></div>
          <div className="dx-value-grid">{valueBlocks.map((item, index) => <article className="dx-value-card" key={item.label}><div className="dx-card-number">0{index + 1}</div><span className="dx-card-label">{item.label}</span><h3>{item.title}</h3><p>{item.text}</p><div className="dx-card-signal" aria-hidden="true"><span /></div></article>)}</div>
        </section>

        <section className="dx-section dx-proof-section" style={deferredSectionStyle} aria-labelledby="dx-proof-title">
          <div className="dx-section-head"><div><span className="dx-kicker">TRUTH FIREWALL</span><h2 id="dx-proof-title">النمو السريع لا يعني ترقية الحقيقة بلا دليل.</h2></div><p>أي score أو AI recommendation أو public signal يبقى أقل سلطة من consent، suppression، evidence وaction authority.</p></div>
          <div className="dx-truth-grid">{truthRules.map(([left, right]) => <article className="dx-truth-card" key={left}><span>{left}</span><b aria-hidden="true">≠</b><strong>{right}</strong></article>)}</div>
        </section>

        <section className="dx-final-cta" style={deferredSectionStyle} aria-labelledby="dx-final-title">
          <div className="dx-final-mark" aria-hidden="true"><img src="/dealix-mark.svg" alt="" /></div><span className="dx-kicker">START WITH ONE EXECUTABLE BUSINESS PROBLEM</span><h2 id="dx-final-title">عندك نمو، عملية، سوق أو قرار مهم لا يتحول اليوم إلى نتيجة قابلة للإثبات؟</h2><p>ابدأ بـFree Execution Diagnostic. إذا لم توجد حالة قابلة للقياس نتوقف؛ وإذا كانت مناسبة ننتقل إلى Qualified Discovery ثم عرض خاص بالعميل بدون fixed public pricing.</p><div className="dx-actions dx-actions-center"><Link href="/book" className="dx-btn dx-btn-primary">ابدأ التشخيص المجاني</Link><Link href="/services" className="dx-btn dx-btn-ghost">شاهد الحلول الاستراتيجية</Link></div>
        </section>
      </main>

      <footer className="dx-footer"><div className="dx-footer-inner"><img src="/dealix-logo.svg" alt="Dealix — Saudi AI Systems Company" className="dx-footer-logo" width={400} height={96} loading="lazy" decoding="async" /><div className="dx-footer-links"><Link href="/company">Company</Link><Link href="/services">Services</Link><Link href="/sectors">Sectors</Link><Link href="/products">Products</Link><Link href="/dealix-os">Dealix OS</Link><Link href="/cases">Proof</Link><Link href="/safety">Safety</Link><Link href="/legal">Legal</Link><a href={`mailto:${founderEmail}`}>Founder Email</a><a href={founderPhoneHref}>Founder Phone</a></div><p>Founder Office: <a href={`mailto:${founderEmail}`}>{founderEmail}</a> · <a href={founderPhoneHref}>{founderPhone}</a></p><p>لا نضمن ROI أو revenue محددًا. الادعاءات الخارجية يجب أن تبنى على evidence وموافقة مناسبة.</p><small>© 2026 Dealix · Strategy → Systems → Intelligence → Products · Signal → Decision → Action → Proof</small></div></footer>
    </div>
  );
}
