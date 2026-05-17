import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { MarketProof } from "@/components/ops/MarketProof";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function MarketProofPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "ops.marketProof" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <MarketProof />
    </AppLayout>
  );
}
