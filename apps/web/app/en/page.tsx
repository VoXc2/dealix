import type { Metadata } from "next";
import Link from "next/link";
import { TrackedLink } from "@/components/analytics/TrackedLink";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export const metadata: Metadata = {
  title: "Dealix — Saudi B2B Strategy, AI Systems & Governed Execution",
  description:
    "Dealix is a Saudi-first B2B company for strategy, AI systems, market intelligence and governed execution. Start with a free Execution Diagnostic, then move to customer-specific scope only when the problem is qualified.",
  alternates: {
    canonical: "/en",
    languages: { "ar-SA": "/", "en-SA": "/en", "x-default": "/" },
  },
  openGraph: {
    type: "website",
    locale: "en_SA",
    url: `${siteUrl}/en`,
    title: "Dealix — Saudi B2B Strategy, AI Systems & Governed Execution",
    description: "From business signal to governed execution and measurable proof.",
  },
};

const capabilities = [
  ["Strategy & Transformation", "Turn growth and transformation goals into an operating model, prioritized bets and measurable execution."],
  ["AI Systems & Automation", "Build governed agents, workflows and integrations above the tools your team already uses."],
  ["Intelligence & Market Access", "Translate Saudi market, regulatory and partner signals into evidence-backed decisions without treating public research as buyer intent."],
  ["Products & Ventures", "Productize repeatable, proven capabilities. Dealix OS is the flagship AI Business Operating System in this layer."],
] as const;

const sectors = [
  ["Government & B2G", "/sectors/government-b2g"],
  ["Construction & EPC", "/sectors/construction-epc"],
  ["Industrial & Manufacturing", "/sectors/industrial-manufacturing"],
  ["Finance, FinTech & Insurance", "/sectors/finance-fintech-insurance"],
  ["Retail & E-commerce", "/sectors/retail-commerce-ecommerce"],
  ["Tourism & Hospitality", "/sectors/tourism-hospitality"],
  ["Logistics & Supply Chain", "/sectors/logistics-supply-chain"],
  ["Technology, SaaS & SI", "/sectors/technology-saas-si"],
] as const;

const structuredData = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Dealix",
  url: `${siteUrl}/en`,
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  inLanguage: "en-SA",
  description: "Saudi-first B2B strategy, AI systems, intelligence and governed execution company.",
};

export default function EnglishHomePage() {
  return (
    <main className="dx-corporate-page" lang="en" dir="ltr" style={{ direction: "ltr", textAlign: "left" }}>
      <script type="application/ld+json" suppressHydrationWarning dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }} />

      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">SAUDI-FIRST B2B · STRATEGY · SYSTEMS · INTELLIGENCE · PRODUCTS</p>
        <h1>Move from business signal to governed execution and measurable proof.</h1>
        <p style={{ maxWidth: 860, margin: "0 auto" }}>
          Dealix is a Saudi B2B company that combines strategy, AI systems, market intelligence and execution. We start with one real business problem, establish evidence and acceptance criteria, then build, adapt, integrate or partner around the smallest intervention that can prove value.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book?source=en-home" ctaId="en_home_diagnostic" surface="en_home_hero">Start a Free Execution Diagnostic</TrackedLink>
          <TrackedLink href="/dealix-os" ctaId="en_home_os" surface="en_home_hero">Explore Dealix OS</TrackedLink>
          <Link href="/" aria-label="Switch to Arabic">العربية</Link>
        </div>
      </section>

      <section className="cards" aria-label="Dealix capabilities">
        {capabilities.map(([title, text]) => (
          <article className="card" key={title}>
            <h2 style={{ fontSize: "1.45rem" }}>{title}</h2>
            <p>{text}</p>
          </article>
        ))}
      </section>

      <section className="card card-cyan">
        <p className="eyebrow">HOW WE ENGAGE</p>
        <h2>Free Diagnostic → Qualified Discovery → Customer-Specific Outcome Sprint → Proof Review</h2>
        <p>
          All diagnostics are free. There is no public fixed price or fixed duration authority. Scope, duration, acceptance criteria and quote become customer-specific only after qualified discovery.
        </p>
        <div className="actions">
          <TrackedLink href="/book?source=en-engagement" ctaId="en_engagement_diagnostic" surface="en_home_engagement">Start the Free Diagnostic</TrackedLink>
          <TrackedLink href="/pricing" ctaId="en_engagement_pricing" surface="en_home_engagement">How commercial scoping works</TrackedLink>
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">SECTOR-SPECIFIC EXECUTION</p>
        <h2>The Company Machine stays consistent. Buyer, workflow and proof change by sector.</h2>
        <div className="cards" style={{ marginTop: "var(--sp-5)" }}>
          {sectors.map(([name, href]) => (
            <article className="card" key={href}>
              <h3>{name}</h3>
              <TrackedLink href={href} ctaId={`en_sector_${href.split("/").pop()}`} surface="en_home_sectors">Explore sector context</TrackedLink>
            </article>
          ))}
        </div>
        <div className="actions"><TrackedLink href="/sectors" ctaId="en_all_sectors" surface="en_home_sectors">View all sectors</TrackedLink></div>
      </section>

      <section className="card">
        <p className="eyebrow">TRUTH FIREWALL</p>
        <h2>Evidence has to survive the transition from research to revenue.</h2>
        <ul>
          <li>Research ≠ Relationship.</li>
          <li>Public contact ≠ Consent.</li>
          <li>Draft ≠ Sent.</li>
          <li>Quote ≠ Invoice; Invoice ≠ Payment; Payment ≠ Revenue.</li>
          <li>Delivery ≠ Customer Value; Customer Value ≠ Public Proof.</li>
        </ul>
      </section>

      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">START WITH ONE EXECUTABLE PROBLEM</p>
        <h2>If there is no measurable case, we stop. If there is, we define the next proof-bearing move.</h2>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book?source=en-bottom" ctaId="en_bottom_diagnostic" surface="en_home_bottom">Start a Free Execution Diagnostic</TrackedLink>
          <TrackedLink href="/company" ctaId="en_bottom_company" surface="en_home_bottom">Explore Dealix</TrackedLink>
        </div>
      </section>
    </main>
  );
}
