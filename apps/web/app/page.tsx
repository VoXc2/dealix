import { InteractiveHome } from "@/components/landing/InteractiveHome";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";
const founderEmail = process.env.NEXT_PUBLIC_FOUNDER_EMAIL ?? "sami.assiri11@gmail.com";

const structuredData = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Dealix",
  url: siteUrl,
  email: founderEmail,
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  description:
    "Dealix is an AI Business Operating System that turns company signals into governed decisions, controlled action, and measurable proof.",
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
      <script
        type="application/ld+json"
        suppressHydrationWarning
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />
      <InteractiveHome />
    </>
  );
}
