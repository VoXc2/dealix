import Link from "next/link";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

const valueBlocks = [
  ["Revenue", "نكشف أين تتعطل المتابعة أو القرار أو التحويل، ثم نعطي كل فرصة owner وnext action واضحًا."],
  ["Proof", "نفصل activity عن value، ونقيس baseline ونتيجة قابلة للمراجعة بدل ادعاءات ROI أو قصص غير مثبتة."],
  ["Command", "نحوّل الإشارات والبيانات إلى قرار يومي، queue، موافقات، وreceipt واضح لما تم وما لم يتم."],
];

const buyingPath = [
  ["01", "Free Mini Diagnostic", "مشكلة واحدة، owner واحد، ومسار إثبات أولي — بدون بطاقة أو التزام شراء."],
  ["02", "Qualified Discovery", "نثبت baseline والنطاق والبيانات وصاحب القرار قبل أن نعرض أي عمل مدفوع."],
  ["03", "Customer-Specific Quote", "لا قائمة أسعار عامة؛ النطاق والسعر يحددان لعميل محدد بعد Discovery."],
  ["04", "30-Day Revenue Command Pilot", "Pilot محكوم يبدأ بعد قبول العرض وإثبات الدفع، مع human approvals للأفعال الحساسة."],
  ["05", "Proof → Stop / Expand / Redesign", "التوسع يُكتسب بالدليل؛ لا Retainer أو Productization تلقائي قبل Proof مقبول."],
];

const qualification = [
  "شركة B2B في السعودية أو تعمل في السوق السعودي.",
  "مشكلة تشغيلية واضحة مرتبطة بالإيراد أو المتابعة أو القرار.",
  "Founder / GM / owner قادر على اتخاذ القرار أو تسمية صاحب القرار.",
  "بيانات مشروعة يمكن استخدامها لقياس baseline والنتيجة.",
  "استعداد لتشغيل AI داخل حدود واضحة مع موافقات بشرية.",
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
    "Dealix is a Saudi-first AI Business Operating System focused on Revenue + Proof + Command with approval-first execution.",
  knowsAbout: [
    "Revenue Operations",
    "AI Governance",
    "B2B Sales Operations",
    "Saudi Business Automation",
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
          <li><Link href="/pricing">مسار الشراء</Link></li>
          <li><Link href="/proof-vault">Proof</Link></li>
          <li><Link href="/safety">Safety</Link></li>
        </ul>
        <div className="actions" style={{ marginTop: 0 }}>
          <Link href="/book" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.82rem" }}>
            Mini Diagnostic مجاني →
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
              background: "radial-gradient(circle, rgba(212,175,55,0.14), transparent 68%)",
              pointerEvents: "none",
            }}
          />
          <p className="eyebrow">Saudi-first · Approval-first · Proof-backed</p>
          <h1 id="hero-title" style={{ maxWidth: 980 }}>
            نظام تشغيل أعمال بالذكاء الاصطناعي<br />
            يحوّل <span className="gradient-text">السوق → القرار → التنفيذ → الإثبات</span>
          </h1>
          <p style={{ maxWidth: 790, fontSize: "1.16rem", lineHeight: 1.85 }}>
            Dealix تربط Revenue + Proof + Command في مسار واحد للشركات السعودية. AI يحلل ويقترح ويجهز،
            بينما التنفيذ الخارجي الحساس يبقى محكومًا بالموافقة والدليل.
          </p>
          <div className="actions" aria-label="Primary actions">
            <Link href="/book">ابدأ Mini Diagnostic مجاني</Link>
            <Link href="/pricing">شاهد مسار الشراء</Link>
            <Link href="/safety">كيف نحكم الـAI؟</Link>
          </div>
        </section>

        <section className="grid-3" aria-label="Dealix wedge">
          {valueBlocks.map(([title, text]) => (
            <article className="card" key={title}>
              <span className="badge badge-gold">{title}</span>
              <p style={{ marginTop: "var(--sp-4)" }}>{text}</p>
            </article>
          ))}
        </section>

        <section aria-labelledby="why-title" style={{ borderTop: "1px solid rgba(255,255,255,0.07)", paddingTop: "var(--sp-10)" }}>
          <p className="eyebrow">The operating problem</p>
          <h2 id="why-title">المشكلة ليست نقص أدوات؛ المشكلة أن القرار والتنفيذ والإثبات منفصلة.</h2>
          <div className="grid-2">
            <div>
              <h3>ما نربطه</h3>
              <ul>
                <li>Signals وMarket Intelligence.</li>
                <li>Company Brain والسياق التجاري.</li>
                <li>Opportunity / next action / approvals.</li>
                <li>Delivery وProof وlearning.</li>
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
          <p className="eyebrow">One buying path</p>
          <h2 id="path-title">نبدأ بالتشخيص، ولا نبيع قبل أن نفهم المشكلة.</h2>
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
            <Link href="/pricing">تفاصيل المسار التجاري →</Link>
          </div>
        </section>

        <section className="card card-gold" aria-labelledby="fit-title">
          <p className="eyebrow">First validation cohort</p>
          <h2 id="fit-title">الأولوية لشركة يمكنها إثبات القيمة، لا لأي lead عابر.</h2>
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
          <p className="eyebrow">Start with one verified problem</p>
          <h2 id="final-cta-title">عندك تسريب إيراد أو متابعة أو قرار يومي غير واضح؟</h2>
          <p style={{ maxWidth: 720, margin: "0 auto var(--sp-6)" }}>
            ابدأ بـMini Diagnostic مجاني. إذا لم تكن المشكلة مناسبة لـDealix نتوقف؛ وإذا كانت مؤهلة ننتقل إلى Discovery ثم عرض خاص بعميلك.
          </p>
          <div className="actions" style={{ justifyContent: "center" }}>
            <Link href="/book">ابدأ Mini Diagnostic</Link>
            <Link href="/proof-vault">شاهد منهج الإثبات</Link>
          </div>
        </section>

        <footer style={{ textAlign: "center", paddingTop: "var(--sp-8)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
          <p className="navbar-brand" style={{ justifyContent: "center", fontSize: "1.2rem", marginBottom: "var(--sp-3)" }}>Dealix</p>
          <div style={{ display: "flex", justifyContent: "center", gap: "var(--sp-4)", marginBottom: "var(--sp-4)", flexWrap: "wrap" }}>
            <Link href="/brain" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Company Brain</Link>
            <Link href="/pricing" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Buying Path</Link>
            <Link href="/proof-vault" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Proof</Link>
            <Link href="/book" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Diagnostic</Link>
            <Link href="/legal" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Legal</Link>
          </div>
          <p style={{ fontSize: "0.78rem", color: "rgba(255,255,255,0.30)", maxWidth: 680, margin: "0 auto var(--sp-3)" }}>
            لا نضمن نتيجة أو عائدًا ماليًا محددًا. كل claim خارجي يجب أن يكون مبنيًا على Evidence قابل للمراجعة وموافقة مناسبة.
          </p>
          <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.34)" }}>
            © 2026 Dealix · Saudi-first AI Business Operating System · Revenue + Proof + Command
          </p>
        </footer>
      </main>
    </>
  );
}
