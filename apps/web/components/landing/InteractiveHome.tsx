"use client";

import Link from "next/link";
import { useRef } from "react";
import type { CSSProperties, PointerEvent as ReactPointerEvent } from "react";

const valueBlocks = [
  { label: "Revenue", title: "حركة اقتصادية، لا نشاط شكلي", text: "نحوّل الإشارات التجارية والتشغيلية إلى أولوية واضحة، تشخيص قابل للتنفيذ، ثم خطوة يمكن قياس أثرها." },
  { label: "Proof", title: "الدليل قبل الادعاء", text: "نفرّق بين activity وdelivery وoutcome وcustomer proof، ونبني baseline وreceipts يمكن مراجعتها." },
  { label: "Command", title: "قرار يومي محكوم", text: "Company Brain + Opportunity Graph + Action Queue + approvals تتحول إلى مسار واحد بدل أدوات منفصلة." },
];

const executionPath = [
  { step: "01", title: "Execution Diagnostic", text: "نبدأ بمشكلة واحدة. نفصل evidence عن assumptions ونحدد أصغر تدخل يستحق الاختبار." },
  { step: "02", title: "Qualified Discovery", text: "نثبت أصحاب القرار، البيانات، النطاق، المخاطر ومعيار القبول قبل أي التزام تجاري." },
  { step: "03", title: "Customer-Specific Outcome Sprint", text: "ننفذ الحل الأنسب: Build / Adapt / Integrate / Partner، بنطاق وسعر خاص بالعميل بعد Discovery." },
  { step: "04", title: "Proof Review", text: "نقارن النتيجة بالـbaseline ونوثق ما تحرك وما لم يتحرك بدون تحويل demo أو synthetic evidence إلى customer proof." },
  { step: "05", title: "Dealix Runtime", text: "إذا ثبتت القيمة والتكرار، نوسع إلى تشغيل مستمر للمراقبة والتنفيذ والإثبات والتحسين." },
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

export function InteractiveHome() {
  const heroRef = useRef<HTMLDivElement>(null);

  function handlePointerMove(event: ReactPointerEvent<HTMLDivElement>) {
    const hero = heroRef.current;
    if (!hero) return;
    const rect = hero.getBoundingClientRect();
    hero.style.setProperty("--dx-pointer-x", `${event.clientX - rect.left}px`);
    hero.style.setProperty("--dx-pointer-y", `${event.clientY - rect.top}px`);
  }

  function handlePointerLeave() {
    const hero = heroRef.current;
    if (!hero) return;
    hero.style.setProperty("--dx-pointer-x", "72%");
    hero.style.setProperty("--dx-pointer-y", "30%");
  }

  return (
    <div className="dx-home">
      <header className="dx-nav-wrap">
        <nav className="dx-nav" aria-label="التنقل الرئيسي">
          <Link href="/" className="dx-logo-link" aria-label="Dealix — الصفحة الرئيسية"><img src="/dealix-logo.svg" alt="Dealix — AI Business Operating System" className="dx-logo" width={400} height={96} loading="eager" decoding="async" /></Link>
          <div className="dx-nav-links" role="list"><Link href="/services">القدرات</Link><Link href="/cases">الاستخدامات</Link><Link href="/proof-vault">Proof</Link><Link href="/safety">الحوكمة</Link></div>
          <Link href="/book" className="dx-nav-cta">التشخيص المجاني <span aria-hidden="true">↗</span></Link>
        </nav>
      </header>

      <main className="dx-main">
        <section ref={heroRef} onPointerMove={handlePointerMove} onPointerLeave={handlePointerLeave} className="dx-hero" aria-labelledby="dx-hero-title">
          <div className="dx-hero-grid" aria-hidden="true" /><div className="dx-hero-glow" aria-hidden="true" /><div className="dx-orb dx-orb-one" aria-hidden="true" /><div className="dx-orb dx-orb-two" aria-hidden="true" />
          <div className="dx-hero-copy">
            <div className="dx-signal-pill"><span className="dx-live-dot" aria-hidden="true" />Saudi Business · Governed AI · Measurable Proof</div>
            <h1 id="dx-hero-title">حوّل إشارات شركتك إلى<span className="dx-cyan-text"> تنفيذ حقيقي يمكن إثباته.</span></h1>
            <p className="dx-hero-lead">Dealix هي <strong>AI Business Operating System</strong> تربط الإشارة بالقرار والتنفيذ والدليل فوق أدواتك الحالية — مع حوكمة واضحة للأفعال الحساسة وبدون تعقيد ظاهر على العميل.</p>
            <div className="dx-actions" aria-label="الإجراءات الرئيسية"><Link href="/book" className="dx-btn dx-btn-primary">أعطِ Dealix workflow مكسورًا <span aria-hidden="true">→</span></Link><Link href="/pricing" className="dx-btn dx-btn-secondary">شاهد Engagement Path</Link></div>
            <div className="dx-trust-line" aria-label="مبادئ التشغيل"><span>Founder-led externally</span><span>Evidence-first</span><span>Approval-aware</span><span>Saudi operating context</span></div>
          </div>

          <div className="dx-command-card" aria-label="Dealix execution loop">
            <div className="dx-command-head"><span>DEALIX EXECUTION LOOP</span><span className="dx-command-status"><i /> GOVERNED MODEL</span></div>
            <div className="dx-flow">{systemFlow.map((item, index) => (
              <div className="dx-flow-row" key={item.label} style={{ "--dx-delay": `${index * 0.14}s` } as CSSProperties}>
                <div className="dx-flow-index">0{index + 1}</div><div><span>{item.label}</span><strong>{item.title}</strong><p>{item.text}</p></div><div className="dx-flow-pulse" aria-hidden="true" />
              </div>
            ))}</div>
            <div className="dx-command-foot"><span>Signal</span><b>→</b><span>Decision</span><b>→</b><span>Action</span><b>→</b><span>Proof</span></div>
          </div>
        </section>

        <section className="dx-strip" aria-label="Dealix value system"><p>Revenue + Proof + Command</p><div className="dx-strip-line" aria-hidden="true"><span /></div><p>From Opportunity to Outcome</p></section>

        <section className="dx-section" aria-labelledby="dx-value-title">
          <div className="dx-section-head"><div><span className="dx-kicker">THE EXECUTION GAP</span><h2 id="dx-value-title">المشكلة ليست نقص أدوات. المشكلة أن القرار لا يتحول دائمًا إلى نتيجة.</h2></div><p>Dealix لا تستبدل CRM أو ERP أو WhatsApp أو فريقك. تعمل فوقها كطبقة تنفيذ تربط السياق الاقتصادي بالـnext action والدليل.</p></div>
          <div className="dx-value-grid">{valueBlocks.map((item, index) => <article className="dx-value-card" key={item.label}><div className="dx-card-number">0{index + 1}</div><span className="dx-card-label">{item.label}</span><h3>{item.title}</h3><p>{item.text}</p><div className="dx-card-signal" aria-hidden="true"><span /></div></article>)}</div>
        </section>

        <section className="dx-system" aria-labelledby="dx-system-title">
          <div className="dx-system-copy"><span className="dx-kicker dx-kicker-light">ONE GOVERNED PATH</span><h2 id="dx-system-title">واجهة بسيطة للعميل. آلة تنفيذ عميقة خلفها.</h2><p>لا نعرض عشرات الخدمات كقائمة مربكة. نبدأ بمشكلة تنفيذ واحدة ثم نختار أفضل طريق للحل والقياس.</p><Link href="/services" className="dx-text-link">استكشف قدرات Dealix <span aria-hidden="true">↗</span></Link></div>
          <div className="dx-path" role="list">{executionPath.map((item) => <article className="dx-path-item" key={item.step} role="listitem"><span>{item.step}</span><div><h3>{item.title}</h3><p>{item.text}</p></div></article>)}</div>
        </section>

        <section className="dx-section dx-proof-section" aria-labelledby="dx-proof-title">
          <div className="dx-section-head"><div><span className="dx-kicker">TRUTH FIREWALL</span><h2 id="dx-proof-title">النظام لا يرقّي الحقيقة بلا دليل.</h2></div><p>أي score أو AI recommendation أو public signal يبقى أقل سلطة من consent، suppression، evidence وaction authority.</p></div>
          <div className="dx-truth-grid">{truthRules.map(([left, right]) => <article className="dx-truth-card" key={left}><span>{left}</span><b aria-hidden="true">≠</b><strong>{right}</strong></article>)}</div>
        </section>

        <section className="dx-final-cta" aria-labelledby="dx-final-title">
          <div className="dx-final-mark" aria-hidden="true"><img src="/dealix-mark.svg" alt="" /></div><span className="dx-kicker">START WITH ONE EXECUTABLE PROBLEM</span><h2 id="dx-final-title">عندك workflow مهم لا يتحول اليوم إلى تنفيذ وProof واضح؟</h2><p>ابدأ بـFree Execution Diagnostic. إذا لم توجد حالة قابلة للقياس نتوقف؛ وإذا كانت مناسبة ننتقل إلى Discovery وعرض خاص بالعميل.</p><div className="dx-actions dx-actions-center"><Link href="/book" className="dx-btn dx-btn-primary">ابدأ التشخيص المجاني</Link><Link href="/proof-vault" className="dx-btn dx-btn-ghost">شاهد منهج الإثبات</Link></div>
        </section>
      </main>

      <footer className="dx-footer"><div className="dx-footer-inner"><img src="/dealix-logo.svg" alt="Dealix — AI Business Operating System" className="dx-footer-logo" width={400} height={96} loading="lazy" decoding="async" /><div className="dx-footer-links"><Link href="/pricing">Engagement Path</Link><Link href="/services">Services</Link><Link href="/proof-vault">Proof</Link><Link href="/safety">Safety</Link><Link href="/legal">Legal</Link></div><p>لا نضمن ROI أو revenue محددًا. الادعاءات الخارجية يجب أن تبنى على evidence وموافقة مناسبة.</p><small>© 2026 Dealix · AI Business Operating System · Signal → Decision → Action → Proof</small></div></footer>
    </div>
  );
}
