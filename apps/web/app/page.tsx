"use client";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

const productAreas = [
  {
    icon: "⚡",
    title: "Revenue OS",
    description: "Lead acquisition, ICP scoring, outreach pipeline visibility, and Saudi B2B growth workflows — all in one engine.",
    href: "/control-plane",
    badge: "نشط"
  },
  {
    icon: "🛡️",
    title: "Agent Governance",
    description: "Approval-first AI execution with audit trails, safety gates, and no blind external commitments.",
    href: "/agents",
    badge: "PDPL"
  },
  {
    icon: "🔒",
    title: "Trust & Safety",
    description: "PDPL-aware controls, approval classes, evidence packs, and live operational guardrails.",
    href: "/safety",
    badge: "SDAIA"
  },
  {
    icon: "📊",
    title: "Value Engine",
    description: "Business-value tracking, executive dashboards, proof curation, and operational scorecards.",
    href: "/value-engine",
    badge: "Proof Pack"
  }
];

const stats = [
  { value: "8",      label: "AI Agents" },
  { value: "PDPL",   label: "Native Compliance" },
  { value: "SAR",    label: "Saudi-first Pricing" },
  { value: "v3.1",   label: "Production Ready" },
];

const operationalLinks = [
  ["⚙️  Control plane",    "/control-plane"],
  ["🤖 Agents",             "/agents"],
  ["✅ Approvals",           "/approvals"],
  ["🔒 Safety",             "/safety"],
  ["🧪 Sandbox",            "/sandbox"],
  ["📈 Value engine",       "/value-engine"],
  ["🔄 Self-evolving OS",   "/self-evolving"],
];

const structuredData = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Dealix",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  url: siteUrl,
  description: "Saudi-first B2B revenue, growth, and compliance engine with approval-first AI execution.",
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  offers: { "@type": "Offer", priceCurrency: "SAR", availability: "https://schema.org/InStock" },
  publisher: { "@type": "Organization", name: "Dealix", url: siteUrl }
};

