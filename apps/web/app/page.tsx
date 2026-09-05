import Link from "next/link";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

const valueBlocks = [
  ["Revenue", "نربط الإشارات التجارية بأولوية واضحة وحركة اقتصادية يمكن تتبعها، بدل نشاط منفصل عن النتيجة."],
  ["Proof", "نفصل activity عن value، ونقيس baseline ونتيجة قابلة للمراجعة بدل ادعاءات ROI أو قصص غير مثبتة."],
  ["Command", "نحوّل الإشارات والبيانات إلى قرار يومي، queue، موافقات، وreceipt واضح لما تم وما لم يتم."],
];

const buyingPath = [
  ["01", "Execution Diagnostic", "نحدد workflow واحدًا ذا أثر اقتصادي، baseline واضحًا، وصاحب قرار — بدون بطاقة أو التزام شراء."],
  ["02", "Qualified Discovery + Quote", "نثبت البيانات والنطاق ومعايير الإثبات، ثم نصدر عرضًا خاصًا بالعميل فقط إذا كانت هناك حالة تنفيذ واضحة."],
  ["03", "Outcome Sprint", "تنفيذ محكوم يركز على نتيجة محددة قابلة للقياس؛ المدة تتحدد بحسب النطاق وعادة تكون نحو 4–6 أسابيع عندما يكون ذلك مناسبًا."],
  ["04", "Proof Review", "نقارن النتيجة بالـbaseline ونراجع ما تحرك اقتصاديًا وما لم يتحرك، بدون تحويل synthetic أو activity إلى customer proof."],
  ["05", "Dealix Runtime", "إذا أثبت الـSprint قيمة قابلة للتكرار، نوسع إلى Runtime مستمر للمراقبة والتنفيذ والإثبات؛ لا توسع تلقائي قبل Proof."],
];

const qualification = [
  "شركة تعمل في السعودية أو لديها مسار واضح لدخول السوق السعودي.",
  "Workflow أو قرار تشغيلي واضح يمكن ربطه بنتيجة اقتصادية أو تشغيلية.",
  "Founder / GM / owner أو صاحب قرار مسمى يمكنه اعتماد النطاق والموافقات.",
  "بيانات مشروعة يمكن استخدامها لبناء baseline وقياس النتيجة.",
  "استعداد لتشغيل AI داخل حدود واضحة مع موافقات بشرية عند الأفعال الحساسة.",
];

const truthRules = [
  "Research ليست Relationship.",
  "Public contact ليست Consent.",
  "Draft ليست Sent.",
  "Quote ليست Invoice.",
  "Invoice ليست Payment.",
  "Synthetic/Demo ليست Customer Proof.",
];

const structuredData = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Dealix",
  url: siteUrl,
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  description:
    "Dealix is a governed AI execution platform for Saudi business that turns company signals into decisions, controlled action, and measurable proof.",
  knowsAbout: [
    "Governed AI Execution",
    "Revenue Operations",
    "AI Governance",
    "Saudi Market Intelligence",
    "Operational Proof",
  ],
};

