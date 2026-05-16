import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { MarketProofConsole } from "@/components/market-proof/MarketProofConsole";

interface MarketProofPageProps {
  params: Promise<{ locale: string }>;
}

export default async function MarketProofPage({ params }: MarketProofPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "marketProof" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <MarketProofConsole />
    </AppLayout>
  );
}
