import type { Metadata } from "next";
import { TrustPage } from "@/components/gtm/TrustPage";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "الثقة والامتثال — PDPL · ZATCA · Approval-First"
      : "Trust & Compliance — PDPL · ZATCA · Approval-First",
    description: isAr
      ? "سياسة الخصوصية، PDPL، ZATCA، Approval-First، ولا outreach بارد. Dealix مبني على الثقة والامتثال."
      : "Privacy policy, PDPL, ZATCA, Approval-First, and no cold outreach. Dealix is built on trust and compliance.",
    alternates: { canonical: `https://dealix.me/${locale}/trust` },
  };
}

export default function TrustPageRoute() {
  return <TrustPage />;
}
