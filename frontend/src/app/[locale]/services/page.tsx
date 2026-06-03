import type { Metadata } from "next";
import { ServicesPage } from "@/components/services/ServicesPage";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "خدمات Dealix — سلم العروض الخمسة"
      : "Dealix Services — Five-Tier Offer Ladder",
    description: isAr
      ? "من التشخيص المجاني إلى مشاريع AI المخصصة — كل مستوى يبني على الإثبات قبل التوسع."
      : "From free diagnostic to custom AI projects — every tier builds on proof before expansion.",
    alternates: { canonical: `https://dealix.me/${locale}/services` },
  };
}

export default function ServicesHubPage() {
  return <ServicesPage />;
}
