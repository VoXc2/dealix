import type { Metadata } from "next";
import { AppLayout } from "@/components/layout/AppLayout";
import { PricingPlans } from "@/components/subscriptions/PricingPlans";

interface PricingPageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({
  params,
}: PricingPageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "الأسعار والاشتراكات — Dealix"
      : "Pricing & Subscriptions — Dealix",
    description: isAr
      ? "ثلاث خطط واضحة — Sprint لمرة واحدة، Managed Ops شهرياً، وEnterprise AI مخصص. كل خطة تبني على الإثبات."
      : "Three clear plans — one-time Sprint, monthly Managed Ops, and custom Enterprise AI. Every plan builds on proof.",
    alternates: {
      canonical: `https://dealix.me/${locale}/pricing`,
    },
  };
}

export default async function PricingPage({ params }: PricingPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "الأسعار والاشتراكات" : "Pricing & Subscriptions"}
      subtitle={
        isAr
          ? "ابدأ من حيث أنت — وسِّع بعد الإثبات"
          : "Start where you are — expand after proof"
      }
    >
      <PricingPlans />
    </AppLayout>
  );
}
