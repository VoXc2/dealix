import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { MarketProofConsole } from "@/components/revenue-ops/RevenueOpsScreens";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function MarketProofPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "revenueOps" });

  return (
    <AppLayout title={t("marketProof.title")} subtitle={t("marketProof.subtitle")}>
      <MarketProofConsole />
    </AppLayout>
  );
}
