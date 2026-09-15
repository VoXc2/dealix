import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Status & Release Verification — Dealix",
  description: "Public Dealix runtime verification links and release-identity boundaries.",
  robots: { index: false, follow: false },
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "https://api.dealix.me";
const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

const receipts = [
  {
    id: "web-release",
    title: "Web release receipt",
    desc: "Inspect the public Web health response and its git_sha. Availability alone does not prove accepted release identity.",
    href: `${siteUrl}/healthz`,
  },
  {
    id: "api-release",
    title: "API release receipt",
    desc: "Inspect the public API version response and its git_sha before treating a release as current.",
    href: `${apiUrl}/version`,
  },
];

export default function StatusPage() {
  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "48px 24px" }}>
      <section className="card" style={{ marginBottom: 32, textAlign: "center" }}>
        <p className="eyebrow">Release verification</p>
        <h1>Dealix Status &amp; Release Verification</h1>
        <p style={{ maxWidth: 680, margin: "0 auto" }}>
          هذه الصفحة لا تفترض أن الإنتاج أخضر. افحص receipts الحية وهوية الإصدار قبل اعتماد أي حالة تشغيلية.
        </p>
        <div style={{ display: "flex", gap: 12, justifyContent: "center", marginTop: 20, flexWrap: "wrap" }}>
          <span className="badge badge-cyan">Verification required</span>
          <span className="badge badge-ocean">HTTP 200 ≠ release identity</span>
        </div>
      </section>

      <section style={{ marginBottom: 32 }}>
        <h2 style={{ marginBottom: 16 }}>Public runtime receipts</h2>
        <div className="cards">
          {receipts.map((receipt) => (
            <article key={receipt.id} className="card" style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 }}>
                <h3 style={{ fontSize: "1rem", margin: 0 }}>{receipt.title}</h3>
                <span className="badge badge-cyan">Inspect</span>
              </div>
              <p style={{ fontSize: "0.875rem", margin: 0 }}>{receipt.desc}</p>
              <a href={receipt.href} target="_blank" rel="noopener noreferrer" style={{ fontSize: "0.8rem", marginTop: "auto" }}>
                Open receipt →
              </a>
            </article>
          ))}
        </div>
      </section>

      <section className="card" style={{ marginBottom: 24 }}>
        <h2>What counts as release truth?</h2>
        <p>
          Production Green requires the accepted source release and the deployed Web/API identities to match, plus the public route checks for that release.
          A reachable endpoint, provider acceptance, or a successful build is not by itself proof of release parity.
        </p>
      </section>

      <section className="card">
        <h2>Trust &amp; support</h2>
        <p>
          This page does not render an incident ledger and does not claim that the absence of a public incident entry means there is no incident.
          Use the trust surface for governance boundaries or start a diagnostic if you need a scoped technical review.
        </p>
        <div className="actions">
          <a href="/safety">Review safety &amp; governance</a>
          <a href="/book">Start free diagnostic</a>
          <a href="/cases">Review proof methodology</a>
        </div>
      </section>
    </main>
  );
}
