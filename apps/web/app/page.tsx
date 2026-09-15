import type { Metadata } from "next";
import { InteractiveHome } from "@/components/landing/InteractiveHome";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export const metadata: Metadata = {
  alternates: { canonical: "/" },
};
const founderEmail = process.env.NEXT_PUBLIC_FOUNDER_EMAIL ?? "sami.assiri11@gmail.com";

const structuredData = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Dealix",
  url: siteUrl,
  email: founderEmail,
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  description:
    "Dealix is a Saudi B2B strategy, systems, intelligence, and product company that turns business signals into governed execution and measurable proof.",
  knowsAbout: [
    "B2B Strategy and Transformation",
    "Governed AI Execution",
    "Workflow Automation",
    "Revenue Operations",
    "AI Governance",
    "Saudi Market Intelligence",
    "Operational Proof",
  ],
  makesOffer: [
    {
      "@type": "Offer",
      itemOffered: {
        "@type": "Service",
        name: "Strategic B2B Solutions",
        description: "Strategy, systems, intelligence, governance, market-access and proof-led execution services.",
      },
    },
    {
      "@type": "Offer",
      itemOffered: {
        "@type": "SoftwareApplication",
        name: "Dealix OS",
        applicationCategory: "BusinessApplication",
        description: "AI Business Operating System for Signal to Decision to Action to Proof workflows.",
      },
    },
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