export default function HomePage() {
  return (
    <>
      <nav className="navbar" aria-label="Primary navigation">
        <Link href="/" className="navbar-brand" aria-label="Dealix Home">Dealix</Link>
        <ul className="navbar-links" role="list">
          <li><Link href="/brain">Company Brain</Link></li>
          <li><Link href="/pricing">Engagement Path</Link></li>
          <li><Link href="/proof-vault">Proof</Link></li>
          <li><Link href="/safety">Safety</Link></li>
        </ul>
        <div className="actions" style={{ marginTop: 0 }}>
          <Link href="/book" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.82rem" }}>
            Execution Diagnostic →
          </Link>
        </div>
      </nav>

      <main className="grid">
        <script
          type="application/ld+json"
          suppressHydrationWarning
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />

        <section
          className="card dot-pattern animate-fade-up"
          aria-labelledby="hero-title"
          style={{
            position: "relative",
            overflow: "hidden",
            paddingTop: "clamp(44px,7vw,86px)",
            paddingBottom: "clamp(44px,7vw,86px)",
          }}
        >
          <div
            aria-hidden="true"
            style={{
              position: "absolute",
              inset: "-120px auto auto -120px",
              width: 460,
              height: 460,
              background: "radial-gradient(circle, rgba(34,211,238,0.14), transparent 68%)",
              pointerEvents: "none",
            }}
          />
          <p className="eyebrow">Saudi Business · Governed AI · Measurable Proof</p>
          <h1 id="hero-title" style={{ maxWidth: 980 }}>
            منصة التنفيذ الذكي المحكوم للأعمال<br />
            <span className="gradient-text">Signal → Decision → Action → Proof</span>
          </h1>
          <p style={{ maxWidth: 790, fontSize: "1.16rem", lineHeight: 1.85 }}>
            Dealix تحوّل إشارات شركتك إلى قرارات وتنفيذ محكوم ونتائج قابلة للإثبات. نعمل فوق أدواتك الحالية،
            ونبقي الأفعال الخارجية الحساسة مرتبطة بالموافقة والدليل.
          </p>
          <div className="actions" aria-label="Primary actions">
            <Link href="/book">ابدأ Execution Diagnostic</Link>
            <Link href="/pricing">شاهد Engagement Path</Link>
            <Link href="/safety">كيف نحكم الـAI؟</Link>
          </div>
        </section>

        <section className="grid-3" aria-label="Dealix architecture">
          {valueBlocks.map(([title, text]) => (
            <article className="card" key={title}>
              <span className="badge badge-gold">{title}</span>
              <p style={{ marginTop: "var(--sp-4)" }}>{text}</p>
            </article>
          ))}
        </section>

        <section aria-labelledby="why-title" style={{ borderTop: "1px solid rgba(255,255,255,0.07)", paddingTop: "var(--sp-10)" }}>
          <p className="eyebrow">The execution gap</p>
          <h2 id="why-title">المشكلة ليست نقص أدوات؛ المشكلة أن الإشارة والقرار والتنفيذ والإثبات منفصلة.</h2>
          <div className="grid-2">
            <div>
              <h3>ما نربطه</h3>
              <ul>
                <li>Signals وMarket Intelligence.</li>
                <li>Company Brain والسياق التجاري.</li>
                <li>Opportunity / next action / approvals.</li>
                <li>Execution وDelivery وProof وlearning.</li>
              </ul>
            </div>
            <div>
              <h3>ما لا ندّعيه</h3>
              <ul>
                <li>لا ROI مضمون أو نتيجة مالية مضمونة.</li>
                <li>لا mass outreach أو cold WhatsApp كاختصار للنمو.</li>
                <li>لا اعتبار بيانات عامة موافقة تواصل.</li>
                <li>لا اعتبار demo أو synthetic data دليل عميل.</li>
              </ul>
            </div>
          </div>
        </section>

        <section aria-labelledby="path-title">
          <p className="eyebrow">One governed engagement path</p>
          <h2 id="path-title">نبدأ بتشخيص التنفيذ، ثم نوسع فقط عندما يثبت الدليل.</h2>
          <div className="grid-3">
            {buyingPath.map(([step, title, text]) => (
              <article className="card" key={step}>
                <span className="badge badge-emerald">{step}</span>
                <h3 style={{ marginTop: "var(--sp-4)" }}>{title}</h3>
                <p>{text}</p>
              </article>
            ))}
          </div>
          <div className="actions">
            <Link href="/pricing">تفاصيل Engagement Path →</Link>
          </div>
        </section>

        <section className="card card-gold" aria-labelledby="fit-title">
          <p className="eyebrow">Best-fit starting point</p>
          <h2 id="fit-title">الأولوية لحالة تنفيذ يمكن إثبات قيمتها، لا لأي lead عابر.</h2>
          <ul>
            {qualification.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </section>

        <section aria-labelledby="truth-title" style={{ borderTop: "1px solid rgba(255,255,255,0.07)", paddingTop: "var(--sp-10)" }}>
          <p className="eyebrow">Truth Firewall</p>
          <h2 id="truth-title">النظام لا يرقّي الحقيقة بلا دليل.</h2>
          <div className="grid-3">
            {truthRules.map((rule) => (
              <article className="card" key={rule}><p>{rule}</p></article>
            ))}
          </div>
        </section>

        <section className="card" aria-labelledby="final-cta-title" style={{ textAlign: "center" }}>
          <p className="eyebrow">Start with one executable problem</p>
          <h2 id="final-cta-title">عندك workflow أو قرار مهم لا يتحول اليوم إلى تنفيذ وProof واضح؟</h2>
          <p style={{ maxWidth: 720, margin: "0 auto var(--sp-6)" }}>
            ابدأ بـExecution Diagnostic. إذا لم توجد حالة تنفيذ قابلة للقياس نتوقف؛ وإذا كانت مناسبة ننتقل إلى Discovery وعرض خاص بالعميل ثم Outcome Sprint.
          </p>
          <div className="actions" style={{ justifyContent: "center" }}>
            <Link href="/book">ابدأ Execution Diagnostic</Link>
            <Link href="/proof-vault">شاهد منهج الإثبات</Link>
          </div>
        </section>

        <footer style={{ textAlign: "center", paddingTop: "var(--sp-8)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
          <p className="navbar-brand" style={{ justifyContent: "center", fontSize: "1.2rem", marginBottom: "var(--sp-3)" }}>Dealix</p>
          <div style={{ display: "flex", justifyContent: "center", gap: "var(--sp-4)", marginBottom: "var(--sp-4)", flexWrap: "wrap" }}>
            <Link href="/brain" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Company Brain</Link>
            <Link href="/pricing" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Engagement Path</Link>
            <Link href="/proof-vault" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Proof</Link>
            <Link href="/book" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Diagnostic</Link>
            <Link href="/legal" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Legal</Link>
          </div>
          <p style={{ fontSize: "0.78rem", color: "rgba(255,255,255,0.30)", maxWidth: 680, margin: "0 auto var(--sp-3)" }}>
            لا نضمن نتيجة أو عائدًا ماليًا محددًا. كل claim خارجي يجب أن يكون مبنيًا على Evidence قابل للمراجعة وموافقة مناسبة.
          </p>
          <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.34)" }}>
            © 2026 Dealix · Governed AI Execution Platform for Saudi Business · Signal → Decision → Action → Proof
          </p>
        </footer>
      </main>
    </>
  );
}
