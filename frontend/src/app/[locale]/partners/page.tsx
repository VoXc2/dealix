import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { PartnerApplyForm } from "@/components/gtm/PartnerApplyForm";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "برنامج شركاء Dealix — عمولة 15-30%" : "Dealix Partner Program — 15-30% Commission",
    description: isAr
      ? "شارك في نمو Dealix — Referral أو Implementation أو Co-sell. عمولة على كل تشخيص وRetainer. PDPL-compliant."
      : "Join Dealix growth — Referral, Implementation, or Co-sell. Commission on every diagnostic and retainer. PDPL-compliant.",
    alternates: { canonical: `https://dealix.me/${locale}/partners` },
    openGraph: {
      title: isAr ? "برنامج شركاء Dealix" : "Dealix Partner Program",
      description: isAr ? "عمولة 15-30% · PDPL-compliant · موافقة أولاً" : "15-30% Commission · PDPL-compliant · Approval-first",
      url: `https://dealix.me/${locale}/partners`,
      images: [{ url: "https://dealix.me/brand/og-dealix.svg", width: 1200, height: 630, alt: "Dealix Partner Program" }],
    },
  };
}

export default function PartnersPage() {
  return (
    <PublicGtmShell compactNav>
      <div className="mx-auto max-w-5xl px-6 py-12">
        <PartnerApplyForm />
      </div>
    </PublicGtmShell>
  );
}