export default function HomePage() {
  return (
    <>
      {/* Navbar */}
      <nav className="navbar" aria-label="Primary navigation">
        <a href="/" className="navbar-brand" aria-label="Dealix Home">
          Dealix
        </a>
        <ul className="navbar-links" role="list">
          <li><a href="/control-plane">Revenue OS</a></li>
          <li><a href="/agents">Agents</a></li>
          <li><a href="/safety">Safety</a></li>
          <li><a href="/ar">العربية</a></li>
        </ul>
        <div className="actions" style={{ marginTop: 0 }}>
          <a href="/ar" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.82rem" }}>
            الموقع العربي
          </a>
          <a href="/control-plane" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.82rem" }}>
            Open Platform →
          </a>
        </div>
      </nav>

      <main className="grid">
        <script
          type="application/ld+json"
          suppressHydrationWarning
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />

        {/* ── Hero ── */}
        <section
          className="card dot-pattern animate-fade-up"
          aria-labelledby="hero-title"
          style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}
        >
          {/* Gold glow blob */}
          <div aria-hidden="true" style={{
            position: "absolute", top: "-80px", left: "-80px",
            width: "400px", height: "400px",
            background: "radial-gradient(circle, rgba(212,175,55,0.12), transparent 70%)",
            pointerEvents: "none"
          }} />

          <p className="eyebrow">Saudi-first · Approval-first · Revenue-focused</p>

          <h1 id="hero-title" style={{ maxWidth: "860px" }}>
            Dealix{" "}
            <span className="gradient-text">Enterprise</span>
            <br />Control Plane
          </h1>

          <p style={{ maxWidth: "680px", fontSize: "1.15rem", lineHeight: 1.7 }}>
            A Saudi-first B2B revenue, growth, and compliance engine for teams that need
            AI assistance without losing policy control, auditability, or human approval
            on critical moves.
          </p>

          <div className="actions" aria-label="Primary actions">
            <a href="/ar">الموقع العربي — P1 · P2 · P3</a>
            <a href="/control-plane">Open control plane</a>
            <a href="/safety">Review safety layer</a>
          </div>
        </section>

        {/* ── Stats ── */}
        <section aria-label="Platform statistics">
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
            gap: "var(--sp-4)"
          }}>
            {stats.map(({ value, label }) => (
              <div
                key={label}
                className="card"
                style={{ textAlign: "center", padding: "var(--sp-6) var(--sp-4)" }}
              >
                <div className="stat-value">{value}</div>
                <p className="stat-label">{label}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── Product Areas ── */}
        <section aria-labelledby="areas-title">
          <h2 id="areas-title" style={{ marginBottom: "var(--sp-6)" }}>
            Core operating areas
          </h2>
          <div className="cards">
            {productAreas.map((area) => (
              <article className="card" key={area.href} style={{ position: "relative" }}>
                <span
                  className="badge badge-gold"
                  style={{ position: "absolute", top: "var(--sp-4)", left: "var(--sp-4)" }}
                >
                  {area.badge}
                </span>
                <div style={{ fontSize: "2rem", marginBottom: "var(--sp-3)", marginTop: "var(--sp-4)" }}>
                  {area.icon}
                </div>
                <h3 style={{ color: "#fff", marginBottom: "var(--sp-2)" }}>{area.title}</h3>
                <p style={{ fontSize: "0.9rem", marginBottom: "var(--sp-5)" }}>{area.description}</p>
                <a
                  href={area.href}
                  className="btn btn-secondary"
                  style={{ fontSize: "0.82rem", minHeight: "36px", padding: "0 16px", borderRadius: "var(--radius-md)" }}
                >
                  Open {area.title} →
                </a>
              </article>
            ))}
          </div>
        </section>

        {/* ── Operational Surfaces ── */}
        <section className="card" aria-labelledby="ops-title">
          <p className="eyebrow">Internal surfaces</p>
          <h2 id="ops-title">Operational surfaces</h2>
          <p>
            Use these internal surfaces to inspect agents, approvals, safety,
            sandbox behavior, and value tracking.
          </p>
          <div className="divider-gold" />
          <ul style={{ listStyle: "none", padding: 0, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "var(--sp-2)" }}>
            {operationalLinks.map(([label, href]) => (
              <li key={href} style={{ margin: 0 }}>
                <a
                  href={href}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "var(--sp-2)",
                    padding: "var(--sp-3) var(--sp-4)",
                    borderRadius: "var(--radius-md)",
                    background: "rgba(255,255,255,0.04)",
                    border: "1px solid rgba(255,255,255,0.07)",
                    color: "rgba(255,255,255,0.70)",
                    fontSize: "0.88rem",
                    fontWeight: 600,
                    textDecoration: "none",
                    transition: "all 0.2s"
                  }}
                  onMouseEnter={e => {
                    const el = e.currentTarget as HTMLAnchorElement;
                    el.style.borderColor = "rgba(212,175,55,0.35)";
                    el.style.color = "var(--dealix-gold)";
                    el.style.background = "rgba(212,175,55,0.06)";
                  }}
                  onMouseLeave={e => {
                    const el = e.currentTarget as HTMLAnchorElement;
                    el.style.borderColor = "rgba(255,255,255,0.07)";
                    el.style.color = "rgba(255,255,255,0.70)";
                    el.style.background = "rgba(255,255,255,0.04)";
                  }}
                >
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </section>

        {/* ── Footer ── */}
        <footer style={{ textAlign: "center", paddingTop: "var(--sp-8)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
          <p className="navbar-brand" style={{ justifyContent: "center", fontSize: "1.2rem", marginBottom: "var(--sp-3)" }}>
            Dealix
          </p>
          <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.30)" }}>
            © 2026 Dealix · Saudi-first AI Revenue Operations ·{" "}
            <a href="/safety" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500 }}>Safety</a>
            {" · "}
            <a href="https://github.com/Dealix-sa/dealix" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500 }}>GitHub</a>
          </p>
        </footer>
      </main>
    </>
  );
}
